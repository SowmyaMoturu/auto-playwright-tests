@client-comparison
Feature: Multi-Client Table Validation
  As a user of the application
  I want to compare multiple clients' information in a table
  So that I can analyze their data efficiently

  # Test Configuration
  @config
  * Test Data Location: test_data/clients/section_validations.json
  * Client Sets: test_data/clients/comparison_sets.json
  * HAR Recording: data/har/client_comparison.har

  # API Endpoints
  @api-endpoints
  * GET /api/clients/compare - Returns comparison data for selected clients

  Background: User is logged in
    Given I am logged in using credentials from "test_data/credentials.json"
    And I am on the client comparison page
    And the API response from "data/har/client_comparison.har" is loaded for interception

  @smoke @data-validation
  Scenario: Validate three-client comparison table data
    When I search and select the following clients:
      | Client ID |
      | C123      |
      | C456      |
      | C789      |
    Then the client comparison table should be displayed
    And the API endpoint "/api/clients/compare" should be called
    And the table data should match the API response for the following sections:
      | Section       | Keys                                          | Format Requirements |
      | basicInfo     | clientId, name, status                       | status: uppercase   |
      | contactInfo   | email, phone, address                        | none               |
      | financialInfo | netWorth, annualIncome, investmentTotal     | all: currency      |
      | riskProfile   | riskScore, riskCategory, riskTolerance      | riskScore: number  |
      | history       | lastTransactionDate, accountAge, relationship| date: lastTransactionDate |

  @field-validation
  Scenario Outline: Validate specific section data for each client
    Given I have selected clients from "three_client_set"
    When I look at the "<section>" section
    Then each client column should display data in the following order:
      | Field Position | Key        | Format    |
      | <positions>    | <keys>     | <format>  |
    And the data should match the API response

    Examples:
      | section       | positions | keys                              | format    |
      | basicInfo     | 0,1,2    | clientId,name,status             | uppercase |
      | contactInfo   | 0,1,2    | email,phone,address              | none      |
      | financialInfo | 0,1,2    | netWorth,annualIncome,investment | currency  |

  @error-handling
  Scenario: Handle missing client data gracefully
    Given I have selected clients "C123, C456, C789"
    When the API response is missing data for client "C456"
    Then the table should:
      | Validation                            |
      | Display "N/A" for missing fields      |
      | Show error indicator for that client  |
      | Continue displaying other client data |

  @performance
  Scenario: Validate table load performance with multiple clients
    When I select 3 clients for comparison
    Then the table should load within 2 seconds
    And the API response time should be less than 1 second
    And the table should render without visual glitches

  # Additional Test Context
  @test-metadata
  * Priority: High
  * Test Level: Integration
  * Data Dependencies: Client data, Comparison configuration
  * Validation Rules:
    - Field positions must match key array indices
    - Format rules must be applied before comparison
    - All sections must be validated for each client
    - Column order must match client selection order 