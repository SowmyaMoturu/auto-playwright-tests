# Data Grid Pagination Test

## Scenario Info
- Feature: User Transaction History Grid
- Description: Display and validate paginated transaction data

## Test Steps
1. Navigate to transactions page
   - URL: "/transactions"
   - Expected: Grid loads with default page size

2. Test pagination
   - Change page size to: 25, 50, 100
   - Navigate: next, previous, first, last
   - Expected: Correct data loads for each page

3. Verify data loading
   - Endpoint: "/api/transactions"
   - Method: GET
   - HAR: data/har/transactions.har

4. Test sorting
   - Sort by: date, amount, status
   - Expected: Data updates in correct order

## Test Data
### Grid Configuration
```json
{
    "defaultView": {
        "pageSize": 25,
        "sortField": "date",
        "sortOrder": "desc"
    },
    "columns": [
        {
            "field": "date",
            "sortable": true,
            "defaultSort": true
        },
        {
            "field": "description",
            "sortable": false
        },
        {
            "field": "amount",
            "sortable": true
        },
        {
            "field": "status",
            "sortable": true,
            "filterOptions": ["completed", "pending", "failed"]
        }
    ]
}
```

### Test Scenarios
```json
{
    "pagination": {
        "scenarios": [
            {
                "pageSize": 25,
                "pageNumber": 1,
                "expectedTotal": 100
            },
            {
                "pageSize": 50,
                "pageNumber": 2,
                "expectedTotal": 100
            }
        ]
    },
    "sorting": {
        "scenarios": [
            {
                "field": "date",
                "order": "desc",
                "firstValue": "2024-03-20"
            },
            {
                "field": "amount",
                "order": "asc",
                "firstValue": "10.00"
            }
        ]
    }
}
``` 