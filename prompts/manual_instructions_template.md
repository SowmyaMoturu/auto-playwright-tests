# Manual Test Instructions Template

## Test Information
- **Feature**: [Feature Name]
- **Description**: [Brief description of what this test covers]
- **Prerequisites**: [Any required setup or conditions]

## Test Data
```json
{
    "credentials": {
        "username": "test_user",
        "password": "test_pass"
    },
    "testData": {
        // Test-specific data
    }
}
```

## Steps

### Step: Login to Application
- Expected: User should be successfully logged in
- Data needed: credentials from test data

### Step: Navigate to Dashboard
- Expected: Dashboard page should load successfully
- Intercept: GET /api/dashboard/summary
- Store Response As: dashboardData
- Validate Using: dashboardData

### Step: Check Dashboard Overview
- Expected: All dashboard sections should display correct data
- Validate Using: dashboardData
- Sections to validate:
  - userProfile
  - recentActivity
  - statistics

### Step: Navigate to Client Comparison
- Expected: Client comparison page should load with data
- Intercept:
  - Endpoint: GET /api/clients/list
    Store As: clientsList
  - Endpoint: GET /api/clients/compare
    Store As: clientCompareData
- Validate Using: clientCompareData

### Step: Select Multiple Clients
- Expected: Selected clients should be highlighted
- Data needed: 
  ```json
  {
    "clientIds": ["C123", "C456", "C789"]
  }
  ```

### Step: Generate Comparison Report
- Expected: Report should be generated with selected clients
- Intercept: POST /api/reports/generate
- Store Response As: comparisonReport
- Validate Using: comparisonReport
- Validation sections:
  - basicInfo
  - financials
  - riskMetrics

### Step: Export Report
- Expected: Report should be downloaded successfully
- Intercept: GET /api/reports/download
- Store Response As: downloadResponse

### Step: Load Client Details
- Expected: Detailed client information should be displayed
- Intercept: GET /api/clients/*/details
- Store Response As: clientDetails
- Validate Using: clientDetails
- Validation points:
  - Personal Information
  - Account History
  - Investment Profile

### Step: Update Client Preferences
- Expected: Client preferences should be updated successfully
- Data needed:
  ```json
  {
    "preferences": {
      "communicationMethod": "email",
      "reportFrequency": "monthly",
      "alertTypes": ["portfolio", "market"]
    }
  }
  ```
- Intercept: PUT /api/clients/*/preferences
- Store Response As: updatedPreferences
- Validate Using: updatedPreferences

### Step: Validate Dashboard Updates
- Expected: Dashboard should reflect recent changes
- Intercept: 
  - Endpoint: GET /api/dashboard/refresh
    Store As: refreshedDashboard
  - Endpoint: GET /api/notifications/new
    Store As: newNotifications
- Validate Using: refreshedDashboard

## API Response Structures

### Dashboard Data
```json
{
    "userProfile": {
        "name": "string",
        "role": "string",
        "lastLogin": "datetime"
    },
    "recentActivity": [
        {
            "type": "string",
            "timestamp": "datetime",
            "details": "object"
        }
    ],
    "statistics": {
        "totalClients": "number",
        "activeReports": "number",
        "pendingTasks": "number"
    }
}
```

### Client Comparison Data
```json
{
    "basicInfo": {
        "clientId": "string",
        "name": "string",
        "status": "string"
    },
    "financials": {
        "portfolioValue": "number",
        "investmentReturn": "number",
        "riskScore": "number"
    },
    "riskMetrics": {
        "tolerance": "string",
        "preferredInvestments": "array",
        "constraints": "array"
    }
}
```

## Notes
- All API responses should be validated for structure and data types
- Date/time values should be in ISO 8601 format
- Numeric values should maintain precision as specified in API contract
- Status codes should be validated for all API calls
- Consider timeout handling for report generation
- Handle pagination for large data sets
- Validate error scenarios and messages 