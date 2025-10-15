# Redeployable Value Dashboard - Python Flask Application

A web-based dashboard for calculating redeployable value across different stakeholders in the energy sector, featuring battery optimization and financial modeling.

## 🏗️ Architecture

### Backend (Python Flask)

- **Framework**: Flask 3.0
- **Calculations**: Pure Python with NumPy for efficiency
- **API**: RESTful endpoints for all calculations
- **Port**: 5000 (default)

### Frontend

- **Templates**: Jinja2 HTML templates
- **Styling**: Tailwind CSS
- **Charts**: Chart.js
- **Communication**: Fetch API to backend

## 📁 Project Structure

```
om_dashboard/
├── app.py                 # Flask application & routes
├── calculators.py         # Core calculation logic
├── requirements.txt       # Python dependencies
├── templates/
│   └── index.html        # Main dashboard template
├── static/               # Static assets (CSS, JS, images)
└── README.md            # This file
```

## 🚀 Setup Instructions

### Step 1: Create Virtual Environment

```bash
git clone https://github.com/rishavsen1/om_dashboard.git
cd om_dashboard
python3 -m venv venv
source venv/bin/activate  # On Linux/Mac
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Run the Application

```bash
python app.py
```

The application will be available at: **http://localhost:5000**

## 🔧 Development Workflow

### Running in Development Mode

```bash
# Activate virtual environment
source venv/bin/activate

# Run with auto-reload enabled
python app.py
```

Flask will automatically reload when you make changes to Python files.

### Testing API Endpoints

You can test individual endpoints using curl or Postman:

```bash
# Test homeowner calculation
curl -X POST http://localhost:5000/api/calculate/homeowner \
  -H "Content-Type: application/json" \
  -d '{
    "pricingModel": "tou",
    "peakRate": 0.28,
    "offPeakRate": 0.12,
    "peakStart": 14,
    "peakEnd": 19,
    "hvacConsumption": 3.5,
    "hvacPeakTime": 16,
    "hvacLoadShape": 5,
    "batteryCapacity": 10,
    "minSoC": 0.1,
    "maxSoC": 0.9,
    "dischargeDuration": 4,
    "batteryPower": 5,
    "batteryEfficiency": 0.85
  }'
```

## 📡 API Endpoints

### Calculation Endpoints

| Endpoint                   | Method | Description                       |
| -------------------------- | ------ | --------------------------------- |
| `/`                        | GET    | Main dashboard page               |
| `/api/calculate/homeowner` | POST   | Calculate daily homeowner savings |
| `/api/calculate/yearly`    | POST   | Calculate annual blended savings  |
| `/api/calculate/rep`       | POST   | Calculate REP value proposition   |
| `/api/calculate/ci`        | POST   | Calculate C&I business value      |
| `/api/calculate/payback`   | POST   | Calculate payback period          |
| `/api/summary/data`        | GET    | Get summary table data            |

### Example Request/Response

**Request:**

```json
POST /api/calculate/homeowner
{
  "pricingModel": "tou",
  "peakRate": 0.28,
  "hvacConsumption": 3.5,
  ...
}
```

**Response:**

```json
{
  "dailySavings": 2.45,
  "totalHVACUsage": 42.5,
  "energyShifted": 8.2,
  "breakdown": {
    "peakCostNoBattery": 8.50,
    "offPeakCostNoBattery": 3.20,
    ...
  },
  "hourlyData": {
    "rates": [0.12, 0.12, ...],
    "hvacUsage": [0.5, 0.6, ...],
    ...
  }
}
```

## 🎯 Next Steps (Optional Enhancements)

### 1. Add Database Support

```bash
pip install flask-sqlalchemy
```

Create models for saving scenarios, user preferences, etc.

### 2. Add User Authentication

```bash
pip install flask-login
```

Implement user accounts to save calculations and scenarios.

### 3. Export Functionality

```bash
pip install reportlab pandas openpyxl
```

Add PDF/Excel export of results.

### 4. API Documentation

```bash
pip install flask-swagger-ui
```

Auto-generate API documentation.

### 5. Deployment

**Option A: Docker**

```bash
# Create Dockerfile
docker build -t om-value-calc .
docker run -p 5000:5000 om-value-calc
```

**Option B: Production Server**

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

**Option C: Cloud Deployment**

- Deploy to Heroku, AWS, Google Cloud, or Azure
- Use environment variables for configuration
- Set up proper logging and monitoring

## 🔨 Key Improvements Over Original

1. **Separation of Concerns**: Business logic in Python, UI in templates
2. **Testability**: Python functions can be unit tested
3. **Scalability**: Can add database, caching, background jobs
4. **API-First**: Frontend and backend communicate via REST API
5. **Reusability**: Calculations can be used by other applications
6. **Performance**: NumPy operations faster for large datasets
7. **Maintainability**: Python code is easier to maintain than complex JS

## 📝 Usage Examples

### Scenario 1: Calculate Homeowner Savings

1. Navigate to "Detailed Calculators" → "Homeowners"
2. Adjust HVAC and battery parameters
3. View real-time daily savings and charts
4. Run yearly simulation for annual estimates

### Scenario 2: Evaluate REP Value

1. Complete homeowner yearly simulation first
2. Switch to "REPs" tab
3. Enter fleet size and wholesale prices
4. View total annual value proposition

### Scenario 3: Payback Analysis

1. Complete homeowner yearly simulation
2. Switch to "Payback Period" tab
3. Enter system costs and incentives
4. View estimated payback period

## 🐛 Troubleshooting

**Port already in use:**

```bash
# Kill process on port 5000
lsof -ti:5000 | xargs kill -9
```

**Import errors:**

```bash
# Ensure virtual environment is activated
which python  # Should point to venv/bin/python
pip list      # Verify all packages installed
```

**CORS issues:**

```bash
# Already configured in app.py with Flask-CORS
# Check browser console for specific errors
```

## 📄 License

This project is provided as-is for educational and commercial use.

## 👥 Contributing

Feel free to submit issues and enhancement requests!
