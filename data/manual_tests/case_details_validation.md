# Case Details Data Validation Test

## Test Information
- **Feature**: Case Management
- **Scenario**: Validate Case Details Data against API Response
- **Description**: Verifies that all displayed case details information matches the data received from the API response, including transaction information, client details, and products data

## Prerequisites
- User must be logged in with appropriate permissions
- Test case ID "123" must exist in the system
- User has access to case management module

## Test Steps
1. Login to the application
   - Expected: User should be successfully logged in
   - Data: 
     ```json
     {
         "username": "test_user",
         "password": "secure_password"
     }
     ```

2. Navigate to case management page
   - Expected: Case management page should be displayed
   - Data: None

3. Search for case by ID
   - Expected: Search results should be displayed
   - Data:
     ```json
     {
         "caseId": "123"
     }
     ```

4. Intercept case details API and click first search result
   - Expected: Case details page should load with intercepted response
   - Data: 
     ```json
     {
         "apiRoute": "/api/cases/*",
         "method": "GET"
     }
     ```

5. Validate transaction information section
   - Expected: All displayed fields should match API response
   - Data: Response path: `response.data.transaction`
   - Fields to validate:
     ```json
     {
         "fields": [
             "transactionId",
             "transactionDate",
             "transactionType",
             "amount",
             "status",
             "currency",
             "merchantName"
         ]
     }
     ```

6. Validate client information section
   - Expected: All displayed fields should match API response
   - Data: Response path: `response.data.client`
   - Fields to validate:
     ```json
     {
         "fields": [
             "clientId",
             "firstName",
             "lastName",
             "email",
             "phone",
             "address"
         ]
     }
     ```

7. Validate products table
   - Expected: All products and their details should match API response
   - Data: Response path: `response.data.products`
   - Fields to validate for each product:
     ```json
     {
         "fields": [
             "productId",
             "name",
             "quantity",
             "price",
             "category",
             "status"
         ]
     }
     ```

## Validation Points
- Verify case details API is intercepted successfully
- Verify all transaction information fields match the API response
- Verify all client information fields match the API response
- Verify number of products in table matches API response
- Verify each product's details match the API response
- Verify data types are correct (numbers, dates, strings)
- Verify currency formatting is correct
- Verify date formatting is consistent

## Test Data
```json
{
    "credentials": {
        "username": "test_user",
        "password": "secure_password"
    },
    "testCaseId": "123",
    "expectedApiResponse": {
        "transaction": {
            "transactionId": "T123456",
            "transactionDate": "2024-03-15T10:30:00Z",
            "transactionType": "PURCHASE",
            "amount": 1500.00,
            "status": "COMPLETED",
            "currency": "USD",
            "merchantName": "Test Merchant"
        },
        "client": {
            "clientId": "C789",
            "firstName": "John",
            "lastName": "Doe",
            "email": "john.doe@example.com",
            "phone": "+1-555-0123",
            "address": "123 Test St, City, Country"
        },
        "products": [
            {
                "productId": "P1",
                "name": "Product 1",
                "quantity": 2,
                "price": 750.00,
                "category": "Electronics",
                "status": "Delivered"
            }
        ]
    }
}
```

## Related Files
- HAR Recording: [data/har/case_details_validation.har]
- DOM Snapshot: [data/dom/case_details_validation.json]

## Notes
- API response structure is crucial for validation
- All amount fields should be validated with proper decimal precision
- Date fields should be validated in the correct timezone
- Table pagination should be handled if products exceed one page
- Network conditions might affect API response time
- Consider adding retry mechanism for API interception 