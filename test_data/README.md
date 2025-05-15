# Test Data Organization

This directory contains JSON files with test data used across different test scenarios.

## Directory Structure
```
test_data/
├── credentials/
│   ├── users.json        # User credentials for different roles
│   └── api_keys.json     # API keys and tokens
├── products/
│   ├── electronics.json  # Electronics category products
│   ├── sports.json      # Sports category products
│   └── home.json        # Home category products
├── cart/
│   ├── single_item.json      # Single item cart scenarios
│   └── multiple_items.json   # Multiple items cart scenarios
└── cases/
    ├── case_details.json     # Case management test data
    └── case_search.json      # Case search test data
```

## File Naming Convention
- Use lowercase with underscores
- Group related data in subdirectories
- Use descriptive names that indicate content
- Include the data type in the name if not obvious

## JSON File Structure
1. Each file should have a root object
2. Use descriptive keys for different test scenarios
3. Include metadata when needed
4. Group related data sets

Example:
```json
{
    "metadata": {
        "description": "Test data for cart scenarios",
        "lastUpdated": "2024-03-15",
        "version": "1.0"
    },
    "test_scenarios": {
        "scenario_key_1": {
            "description": "Scenario description",
            "data": {
                // Test data
            }
        }
    }
}
```

## Usage in Tests
1. Reference files using relative paths from project root
2. Specify the scenario key in test steps
3. Document any dependencies between data files
4. Keep sensitive data in separate files

## Maintenance
1. Regular validation of JSON structure
2. Update metadata when making changes
3. Document any breaking changes
4. Keep test data in sync with application changes

## Best Practices
1. Use version control for test data
2. Avoid duplicating data across files
3. Keep files focused and manageable in size
4. Include examples and comments
5. Validate data format before committing 