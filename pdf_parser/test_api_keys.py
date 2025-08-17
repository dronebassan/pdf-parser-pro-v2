#!/usr/bin/env python3
"""
Test if your API keys are working
"""

import os
import sys

def test_openai_key():
    """Test OpenAI API key"""
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        print("❌ OPENAI_API_KEY not found")
        print("   Set it with: export OPENAI_API_KEY='sk-your-key-here'")
        return False
    
    if not api_key.startswith("sk-"):
        print("❌ OPENAI_API_KEY doesn't look right (should start with 'sk-')")
        return False
    
    print(f"✅ OPENAI_API_KEY found: {api_key[:8]}...{api_key[-4:]}")
    
    # Try to import and test
    try:
        import openai
        client = openai.OpenAI(api_key=api_key)
        
        # Test with a simple call
        print("   Testing connection...")
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Say 'hello'"}],
            max_tokens=5
        )
        print("   ✅ OpenAI API working!")
        return True
        
    except Exception as e:
        print(f"   ❌ OpenAI API test failed: {e}")
        return False

def test_anthropic_key():
    """Test Anthropic API key"""
    api_key = os.getenv("ANTHROPIC_API_KEY")
    
    if not api_key:
        print("❌ ANTHROPIC_API_KEY not found")
        print("   Set it with: export ANTHROPIC_API_KEY='sk-ant-your-key-here'")
        return False
    
    if not api_key.startswith("sk-ant-"):
        print("❌ ANTHROPIC_API_KEY doesn't look right (should start with 'sk-ant-')")
        return False
    
    print(f"✅ ANTHROPIC_API_KEY found: {api_key[:10]}...{api_key[-4:]}")
    
    # Try to import and test
    try:
        import anthropic
        client = anthropic.Anthropic(api_key=api_key)
        
        # Test with a simple call
        print("   Testing connection...")
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=5,
            messages=[{"role": "user", "content": "Say hello"}]
        )
        print("   ✅ Anthropic API working!")
        return True
        
    except Exception as e:
        print(f"   ❌ Anthropic API test failed: {e}")
        return False

def test_gemini_key():
    """Test Gemini API key"""
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        print("❌ GEMINI_API_KEY not found")
        print("   Set it with: export GEMINI_API_KEY='your-key-here'")
        return False
    
    print(f"✅ GEMINI_API_KEY found: {api_key[:8]}...{api_key[-4:]}")
    
    # Try to import and test
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        
        # Test with a simple call
        print("   Testing connection...")
        model = genai.GenerativeModel("gemini-2.0-flash-exp")
        response = model.generate_content("Say 'hello'")
        print("   ✅ Gemini API working!")
        return True
        
    except Exception as e:
        print(f"   ❌ Gemini API test failed: {e}")
        return False

def main():
    print("🔑 Testing API Keys")
    print("=" * 40)
    
    openai_works = test_openai_key()
    print()
    anthropic_works = test_anthropic_key()
    print()
    gemini_works = test_gemini_key()
    print()
    
    if openai_works or anthropic_works or gemini_works:
        print("🎉 At least one API key is working!")
        print("   Your PDF parser will have AI fallback capabilities.")
        print("   Start server with: uvicorn main:app --reload")
    else:
        print("😔 No API keys are working.")
        print("   Your PDF parser will work in library-only mode (still good!).")
        print("\n🔧 To enable AI features:")
        print("   1. Get API key from:")
        print("      - OpenAI: https://platform.openai.com/")
        print("      - Anthropic: https://console.anthropic.com/")
        print("      - Google Gemini: https://aistudio.google.com/app/apikey")
        print("   2. Set environment variable:")
        print("      export OPENAI_API_KEY='your-key-here'")
        print("      export ANTHROPIC_API_KEY='your-key-here'")
        print("      export GEMINI_API_KEY='your-key-here'")
        print("   3. Restart this test")

if __name__ == "__main__":
    main()