# 🔑 API Key Setup Guide - PDF Parser Pro

## Step-by-Step Instructions to Add API Keys

### **OPTION A: OpenAI (Recommended First)**

#### 1. Get OpenAI API Key
1. Go to: https://platform.openai.com/
2. Click "Sign up" or "Log in"
3. Navigate to "API Keys" section
4. Click "Create new secret key"
5. Copy the key (starts with `sk-`)

#### 2. Add Credits (Required)
- Minimum: $5-10 to start
- Go to: https://platform.openai.com/settings/billing
- Add payment method and credits

#### 3. Set the API Key (macOS)
```bash
# Open Terminal and run:
export OPENAI_API_KEY="sk-your-actual-key-here"

# To make it permanent, add to your shell profile:
echo 'export OPENAI_API_KEY="sk-your-actual-key-here"' >> ~/.zshrc
source ~/.zshrc
```

---

### **OPTION B: Google Gemini (Most Cost-Effective)**

#### 1. Get Gemini API Key
1. Go to: https://aistudio.google.com/app/apikey
2. Sign in with Google account
3. Click "Create API Key"
4. Copy the key

#### 2. Set the API Key (macOS)
```bash
# Open Terminal and run:
export GEMINI_API_KEY="your-gemini-key-here"

# To make it permanent:
echo 'export GEMINI_API_KEY="your-gemini-key-here"' >> ~/.zshrc
source ~/.zshrc
```

#### 3. Install Google AI SDK
```bash
cd /Users/dronebassan/Desktop/pdf_parser
pip install google-generativeai
```

---

### **OPTION C: Anthropic Claude (Good Balance)**

#### 1. Get Anthropic API Key
1. Go to: https://console.anthropic.com/
2. Sign up or log in
3. Navigate to "API Keys"
4. Click "Create Key"
5. Copy the key (starts with `sk-ant-`)

#### 2. Add Credits (Required)
- Minimum: $5-10 to start
- Add payment method in billing section

#### 3. Set the API Key (macOS)
```bash
# Open Terminal and run:
export ANTHROPIC_API_KEY="sk-ant-your-actual-key-here"

# To make it permanent:
echo 'export ANTHROPIC_API_KEY="sk-ant-your-actual-key-here"' >> ~/.zshrc
source ~/.zshrc
```

---

## **Quick Test After Setup**

### 1. Test Your Keys
```bash
cd /Users/dronebassan/Desktop/pdf_parser
python test_api_keys.py
```

### 2. Expected Output
```
🔑 Testing API Keys
========================================
✅ OPENAI_API_KEY found: sk-proj...xyz
   Testing connection...
   ✅ OpenAI API working!

✅ GEMINI_API_KEY found: AIzaSyC...xyz  
   Testing connection...
   ✅ Gemini API working!

✅ ANTHROPIC_API_KEY found: sk-ant...xyz
   Testing connection...
   ✅ Anthropic API working!

🎉 At least one API key is working!
   Your PDF parser will have AI fallback capabilities.
```

### 3. Start Your Server
```bash
uvicorn main:app --reload
```

### 4. Test AI Features
```bash
# Test the smart parsing with AI fallback
curl -X POST "http://localhost:8000/parse-smart/" \
  -F "file=@your_test_document.pdf" \
  -F "strategy=auto" \
  -F "llm_provider=gemini"
```

---

## **Troubleshooting**

### ❌ "API Key Not Found"
```bash
# Check if key is set:
echo $OPENAI_API_KEY
echo $GEMINI_API_KEY  
echo $ANTHROPIC_API_KEY

# If empty, re-run the export commands
```

### ❌ "API Key Invalid"
- Double-check you copied the FULL key
- Make sure no extra spaces
- Verify key starts with correct prefix:
  - OpenAI: `sk-`
  - Gemini: Usually starts with `AIza`
  - Anthropic: `sk-ant-`

### ❌ "Insufficient Credits"
- Add $5-10 to your account billing
- Check usage limits in API dashboard

### ❌ "Module Not Found"
```bash
# Install missing dependencies:
pip install openai anthropic google-generativeai
```

---

## **Cost Estimates**

### **OpenAI GPT-4V**
- ~$0.03 per page
- Good for: High accuracy needs

### **Gemini 2.5 Flash**
- ~$0.001 per page (30x cheaper!)
- Good for: Cost optimization

### **Claude 3.5 Sonnet**
- ~$0.02 per page  
- Good for: Balanced performance

### **Your Smart System**
- Uses library parsing (FREE) for 90% of pages
- Only uses AI for problematic pages
- Actual cost: ~$0.001 per page average

---

## **Recommended Setup Priority**

### **For Testing/Development:**
1. **Gemini first** (cheapest, fastest setup)
2. **OpenAI second** (most accurate)
3. **Anthropic third** (good balance)

### **For Production:**
- **All three** for maximum reliability
- **Smart fallback** between providers
- **Cost optimization** with page-by-page processing

---

## **Next Steps After API Keys**

1. ✅ **Test all providers work**
2. ✅ **Process a sample PDF**  
3. ✅ **Check cost monitoring**
4. 🚀 **Ready for production deployment!**