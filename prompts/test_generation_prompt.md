# Test Generation Instructions

You are tasked with generating Playwright-Cucumber tests for a Magento e-commerce application. Follow these specific guidelines:

## Framework Context
- TypeScript-based Playwright-Cucumber framework
- Page Object Model with centralized PageObjects.ts
- Custom World implementation with specific properties:
  - context: BrowserContext
  - page: Page
  - baseUrl: string (from world parameters)
  - apiUrl: string (for API calls)
  - debug: boolean
  - data: any (for test data)

## Input Processing
1. Parse the manual test instructions carefully
2. Extract test data and validation points
3. Analyze HAR recordings for:
   - Network requests
   - API endpoints
   - Response patterns
4. Use DOM snapshots for:
   - Locator generation (prefer data-testid)
   - Element hierarchy
   - Dynamic content patterns

## Output Requirements

### 1. Feature File
- Location: src/features/{feature_name}.feature
- Format:
```gherkin
@feature_tag
Feature: {feature_name}

  @scenario_tag
  Scenario: {scenario_name}
    Given {precondition}
    When {action}
    Then {assertion}
```

### 2. Step Definitions
- Location: src/step-definitions/{feature_name}.steps.ts
- Format:
```typescript
import { Given, When, Then } from '@cucumber/cucumber';
import { ScenarioWorld } from '../support/world';
import { expect } from '@playwright/test';
import { PageObjects } from '../pages/PageObjects';

Given('precondition', async function(this: ScenarioWorld) {
    const page = this.page!;
    // Implementation
});
```

### 3. Page Objects
- Location: src/pages/{page_name}.ts
- Format:
```typescript
import { Page } from '@playwright/test';
import { BasePage } from './base_page';

export class PageName extends BasePage {
    constructor(page: Page) {
        super(page);
    }

    // Locators
    private locators = {
        element: '[data-testid="element"]'
    };

    // Methods
    async performAction(): Promise<void> {
        await this.page.click(this.locators.element);
    }
}
```

### 4. PageObjects.ts Updates
- Add new page getter methods
- Follow existing patterns
- Maintain singleton instances

## Best Practices
1. Use async/await consistently
2. Implement proper error handling
3. Add comments for complex logic
4. Use strong typing
5. Follow existing naming conventions
6. Reuse existing page objects when possible
7. Implement proper waits and assertions

## Test Data Handling
1. Use world.data for test data storage
2. Handle environment-specific data
3. Secure sensitive information
4. Support parallel execution

## Validation Guidelines
1. Use Playwright's expect for assertions
2. Implement comprehensive checks
3. Handle dynamic content
4. Add proper error messages
5. Consider cross-browser compatibility

## Error Handling
1. Implement try-catch blocks
2. Add proper error messages
3. Handle timeouts gracefully
4. Consider retry mechanisms
5. Log relevant information

Remember to maintain consistency with the existing framework and follow TypeScript best practices. 

# Test Generation Prompt Guidelines

## Basic Structure
```gherkin
Feature: [Feature Name]

  Background: Common Setup
    Given I am logged into the application
    And I navigate to the target page

  @validation
  Scenario Outline: [Validation Scenario Name]
    When I validate "<key>" data on the page
    Then the data should match the saved response

    Examples:
      | key           |
      | section_key_1 |
      | section_key_2 |
```

## Key Components

### 1. World Context Integration
```typescript
// world.ts usage pattern
interface CustomWorld {
  savedResponse: any;  // API response data
  pageObjects: Record<string, any>;  // Page objects
  testData: Record<string, any>;     // Test data
}

// Access pattern in step definitions
const { savedResponse } = this.world;
```

### 2. Page Object References
- ✅ DO: Reference page object keys in scenario outlines
- ❌ DON'T: Hardcode selectors or test data paths

Example:
```gherkin
# Good - Using page object keys
Examples:
  | key              |
  | basicInfo        |
  | contactDetails   |

# Bad - Hardcoding paths
Examples:
  | key                                    |
  | test_data/clients/basic_info.json     |
  | test_data/clients/contact_details.json |
```

### 3. Step Definition Pattern
```typescript
When('I validate {string} data on the page', async function(key: string) {
  const pageObject = this.world.pageObjects[key];
  const expectedData = this.world.savedResponse[key];
  await pageObject.validateSection(expectedData);
});
```

## Best Practices

### 1. Response Interception
```typescript
// In Background steps
Given('the API response is intercepted', async function() {
  // Response is automatically saved to world.ts
  // No need to specify in feature file
});
```

### 2. Data Validation
```gherkin
# Good - Simple key reference
Scenario Outline: Validate client data sections
  When I validate "<section>" data
  Examples:
    | section     |
    | basicInfo   |
    | financial   |

# Bad - Complex validation in feature
Scenario: Validate with complex data
  When I validate data from "test_data/complex.json"
```

### 3. Page Object Integration
```typescript
// Page Object Pattern
export class ClientComparisonPage {
  readonly sections = {
    basicInfo: '[data-testid=basic-info]',
    financial: '[data-testid=financial-info]'
  };

  async validateSection(key: string, expectedData: any) {
    // Implementation details in page object, not in feature
  }
}
```

## Validation Patterns

### 1. Simple Section Validation
```gherkin
Scenario Outline: Validate client information sections
  When I validate "<section>" information
  Then the data should match the saved response

  Examples:
    | section  |
    | basic    |
    | contact  |
    | finance  |
```

### 2. Complex Data Structures
```gherkin
Scenario Outline: Validate nested data structures
  When I validate "<parent>.<child>" information
  Then the data should match the saved response

  Examples:
    | parent    | child    |
    | profile   | personal |
    | profile   | business |
```

## Common Anti-patterns to Avoid

1. ❌ **Hardcoding Test Data Paths**
   ```gherkin
   When I validate data from "specific/path/data.json"
   ```

2. ❌ **Complex Data Tables in Features**
   ```gherkin
   Then I should see:
     | field1 | field2 | field3 |
     | value1 | value2 | value3 |
   ```

3. ❌ **Multiple Validations in One Scenario**
   ```gherkin
   When I validate basic info and contact info and financial info
   ```

## Example Implementation

### Feature File
```gherkin
Feature: Client Data Validation

  Background: 
    Given I am logged into the application
    And I navigate to Client Comparison Page

  @validation
  Scenario Outline: Validate client data sections
    When I validate "<section>" data on the page
    Then the data should match the saved response

    Examples:
      | section          |
      | basicInfo        |
      | contactInfo      |
      | financialInfo    |
      | riskProfile      |
```

### Step Definition
```typescript
import { When, Then } from '@cucumber/cucumber';
import { CustomWorld } from '../support/world';

When('I validate {string} data on the page', async function(section: string) {
  const page = this.world.pageObjects.clientComparison;
  await page.validateSection(section, this.world.savedResponse[section]);
});

Then('the data should match the saved response', async function() {
  // Validation is handled in the page object
  // This step is mainly for readability
});
```

### Page Object
```typescript
export class ClientComparisonPage {
  constructor(private page: Page) {}

  async validateSection(section: string, expectedData: any) {
    const selector = this.getSectionSelector(section);
    await this.page.waitForSelector(selector);
    // Validation logic here
  }

  private getSectionSelector(section: string): string {
    return `[data-testid=${section}-section]`;
  }
}
```

## Notes
- Keep feature files focused on business logic
- Maintain technical details in step definitions and page objects
- Use world.ts for sharing context between steps
- Reference keys instead of hardcoding paths
- Let page objects handle selectors and validation logic 