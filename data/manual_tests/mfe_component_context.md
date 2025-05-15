# MFE Component Context Template

## Component Structure
```json
{
    "componentName": "ClientComparisonTable",
    "type": "container",
    "path": "src/components/ClientComparison/ClientComparisonTable.tsx",
    "testId": "client-comparison-table",
    "children": {
        "TableHeader": {
            "type": "component",
            "testId": "comparison-table-header",
            "props": ["title", "selectedClients"]
        },
        "TableSection": {
            "type": "component",
            "testId": "comparison-table-section-${sectionName}",
            "props": ["sectionData", "clientIds"],
            "children": {
                "SectionHeader": {
                    "testId": "section-header-${sectionName}"
                },
                "SectionRow": {
                    "testId": "section-row-${sectionName}-${fieldIndex}",
                    "repeatable": true,
                    "childCell": {
                        "testId": "section-cell-${sectionName}-${fieldIndex}-${clientIndex}"
                    }
                }
            }
        }
    }
}
```

## State Management
```json
{
    "store": {
        "clients": {
            "selected": {
                "type": "array",
                "selector": "useSelector(state => state.clients.selectedClients)",
                "actions": ["selectClient", "deselectClient"]
            },
            "comparison": {
                "type": "object",
                "selector": "useSelector(state => state.clients.comparisonData)",
                "actions": ["fetchComparisonData", "updateComparison"]
            }
        }
    },
    "local": {
        "sortState": {
            "type": "object",
            "default": {
                "field": null,
                "direction": "asc"
            }
        },
        "activeSection": {
            "type": "string",
            "default": "basicInfo"
        }
    }
}
```

## Event Handlers
```json
{
    "userInteractions": {
        "onClientSelect": {
            "type": "action",
            "dispatch": "selectClient",
            "payload": "clientId"
        },
        "onSectionExpand": {
            "type": "state",
            "updates": ["activeSection"]
        },
        "onSort": {
            "type": "state",
            "updates": ["sortState"],
            "triggers": ["reorderClients"]
        }
    },
    "dataFlow": {
        "onMount": [
            "fetchSelectedClients",
            "fetchComparisonData"
        ],
        "onClientChange": [
            "fetchComparisonData",
            "updateTableView"
        ]
    }
}
```

## API Integration
```json
{
    "endpoints": {
        "getComparison": {
            "path": "/api/clients/compare",
            "method": "GET",
            "params": ["clientIds"],
            "response": "ComparisonDataType"
        }
    },
    "dataTransforms": {
        "ComparisonDataType": {
            "toComponent": "transformApiToTableData",
            "toApi": "transformTableToApiData"
        }
    }
}
```

## Component Props
```typescript
interface ClientComparisonTableProps {
    selectedClientIds: string[];
    onClientSelect: (clientId: string) => void;
    onDataLoad: (data: ComparisonDataType) => void;
    viewOptions?: {
        sortable?: boolean;
        expandable?: boolean;
        showDiff?: boolean;
    };
}
``` 