# Multi-Client Table Validation

## Test Info
- Base Template: test_generation_template.md
- Feature: Client Information Display
- Description: Validate multi-client table data against API response using section-based key validation

## Test Steps
1. Login into the application
   - Data needed: Login credentials from test_data/credentials.json
   - Expected: Successfully logged in

2. Navigate to client comparison page
   - Expected: Client comparison table is displayed

3. Search and select clients for comparison
   - Data needed: Client IDs from test_data/clients/comparison_sets.json (key: three_client_set)
   - Expected: Selected clients should be displayed in table

4. Intercept client details API response
   - Data needed: 
     - Endpoint: "/api/clients/compare"
     - HAR Recording: data/har/client_comparison.har
   - Expected: Response contains data for all selected clients

5. Validate table data against response
   - Data needed: Section validation config from test_data/clients/section_validations.json
   - Expected: All specified fields match API data

## Validation Instructions
1. Field Location:
   - Each section contains fields in the order specified by 'keys' array
   - Field position = index of key in the array
   - Example: For basicInfo, 'clientId' is at index 0, 'name' at index 1

2. Section Processing:
   - Loop through each section defined in configuration
   - For each section:
     - Get array of keys for that section
     - Use key index as field position in DOM
     - Apply format specified for the key

3. Client Data:
   - Process each client column (left to right)
   - Client index determines column position
   - Validate all fields for each client



## Test Configuration
### Section Validation (test_data/clients/section_validations.json)
```json
{
    "basicInfo": {
        "keys": ["clientId", "name", "status"],
        "formats": {
            "status": "uppercase"
        }
    },
    "contactInfo": {
        "keys": ["email", "phone", "address"],
        "formats": {}
    },
    "financialInfo": {
        "keys": ["netWorth", "annualIncome", "investmentTotal"],
        "formats": {
            "netWorth": "currency",
            "annualIncome": "currency",
            "investmentTotal": "currency"
        }
    },
    "riskProfile": {
        "keys": ["riskScore", "riskCategory", "riskTolerance"],
        "formats": {
            "riskScore": "number"
        }
    },
    "history": {
        "keys": ["lastTransactionDate", "accountAge", "relationshipStatus"],
        "formats": {
            "lastTransactionDate": "date"
        }
    }
}
```

## Test Data Sets
```json
{
    "three_client_set": {
        "clientIds": ["C123", "C456", "C789"],
        "description": "Comparison set with three clients"
    }
}
``` 