# Healthcare Management System

A modern healthcare management system built with FastAPI and vanilla JavaScript.

## Issues Fixed

### Critical Issues:
1. **Register Button Not Working** - Fixed JavaScript scope issue where navigation functions were not accessible globally
2. **Hardcoded File Paths** - Replaced Windows-specific absolute paths with relative paths using pathlib
3. **Missing Environment Variables Validation** - Added validation for required Supabase configuration
4. **CORS Security Risk** - Restricted CORS origins to specific domains instead of allowing all origins
5. **Missing Error Handling** - Added proper error handling for environment variables

### Non-Critical Issues:
1. **Inconsistent Form Validation** - Cleaned up login form to only send required fields
2. **Poor User Experience** - Added proper success/error message styling (green for success, red for errors)
3. **Missing Input Validation** - Added password minimum length validation

## Setup Instructions

1. **Install Dependencies**
   ```bash
   cd healthcare_app/backend
   pip install -r requirements.txt
   ```

2. **Environment Configuration**
   ```bash
   cp .env.example .env
   # Edit .env file with your Supabase credentials
   ```

3. **Required Environment Variables**
   ```
   SUPABASE_URL=your_supabase_project_url
   SUPABASE_KEY=your_supabase_anon_key
   ALLOWED_ORIGINS=http://localhost:8000,http://127.0.0.1:8000
   ```

4. **Run the Application**
   ```bash
   cd healthcare_app/backend
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

5. **Access the Application**
   Open your browser and navigate to `http://localhost:8000`

## Features

- User registration and authentication
- Role-based access (Doctor, Nurse, Admin)
- Patient management
- Multi-tenant support (Hospital ID)
- Secure API with JWT tokens
- Responsive web interface

## Security Improvements

- Environment variable validation
- Restricted CORS origins
- Input validation on both client and server side
- Secure password requirements (minimum 8 characters)
- JWT token-based authentication

## File Structure

```
healthcare_app/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── requirements.txt     # Python dependencies
│   └── __pycache__/
├── static/
│   ├── main.js             # Frontend JavaScript (fixed)
│   └── styles.css          # CSS styles
├── templates/
│   └── index.html          # Main HTML template
├── .env.example            # Environment variables template
└── README.md              # This file
```

## API Endpoints

- `GET /` - Main application page
- `POST /login` - User authentication
- `POST /register` - User registration
- `GET /patients` - Get patients list (requires authentication)

## Browser Compatibility

- Modern browsers with ES6+ support
- Chrome 60+
- Firefox 55+
- Safari 12+
- Edge 79+
