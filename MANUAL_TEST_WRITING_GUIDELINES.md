# Manual Test Writing Guidelines

## Overview
This document provides guidelines for writing manual test instructions that will work effectively with our test generation system. The instructions are designed to work with three different prompts:
1. Feature file generation (business-focused scenarios)
2. Step definitions (technical implementation)
3. Overall test generation (framework integration)

## Why Detailed Manual Instructions?

Our approach of using detailed manual test instructions instead of direct feature files as input offers several key advantages:

1. **Separation of Concerns**
   - Feature files focus purely on business behavior
   - Technical details are kept separate but linked
   - Easier maintenance and updates
   - Clear distinction between what vs how

2. **Rich Technical Context**
   - Manual instructions can include implementation details
   - API specifications and response structures
   - DOM element selectors and validation rules
   - State management requirements
   - Error scenarios and edge cases

3. **Better Test Generation**
   - More accurate step definitions
   - Proper error handling
   - Comprehensive validation
   - Framework-specific optimizations

4. **Reusability**
   - Technical details can be shared across tests
   - Common patterns are easier to identify
   - Better template generation
   - More consistent implementation

5. **Maintainability**
   - Changes to technical implementation don't affect business logic
   - Easier to update API versions or UI changes
   - Clear documentation of technical requirements
   - Better tracking of dependencies

6. **Quality Assurance**
   - Complete test coverage
   - Proper validation of all scenarios
   - Better handling of edge cases
   - Clear documentation of test requirements

7. **Framework Integration**
   - Better integration with page objects
   - Proper use of framework utilities
   - Consistent coding patterns
   - Optimized test structure

## Document Structure

### 1. Basic Information (Required)
```markdown
# Test Title

## Test Information
- **Feature**: [Feature name]
- **Scenario**: [Main scenario description]
- **Description**: [Detailed description]
```

### 2. Prerequisites (Required)
```markdown
## Prerequisites
- System state requirements
- User permissions needed
- Data setup requirements
- Environment configuration
```

### 3. Test Steps (Required)
```markdown
## Test Steps
1. [Action]
   - Expected: [Expected outcome]
   - Data: 
     ```json
     {
         "key": "value"
     }
     ```
   - Technical Details: [API endpoints, selectors, etc.]
```

### 4. Technical Implementation Details (Required)
```markdown
## API Details
- Endpoints:
  ```json
  {
      "endpoint": "/api/resource",
      "method": "GET",
      "headers": {},
      "queryParams": {}
  }
  ```
- Response Structure:
  ```json
  {
      "data": {
          "field": "type"
      }
  }
  ```

## Validation Rules
- Data Types:
  ```json
  {
      "field": "string|number|date",
      "formatting": "currency|date|phone"
  }
  ```
- Required Fields: ["field1", "field2"]
```

### 5. Test Data (Required)
```markdown
## Test Data
```json
{
    "testData": {},
    "mockData": {},
    "expectedResults": {}
}
```
```

### 6. Related Files (Optional)
```markdown
## Related Files
- HAR Recording: [data/har/filename.har]
- DOM Snapshot: [data/dom/filename.json]
```

## Writing Guidelines

### 1. For Feature File Generation
- Write clear, business-focused scenario descriptions
- Use Given-When-Then format in test steps
- Avoid technical details in main scenario description
- Focus on business value and user actions
- Use declarative language
- Include clear success criteria

Example:
```markdown
## Test Steps
1. Given user is on dashboard
   - Expected: Dashboard is displayed with all widgets
2. When user selects "Export Report"
   - Expected: Export options are displayed
3. Then report should download in selected format
   - Expected: File is downloaded with correct format
```

### 2. For Step Definitions
- Include technical details with each step
- Specify exact API endpoints and methods
- Include data structures and types
- Provide selectors or element identifiers
- Document state management requirements
- Specify validation rules

Example:
```markdown
## Technical Details
- API Endpoint: `/api/reports/export`
- Method: POST
- Request Body:
  ```json
  {
      "format": "string",
      "filters": "object",
      "dateRange": "object"
  }
  ```
- Selectors:
  ```json
  {
      "exportButton": "[data-testid='export-btn']",
      "formatDropdown": "#format-select"
  }
  ```
```

### 3. For Test Generation
- Include framework-specific requirements
- Specify any custom commands or helpers needed
- Document page object requirements
- Include error handling scenarios
- Specify retry mechanisms
- Document cleanup requirements

Example:
```markdown
## Framework Integration
- Required Page Objects: ["DashboardPage", "ExportModal"]
- Custom Commands: ["waitForDownload", "validateFileFormat"]
- Error Scenarios:
  - Network timeout
  - Invalid file format
  - Missing permissions
```

## Best Practices

1. **Completeness**
   - Include all required sections
   - Provide comprehensive test data
   - Document all technical requirements

2. **Clarity**
   - Use clear, consistent formatting
   - Separate business logic from technical details
   - Use proper JSON formatting for data structures

3. **Maintainability**
   - Use variables for repeated values
   - Document dependencies clearly
   - Include cleanup steps

4. **Reusability**
   - Use parameterized test data
   - Document reusable components
   - Specify shared utilities

## Common Pitfalls to Avoid

1. **Missing Technical Details**
   - Always include API structures
   - Document all selectors
   - Specify validation rules

2. **Unclear Steps**
   - Avoid ambiguous language
   - Include specific expected results
   - Document state requirements

3. **Incomplete Test Data**
   - Include all required fields
   - Specify data types
   - Document dependencies

4. **Poor Organization**
   - Follow the standard structure
   - Separate concerns properly
   - Use consistent formatting

## Example Template
See `data/manual_tests/template.md` for a complete example implementing these guidelines. 