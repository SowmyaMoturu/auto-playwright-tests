# Test Generation Template

## Common Requirements

### Recording Files
1. HAR Recording:
   - Contains actual API responses
   - Records all network interactions
   - Used as source of truth for validation
   - Captures request/response timing
   - Stores response data format

2. DOM Snapshot:
   - Contains page structure and layout
   - Used for element locator extraction
   - Captures dynamic content areas
   - Provides component hierarchy

### Locator Extraction Rules
- Extract locators from DOM snapshots
- Prioritize data-testid attributes
- Use semantic selectors when data-testid not available
- Generate stable selectors based on DOM structure
- Handle dynamic content areas
- Consider component hierarchy
- Support indexed elements for lists/tables

### Data Format Requirements
1. Standard Formats:
   - currency: Format numbers with currency symbol and decimals
   - date: Format as specified date string pattern
   - number: Format as plain numbers with optional decimals
   - uppercase: Convert text to uppercase
   - lowercase: Convert text to lowercase
   - boolean: Convert to Yes/No or True/False display
   - percentage: Format as percentage with symbol
   - default: Use raw value comparison

2. Custom Formats:
   - Define in test configuration
   - Support regex patterns
   - Allow format chaining
   - Handle locale-specific formats

### Validation Requirements
1. Structure Validation:
   - Verify DOM structure matches expected layout
   - Validate element hierarchy
   - Check section ordering
   - Verify field positions
   - Validate table/list structures

2. Data Validation:
   - Compare UI values with API response data
   - Apply specified formatting rules
   - Handle null/undefined/empty values
   - Skip validation for missing fields
   - Support partial validation
   - Handle dynamic data updates

3. API Response Processing:
   - Extract data from HAR recording
   - Match response to correct request
   - Handle multiple response formats
   - Process paginated responses
   - Support response transformation

### Error Handling Requirements
1. Validation Errors:
   - Report field-level validation failures
   - Include section and context information
   - Capture formatting mismatches
   - Report missing required fields
   - Handle unexpected data types

2. Technical Errors:
   - Handle network failures
   - Report DOM structure mismatches
   - Capture selector failures
   - Handle timeout issues
   - Report API response errors

3. Error Reporting:
   - Provide clear error messages
   - Include expected vs actual values
   - Add context information
   - Support error categorization
   - Enable error filtering

## Notes for Test Generation
1. HAR Processing:
   - Extract relevant API responses
   - Match responses to test context
   - Consider response timing
   - Handle response dependencies
   - Process response transformations
   - Extract API response data
   - Consider HAR recording timing for response matching

2. DOM Processing:
   - Extract stable locators
   - Generate selector strategies
   - Handle dynamic content
   - Support component reuse
   - Consider state changes
   - Use base locators for element selection
   - Follow element order in validation

3. Validation Logic:
   - Generate optimized validation code
   - Include error handling
   - Support async operations
   - Handle retry logic
   - Enable partial validation
   - Generate appropriate test assertions
   - Handle dynamic data comparison
   - Follow key order for field validation
   - Apply specified formatting rules

4. Test Structure:
   - Create modular test steps
   - Support test data injection
   - Enable configuration override
   - Handle setup/teardown
   - Support test parallelization
   - Generate validation logic based on configuration
   - Include comprehensive error handling and reporting 