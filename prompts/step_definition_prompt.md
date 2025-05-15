# Step Definition Generation Guide

## Overview
You are a QA automation architect. Generate step definitions for Cucumber feature files that handle API interception automatically when specified in manual instructions.

## Input Requirements
1. Feature file content
2. Manual test instructions (including API interception details and data validation sources)
3. Framework configuration
4. Test data structure

## Manual Instructions Format

### Basic Step Pattern
```markdown
## Step: [Action Description]
- Intercept: [Optional] [HTTP Method] [API Endpoint]
- Store Response As: [Optional] [Response Variable Name]
- Validate Using: [Optional] [World Object Property]
```

### Examples
```markdown
# Simple Navigation
## Step: Navigate to Dashboard

# With API Interception
## Step: Navigate to Client Comparison
- Intercept: /api/clients/compare
- Store Response As: clientCompareResponse

# With Data Validation
## Step: Validate Client Details
- Validate Using: clientsData

# With Multiple Interceptions and Validation
## Step: Load and Validate Dashboard
- Intercept:
  - Endpoint: GET /api/user-profile
    Store As: userProfileData
  - Endpoint: POST /api/dashboard-stats
    Store As: dashboardStats
- Validate Using: dashboardStats
```

## Framework Context
```typescript
interface CustomWorld {
  page: Page;
  pageObjects: any;
  testData: {
    apiConfig?: {
      interceptions?: Array<{
        endpoint: string;
        storageKey: string;
      }>;
    };
  };
  [key: string]: any;  // For dynamically stored responses
}
```

## Core Implementation Patterns

### 1. API Interception Pattern
```typescript
// Reusable API interception setup
async function setupApiInterceptions(this: CustomWorld) {
  if (this.testData.apiConfig?.interceptions) {
    for (const {endpoint, storageKey} of this.testData.apiConfig.interceptions) {
      await this.page.route(endpoint, async route => {
        const response = await route.fetch();
        const json = await response.json();
        this[storageKey] = json;
        await route.fulfill({ response });
      });
    }
  }
}

// Usage in step definition
Given('I navigate to {string}', async function(this: CustomWorld, path: string) {
  await setupApiInterceptions.call(this);
  await this.page.goto(path);
  await this.page.waitForLoadState('networkidle');
});
```

### 2. Data Validation Pattern
```typescript
Then('I validate the data in {string} page', async function(
  this: CustomWorld, 
  pageName: string
) {
  const page = this.pageObjects[pageName];
  // Data source is explicitly specified in manual instructions
  const data = this[this.testData.validationSource];
  
  if (!data) {
    throw new Error(`No data found in world.${this.testData.validationSource} for validation`);
  }
  
  await page.validateData(data);
});

// Example with specific section validation
Then('I validate the {string} section in {string} page', async function(
  this: CustomWorld,
  section: string,
  pageName: string
) {
  const page = this.pageObjects[pageName];
  const data = this[this.testData.validationSource];
  
  if (!data) {
    throw new Error(`No data found in world.${this.testData.validationSource} for validation`);
  }
  
  await page.validateSection(section, data[section]);
});
```

## Best Practices

1. API Interception
   - Set up interceptions before any actions
   - Store responses with descriptive names
   - Maintain original response behavior
   - Handle errors for missing responses

2. Step Implementation
   - Use reusable interception patterns
   - Wait for network idle after actions
   - Support multiple API endpoints
   - Keep steps focused and atomic

3. Data Validation
   - Use explicitly specified data sources
   - Access data directly from world object
   - Support both full and partial validation
   - Clear error messages for missing data

4. Error Handling
   - Check data availability
   - Use proper async/await
   - Handle timeouts
   - Validate data structure

## Real Examples in Codebase
- Basic step implementation: `src/step-definitions/navigation.steps.ts`
- API interception: `src/step-definitions/api.steps.ts`
- Data validation: `src/step-definitions/validation.steps.ts`
- Error handling: `src/support/error-handling.ts` 