
Feature: The shopcarts service back-end
    As a Shopcarts Service Owner
    I need a RESTful catalog service
    So that I can keep track of all my shopcarts

    Background:
        Given the following shopcarts
            | user_id |
            | 1       |
            | 2       |
            | 3       |
        And the following items
            | user_id | product_name   | product_id | product_price | quantity |
            | 1       | MacBook 13 Pro | 1          | 1500.0        | 2        |
            | 2       | MacBook 13 Air | 2          | 1000.0        | 1        |
            | 2       | MacBook 13 Pro | 1          | 1500.0        | 1        |
            | 1       | MacBook 15 Air | 3          | 1200.0        | 3        |
            | 3       | MacBook 15 Pro | 4          | 2700.0        | 1        |


    Scenario: The server is running
        When I visit the "Home Page"
        Then I should see "Shopcart Demo RESTful Service" in the title
        And I should not see "404 Not Found"

    # CREATE A SHOPCART
    Scenario: Create a shopcart
        When I visit the "Home Page"
        And I set the "Shopcart User ID" to "10"
        And I press the "Create Shopcart" button
        Then I should see the message "Success"

    # LIST ALL SHOPCARTS
    Scenario: List shopcarts
        When I visit the "Home Page"
        And I press the "Search Shopcart" button
        Then I should see "1" under the row "User ID 1" in the table
        And I should see "2" under the row "User ID 2" in the table
        And I should see "3" under the row "User ID 3" in the table

    # LIST FILTERED SHOPCARTS
    Scenario: Filter shopcarts by user ID
        When I visit the "Home Page"
        And I set the "Shopcart User ID" to "1"
        And I press the "Search Shopcart" button
        Then I should see "1" under the row "User ID 1" in the table
        And I should not see "User ID 2" in the results
        And I should not see "User ID 3" in the results

    # GET A SHOPCART
    Scenario: Retrieve a shopcart
        When I visit the "Home Page"
        And I press the "Search Shopcart" button
        When I copy the "Shopcart ID" field
        And I press the "Retrieve Shopcart" button
        Then the "Shopcart ID" field should not be empty
        And the "Shopcart User ID" field should not be empty
        And the "Shopcart Creation Date" field should not be empty

    # UPDATE A SHOPCART
    Scenario: Update a shopcart
        When I visit the "Home Page"
        And I press the "Search Shopcart" button
        Then I should see "1" under the row "User ID 1" in the table
        When I copy the "Shopcart ID" field
        And I set the "Shopcart User ID" to "10"
        And I press the "Update Shopcart" button
        Then I should see the message "Success"

    # DELETE A SHOPCART
    Scenario: Delete a shopcart
        When I visit the "Home Page"
        And I set the "Shopcart User ID" to "1"
        And I press the "Search Shopcart" button
        Then I should see the message "Success"
        And I should see "1" under the row "User ID 1" in the table
        When I press the "Delete Shopcart" button
        Then I should see the message "Success"
        When I press the "Search Shopcart" button
        Then I should see the message "Success"
        And I should not see "User ID 1" in the results

    # CREATE AN ITEM
    Scenario: Create an item
        When I visit the "Home Page"
        And I set the "Shopcart User ID" to "10"
        And I press the "Create Shopcart" button
        Then I should see the message "Success"
        When I copy the "Shopcart ID" field
        And I paste the "Item Shopcart ID" field
        And I set the "Item Product Name" to "MacBook 15 Pro+"
        And I set the "Item Product ID" to "4"
        And I set the "Item Product Price" to "2700.0"
        And I set the "Item Quantity" to "1"
        And I press the "Create Item" button
        Then I should see the message "Success"
        And I should see "4" in the "Item Product ID" field
        And I should see "1" in the "Item Quantity" field
        And I should see "2700.0" in the "Item Product Price" field
        And I should see "MacBook 15 Pro+" in the "Item Product Name" field

    # DELETE AN ITEM
    Scenario: Delete an item
        When I visit the "Home Page"
        And I press the "Search Shopcart" button
        Then I should see the message "Success"
        When I copy the "Shopcart ID" field
        And I paste the "Item Shopcart ID" field
        And I press the "Search Item" button
        Then the "Item ID" field should not be empty
        When I press the "Delete Item" button
        Then I should see the message "Success"

    # UPDATE AN ITEM
    Scenario: Update an item
        When I visit the "Home Page"
        And I press the "Search Shopcart" button
        Then I should see the message "Success"
        When I copy the "Shopcart ID" field
        And I paste the "Item Shopcart ID" field
        And I press the "Search Item" button
        Then the "Item ID" field should not be empty
        When I change "Item Product Price" to "150"
        And I change "Item Quantity" to "2"
        When I press the "Update Item" button
        Then I should see the message "Success"
        And I should see "150.00" in the "Item Product Price" field
        And I should see "2" in the "Item Quantity" field

    # RETRIEVE AN ITEM
    Scenario: Retrieve an item
        When I visit the "Home Page"
        And I press the "Search Shopcart" button
        Then I should see the message "Success"
        When I copy the "Shopcart ID" field
        And I paste the "Item Shopcart ID" field
        And I press the "Search Item" button
        Then the "Item ID" field should not be empty
        When I press the "Retrieve Item" button
        Then I should see the message "Success"
        And the "Item ID" field should not be empty
        And the "Item Product ID" field should not be empty
        And the "Item Product Price" field should not be empty
        And the "Item Quantity" field should not be empty