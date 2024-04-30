# NYU DevOps Project Template

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/Language-Python-blue.svg)](https://python.org/)
[![Build Status](https://github.com/CSCI-GA-2820-SP24-001/shopcarts/actions/workflows/ci.yml/badge.svg)](https://github.com/CSCI-GA-2820-SP24-001/shopcarts/actions)

## Overview

This project contains code for `shopcarts` microservice. The `/service` folder contains your `models/` folder for our models and a `routes.py` file for the `shopcarts` API service. The `/tests` folder has test cases for testing the model and the service separately. You can simply start the testing process once you clone the repository and reopen it in the container. After that is done, please run `flask run` for the local server to test the endpoints, or `honcho start` to test our UI integration with the API endpoints.

The following issues with functions described have been added to the model:

- Query Capability: Model querying for items and shopcarts.
- Code Refactoring: Improved code organization and readability, simplifying feature additions.
- Item and Shopcart Querying: Feature for querying items by productID for detailed insights.
- Shopcart Querying by ID: Detailed querying of shopcarts, showing items, quantities, and prices.
- Shopcart Clear Functionality: Ability to clear all items from shopcarts in one action.
- Item Quantity Incrementation: Updated functionality for adjusting item quantities in shopcarts.
- Item Quantity Decrease: Enabled decreasing item quantities in shopcarts for shopping needs.

## Contents

The project contains the following:

```text
.gitignore          - this will ignore vagrant and other metadata files
.flaskenv           - Environment variables to configure Flask
.gitattributes      - File to gix Windows CRLF issues
.devcontainers/     - Folder with support for VSCode Remote Containers
dot-env-example     - copy to .env to use environment variables
pyproject.toml      - Poetry list of Python libraries required by your code

service/                   - service python package
├── __init__.py            - package initializer
├── config.py              - configuration parameters
├── models/                - module with data models (Shopcart, Item models both are here)
├── routes.py              - module with service routes
└── common                 - common code package
    ├── cli_commands.py    - Flask command to recreate all tables
    ├── error_handlers.py  - HTTP error handling code
    ├── log_handlers.py    - logging setup code
    └── status.py          - HTTP status constants

tests/                     - test cases package
├── __init__.py            - package initializer
├── factories.py           - factory faker file which generates data for our models
├── test_cli_commands.py   - test suite for the CLI
├── test_models.py         - test suite for data models
└── test_routes.py         - test suite for service routes
```
## Models

##### `Shopcart`

| `Name`      | `Description`             | `Data type` |
| ----------- | --------------------- | --------------- |
| id | Unique ID for the shopcart. | Integer         |
| user_id | Unique ID tying a User ID to the shopcart. | String         |
| items | List of items in the shopcart | `items`: List        |

##### `Item`

| `Name`      | `Description`             | `Data type` |
| ----------- | --------------------- | --------------- |
| id | Unique ID for the item. | Integer         |
| cart_id | ID of the shopcart it belongs to | Integer       |
| product_name | Name of the product | String       |
| product_id | ID of the product | Integer       |
| quantity | Quantity of the product in the cart | Integer       |
| product_price | Price of the product when it was added | Numeric       |

## Routes

```text
$ flask routes

Endpoint                       Methods  Rule
-----------------------------  -------  -----------------------------------------------------
index                          GET      /
health                         GET      /health      

create_shopcarts               POST     /api/shopcarts
get_shopcarts                  GET      /api/shopcarts/<int:shopcart_id
delete_shopcarts               DELETE   /api/shopcarts/<int:shopcart_id>
list_shopcarts                 GET      /api/shopcarts
update_shopcarts               PUT      /api/shopcarts/<int:shopcart_id>

delete_item                    DELETE   /api/shopcarts/<int:shopcart_id>/items/<int:product_id> 
delete_items                   DELETE   /api/shopcarts/<int:shopcart_id>/items              
list_items                     GET      /api/shopcarts/<int:shopcart_id>/items
create_item                    POST     /api/shopcarts/<int:shopcart_id>/items
get_item                       GET      /api/shopcarts/<int:shopcart_id>/items/<int:product_id>
update_shopcarts_item          PUT      /api/shopcarts/<int:shopcart_id>/items/<int:product_id>
clear_shopcart                 DELETE   /api/shopcarts/<int:shopcart_id>/items/clear
increment_item_quantity        PUT      /api//shopcarts/<int:shopcart_id>/items/<int:item_id>/increment
decrement_item_quantity        PUT      /api/shopcarts/<int:shopcart_id>/items/<int:item_id>/decrement           
```
## License

Copyright (c) 2016, 2024 [John Rofrano](https://www.linkedin.com/in/JohnRofrano/). All rights reserved.

Licensed under the Apache License. See [LICENSE](LICENSE)

This repository is part of the New York University (NYU) masters class: **CSCI-GA.2820-001 DevOps and Agile Methodologies** created and taught by [John Rofrano](https://cs.nyu.edu/~rofrano/), Adjunct Instructor, NYU Courant Institute, Graduate Division, Computer Science, and NYU Stern School of Business.
