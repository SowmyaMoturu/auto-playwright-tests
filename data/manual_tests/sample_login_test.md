# Login Test Instructions

## Test Information
- **Feature**: Authentication
- **Scenario**: User can login with valid credentials
- **Description**: Verifies that a user can successfully log in to the Magento demo store using valid credentials

## Prerequisites
- Clean browser session (no existing login)
- Test user account exists in the system

## Test Steps
1. Navigate to the login page
   - Expected: Login page should be displayed
   - Data: Base URL from world parameters

2. Click on "Sign In" link in header
   - Expected: Login form should be visible
   - Data: None

3. Enter email address
   - Expected: Email field should accept input
   - Data: 
     ```json
     {
         "email": "test@example.com"
     }
     ```

4. Enter password
   - Expected: Password field should accept input
   - Data:
     ```json
     {
         "password": "Test123!"
     }
     ```

5. Click "Sign In" button
   - Expected: User should be logged in successfully
   - Data: None

## Validation Points
- Verify successful login message appears
- Verify user is redirected to My Account page
- Verify "Welcome, [username]" text is displayed in header
- Verify "Sign Out" link is visible

## Test Data
```json
{
    "email": "test@example.com",
    "password": "Test123!",
    "expectedWelcomeText": "Welcome, Test User!"
}
```

## Related Files
- HAR Recording: [data/har/login_success.har]
- DOM Snapshot: [data/dom/login_success.json]

## Notes
- Test uses the Magento demo store URL from world parameters
- Password field should be handled securely
- Test should work across all environments (default, sit, uat) 