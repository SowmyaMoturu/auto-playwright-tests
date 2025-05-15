# React Component Test Mapping

## Component to Test Mapping
```json
{
    "ClientComparisonTable": {
        "testScenarios": {
            "multi_client_table_validation": {
                "componentPath": "src/components/ClientComparison/ClientComparisonTable.tsx",
                "testFile": "data/manual_tests/multi_client_table_validation.md",
                "selectors": {
                    "table": {
                        "base": "[data-testid='client-comparison-table']",
                        "section": "[data-testid='comparison-table-section-${sectionName}']",
                        "cell": "[data-testid='section-cell-${sectionName}-${fieldIndex}-${clientIndex}']"
                    }
                }
            }
        },
        "stateMapping": {
            "selectedClients": {
                "testData": "test_data/clients/comparison_sets.json",
                "stateKey": "store.clients.selected"
            },
            "comparisonData": {
                "testData": "test_data/clients/section_validations.json",
                "stateKey": "store.clients.comparison"
            }
        }
    }
}
```

## Test Data to Props Mapping
```json
{
    "testDataMapping": {
        "section_validations.json": {
            "componentProps": {
                "sections": "sectionConfig",
                "formats": "formatConfig"
            },
            "stateData": {
                "comparisonData": "transformTestDataToState"
            }
        },
        "comparison_sets.json": {
            "componentProps": {
                "clientIds": "selectedClientIds"
            },
            "stateData": {
                "selectedClients": "transformToClientList"
            }
        }
    }
}
```

## Component Event Testing
```json
{
    "eventSequences": {
        "clientSelection": {
            "setup": [
                {
                    "action": "setState",
                    "target": "store.clients.selected",
                    "value": "comparison_sets.json:three_client_set.clientIds"
                }
            ],
            "actions": [
                {
                    "type": "click",
                    "target": "[data-testid='client-selector']",
                    "expectState": {
                        "store.clients.selected": "length === 3"
                    }
                }
            ]
        },
        "sectionExpansion": {
            "setup": [
                {
                    "action": "setState",
                    "target": "local.activeSection",
                    "value": "basicInfo"
                }
            ],
            "actions": [
                {
                    "type": "click",
                    "target": "[data-testid='section-header-${sectionName}']",
                    "expectState": {
                        "local.activeSection": "${sectionName}"
                    }
                }
            ]
        }
    }
}
```

## Validation Rules Mapping
```json
{
    "componentValidation": {
        "sections": {
            "mapping": "section_validations.json",
            "rules": {
                "fieldOrder": "matchKeysOrder",
                "dataDisplay": "matchFormatRules",
                "stateSync": "matchApiData"
            }
        },
        "interactions": {
            "sorting": {
                "trigger": "click:header",
                "expect": "reorderedData"
            },
            "expansion": {
                "trigger": "click:section",
                "expect": "sectionVisible"
            }
        }
    }
}
``` 