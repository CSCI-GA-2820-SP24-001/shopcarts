
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

