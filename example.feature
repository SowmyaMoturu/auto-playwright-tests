# This is an enhanced feature file format that includes MFE-specific metadata and testing requirements
@mfe-component=UserDashboard
@state-management=redux
@api-integration=true
@test-level=integration
Feature: User Dashboard Component Testing
  As a user of the MFE application
  I want to interact with the dashboard
  So that I can view and manage my data

  # API Endpoints to be intercepted
  @api-endpoints
  * GET /api/user/dashboard - Returns dashboard data
  * POST /api/user/preferences - Updates user preferences
  * GET /api/notifications - Fetches user notifications

  # State Management
  @redux-store
  * slice: userDashboard
  * actions: [FETCH_DASHBOARD, UPDATE_PREFERENCES, TOGGLE_NOTIFICATION]
  * selectors: [getDashboardData, getUserPreferences, getNotifications]

  # Component Dependencies
  @components
  * NotificationPanel (test-id: notification-panel)
  * PreferencesWidget (test-id: preferences-widget)
  * DataGrid (test-id: dashboard-grid)

  Background: User is logged in and on dashboard
    Given I am logged in as "test.user@example.com"
    And I am on the dashboard page
    And the following mock API responses are set up:
      | Endpoint               | Status | Response File               |
      | /api/user/dashboard    | 200    | mocks/dashboard-data.json  |
      | /api/notifications     | 200    | mocks/notifications.json   |
      | /api/user/preferences  | 200    | mocks/preferences.json     |

  @smoke @critical
  Scenario: Dashboard loads with user data
    When the dashboard component mounts
    Then I should see the element "dashboard-grid"
    And the following data should be displayed:
      | Section      | Test ID              | Key Fields                    |
      | Header       | dashboard-header     | userName, lastLoginDate       |
      | Stats        | dashboard-stats      | totalOrders, pendingDelivery |
      | Preferences  | preferences-widget   | theme, notifications         |

    # State Validation
    And the redux store should contain:
      | Selector           | Expected Value    |
      | getDashboardData   | {status: loaded}  |
      | getNotifications   | {count: 3}        |

  @user-interaction
  Scenario: User updates dashboard preferences
    When I click the element "preferences-widget"
    And I toggle the "notifications" switch
    Then the following API call should be made:
      | Method | Endpoint              | Payload                    |
      | POST   | /api/user/preferences | {"notifications": false}   |
    And the redux action "UPDATE_PREFERENCES" should be dispatched
    And the redux store should be updated:
      | Selector           | Expected Value         |
      | getUserPreferences | {notifications: false} |

  @error-handling
  Scenario: Dashboard handles API error gracefully
    Given the API endpoint "/api/user/dashboard" returns error 500
    When the dashboard component mounts
    Then I should see the element "error-message"
    And the text "Unable to load dashboard" should be visible
    And the redux store should contain:
      | Selector           | Expected Value      |
      | getDashboardData   | {status: error}    |

  @performance @monitoring
  Scenario: Dashboard performance metrics
    When the dashboard component mounts
    Then the following metrics should be collected:
      | Metric                    | Threshold |
      | Time to First Byte        | 200ms     |
      | First Contentful Paint    | 1000ms    |
      | Component Load Time       | 500ms     |
      | API Response Time         | 300ms     |

  # Additional Test Metadata
  @test-metadata
  * Priority: High
  * Test Level: Integration
  * Dependencies: NotificationService, PreferencesService
  * Data Requirements: User profile, Notifications, Preferences
  * Environment Variables: API_BASE_URL, FEATURE_FLAGS 