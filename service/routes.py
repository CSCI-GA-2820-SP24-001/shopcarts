######################################################################
# Copyright 2016, 2024 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
######################################################################

"""
Shopcart Store Service

This service implements a REST API that allows you to Create, Read, Update
and Delete Shopcarts from the inventory of shopcarts in the ShopcartShop
"""
from flask import jsonify, request, url_for, abort
from flask import current_app as app  # Import Flask application
from service.common import status  # HTTP Status Codes
from service.models import Shopcart, Item


######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """Root URL response"""
    app.logger.info("Request for the index page to be returned.")
    return (
        jsonify(
            name="Shopcart REST API Service",
            version="1.0",
            url=url_for("index", _external=True),
        ),
        status.HTTP_200_OK,
    )


######################################################################
#  R E S T   A P I   E N D P O I N T S
######################################################################


######################################################################
# CREATE A NEW SHOPCART
######################################################################
@app.route("/shopcarts", methods=["POST"])
def create_shopcarts():
    """
    Creates a Shopcart

    This endpoint will create a Shopcart based the data in the body that is posted
    """
    app.logger.info("Request to create a shopcart")
    check_content_type("application/json")

    shopcart = Shopcart()
    shopcart.deserialize(request.get_json())
    shopcart.create()
    message = shopcart.serialize()
    location_url = url_for("get_shopcarts", shopcart_id=shopcart.id, _external=True)

    app.logger.info("Shopcart with ID: %d created.", shopcart.id)
    return jsonify(message), status.HTTP_201_CREATED, {"Location": location_url}


######################################################################
# READ A SHOPCART
######################################################################
@app.route("/shopcarts/<int:shopcart_id>", methods=["GET"])
def get_shopcarts(shopcart_id):
    """
    Retrieve a single Shopcart

    This endpoint will return a Shopcart based on it's id
    """
    app.logger.info("Request for shopcart with id: %s", shopcart_id)

    shopcart = Shopcart.find(shopcart_id)
    if not shopcart:
        error(
            status.HTTP_404_NOT_FOUND,
            f"Shopcart with id '{shopcart_id}' was not found.",
        )

    app.logger.info("Returning shopcart for the user with an id: %s", shopcart.user_id)
    return jsonify(shopcart.serialize()), status.HTTP_200_OK


######################################################################
# DELETE A Shopcart
######################################################################
@app.route("/shopcarts/<int:shopcart_id>", methods=["DELETE"])
def delete_shopcarts(shopcart_id):
    """
    Delete a Shopcart

    This endpoint will delete a Shopcart based the id specified in the path
    """
    app.logger.info("Request to delete shopcart with id: %d", shopcart_id)

    shopcart = Shopcart.find(shopcart_id)
    if shopcart:
        shopcart.delete()

    app.logger.info("Shopcart with ID: %d delete complete.", shopcart_id)
    return "", status.HTTP_204_NO_CONTENT


######################################################################
# DELETE AN ITEM
######################################################################
@app.route("/shopcarts/<int:shopcart_id>/items/<int:item_id>", methods=["DELETE"])
def delete_items(shopcart_id, item_id):
    """
    Delete an Item

    This endpoint will delete an Item based the id specified in the path
    """
    app.logger.info(
        "Request to delete Item %s for Shopcart id: %s", (item_id, shopcart_id)
    )

    # See if the item exists and delete it if it does
    item = Item.find(item_id)
    if item:
        item.delete()
    return "", status.HTTP_204_NO_CONTENT


######################################################################
# LIST ALL SHOPCARTS
######################################################################
@app.route("/shopcarts", methods=["GET"])
def list_shopcarts():
    """Returns all Shopcarts"""
    app.logger.info("Request for shopcart list")

    shopcarts = []

    # # See if any query filters were passed in
    # category = request.args.get("category")
    # name = request.args.get("name")
    # if category:
    #     shopcarts = Shopcart.find_by_category(category)
    # elif name:
    #     shopcarts = Shopcart.find_by_name(name)
    # else:
    shopcarts = Shopcart.all()

    results = [shopcart.serialize() for shopcart in shopcarts]
    app.logger.info("Returning %d shopcarts", len(results))
    return jsonify(results), status.HTTP_200_OK


######################################################################
# UPDATE AN EXISTING SHOPCART
######################################################################
@app.route("/shopcarts/<int:shopcart_id>", methods=["PUT"])
def update_shopcarts(shopcart_id):
    """
    Update a Shopcart

    This endpoint will update a Shopcart based the body that is posted
    """
    app.logger.info("Request to update shopcart with id: %d", shopcart_id)
    check_content_type("application/json")

    shopcart = Shopcart.find(shopcart_id)
    if not shopcart:
        error(
            status.HTTP_404_NOT_FOUND,
            f"Shopcart with id: '{shopcart_id}' was not found.",
        )

    shopcart.deserialize(request.get_json())
    shopcart.id = shopcart_id
    shopcart.update()

    app.logger.info("Shopcart with ID: %d updated.", shopcart.id)
    return jsonify(shopcart.serialize()), status.HTTP_200_OK


######################################################################
# ADD AN ITEM TO A SHOPCART
######################################################################
@app.route("/shopcarts/<int:shopcart_id>/items", methods=["POST"])
def create_items(shopcart_id):
    """
    Create an Item on an Shopcart

    This endpoint will add an item to an shopcart
    """
    app.logger.info("Request to create an Item for Shopcart with id: %s", shopcart_id)
    check_content_type("application/json")

    # See if the shopcart exists and abort if it doesn't
    shopcart = Shopcart.find(shopcart_id)
    if not shopcart:
        abort(
            status.HTTP_404_NOT_FOUND,
            f"Shopcart with id '{shopcart_id}' could not be found.",
        )

    # Create an item from the json data
    item = Item()
    item.deserialize(request.get_json())

    # Append the item to the shopcart
    shopcart.items.append(item)
    shopcart.update()

    # Prepare a message to return
    message = item.serialize()

    return jsonify(message), status.HTTP_201_CREATED


######################################################################
# RETRIEVE AN ITEM FROM A SHOPCART
######################################################################
@app.route("/shopcarts/<int:shopcart_id>/items/<int:item_id>", methods=["GET"])
def get_items(shopcart_id, item_id):
    """
    Get an Item

    This endpoint returns just an item
    """
    app.logger.info(
        "Request to retrieve Item %s for Account id: %s", (item_id, shopcart_id)
    )

    # See if the item exists and abort if it doesn't
    item = Item.find(item_id)
    if not item:
        abort(
            status.HTTP_404_NOT_FOUND,
            f"Account with id '{item_id}' could not be found.",
        )

    return jsonify(item.serialize()), status.HTTP_200_OK


######################################################################
# UPDATE AN EXISTING ITEM IN THE SHOPCART
######################################################################
@app.route("/shopcarts/<int:shopcart_id>/items/<int:item_id>", methods=["PUT"])
def update_shopcarts_item(shopcart_id, item_id):
    """
    Update an item in a Shopcart

    This endpoint will update an item in a Shopcart based the body that is posted
    """
    app.logger.info(
        "Request to update item with id %d in a shopcart with id: %d",
        item_id,
        shopcart_id,
    )
    check_content_type("application/json")

    shopcart = Shopcart.find(shopcart_id)
    if not shopcart:
        error(
            status.HTTP_404_NOT_FOUND,
            f"Shopcart with id: '{shopcart_id}' was not found.",
        )

    item = Item.find(item_id)
    if not item:
        error(
            status.HTTP_404_NOT_FOUND,
            f"Item with id: '{item_id}' was not found in shopcart with id: '{shopcart_id}'",
        )

    item.deserialize(request.get_json())
    item.update()

    app.logger.info(
        "Item with id %d in shopcart with id %d updated.", item_id, shopcart_id
    )
    return jsonify(item.serialize()), status.HTTP_200_OK


######################################################################
# LIST ITEMS IN A SHOPCART
######################################################################
@app.route("/shopcarts/<int:shopcart_id>/items", methods=["GET"])
def list_items(shopcart_id):
    """Returns all of the Items for a Shopcart"""
    app.logger.info("Request for all Items for Shopcart with id: %s", shopcart_id)

    # See if the shopcart exists and abort if it doesn't
    shopcart = Shopcart.find(shopcart_id)
    if not shopcart:
        abort(
            status.HTTP_404_NOT_FOUND,
            f"Account with id '{shopcart_id}' could not be found.",
        )

    # Get the items for the shopcart
    results = [item.serialize() for item in shopcart.items]

    return jsonify(results), status.HTTP_200_OK


######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################


######################################################################
# Checks the ContentType of a request
######################################################################
def check_content_type(content_type):
    """Checks that the media type is correct"""
    if "Content-Type" not in request.headers:
        app.logger.error("No Content-Type specified.")
        error(
            status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            f"Content-Type must be {content_type}",
        )

    if request.headers["Content-Type"] == content_type:
        return

    app.logger.error("Invalid Content-Type: %s", request.headers["Content-Type"])
    error(
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        f"Content-Type must be {content_type}",
    )


######################################################################
# Logs error messages before aborting
######################################################################
def error(status_code, reason):
    """Logs the error and then aborts"""
    app.logger.error(reason)
    abort(status_code, reason)
