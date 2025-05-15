# Step Definition Generation Prompt

You are a QA automation architect. Generate step definitions for a Cucumber feature file following these guidelines:

## Input Format
1. Feature file content
2. Manual test instructions (contains technical implementation details)
3. World context configuration
4. Page object structure

## Manual Test Instructions Processing
1. Extract technical details from manual test:
   - API endpoint information
   - Response validation rules
   - Data formatting requirements
   - Test data structure
   - Validation mappings
   - Error scenarios

2. Use these details in step implementations:
   ```typescript
   // Example: If manual test specifies API endpoint and response format
   Given('the API response is intercepted', async function(this: CustomWorld) {
     await this.page.route('/api/endpoint', async route => {
       const response = this.testData.mockResponse;
       await route.fulfill({ json: response });
       this.savedResponse = response;
     });
   });
   ```

## Framework Context
```typescript
interface CustomWorld {
  page: Page;
  savedResponse: any;  // API response data
  pageObjects: Record<string, any>;  // Page objects
  testData: Record<string, any>;     // Test data
}
```

## Implementation Guidelines

### 1. Technical Details from Manual Test
- Use API endpoints specified in manual test
- Follow data validation rules from manual test
- Implement formatting as per manual test requirements
- Handle error scenarios described in manual test
- Use test data structure defined in manual test

### 2. Common Implementation Patterns

#### API Interception
```typescript
// If manual test specifies API details:
Given('the data is loaded', async function(this: CustomWorld) {
  const { endpoint, mockData } = this.testData.apiConfig;
  await this.page.route(endpoint, async route => {
    await route.fulfill({ json: mockData });
    this.savedResponse = mockData;
  });
});
```

#### Data Validation with Formatting
```typescript
// If manual test specifies formatting rules:
When('I validate {string} data', async function(this: CustomWorld, section: string) {
  const page = this.pageObjects.currentPage;
  const expectedData = this.world.savedResponse[section];
  const formatRules = this.testData.formatConfig[section];
  await page.validateSection(section, expectedData, formatRules);
});
```

#### Error Handling
```typescript
// If manual test includes error scenarios:
When('API returns error {int}', async function(this: CustomWorld, status: number) {
  const { endpoint } = this.testData.apiConfig;
  await this.page.route(endpoint, route => 
    route.fulfill({ status, body: this.testData.errorResponse })
  );
});
```

### 3. Example Implementation

Manual Test:
```markdown
## Validation Rules
- Format currency with 2 decimal places
- Dates in MM/DD/YYYY format
- Status in uppercase
- Numbers with thousand separators

## API Details
- Endpoint: /api/clients/compare
- Response structure: { basicInfo: {}, financials: {} }
```

Feature File:
```gherkin
Scenario Outline: Validate client information sections
  When I validate "<section>" data
  Then the data should match the saved response

  Examples:
    | section   |
    | basicInfo |
```

Step Definition:
```typescript
import { When, Then } from '@cucumber/cucumber';
import { CustomWorld } from '../support/world';
import { expect } from '@playwright/test';

When('I validate {string} data', async function(this: CustomWorld, section: string) {
  const page = this.pageObjects.clientComparison;
  const expectedData = this.world.savedResponse[section];
  const formatRules = this.testData.formatConfig[section];
  
  // Apply formatting rules from manual test
  await page.validateSection(section, expectedData, formatRules);
});

Then('the data should match the saved response', async function(this: CustomWorld) {
  // Validation with formatting rules from manual test
  const formatConfig = this.testData.formatConfig;
  await this.pageObjects.currentPage.validateAllSections(formatConfig);
});
```

## Best Practices

1. Manual Test Integration:
# Step Definition Generation Prompt

You are a QA automation architect. Generate step definitions for a Cucumber feature file following these guidelines:

## Input Format
1. Feature file content
2. World context configuration
3. Page object structure
4. Test data configuration

## Framework Context
```typescript
interface CustomWorld {
  page: Page;
  savedResponse: any;  // API response data
  pageObjects: Record<string, any>;  // Page objects
  testData: Record<string, any>;     // Test data
}
```

## Output Requirements

### 1. Basic Structure
```typescript
import { Given, When, Then } from '@cucumber/cucumber';
import { CustomWorld } from '../support/world';
import { expect } from '@playwright/test';

Given('step pattern', async function(this: CustomWorld) {
  // Implementation
});
```

### 2. Key Principles
1. Use world context for data sharing
2. Access page objects through world.pageObjects
3. Use saved API responses from world.savedResponse
4. Keep implementation focused on single responsibility
5. Handle async operations properly

### 3. Common Patterns

#### Navigation Steps
```typescript
Given('I navigate to {string} page', async function(this: CustomWorld, page: string) {
  await this.pageObjects[page].navigate();
});
```

#### Validation Steps
```typescript
When('I validate {string} data', async function(this: CustomWorld, section: string) {
  const page = this.pageObjects.currentPage;
  const expectedData = this.world.savedResponse[section];
  await page.validateSection(section, expectedData);
});
```

#### Response Matching
```typescript
Then('the data should match the saved response', async function(this: CustomWorld) {
  // Validation is handled in the page object
  // This step is mainly for readability
});
```

### 4. DO's and DON'Ts

✅ DO:
- Use world context for state management
- Handle async operations properly
- Use page object methods
- Implement proper error handling
- Add meaningful error messages

❌ DON'T:
- Access DOM directly (use page objects)
- Hardcode selectors
- Mix validation logic with UI interaction
- Skip error handling
- Ignore async/await

### 5. Example Implementation

Feature File:
```gherkin
Scenario Outline: Validate client information sections
  When I validate "<section>" data
  Then the data should match the saved response

  Examples:
    | section   |
    | basicInfo |
```

Step Definition:
```typescript
import { When, Then } from '@cucumber/cucumber';
import { CustomWorld } from '../support/world';
import { expect } from '@playwright/test';

When('I validate {string} data', async function(this: CustomWorld, section: string) {
  const page = this.pageObjects.clientComparison;
  await page.validateSection(section, this.world.savedResponse[section]);
});

Then('the data should match the saved response', async function(this: CustomWorld) {
  // Validation handled in page object
});
```

## Notes
- Keep step definitions simple and focused
- Use page objects for complex logic
- Leverage world context for data sharing
- Handle errors gracefully
- Follow TypeScript best practices 