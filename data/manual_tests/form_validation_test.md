# Form Validation Test

## Scenario Info
- Feature: User Registration Form
- Description: Validate registration form fields and submission

## Test Steps
1. Navigate to registration form
   - URL: "/register"
   - Expected: Form is displayed

2. Fill form fields
   - Fields defined in: test_data/forms/fields.json
   - Test invalid and valid inputs

3. Submit form
   - Endpoint: "/api/register"
   - Method: POST
   - HAR: data/har/registration.har

## Test Data
### Fields Configuration
```json
{
    "username": {
        "testValues": {
            "valid": ["john_doe", "jane_smith"],
            "invalid": ["j", "user@123", "very-long-username-exceeds-limit"]
        }
    },
    "email": {
        "testValues": {
            "valid": ["user@example.com"],
            "invalid": ["invalid-email", "user@", "@domain.com"]
        }
    },
    "password": {
        "testValues": {
            "valid": ["StrongPass123!"],
            "invalid": ["weak", "12345", "nouppercasepass1"]
        }
    }
}
```

### Expected Results
```json
{
    "validSubmission": {
        "status": 200,
        "redirect": "/dashboard"
    },
    "fieldErrors": {
        "username": {
            "tooShort": "Username must be at least 3 characters",
            "invalidChars": "Username can only contain letters, numbers, and underscore",
            "tooLong": "Username cannot exceed 30 characters"
        },
        "email": {
            "invalid": "Please enter a valid email address"
        },
        "password": {
            "weak": "Password must contain at least 8 characters, one uppercase letter, one number, and one special character"
        }
    }
} 