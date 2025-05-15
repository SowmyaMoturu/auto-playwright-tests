# Step Definition Generation Guide

## Overview
You are a QA automation architect. Generate step definitions for Cucumber feature files that handle API interception automatically when specified in manual instructions.

## Input Requirements
1. Feature file content
2. Manual test instructions (including API interception details)
3. Framework configuration
4. Test data structure

## Manual Instructions Format

### Simple Step (No Interception)
```markdown
## Step: Navigate to Dashboard
```

### Step with Single API Interception
```markdown
## Step: Navigate to Client Comparison
- Intercept: /api/clients/compare
- Store Response As: clientCompareResponse
```

### Step with Navigation and API Interception
```markdown
## Step: Continue to Review Page
- Intercept: POST /api/recommended-products
- Store Response As: recommendedProducts
```

### Step with API Interception
```markdown
## Step: Add Product in Review
- Intercept: POST /api/review-products
- Store Response As: reviewProducts
```

### Step with Multiple API Interceptions
```markdown
## Step: Load Dashboard Data
- Intercept:
  - Endpoint: GET /api/user-profile
    Store As: userProfileData
  - Endpoint: POST /api/dashboard-stats
    Store As: dashboardStats
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

## Step Definition Patterns

### 1. Step Implementation with API Interception
```typescript
Given('I navigate to the client comparison page', async function(this: CustomWorld) {
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

  // Your step implementation here
  await this.page.goto('/client-comparison');
  await this.page.waitForLoadState('networkidle');
});
```

### 2. Step with Multiple API Interceptions
```typescript
When('I click continue to proceed to review page', async function(this: CustomWorld) {
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

  // Your step implementation here
  await this.page.click('[data-testid="continue-button"]');
  await this.page.waitForLoadState('networkidle');
});
```

### 3. Data Validation
```typescript
Then('the {string} section should match the API data', async function(this: CustomWorld, section: string) {
  const page = this.pageObjects.currentPage;
  if (!this.clientCompareResponse) {
    throw new Error('No API response captured for validation');
  }
  await page.validateSection(section, this.clientCompareResponse[section]);
});
```

## Example Implementation

### Manual Instructions
```markdown
## Step: Navigate to Client Comparison
- Intercept: /api/clients/compare
- Store Response As: clientCompareResponse

## Step: Validate Client Data
```

### Feature File
```gherkin
Scenario: Validate client comparison data
  Given I navigate to the client comparison page
  Then the "basicInfo" section should match the API data
  And the "financials" section should match the API data
```

### Step Definition
```typescript
import { Given, Then } from '@cucumber/cucumber';
import { CustomWorld } from '../support/world';
import { expect } from '@playwright/test';

Given('I navigate to the client comparison page', async function(this: CustomWorld) {
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

  await this.page.goto('/client-comparison');
  await this.page.waitForLoadState('networkidle');
});

Then('the {string} section should match the API data', async function(this: CustomWorld, section: string) {
  const page = this.pageObjects.currentPage;
  if (!this.clientCompareResponse) {
    throw new Error('No API response captured for validation');
  }
  await page.validateSection(section, this.clientCompareResponse[section]);
});
```

## Best Practices

1. API Interception
   - Only intercept when specified in manual instructions
   - Store responses with specified names
   - Maintain original response behavior
   - Clear error handling for missing responses

2. Step Implementation
   - Keep manual instructions focused on API interception
   - Handle API setup before any actions
   - Wait for network idle after actions
   - Support multiple API interceptions

3. Validation
   - Check for API response availability by name
   - Provide clear error messages
   - Use page object validation methods
   - Support section-specific validation

4. Error Handling
   - Clear error messages for missing API data
   - Proper async/await usage
   - Timeout handling
   - Response validation errors 