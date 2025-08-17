"""
Multi-tenant API key management for SaaS deployment
"""

import os
from typing import Dict, Optional
from enum import Enum
import redis
import json
from dataclasses import dataclass

class SubscriptionTier(Enum):
    FREE = "free"
    BASIC = "basic"
    PREMIUM = "premium"
    ENTERPRISE = "enterprise"

@dataclass
class CustomerConfig:
    customer_id: str
    subscription_tier: SubscriptionTier
    monthly_quota: int
    current_usage: int
    preferred_llm: str
    custom_api_keys: Dict[str, str]  # Customer's own keys (optional)

class APIKeyManager:
    def __init__(self, redis_client=None):
        self.redis_client = redis_client or redis.Redis(
            host=os.getenv('REDIS_HOST', 'localhost'),
            port=int(os.getenv('REDIS_PORT', 6379)),
            decode_responses=True
        )
        
        # Your master API keys (you pay for these)
        self.master_keys = {
            'openai': os.getenv('MASTER_OPENAI_API_KEY'),
            'anthropic': os.getenv('MASTER_ANTHROPIC_API_KEY'),
            'openai_premium': os.getenv('PREMIUM_OPENAI_API_KEY'),  # Higher limits
            'anthropic_premium': os.getenv('PREMIUM_ANTHROPIC_API_KEY')
        }
        
        # Usage costs per provider (you'll mark up these prices)
        self.api_costs = {
            'openai': 0.03,  # per page
            'anthropic': 0.02,  # per page
        }
        
        # Your pricing (markup on API costs)
        self.customer_pricing = {
            SubscriptionTier.FREE: {'quota': 10, 'price_per_page': 0.0},
            SubscriptionTier.BASIC: {'quota': 500, 'price_per_page': 0.05},
            SubscriptionTier.PREMIUM: {'quota': 5000, 'price_per_page': 0.04},
            SubscriptionTier.ENTERPRISE: {'quota': -1, 'price_per_page': 0.03}  # unlimited
        }
    
    def get_api_key_for_customer(self, customer_id: str, provider: str) -> Optional[str]:
        """Get the appropriate API key for a customer"""
        
        customer_config = self.get_customer_config(customer_id)
        if not customer_config:
            return None
        
        # Check if customer has their own API keys (enterprise tier)
        if customer_config.custom_api_keys.get(provider):
            return customer_config.custom_api_keys[provider]
        
        # Check usage quota
        if not self.check_usage_quota(customer_id):
            raise Exception("Monthly quota exceeded. Please upgrade your plan.")
        
        # Return appropriate master key based on subscription tier
        if customer_config.subscription_tier == SubscriptionTier.PREMIUM:
            return self.master_keys.get(f'{provider}_premium') or self.master_keys.get(provider)
        else:
            return self.master_keys.get(provider)
    
    def get_customer_config(self, customer_id: str) -> Optional[CustomerConfig]:
        """Get customer configuration"""
        try:
            config_data = self.redis_client.get(f"customer:{customer_id}")
            if config_data:
                data = json.loads(config_data)
                return CustomerConfig(
                    customer_id=customer_id,
                    subscription_tier=SubscriptionTier(data['subscription_tier']),
                    monthly_quota=data['monthly_quota'],
                    current_usage=data['current_usage'],
                    preferred_llm=data['preferred_llm'],
                    custom_api_keys=data.get('custom_api_keys', {})
                )
            return None
        except Exception as e:
            print(f"Error getting customer config: {e}")
            return None
    
    def check_usage_quota(self, customer_id: str) -> bool:
        """Check if customer has remaining quota"""
        config = self.get_customer_config(customer_id)
        if not config:
            return False
        
        # Enterprise has unlimited quota
        if config.monthly_quota == -1:
            return True
        
        return config.current_usage < config.monthly_quota
    
    def record_usage(self, customer_id: str, pages_processed: int, provider: str):
        """Record API usage for billing"""
        try:
            config = self.get_customer_config(customer_id)
            if config:
                # Update usage count
                config.current_usage += pages_processed
                
                # Calculate cost
                api_cost = self.api_costs[provider] * pages_processed
                customer_cost = self.customer_pricing[config.subscription_tier]['price_per_page'] * pages_processed
                profit = customer_cost - api_cost
                
                # Save updated config
                self.save_customer_config(config)
                
                # Record billing event
                self.record_billing_event(customer_id, pages_processed, customer_cost, api_cost, profit, provider)
                
        except Exception as e:
            print(f"Error recording usage: {e}")
    
    def save_customer_config(self, config: CustomerConfig):
        """Save customer configuration"""
        data = {
            'subscription_tier': config.subscription_tier.value,
            'monthly_quota': config.monthly_quota,
            'current_usage': config.current_usage,
            'preferred_llm': config.preferred_llm,
            'custom_api_keys': config.custom_api_keys
        }
        self.redis_client.set(f"customer:{config.customer_id}", json.dumps(data))
    
    def record_billing_event(self, customer_id: str, pages: int, customer_cost: float, 
                           api_cost: float, profit: float, provider: str):
        """Record billing event for analytics"""
        billing_event = {
            'customer_id': customer_id,
            'timestamp': int(time.time()),
            'pages_processed': pages,
            'customer_charged': customer_cost,
            'api_cost': api_cost,
            'profit': profit,
            'provider': provider
        }
        
        # Store in time-series for analytics
        key = f"billing:{customer_id}:{int(time.time())}"
        self.redis_client.set(key, json.dumps(billing_event), ex=86400*90)  # Keep 90 days
        
        # Add to daily aggregations
        date_key = f"daily_revenue:{time.strftime('%Y-%m-%d')}"
        self.redis_client.incrbyfloat(date_key, profit)
    
    def create_customer(self, customer_id: str, email: str, subscription_tier: SubscriptionTier) -> CustomerConfig:
        """Create new customer"""
        pricing = self.customer_pricing[subscription_tier]
        
        config = CustomerConfig(
            customer_id=customer_id,
            subscription_tier=subscription_tier,
            monthly_quota=pricing['quota'],
            current_usage=0,
            preferred_llm='openai',
            custom_api_keys={}
        )
        
        self.save_customer_config(config)
        
        # Store customer profile
        profile = {
            'email': email,
            'created_at': int(time.time()),
            'subscription_tier': subscription_tier.value
        }
        self.redis_client.set(f"profile:{customer_id}", json.dumps(profile))
        
        return config
    
    def get_usage_stats(self, customer_id: str) -> Dict:
        """Get customer usage statistics"""
        config = self.get_customer_config(customer_id)
        if not config:
            return {}
        
        quota_remaining = config.monthly_quota - config.current_usage
        if config.monthly_quota == -1:  # Unlimited
            quota_remaining = -1
        
        return {
            'current_usage': config.current_usage,
            'monthly_quota': config.monthly_quota,
            'quota_remaining': quota_remaining,
            'subscription_tier': config.subscription_tier.value,
            'preferred_llm': config.preferred_llm
        }

# Global instance
api_key_manager = APIKeyManager()