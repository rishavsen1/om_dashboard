# Quick Start Guide

## 🚀 Getting Started in 3 Steps

### Step 1: Run Setup

```bash
./setup.sh
```

This will:

- Create a Python virtual environment
- Install all dependencies (Flask, NumPy, etc.)
- Prepare the application for running

### Step 2: Start the Server

```bash
./run.sh
```

Or manually:

```bash
source venv/bin/activate
python app.py
```

### Step 3: Open Your Browser

Navigate to: **http://localhost:5000**

---

## 📋 What Changed from Pure HTML/JS?

### Before (Pure Frontend)

```
index.html (everything in one file)
├── HTML structure
├── Inline CSS
└── JavaScript calculations (complex, hard to test)
```

### After (Frontend + Backend)

```
Frontend (templates/index.html)
├── HTML structure
├── Inline CSS
└── JavaScript (UI only, calls API)

Backend (Python)
├── app.py (Flask routes & API)
├── calculators.py (business logic)
└── API endpoints (clean separation)
```

---

## 🔄 How It Works Now

### Frontend (Browser)

1. User adjusts sliders/inputs
2. JavaScript collects form data
3. **Sends to backend via API** (NEW!)
4. Receives calculated results
5. Updates charts and displays

### Backend (Python Server)

1. Receives calculation request
2. Runs Python calculation functions
3. Returns JSON results
4. Handles all complex math

---

## 📡 API Usage Example

### Old Way (JavaScript in Browser)

```javascript
// Complex calculation code in browser
function calculate() {
  // 100+ lines of math...
  const result = complexCalculation();
  updateUI(result);
}
```

### New Way (API Call to Backend)

```javascript
// Simple API call
async function calculate() {
  const params = getFormData();
  const result = await dashboardAPI.calculateHomeowner(params);
  updateUI(result);
}
```

The Python backend handles all the complex calculations!

---

## 🎯 Benefits of This Architecture

### ✅ Separation of Concerns

- Frontend: UI/UX only
- Backend: Business logic only
- Each can be updated independently

### ✅ Easier Testing

- Python functions can be unit tested
- Can test calculations without browser
- Better code quality

### ✅ Performance

- NumPy calculations faster than JavaScript
- Can add caching on backend
- Can scale horizontally

### ✅ Reusability

- Same API can power mobile app
- Can integrate with other systems
- Python functions reusable elsewhere

### ✅ Maintainability

- Python code more readable for complex math
- Type hints available
- Better debugging tools

---

## 🔧 Development Tips

### Making Changes

**Frontend changes** (HTML/CSS/JavaScript):

- Edit `templates/index.html`
- Refresh browser to see changes

**Backend changes** (Python):

- Edit `app.py` or `calculators.py`
- Flask auto-reloads in debug mode
- Just refresh browser

### Testing API Endpoints

Use curl to test:

```bash
curl -X POST http://localhost:5000/api/calculate/homeowner \
  -H "Content-Type: application/json" \
  -d '{"peakRate": 0.28, "hvacConsumption": 3.5}'
```

### Debugging

**Backend errors:**

- Check terminal running `python app.py`
- Errors will show with stack traces

**Frontend errors:**

- Open browser DevTools (F12)
- Check Console tab
- Check Network tab for API calls

---

## 📦 Project Structure

```
om_value_calc/
│
├── app.py                    # Flask server & routes
├── calculators.py            # All calculation logic
├── requirements.txt          # Python dependencies
│
├── templates/
│   └── index.html           # Main dashboard page
│
├── static/
│   └── api-client.js        # API client for frontend
│
├── setup.sh                 # One-time setup script
├── run.sh                   # Start server script
│
└── README.md                # Full documentation
```

---

## 🚀 Next Steps

### Immediate

1. ✅ Run `./setup.sh`
2. ✅ Run `./run.sh`
3. ✅ Open browser to http://localhost:5000
4. ✅ Test calculations

### Optional Enhancements

- [ ] Add database (save scenarios)
- [ ] User authentication (personal dashboards)
- [ ] Export to PDF/Excel
- [ ] Email reports
- [ ] Deploy to cloud (AWS, Heroku, etc.)

---

## ❓ FAQ

**Q: Do I need to keep both files?**
A: The original `index.html` is now in `templates/`. The frontend and backend work together.

**Q: Can I still use it without internet?**
A: Yes! It runs locally. Only needs localhost connection between frontend/backend.

**Q: How do I stop the server?**
A: Press `Ctrl+C` in the terminal running the app.

**Q: How do I update dependencies?**
A: Run `pip install -r requirements.txt` after activating venv.

**Q: Can I deploy this?**
A: Yes! See README.md for deployment options (Docker, Heroku, AWS, etc.).

---

## 🆘 Need Help?

Check the full README.md for:

- Detailed API documentation
- Deployment guides
- Troubleshooting tips
- Advanced features
