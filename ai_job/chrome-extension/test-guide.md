# Chrome Extension Validation Testing Guide

## Prerequisites
1. **Start the Backend API Server**
   ```bash
   python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```
   - Verify server is running by visiting: http://localhost:8000/health
   - Should return: `{"status": "healthy", "service": "job-analysis-api"}`

## Chrome Extension Testing Steps

### 1. Load Extension in Developer Mode

1. Open Chrome and navigate to `chrome://extensions/`
2. Enable "Developer mode" (toggle in top-right corner)
3. Click "Load unpacked"
4. Select the `chrome-extension/` folder from this project
5. Verify the extension appears with name "Fake Job Detector AI"

### 2. Basic Functionality Tests

#### Test 1: Popup Opens Without Errors
- Click the extension icon in Chrome toolbar
- **Expected**: Popup opens showing "Job Scam Detector" title
- **Expected**: Textarea and "Analyze Job" button are visible
- **Expected**: No console errors in popup DevTools

#### Test 2: Empty Input Validation
- Click "Analyze Job" button without entering text
- **Expected**: Alert appears: "Please enter a job description to analyze."
- **Expected**: No API request is made
- **Expected**: Results section remains hidden

#### Test 3: Successful Analysis
- Paste this sample job description:
  ```
  Software Engineer position at TechCorp. 
  $150,000 salary for entry-level position.
  Must provide SSN and bank details upfront.
  Work from home, no experience required.
  Contact recruiter@suspicious-domain.com
  ```
- Click "Analyze Job"
- **Expected**: Button shows "Analyzing..." during request
- **Expected**: Results section appears with:
  - Verdict (likely "High Risk" in red)
  - Risk score (likely 70-90/100)
  - List of warning flags as bullet points
- **Expected**: Verdict color matches risk level

### 3. Error Scenario Tests

#### Test 4: Backend Not Running
- Stop the backend server
- Try to analyze a job description
- **Expected**: Alert appears with message about API not running
- **Expected**: Results section remains hidden
- **Expected**: Button returns to "Analyze Job" state

#### Test 5: Rate Limit Testing
- Start backend server
- Rapidly click "Analyze Job" multiple times (>60 requests/minute)
- **Expected**: Eventually get 429 error alert
- **Expected**: Graceful error handling, no crashes

### 4. DevTools Console Check
1. Right-click on extension popup
2. Select "Inspect" to open DevTools
3. Check Console tab for any errors
4. **Expected**: No red error messages
5. **Expected**: Only info logs like "Job Scam Detector Extension loaded"

## Sample Test Data

### Low Risk Job (Expected: Green "Safe")
```
Senior Software Engineer at Google
Competitive salary based on experience
Full benefits package including health insurance
Apply through official Google careers page
Contact: careers@google.com
```

### Medium Risk Job (Expected: Orange "Caution")
```
Marketing Assistant position
$50,000 salary
Some requirements unclear
Contact: hr@newcompany.biz
Remote work available
```

### High Risk Job (Expected: Red "High Risk")
```
Easy money opportunity!
$5000/week working from home
No experience needed
Send personal information to get started
Contact: money@get-rich-quick.net
Urgent hiring!
```

## Validation Checklist

- [ ] Extension loads without errors
- [ ] Popup UI displays correctly (320px width)
- [ ] Empty input shows alert
- [ ] API requests are sent with correct format
- [ ] Successful responses display correctly
- [ ] Verdict colors match risk levels:
  - Safe = Green
  - Caution = Orange  
  - High Risk = Red
- [ ] Flags render as bullet points with warning icons
- [ ] Error handling works for:
  - [ ] Backend not running
  - [ ] Network errors
  - [ ] Rate limiting (429)
  - [ ] Invalid responses
- [ ] No console errors in popup DevTools
- [ ] Button states work correctly (disabled/enabled)
- [ ] Loading state shows "Analyzing..."

## Troubleshooting

### Common Issues:
1. **CORS errors**: Backend should allow requests from chrome-extension://
2. **Network errors**: Check if localhost:8000 is accessible
3. **Manifest errors**: Verify manifest.json is valid
4. **Permission errors**: Check host_permissions in manifest

### Debug Steps:
1. Check browser console for errors
2. Verify API server is running: `curl http://localhost:8000/health`
3. Test API directly: `curl -X POST http://localhost:8000/api/v1/analyze-job -H "Content-Type: application/json" -d '{"job_text":"test","company_url":"","recruiter_email":"","platform_source":"chrome"}'`
4. Check extension permissions in chrome://extensions/