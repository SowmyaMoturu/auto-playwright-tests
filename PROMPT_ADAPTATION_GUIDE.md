# Prompt Adaptation Guide

## Overview
This guide explains how to adapt the test generation prompts for different testing frameworks while maintaining the Cucumber integration.

## Core Prompts

### 1. Feature File Prompt (`prompts/feature_file_prompt.md`)
**Status**: ✅ No Changes Needed
- This prompt is framework-agnostic
- Focuses on business scenarios and Gherkin syntax
- Remains the same across all frameworks

### 2. Step Definition Prompt (`prompts/step_definition_prompt.md`)
**Status**: 🔄 Requires Framework-Specific Updates

Areas to Update:
```markdown
## Framework Context
```typescript
interface CustomWorld {
    // Update with framework-specific context
    // Example for Selenium:
    driver: WebDriver;
    // Example for Cypress:
    cy: Cypress.cy;
}
```

## Implementation Patterns
- Update action patterns:
  ```typescript
  // Playwright:
  await page.click(selector);
  
  // Your Framework:
  // Add your framework's action patterns
  ```

- Update assertion patterns:
  ```typescript
  // Playwright:
  await expect(page.locator(selector)).toHaveText(text);
  
  // Your Framework:
  // Add your framework's assertion patterns
  ```

- Update wait strategies:
  ```typescript
  // Playwright:
  await page.waitForSelector(selector);
  
  // Your Framework:
  // Add your framework's wait patterns
  ```
```

### 3. Test Generation Prompt (`prompts/test_generation_prompt.md`)
**Status**: 🔄 Requires Framework-Specific Updates

Areas to Update:
```markdown
## Technical Implementation
1. Page Object Structure:
   ```typescript
   // Update with your framework's page object pattern
   export class PageName {
       // Update element definitions
       // Update action methods
       // Update helper functions
   }
   ```

2. Step Definition Structure:
   ```typescript
   // Update imports
   import { Given, When, Then } from '@cucumber/cucumber';
   // Add framework-specific imports
   
   // Update step implementation patterns
   Given('pattern', async function(this: CustomWorld) {
       // Update with framework-specific implementation
   });
   ```

3. Framework Setup:
   ```typescript
   // Update with framework-specific setup
   // - Browser/driver initialization
   // - Custom world configuration
   // - Hook definitions
   ```
```

## Adaptation Process

### 1. Analyze Current Framework
1. Document your framework's:
   - Action patterns
   - Selector strategies
   - Wait mechanisms
   - Assertion styles
   - Page object patterns

### 2. Update Step Definition Prompt
1. Replace Playwright-specific patterns with your framework's patterns
2. Update technical implementation examples
3. Modify world context interface
4. Update common step patterns

### 3. Update Test Generation Prompt
1. Update page object templates
2. Modify step definition structure
3. Update framework setup code
4. Adjust utility functions

### 4. Validate Prompt Updates
1. Test with simple scenarios first
2. Verify generated code follows framework patterns
3. Check for framework-specific best practices
4. Validate custom command integration

## Example: Framework-Specific Updates

### Selenium WebDriver
```typescript
// Step Definition Pattern
Given('user clicks {string}', async function(this: CustomWorld, selector: string) {
    await this.driver.findElement(By.css(selector)).click();
});

// Page Object Pattern
export class LoginPage {
    private elements = {
        username: By.id('username'),
        password: By.id('password')
    };

    async login(username: string, password: string) {
        await this.driver.findElement(this.elements.username).sendKeys(username);
        await this.driver.findElement(this.elements.password).sendKeys(password);
    }
}
```

### Cypress
```typescript
// Step Definition Pattern
Given('user clicks {string}', function(selector: string) {
    cy.get(selector).click();
});

// Page Object Pattern
export class LoginPage {
    elements = {
        username: '#username',
        password: '#password'
    };

    login(username: string, password: string) {
        cy.get(this.elements.username).type(username);
        cy.get(this.elements.password).type(password);
    }
}
```

## Best Practices

1. **Maintain Structure**
   - Keep the same prompt sections
   - Preserve documentation patterns
   - Follow consistent formatting

2. **Framework Optimization**
   - Use framework-recommended patterns
   - Include framework-specific utilities
   - Follow framework conventions

3. **Documentation**
   - Document framework-specific changes
   - Include example patterns
   - Note any limitations

4. **Testing**
   - Validate generated code
   - Test edge cases
   - Verify framework integration 