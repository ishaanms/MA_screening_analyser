# 🚀 Quick Start Guide

Get up and running in 5 minutes!

## Step 1: Get Gemini API Key (2 min)

1. Visit: https://makersuite.google.com/app/apikey
2. Click **"Get API Key"**
3. Click **"Create API key in new project"**
4. Copy your API key (starts with `AIza...`)

## Step 2: Install (1 min)

```bash
# Clone repo
git clone https://github.com/yourusername/m-and-a-fit-analyzer.git
cd m-and-a-fit-analyzer

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Step 3: Configure API Key (30 sec)

```bash
# Copy env file
cp .env.example .env

# Open .env in any text editor and paste your API key:
# GEMINI_API_KEY=AIza...your_key_here
```

## Step 4: Run! (30 sec)

```bash
streamlit run app.py
```

The app opens automatically at `http://localhost:8501`

## Step 5: Test with Example (30 sec)

1. Click **"Shopify → Deliverr"** button
2. Keep default settings (Fast Mode)
3. Click **"🚀 Analyze Strategic Fit"**
4. Wait ~45 seconds
5. Explore results! 🎉

---

## Troubleshooting

### "GEMINI_API_KEY not found"
- Make sure you created `.env` file (not `.env.example`)
- Check the key is pasted correctly (no extra spaces)
- Restart Streamlit after adding the key

### "Module not found"
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Reinstall dependencies
pip install -r requirements.txt
```

### Website scraping fails
- This is normal for some sites (robots.txt, blocks)
- Gemini will still provide analysis using general knowledge
- Try different companies or leave website field empty

### Gemini API rate limit
- Free tier: 60 requests/minute
- Wait 1 minute and try again
- Use Fast Mode to minimize API calls

---

## What to Try

1. **Pre-configured Examples**
   - Shopify → Deliverr (E-commerce logistics)
   - Stripe → Plaid (FinTech banking APIs)
   - Salesforce → Slack (SaaS collaboration)

2. **Custom Analysis**
   - Pick any two companies you know
   - Test different industries
   - Compare Fast vs Deep mode

3. **Portfolio Demo**
   - Screenshot the results dashboard
   - Export key metrics for your resume
   - Record a 30-second demo video

---

## Next Steps

- ✅ Deploy to Streamlit Cloud (free!)
- ✅ Customize industries in `config/examples.py`
- ✅ Add more examples
- ✅ Write your portfolio case study

**Ready to deploy?** See [README.md](README.md) deployment section.

---

**Need help?** Open a GitHub issue or email your.email@example.com
