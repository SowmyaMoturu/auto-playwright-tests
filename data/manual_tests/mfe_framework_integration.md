# MFE Framework Integration

## Framework Configuration
```json
{
    "mfeConfig": {
        "name": "client-comparison",
        "type": "react",
        "version": "1.0.0",
        "dependencies": {
            "react": "^18.0.0",
            "redux": "^4.0.0",
            "playwright": "^1.0.0"
        }
    },
    "testFramework": {
        "baseTemplate": "test_generation_template.md",
        "componentContext": "mfe_component_context.md",
        "testMapping": "react_component_test_mapping.md"
    }
}
```

## Component Discovery
```json
{
    "discovery": {
        "patterns": {
            "components": "src/components/**/*.{tsx,jsx}",
            "tests": "src/**/*.test.{ts,tsx}",
            "testData": "test_data/**/*.json"
        },
        "analysis": {
            "extractTestIds": true,
            "parseProps": true,
            "mapStateUsage": true
        }
    }
}
```

## Test Generation Integration
```json
{
    "generation": {
        "templates": {
            "component": {
                "source": "mfe_component_context.md",
                "variables": ["componentName", "testId", "props"]
            },
            "test": {
                "source": "test_generation_template.md",
                "variables": ["feature", "description", "steps"]
            }
        },
        "mapping": {
            "source": "react_component_test_mapping.md",
            "variables": ["selectors", "stateMapping", "eventSequences"]
        }
    }
}
```

## State Management Integration
```json
{
    "stateIntegration": {
        "redux": {
            "selectors": "src/selectors/**/*.ts",
            "actions": "src/actions/**/*.ts",
            "reducers": "src/reducers/**/*.ts"
        },
        "testHooks": {
            "setState": "useTestState",
            "getState": "useTestSelector",
            "dispatch": "useTestDispatch"
        }
    }
}
```

## Test Execution Context
```json
{
    "executionContext": {
        "setup": {
            "mfe": {
                "mount": "mountComponent",
                "unmount": "unmountComponent",
                "setState": "setInitialState"
            },
            "network": {
                "mock": "setupApiMocks",
                "har": "loadHarFile"
            }
        },
        "validation": {
            "dom": "validateDomState",
            "redux": "validateReduxState",
            "component": "validateComponentProps"
        }
    }
}
```

## Framework Extensions
```json
{
    "extensions": {
        "selectors": {
            "generate": "generateTestSelectors",
            "validate": "validateSelectors"
        },
        "stateHandling": {
            "transform": "transformStateData",
            "compare": "compareStateValues"
        },
        "testData": {
            "load": "loadTestData",
            "transform": "transformTestData"
        }
    }
}
``` 