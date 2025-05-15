# Feature File Writing Guidelines

## Structure and Organization

### 1. Test Configuration Section
```gherkin
@config
* Test Data Location: path/to/test/data.json
* API Recording: path/to/har/file.har
```
- Always specify test data locations at the top
- Include HAR recordings for API interception
- Reference configuration files explicitly

### 2. API Endpoints
```gherkin
@api-endpoints
* GET /api/endpoint - Description
* POST /api/endpoint - Description
```
- List all endpoints that need to be intercepted
- Include HTTP method and brief description
- Specify if response manipulation is needed

### 3. Background Setup
```gherkin
Background: Context description
  Given [precondition]
  And [additional setup]
```
- Include all necessary setup steps
- Reference test data files explicitly
- Set up API interceptions

### 4. Data Tables
```gherkin
Then verify data:
  | Column1 | Column2 | Column3 |
  | value1  | value2  | value3  |
```
- Use for structured data validation
- Keep columns aligned for readability
- Include headers for clarity

## Best Practices

### 1. Test Data References
- ✅ DO:
  ```gherkin
  Given I load test data from "test_data/specific_file.json"
  ```
- ❌ DON'T:
  ```gherkin
  Given I load test data from some file
  ```

### 2. Validation Steps
- ✅ DO:
  ```gherkin
  Then the table data should match:
    | Field    | Format    | Validation |
    | amount   | currency  | required   |
  ```
- ❌ DON'T:
  ```gherkin
  Then the data should be correct
  ```

### 3. API Validations
- ✅ DO:
  ```gherkin
  And the API endpoint "/api/data" should be called with:
    | Parameter | Value  |
    | id        | 12345  |
  ```
- ❌ DON'T:
  ```gherkin
  And the API should be called correctly
  ```

## Section-Specific Guidelines

### 1. Data Validation Scenarios
```gherkin
@data-validation
Scenario: Validate specific data
  When I look at [section]
  Then each field should match:
    | Field | Format | Validation Rule |
```
- Include format requirements
- Specify validation rules
- Reference test data explicitly

### 2. Error Handling
```gherkin
@error-handling
Scenario: Handle error condition
  When [error condition occurs]
  Then the system should:
    | Validation                    |
    | Show appropriate error        |
    | Maintain existing valid data  |
```
- Cover common error cases
- Specify expected behavior
- Include recovery steps

### 3. Performance Testing
```gherkin
@performance
Scenario: Validate performance
  Then the operation should complete within [time]
  And meet the following metrics:
    | Metric        | Threshold |
```
- Include specific thresholds
- Define measurement criteria
- Specify test conditions

## Test Metadata

### 1. Required Metadata Tags
```gherkin
@test-metadata
* Priority: [priority level]
* Test Level: [level]
* Dependencies: [list]
```
- Always include priority
- Specify test level
- List all dependencies

### 2. Validation Rules
```gherkin
@validation-rules
- Rule 1: [description]
- Rule 2: [description]
```
- Document all validation rules
- Include format requirements
- Specify order dependencies

## Common Pitfalls to Avoid

1. **Ambiguous Steps**
   - ❌ "Then the data is correct"
   - ✅ "Then the table shows exactly 3 clients with valid IDs"

2. **Missing Data References**
   - ❌ "Given I have some test data"
   - ✅ "Given I load client data from 'test_data/clients.json'"

3. **Unclear Validation Rules**
   - ❌ "Then the format is correct"
   - ✅ "Then the amount is formatted as currency with 2 decimal places"

4. **Implicit Dependencies**
   - ❌ "When the API returns data"
   - ✅ "When the API '/api/clients' returns data matching 'test_data/response.json'"

## Example Template
```gherkin
@feature-tag
Feature: [Feature Name]

  @config
  * Test Data: [paths]
  * API Recording: [path]

  Background: [Setup context]
    Given [preconditions]
    And [setup steps]

  @scenario-tag
  Scenario: [Scenario name]
    When [action]
    Then [validation] with:
      | Field | Validation |
      | ...   | ...        |

  @test-metadata
  * Priority: [level]
  * Dependencies: [list]
  * Validation Rules:
    - [rules list]
``` 