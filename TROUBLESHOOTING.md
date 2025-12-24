# 🔧 Troubleshooting Guide

Common issues and solutions for the M&A Strategic Fit Analyzer.

---

## 🔑 API Key Issues

### "GEMINI_API_KEY not found"

**Problem**: App can't find your Gemini API key.

**Solutions**:
1. Check `.env` file exists (not `.env.example`)
   ```bash
   ls -la | grep .env
   # Should show: .env (not just .env.example)
   ```

2. Verify key format in `.env`:
   ```bash
   # Correct format:
   GEMINI_API_KEY=AIzaSyC...your_actual_key

   # Wrong formats:
   GEMINI_API_KEY = AIza...  # No spaces around =
   GEMINI_API_KEY="AIza..."  # No quotes needed
   ```

3. Restart Streamlit after adding key:
   ```bash
   # Press Ctrl+C in terminal
   streamlit run app.py
   ```

### "Invalid API key" error

**Problem**: Gemini rejects your API key.

**Solutions**:
1. Verify key is active at [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Check you copied the entire key (starts with `AIza`)
3. Try generating a new API key
4. Ensure no extra spaces before/after key in `.env`

---

## 📦 Installation Issues

### "Module not found" errors

**Problem**: Python can't find installed packages.

**Solutions**:
1. Ensure virtual environment is activated:
   ```bash
   # You should see (venv) in terminal prompt
   # If not, activate:
   source venv/bin/activate  # Mac/Linux
   venv\Scripts\activate     # Windows
   ```

2. Reinstall dependencies:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

3. Check Python version:
   ```bash
   python --version
   # Should be 3.9 or higher
   ```

### ImportError: cannot import name '...'

**Problem**: Conflicting package versions.

**Solution**:
```bash
# Clean install
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## 🌐 Web Scraping Issues

### "Failed to scrape website"

**Problem**: Website blocking or doesn't exist.

**Solutions**:
1. **This is normal!** Many sites block scrapers
2. Try leaving website field empty - Gemini will use general knowledge
3. Check URL format:
   ```
   ✅ https://www.company.com
   ✅ company.com
   ❌ www.company.com (missing https://)
   ```

4. Some companies to try that usually work:
   - Shopify, Stripe, Slack (good About pages)
   - GitHub, HubSpot, Notion

### Website scraping returns no data

**Problem**: Site structure doesn't match scraper expectations.

**Solutions**:
1. Leave website blank - still get good analysis
2. The AI will use general company knowledge
3. Deep Mode (Phase 2) will add more data sources

---

## 🤖 Gemini API Issues

### "Rate limit exceeded"

**Problem**: Too many requests to Gemini API.

**Solutions**:
1. Free tier limit: 60 requests/minute
2. Wait 60 seconds and try again
3. Use Fast Mode (fewer API calls)
4. Don't click analyze button multiple times

### "Could not parse Gemini response"

**Problem**: LLM returned non-JSON format.

**Solutions**:
1. App has fallback analysis - you'll still get results
2. Try analyzing again (LLM responses vary)
3. Check terminal for full error message
4. If persistent, open GitHub issue with error details

### Analysis seems generic

**Problem**: Not enough specific data collected.

**Solutions**:
1. Provide company websites for better context
2. Use well-known companies (more training data)
3. Try Deep Mode (Phase 2) for richer analysis
4. Ensure industry selection matches actual companies

---

## 💻 Streamlit Issues

### Port already in use

**Problem**: Port 8501 is occupied.

**Solutions**:
```bash
# Use different port
streamlit run app.py --server.port 8502

# Or kill existing Streamlit process
pkill -f streamlit
streamlit run app.py
```

### "Browser failed to open"

**Problem**: Auto-open didn't work.

**Solution**:
Manually open: `http://localhost:8501`

### Changes not showing

**Problem**: Streamlit not detecting code updates.

**Solutions**:
1. Click "Always rerun" in top-right
2. Or press `R` to rerun manually
3. Or restart Streamlit (Ctrl+C, then rerun)

### Session state errors

**Problem**: Variables not persisting.

**Solution**:
1. Clear cache: Press `C` in browser
2. Or click "Clear cache" in Streamlit menu (☰)
3. Refresh page

---

## 🚀 Deployment Issues

### Streamlit Cloud: "App failed to load"

**Problem**: Deployment error.

**Solutions**:
1. Check requirements.txt has all packages
2. Verify .env secrets set in Streamlit Cloud settings
3. Check logs in Streamlit Cloud dashboard
4. Ensure Python version ≥ 3.9 in runtime.txt

### Streamlit Cloud: API key not found

**Problem**: Environment variable not set.

**Solution**:
1. Go to app settings (gear icon)
2. Secrets section
3. Add:
   ```toml
   GEMINI_API_KEY = "your_key_here"
   ```
4. Save and reboot app

### GitHub push rejected

**Problem**: Large files or credentials in repo.

**Solutions**:
```bash
# Remove .env from git if accidentally added
git rm --cached .env
echo ".env" >> .gitignore
git add .gitignore
git commit -m "Remove .env from tracking"
git push
```

---

## 📊 Results Issues

### Scores all seem similar

**Problem**: Not enough differentiation.

**Explanation**: 
- This is sometimes accurate! Many deals score 60-75
- Real M&A deals rarely score >90 or <30
- Dimension-level details show differences

**To see more variation**:
- Compare very different industries (e.g., E-commerce vs Healthcare)
- Compare different-sized companies (startup vs Fortune 500)

### Evidence seems generic

**Problem**: LLM making assumptions without data.

**Solutions**:
1. This is a limitation of free web data
2. Provide websites for both companies
3. Use well-known companies with public info
4. Phase 2 (Deep Mode) will improve this

### Missing risks/synergies

**Problem**: Incomplete analysis.

**Solutions**:
1. Try running analysis again (LLM variance)
2. Check terminal logs for errors
3. Ensure good internet connection
4. Try different company pair to verify tool works

---

## 🐛 Other Common Issues

### "Connection timeout" errors

**Problem**: Network issues.

**Solutions**:
1. Check internet connection
2. Try different company websites
3. Increase timeout in `scrapers/website_scraper.py`:
   ```python
   self.timeout = 15  # Was 10
   ```

### Application crashes

**Problem**: Unhandled exception.

**Solutions**:
1. Check terminal for full error trace
2. Note which companies caused crash
3. Report on GitHub with error details
4. Try different company pair to verify

### Results look wrong

**Problem**: Analysis doesn't match your expectations.

**Remember**:
- AI analysis is probabilistic, not deterministic
- Results may differ from your view (that's ok!)
- Dimension scores are weighted (check weights)
- Evidence is based on public data only

**Verification**:
1. Test with well-known deals (Shopify→Deliverr)
2. Check dimension breakdown for reasoning
3. Compare Fast vs Deep mode (Phase 2)

---

## 🆘 Getting Help

### Before asking for help:

1. ✅ Check terminal for error messages
2. ✅ Verify API key is set correctly
3. ✅ Try with example companies first
4. ✅ Restart Streamlit
5. ✅ Check this troubleshooting guide

### How to report issues:

Create GitHub issue with:
- Error message (full text from terminal)
- Steps to reproduce
- Companies you tried analyzing
- Python version: `python --version`
- OS: Windows/Mac/Linux

### Emergency contacts:

- GitHub Issues: [github.com/yourusername/m-and-a-fit-analyzer/issues](https://github.com/yourusername/m-and-a-fit-analyzer/issues)
- Email: your.email@example.com

---

## ✅ Quick Diagnostic Checklist

Run through this if things aren't working:

```bash
# 1. Check Python version
python --version
# Should be 3.9+

# 2. Check virtual environment
which python
# Should point to venv/bin/python

# 3. Check packages installed
pip list | grep streamlit
pip list | grep google-generativeai
# Should show version numbers

# 4. Check .env file
cat .env
# Should show GEMINI_API_KEY=...

# 5. Test imports
python -c "import streamlit; import google.generativeai"
# Should complete without errors

# 6. Run app
streamlit run app.py
# Should start without errors
```

If all above pass but still having issues, it's likely:
- Network/firewall blocking
- API key issue
- Website blocking scrapers (not your fault!)

---

## 💡 Tips for Best Results

### Company Selection
✅ **Good choices**:
- Well-known tech companies (Shopify, Stripe, etc.)
- Companies with detailed About pages
- Recently in the news

❌ **Avoid**:
- Very small unknown startups (limited data)
- Companies without websites
- Non-tech companies (outside scope)

### Website URLs
✅ **Works best**:
- Official company website (.com domains)
- HTTPS URLs
- English-language sites

❌ **May fail**:
- Social media profiles
- Third-party review sites
- Non-English sites

### Analysis Mode
- **Fast Mode**: Use for quick tests, demos
- **Deep Mode**: Use when you need comprehensive analysis (Phase 2)

---

**Most issues are normal!** Web scraping is imperfect, LLMs are probabilistic. The tool still provides value even with limited data.

---

**Still stuck?** Open a GitHub issue - we're here to help! 🚀
