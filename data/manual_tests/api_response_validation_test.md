# API Response Validation Test

## Scenario Info
- Feature: User Profile API
- Description: Validate user profile data retrieval and updates

## Test Steps
1. Get user profile
   - Endpoint: "/api/users/{id}/profile"
   - Method: GET
   - HAR: data/har/user_profile.har

2. Update profile
   - Endpoint: "/api/users/{id}/profile"
   - Method: PUT
   - HAR: data/har/profile_update.har

3. Verify error cases
   - Test invalid data updates
   - Test missing required fields
   - Test permission scenarios

## Test Data
### Profile Data
```json
{
    "validProfiles": [
        {
            "name": "John Doe",
            "email": "john@example.com",
            "preferences": {
                "theme": "dark",
                "notifications": true
            }
        },
        {
            "name": "Jane Smith",
            "email": "jane@example.com",
            "preferences": {
                "theme": "light",
                "notifications": false
            }
        }
    ],
    "invalidUpdates": [
        {
            "scenario": "invalid_email",
            "data": {
                "email": "not-an-email"
            },
            "expectedError": "Invalid email format"
        },
        {
            "scenario": "missing_name",
            "data": {
                "name": ""
            },
            "expectedError": "Name is required"
        }
    ]
}
```

### Test Cases
```json
{
    "getProfile": {
        "scenarios": [
            {
                "userId": "123",
                "expectedStatus": 200,
                "validateFields": ["name", "email", "preferences"]
            },
            {
                "userId": "invalid",
                "expectedStatus": 404,
                "expectedError": "User not found"
            }
        ]
    },
    "updateProfile": {
        "scenarios": [
            {
                "userId": "123",
                "update": {
                    "preferences": {
                        "theme": "dark"
                    }
                },
                "expectedStatus": 200,
                "expectedResponse": {
                    "success": true,
                    "message": "Profile updated"
                }
            }
        ]
    }
} 