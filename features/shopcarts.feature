Feature: The shopcart service back-end
    As an eCommerce manager
    I need a RESTful catalog service
    So that I can keep track of all my shopcarts

Background:
    Given the following shopcarts
        | cart_id     |
        | 1           |
        | 2           |
        | 3           |
    And the following items
        | product_id  | product_price  | quantity | user_id   |
        | 1           | 10.0           | 2        | 1         |
        | 1           | 10.0           | 1        | 2         |
        | 2           | 30.0           | 3        | 1         |
        | 3           | 25.0           | 1        | 3         |

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Shopcarts REST API Service" in the title
    And I should not see "404 Not Found"

Scenario: List all shopcarts
    When I visit the "Home Page"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "user-id-1" in the results
    And I should see "user-id-2" in the results
    And I should not see "user-id-4" in the results

Scenario: Create a shopcart
    When I visit the "Home Page"
    And I set the "user_id" to "4"
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "shopcart_id" field
    And I press the "Clear" button
    Then the "user_id" field should be empty
    And the "shopcart_id" field should be empty
    When I paste the "shopcart_id" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "4" in the "user_id" field

Scenario: Delete a shopcart
    When I visit the "Home Page"
    And I set the "user_id" to "3"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "user-id-3" in the results
    When I press the "Delete" button
    Then I should see the message "Shopcart has been deleted!"
    When I press the "Search" button
    Then I should see the message "Success"
    And I should not see "user-id-3" in the results

Scenario: Add item to a shopcart
    When I visit the "Home Page"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "user-id-1" in the results
    When I copy the "shopcart_id" field
    And I paste the "shopcart_id" field
    And I set the "product_id" to "4"
    And I set the "product_price" to "50"
    And I set the "quantity" to "2"
    And I press the "Create" button
    Then I should see the message "Success"
    When I press the "Search" button
    Then I should see "product-id-4" in the results

Scenario: Delete an item from a shopcart
    When I visit the "Home Page"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "user-id-1" in the results
    When I copy the "shopcart_id" field
    And I paste the "shopcart_id" field
    And I set the "product_id" to "4"
    And I set the "product_price" to "50"
    And I set the "quantity" to "2"
    And I press the "Create" button
    Then I should see the message "Success"
    When I press the "Search" button
    Then I should see "product-id-4" in the results
    When I visit the "Home Page"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "user-id-1" in the results
    When I copy the "shopcart_id" field
    And I paste the "shopcart_id" field
    And I set the "product_id" to "4"
    And I press the "Delete" button
    Then I should see the message "Success"
    When I visit the "Home Page"
    And I press the "Search" button
    And I should see "user-id-1" in the results
    When I set the "user_id" to "1"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should not see "product-id-4" in the results

Scenario: Query shopcart by user id
    When I visit the "Home Page"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "user-id-1" in the results
    And I should see "user-id-2" in the results
    And I should see "user-id-3" in the results
    And I should not see "user-id-4" in the results
    When I set the "user_id" to "4"
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "shopcart_id" field
    And I press the "Clear" button
    Then the "user_id" field should be empty
    And the "shopcart_id" field should be empty
    When I set the "user_id" to "4"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "user-id-4" in the results
    And I should not see "user-id-3" in the results
    And I should not see "user-id-2" in the results
    And I should not see "user-id-1" in the results
    When I press the "Clear" button
    Then the "user_id" field should be empty
    And the "shopcart_id" field should be empty

Scenario: Read shopcart by shopcart id
    When I visit the "Home Page"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "user-id-1" in the results
    And I should see "user-id-2" in the results
    And I should see "user-id-3" in the results
    And I should not see "user-id-4" in the results
    When I set the "user_id" to "4"
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "shopcart_id" field
    And I press the "Clear" button
    Then the "user_id" field should be empty
    And the "shopcart_id" field should be empty
    When I paste the "shopcart_id" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "4" in the "user_id" field
    And I should see "user-id-4" in the results
    And I should not see "user-id-3" in the results
    And I should not see "user-id-2" in the results
    And I should not see "user-id-1" in the results
    When I copy the "shopcart_id" field
    And I press the "Clear" button
    Then the "user_id" field should be empty
    And the "shopcart_id" field should be empty
    When I paste the "shopcart_id" field
    And I press the "Delete" button
    Then I should see the message "Deleted!"
    When I press the "Clear" button
    Then the "user_id" field should be empty
    And the "shopcart_id" field should be empty
    When I paste the "shopcart_id" field
    And I press the "Retrieve" button
    Then I should see the message "404 Not Found"

Scenario: Read shopcart by shopcart id
    When I visit the "Home Page"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "user-id-1" in the results
    And I should see "user-id-2" in the results
    And I should see "user-id-3" in the results
    And I should not see "user-id-4" in the results
    When I set the "user_id" to "4"
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "shopcart_id" field
    And I press the "Clear" button
    Then the "user_id" field should be empty
    And the "shopcart_id" field should be empty
    When I paste the "shopcart_id" field
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "4" in the "user_id" field
    And I should see "user-id-4" in the results
    And I should not see "user-id-3" in the results
    And I should not see "user-id-2" in the results
    And I should not see "user-id-1" in the results
    When I copy the "shopcart_id" field
    And I press the "Clear" button
    Then the "user_id" field should be empty
    And the "shopcart_id" field should be empty
    When I paste the "shopcart_id" field
    And I press the "Delete" button
    Then I should see the message "Deleted!"
    When I press the "Clear" button
    Then the "user_id" field should be empty
    And the "shopcart_id" field should be empty
    When I paste the "shopcart_id" field
    And I press the "Search" button
    Then I should see the message "404 Not Found"

Scenario: Clear shopcart items by shopcart id
    When I visit the "Home Page"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "user-id-1" in the results
    And I should see "user-id-2" in the results
    And I should see "user-id-3" in the results
    And I should not see "user-id-4" in the results
    When I copy the "shopcart_id" field
    And I press the "Clear" button
    Then I should see the message "Shopcart has been cleared!"
    When I paste the "shopcart_id" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should not see "product-id-1" in the results
    And I should not see "product-id-2" in the results
    And I should not see "product-id-3" in the results
    And I should not see "product-id-4" in the results

Scenario: Update the quantity of an item in a shop cart
    When I visit the "Home Page"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "user-id-1" in the results
    When I copy the "shopcart_id" field
    And I paste the "shopcart_id" field
    And I set the "product_id" to "1"
    And I set the "quantity" to "50"
    And I press the "Update" button
    Then I should see the message "Success"
    When I press the "Search" button
    Then I should see "product-id-1" in the results with "quantity" being "50"
    When I set the "quantity" to "500"
    And I press the "Update" button
    Then I should see the message "Success"
    When I press the "Search" button
    Then I should see "product-id-1" in the results with "quantity" being "500"
    And I should not see "product-id-1" in the results with "quantity" being "50"

Scenario: Update the price of an item in a shopcart
    When I visit the "Home Page"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "user-id-1" in the results
    When I copy the "shopcart_id" field
    And I paste the "shopcart_id" field
    And I set the "product_id" to "1"
    And I set the "product_price" to "100"
    And I press the "Update" button
    Then I should see the message "Success"
    When I press the "Search" button
    Then I should see "product-id-1" in the results with "product_price" being "100"
    When I set the "product_price" to "1000"
    And I press the "Update" button
    Then I should see the message "Success"
    When I press the "Search" button
    Then I should see "product-id-1" in the results with "product_price" being "1000"

Scenario: Update the quantity and price of an item in a shopcart
    When I visit the "Home Page"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "user-id-1" in the results
    When I copy the "shopcart_id" field
    And I paste the "shopcart_id" field
    And I set the "product_id" to "1"
    And I set the "product_quantity" to "10"
    And I set the "product_price" to "50"
    And I press the "Update" button
    Then I should see the message "Success"
    When I press the "Search" button
    Then I should see "product-id-1" in the results with "quantity" being "10"
    And I should see "product-id-1" in the results with "price" being "50"
    When I set the "quantity" to "100"
    And I set the "product_price" to "500"
    And I press the "Update" button
    Then I should see the message "Success"
    When I press the "Search" button
    Then I should see "product-id-1" in the results with "quantity" being "100"
    And I should see "product-id-1" in the results with "product_price" being "500"