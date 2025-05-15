# Add Multiple Products Test

## Basic Info
- Feature: Shopping Cart
- Description: Add multiple products from different categories and validate cart details

## Test Steps
1. Login into the application
   - Data needed: Login credentials from test_data/credentials.json
   - Expected: Successfully logged in

2. Navigate to products page
   - Expected: Products listing page is displayed

3. Add products to cart
   - Data needed: Use products from test_data/cart_products.json (key: multiple_category_products)
   - Expected: Each product should be added successfully
   - Note: Iterate through products array and add each item

4. Navigate to cart
   - Expected: Shopping cart page is displayed

5. Validate cart details
   - Data needed: Same products array from test_data/cart_products.json
   - Expected: All products should be listed with correct details
   - Validate:
     - Product names
     - Categories
     - Individual prices
     - Total amount

## Referenced Test Data Files
1. test_data/credentials.json:
   ```json
   {
       "test_user": {
           "username": "test_user",
           "password": "test_pass"
       }
   }
   ```

2. test_data/cart_products.json:
   ```json
   {
       "multiple_category_products": {
           "products": [
               {
                   "name": "Gaming Laptop",
                   "category": "Electronics",
                   "price": 1299.99,
                   "currency": "USD",
                   "quantity": 1
               },
               {
                   "name": "Running Shoes",
                   "category": "Sports",
                   "price": 89.99,
                   "currency": "USD",
                   "quantity": 1
               },
               {
                   "name": "Coffee Maker",
                   "category": "Home Appliances",
                   "price": 199.99,
                   "currency": "USD",
                   "quantity": 1
               }
           ],
           "expectedTotal": 1589.97,
           "expectedItemCount": 3
       },
       "single_category_bulk": {
           "products": [
               // Another test data set...
           ]
       }
   }
   ```

## Field Mapping


## API Details
- Endpoints to intercept: 
  - GET "/api/products/*" - For product details
  - POST "/api/cart/add" - For add to cart
  - GET "/api/cart" - For cart details

## Files
- HAR: [data/har/add_products.har]
- DOM: [data/dom/cart_page.json]

## Notes
- Test data file paths are relative to project root
- Use specific key from JSON file as specified in test step
- Handle currency formatting in price display
- Consider stock availability checks

## Validation Rules
1. Data Loading:
   - Verify JSON files exist and are valid
   - Check required keys are present
   - Validate data structure matches expected format

2. Product Addition:
   - Verify each product is added successfully
   - Handle any stock availability messages
   - Validate running total after each addition

3. Cart Validation:
   - Match each product against test data
   - Verify calculations (item totals, cart total)
   - Check currency formatting
   - Validate category grouping if applicable

4. Error Handling:
   - Product not found
   - Out of stock scenarios
   - Invalid quantity
   - Price mismatches 