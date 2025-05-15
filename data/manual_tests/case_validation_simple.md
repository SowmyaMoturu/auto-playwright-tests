# Case Details Validation

## Basic Info
- Feature: Case Management
- Description: Validate case details data matches API response

## Test Steps
1. Login into the application
   - Data needed: Login credentials
   - Expected: Successfully logged in

2. Navigate to case-management page
   - Expected: Case management page is displayed

3. Search for Case-ID
   - Data needed: Case number "123"
   - Expected: Search results displayed

4. Click first search result and validate case details
   - Data needed: Intercept "/api/cases/*" response
   - Expected: Case details page loads with data

5. Validate transaction information section
   - Data needed: transaction object from API response
   - Expected: All fields match API data

6. Validate client information section
   - Data needed: client object from API response
   - Expected: All fields match API data

7. Validate products table
   - Data needed: products array from API response
   - Expected: All products and their details match API data

## API Details
- Endpoints to intercept: "/api/cases/*"
- Response structure:
  ```json
  {
    "transaction": {
      "transactionId": "",
      "date": "",
      "type": "",
      "amount": 0,
      "status": ""
    },
    "client": {
      "id": "",
      "name": "",
      "contact": ""
    },
    "products": [
      {
        "id": "",
        "name": "",
        "details": {}
      }
    ]
  }
  ```

## Test Data
```json
{
    "credentials": {
        "username": "test_user",
        "password": "test_pass"
    },
    "testData": {
        "caseId": "123"
    }
}
```

## Files
- HAR: [data/har/case_validation.har]
- DOM: [data/dom/case_validation.json]

## Notes
- Validate all fields in each section against API response
- Check data types and formatting (dates, currency)
- Handle pagination if products list is long 