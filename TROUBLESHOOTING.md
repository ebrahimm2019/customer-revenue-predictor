# 🔧 TROUBLESHOOTING GUIDE

## Common Issues & Solutions

---

## 1. ImportError: attempted relative import with no known parent package

**Error:**
```
ImportError: attempted relative import with no known parent package
```

**Cause:** Running `python app/main.py` directly instead of as a module.

**Solutions:**

### ✅ Solution A: Use the run script (EASIEST)
```bash
# Windows
start.bat

# Linux/Mac
./start.sh

# Or directly
python run.py
```

### ✅ Solution B: Use uvicorn (RECOMMENDED)
```bash
# From project root
uvicorn app.main:app --reload

# With uv
uv run uvicorn app.main:app --reload
```

### ✅ Solution C: Run as module
```bash
# From project root
python -m app.main
```

---

## 2. Model file not found

**Error:**
```
FileNotFoundError: Model not found: models/trained_model.pkl
```

**Solution:**
```bash
# 1. Ensure dataset CSVs are in project root:
#    - Year 2009-2010.csv
#    - Year 2010-2011.csv

# 2. Train the model
uv run python scripts/train_model.py

# 3. Verify model was created
ls models/trained_model.pkl  # Linux/Mac
dir models\trained_model.pkl  # Windows
```

---

## 3. Dataset not found

**Error:**
```
FileNotFoundError: Data files not found
```

**Solution:**

1. **Download UCI Online Retail II dataset** from:
   - https://archive.ics.uci.edu/ml/datasets/Online+Retail+II
   - Or use your existing dataset

2. **Place CSV files in project root** (not in `data/` folder):
   ```
   customer-revenue-predictor/
   ├── Year 2009-2010.csv    ← HERE
   ├── Year 2010-2011.csv    ← HERE
   ├── app/
   ├── data/
   └── ...
   ```

3. **Verify files exist:**
   ```bash
   # Windows
   dir "Year 2009-2010.csv"
   dir "Year 2010-2011.csv"
   
   # Linux/Mac
   ls "Year 2009-2010.csv"
   ls "Year 2010-2011.csv"
   ```

---

## 4. Module not found errors

**Error:**
```
ModuleNotFoundError: No module named 'fastapi'
ModuleNotFoundError: No module named 'xgboost'
```

**Solution:**
```bash
# Reinstall dependencies
uv sync

# If uv not installed
pip install uv
uv sync

# Alternative: Use pip
pip install -r requirements.txt
```

---

## 5. UV command not found

**Error:**
```
'uv' is not recognized as an internal or external command
```

**Solution:**

### Windows:
```powershell
# Install UV
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Add to PATH (restart terminal after)
```

### Linux/Mac:
```bash
# Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# Add to PATH
echo 'export PATH="$HOME/.cargo/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### Alternative: Use pip
```bash
pip install -r requirements.txt
python run.py
```

---

## 6. Port already in use

**Error:**
```
OSError: [Errno 48] Address already in use
```

**Solution:**

### Option A: Change port
```bash
# Edit run.py, change port=8000 to port=8001
uvicorn app.main:app --port 8001
```

### Option B: Kill existing process

**Windows:**
```cmd
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

**Linux/Mac:**
```bash
lsof -ti:8000 | xargs kill -9
```

---

## 7. CORS errors in browser

**Error in browser console:**
```
Access to fetch at 'http://localhost:8000/api/...' has been blocked by CORS policy
```

**Solution:**

This shouldn't happen with the default config, but if it does:

1. **Check `app/config.py`:**
   ```python
   CORS_ORIGINS = [
       "http://localhost:8000",
       "http://127.0.0.1:8000",
   ]
   ```

2. **Add your origin if different:**
   ```python
   CORS_ORIGINS = [
       "http://localhost:8000",
       "http://localhost:3000",  # If frontend on different port
   ]
   ```

---

## 8. Static files not loading

**Symptoms:**
- CSS not applied
- HTML pages show but unstyled
- 404 errors for static files

**Solution:**

1. **Verify static directory structure:**
   ```
   app/static/
   ├── index.html
   ├── dashboard.html
   ├── predict.html
   └── insights.html
   ```

2. **Check file paths in code:**
   ```python
   # In app/config.py
   STATIC_DIR: Path = BASE_DIR / "app" / "static"
   ```

3. **Restart server** after changes

---

## 9. Prediction returns 500 error

**Error in API response:**
```json
{"detail": "Internal server error"}
```

**Debug steps:**

1. **Check server logs** for detailed error
2. **Verify model is loaded:**
   ```bash
   curl http://localhost:8000/api/health
   ```
3. **Test with valid data:**
   ```bash
   curl -X POST http://localhost:8000/api/predict/single \
     -H "Content-Type: application/json" \
     -d '{
       "frequency": 8,
       "monetary_total": 2500.0,
       "recency": 45,
       "is_uk": true
     }'
   ```

---

## 10. Python version issues

**Error:**
```
SyntaxError: invalid syntax
```

**Solution:**

Ensure Python 3.9+:
```bash
python --version  # Should be 3.9 or higher

# If wrong version, install Python 3.11
# Then use:
python3.11 -m uvicorn app.main:app --reload
```

---

## 11. Memory errors during training

**Error:**
```
MemoryError: Unable to allocate array
```

**Solution:**

1. **Reduce batch size** (if applicable)
2. **Close other applications**
3. **Use sample data for testing:**
   ```python
   # In scripts/train_model.py
   # Add this after loading data:
   df = df.sample(frac=0.5, random_state=42)  # Use 50% of data
   ```

---

## 12. Windows path issues

**Error:**
```
FileNotFoundError: [Errno 2] No such file or directory
```

**Solution:**

Windows uses backslashes. Use raw strings or forward slashes:
```python
# Good
path = Path("data/file.csv")
path = r"C:\Users\Mohamed\data\file.csv"

# Bad
path = "C:\Users\Mohamed\data\file.csv"  # \U and \d are escape sequences
```

---

## 13. Virtual environment issues

**Symptoms:**
- Packages not found even after install
- Wrong Python version
- Module conflicts

**Solution:**

```bash
# Delete and recreate virtual environment
rm -rf .venv  # Linux/Mac
rmdir /s .venv  # Windows

# Recreate
uv sync

# Verify it's active
which python  # Should show .venv path
```

---

## 14. API returns empty response

**Symptom:** API call succeeds but returns `{}` or null data

**Solution:**

1. **Check model is trained:**
   ```bash
   ls models/trained_model.pkl
   ```

2. **Verify model loads on startup:**
   - Look for "✓ Model loaded" in server logs

3. **Check feature names match:**
   - Model expects exact feature names from training

---

## 15. Deployment fails

### Railway/Render/Fly

**Common issues:**

1. **Build timeout:**
   - Dataset CSVs are too large for git
   - Solution: Remove CSVs from repo, train locally, commit model

2. **Memory limit:**
   - Free tier has memory limits
   - Solution: Use smaller model or upgrade tier

3. **Missing dependencies:**
   - Check `requirements.txt` has all packages
   - Solution: `pip freeze > requirements.txt`

---

## 🆘 Still Having Issues?

### Debug Checklist:

- [ ] Python 3.9+ installed
- [ ] UV installed (`uv --version`)
- [ ] Dependencies installed (`uv sync`)
- [ ] Dataset CSVs in project root
- [ ] Model trained (`models/trained_model.pkl` exists)
- [ ] Running from project root directory
- [ ] Using correct startup method (`run.py` or `uvicorn`)

### Get More Help:

1. **Check server logs** for detailed error messages
2. **Review README.md** for setup instructions
3. **Test API endpoints individually:**
   ```bash
   curl http://localhost:8000/api/health
   curl http://localhost:8000/api/model/info
   ```

4. **Enable debug mode:**
   ```python
   # In run.py
   uvicorn.run("app.main:app", reload=True, log_level="debug")
   ```

---

## Quick Reference Commands

```bash
# Setup
uv sync

# Train model
uv run python scripts/train_model.py

# Start server (choose one)
python run.py                           # Easiest
uv run uvicorn app.main:app --reload    # Standard
./start.sh                              # Linux/Mac script
start.bat                               # Windows script

# Test
curl http://localhost:8000/api/health

# Stop
CTRL+C
```

---

**Most issues are solved by:**
1. Running from project root
2. Using proper startup command
3. Training model first
4. Having dataset CSVs in place

**Good luck! 🚀**
