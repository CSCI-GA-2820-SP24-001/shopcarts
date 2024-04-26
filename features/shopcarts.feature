
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

    Scenario: Create a shopcart
        When I visit the "Home Page"
        And I set the "Shopcart User ID" to "10"
        And I press the "Create Shopcart" button
        Then I should see the message "Success"

    Scenario: List shopcarts
        When I visit the "Home Page"
        And I press the "Search Shopcart" button
        Then I should see "1" under the row "User ID 1" in the table
        And I should see "2" under the row "User ID 2" in the table
        And I should see "3" under the row "User ID 3" in the table

    Scenario: Retrieve a shopcart
        When I visit the "Home Page"
        And I press the "Search Shopcart" button
        When I copy the "Shopcart ID" field
        And I press the "Retrieve Shopcart" button
        Then the "Shopcart ID" field should not be empty
        And the "Shopcart User ID" field should not be empty
        And the "Shopcart Creation Date" field should not be empty

    Scenario: Update a shopcart
        When I visit the "Home Page"
        And I press the "Search Shopcart" button
        Then I should see "1" under the row "User ID 1" in the table
        When I copy the "Shopcart ID" field
        And I set the "Shopcart User ID" to "10"
        And I press the "Update Shopcart" button
        Then I should see the message "Success"

    Scenario: Filter shopcarts by user ID
        When I visit the "Home Page"
        And I set the "Shopcart User ID" to "1"
        And I press the "Search Shopcart" button
        Then I should see "1" under the row "User ID 1" in the table
        And I should not see "User ID 2" in the results
        And I should not see "User ID 3" in the results


