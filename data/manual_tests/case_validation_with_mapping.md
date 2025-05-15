# Case Details Validation with Field Mapping

## Basic Info
- Feature: Case Management
- Description: Validate case details data matches API response with field mapping

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

5. Validate all mapped fields
   - Data needed: API response and field mapping document
   - Expected: All UI fields match mapped API data


## Mapping


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
- All date fields should be converted to local timezone before comparison
- Phone numbers may need formatting before comparison
- Amount should be validated with proper decimal precision
- Some fields require concatenation or formatting before comparison
- Status and type fields may need case transformation

## Validation Rules
1. Data Type Checks:
   - Dates: Valid format and timezone
   - Numbers: Proper decimal places
   - Strings: Proper case and formatting

2. Field Transformations:
   - Name concatenation: firstName + " " + lastName
   - Phone formatting: Raw -> (XXX) XXX-XXXX
   - Status: UPPERCASE
   - Type: Title Case

3. Special Cases:
   - Empty/null handling
   - Currency formatting
   - Date/time localization 