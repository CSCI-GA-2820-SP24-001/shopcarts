$(function () {

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the SHOPCARTS form with data from the response
    function update_shopcarts_form_data(res) {
        $("#shopcart_id").val(res.id);
        $("#shopcart_user_id").val(res.user_id);
        const creation_date = new Date(res.creation_date);
        const creation_day = creation_date.getDate();
        const creation_month = creation_date.getMonth() + 1;
        const creation_year = creation_date.getFullYear();
        const creation_date_formatted = `${creation_year}-${creation_month < 10 ? '0' + creation_month : creation_month}-${creation_day < 10 ? '0' + creation_day : creation_day}`;
        $("#shopcart_creation_date").val(creation_date_formatted);

        const last_updated_date = new Date(res.last_updated);
        const last_updated_day = last_updated_date.getDate();
        const last_updated_month = last_updated_date.getMonth() + 1;
        const last_updated_year = last_updated_date.getFullYear();
        const last_updated_formatted = `${last_updated_year}-${last_updated_month < 10 ? '0' + last_updated_month : last_updated_month}-${last_updated_day < 10 ? '0' + last_updated_day : last_updated_day}`;
        $("#shopcart_last_update_date").val(last_updated_formatted);
        $("#shopcart_total_price").val(res.total_price);
    }

    /// Clears all SHOPCART form fields
    function clear_shopcarts_form_data() {
        $("#shopcart_id").val("");
        $("#shopcart_user_id").val("");
        $("#shopcart_creation_date").val("");
        $("#shopcart_last_update_date").val("");
        $("#shopcart_items").val("");
        $("#shopcart_total_price").val("");
    }

    // Updates the ITEMS form with data from the response
    function update_items_form_data(res) {
        $("#item_id").val(res.id);
        $("#item_product_name").val(res.product_name);
        $("#item_shopcart_id").val(res.cart_id);
        $("#item_product_id").val(res.product_id);
        $("#item_product_price").val(res.product_price);
        $("#item_quantity").val(res.quantity);
        $("#item_subtotal_price").val(res.subtotal);
    }

    /// Clears all ITEMS form fields
    function clear_items_form_data() {
        $("#item_id").val("");
        $("#item_product_name").val("");
        $("#item_shopcart_id").val("");
        $("#item_product_id").val("");
        $("#item_product_price").val("");
        $("#item_quantity").val("");
        $("#item_subtotal_price").val("");
    }

    // Updates the flash message area
    function flash_message(message) {
        $("#flash_message").empty();
        $("#flash_message").append(message);
    }

    // ****************************************
    // Create a Shopcart
    // ****************************************

    $("#create-shopcart-btn").click(function () {

        let shopcart_user_id = $("#shopcart_user_id").val();

        let data = {
            "user_id": shopcart_user_id,
            "items": [],
        };

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "POST",
            url: "/shopcarts",
            contentType: "application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function (res) {
            update_shopcarts_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function (res) {
            flash_message(res.responseJSON.message)
        });
    });

    // ****************************************
    // Create an Item
    // ****************************************

    $("#create-item-btn").click(function () {
        let item_product_name = $("#item_product_name").val();
        let item_shopcart_id = $("#item_shopcart_id").val();
        let item_product_id = $("#item_product_id").val();
        let item_product_price = $("#item_product_price").val();
        let item_quantity = $("#item_quantity").val();

        let data = {
            "cart_id": item_shopcart_id,
            "product_name": item_product_name,
            "product_id": item_product_id,
            "product_price": item_product_price,
            "quantity": item_quantity
        }

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "POST",
            url: `/shopcarts/${item_shopcart_id}/items`,
            contentType: "application/json",
            data: JSON.stringify(data),
        });


        ajax.done(function (res) {
            update_items_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function (res) {
            flash_message(res.responseJSON.message)
        });
    });

    // ****************************************
    // Update a Shopcart: WIP
    // ****************************************

    $("#update-shopcart-btn").click(function () {

        let shopcart_id = $("#shopcart_id").val();
        let shopcart_user_id = $("#shopcart_user_id").val();

        let data = {
            "user_id": shopcart_user_id,
            // TODO: figure out what to do with this?
            "items": [],
        };

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "PUT",
            url: `/shopcarts/${shopcart_id}`,
            contentType: "application/json",
            data: JSON.stringify(data)
        })

        ajax.done(function (res) {
            update_shopcarts_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function (res) {
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Update an Item
    // ****************************************
    $("#update-item-btn").click(function () {
        let item_id = $("#item_id").val();
        let item_product_name = $("#item_product_name").val();
        let item_shopcart_id = $("#item_shopcart_id").val();
        let item_product_id = $("#item_product_id").val();
        let item_product_price = $("#item_product_price").val();
        let item_quantity = $("#item_quantity").val();

        let data = {
            "cart_id": item_shopcart_id,
            "product_name": item_product_name,
            "product_id": item_product_id,
            "product_price": item_product_price,
            "quantity": item_quantity
        }

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "PUT",
            url: `/shopcarts/${item_shopcart_id}/items/${item_id}`,
            contentType: "application/json",
            data: JSON.stringify(data)
        })

        ajax.done(function (res) {
            update_items_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function (res) {
            flash_message(res.responseJSON.message)
        });

    });


    // ****************************************
    // Retrieve a Shopcart
    // ****************************************

    $("#retrieve-shopcart-btn").click(function () {

        let shopcart_id = $("#shopcart_id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: `/shopcarts/${shopcart_id}`,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function (res) {
            //alert(res.toSource())
            update_shopcarts_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function (res) {
            clear_shopcarts_form_data()
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Retrieve an Item
    // ****************************************

    $("#retrieve-item-btn").click(function () {

        let shopcart_id = $("#item_shopcart_id").val();
        let item_id = $("#item_id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: `/shopcarts/${shopcart_id}/items/${item_id}`,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function (res) {
            //alert(res.toSource())
            update_items_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function (res) {
            clear_items_form_data()
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Delete a Shopcart
    // ****************************************

    $("#delete-shopcart-btn").click(function () {

        let shopcart_id = $("#shopcart_id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "DELETE",
            url: `/shopcarts/${shopcart_id}`,
            contentType: "application/json",
            data: '',
        })

        ajax.done(function (res) {
            clear_shopcarts_form_data()
            // note: delete is idempotent, so it will always return success even if there is nothing to delete
            flash_message("Success")
        });

        ajax.fail(function (res) {
            flash_message("Server error!")
        });
    });


    // ****************************************
    // Delete an Item
    // ****************************************

    $("#delete-item-btn").click(function () {

        let shopcart_id = $("#item_shopcart_id").val();
        let item_id = $("#item_id").val();


        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "DELETE",
            url: `/shopcarts/${shopcart_id}/items/${item_id}`,
            contentType: "application/json",
            data: '',
        })

        ajax.done(function (res) {
            clear_shopcarts_form_data()
            // note: delete is idempotent, so it will always return success even if there is nothing to delete
            flash_message("Success")
        });

        ajax.fail(function (res) {
            flash_message("Server error!")
        });
    });

    // ****************************************
    // Clearing our forms
    // ****************************************

    $("#clear-shopcart-btn").click(function () {
        $("#shopcart_id").val("");
        $("#flash_message").empty();
        clear_shopcarts_form_data()
    });

    $("#clear-item-btn").click(function () {
        $("#item_id").val("");
        $("#flash_message").empty();
        clear_items_form_data()
    });

    // ****************************************
    // Search for a Shopcart
    // ****************************************

    $("#search-shopcart-btn").click(function () {

        let user_id = $("#shopcart_user_id").val();
        let queryString = ""

        if (user_id) {
            queryString += 'user_id=' + user_id
        }

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: `/shopcarts?${queryString}`,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function (res) {
            //alert(res.toSource())
            $("#search_results").empty();
            let table = '<table class="table table-striped" cellpadding="10">'
            table += '<thead><tr>'
            table += '<th class="col-md-1">Shopcart ID</th>'
            table += '<th class="col-md-4">User ID</th>'
            table += '<th class="col-md-3">Creation Date</th>'
            table += '<th class="col-md-3">Last Update</th>'
            table += '<th class="col-md-3">Total price</th>'
            table += '</tr></thead><tbody>'
            let firstShopcart = "";
            for (let i = 0; i < res.length; i++) {
                let shopcart = res[i];
                table += `<tr id="row_${i}"><td>${shopcart.id}</td><td id="user-id-${shopcart.user_id}">${shopcart.user_id}</td><td>${shopcart.creation_date}</td><td>${shopcart.last_updated}</td><td>${shopcart.total_price}</td></tr>`;
                if (i == 0) {
                    firstShopcart = shopcart;
                }
            }
            table += '</tbody></table>';
            $("#search_results").append(table);

            // copy the first result to the form
            if (firstShopcart != "") {
                update_shopcarts_form_data(firstShopcart)
            }
            else {
                clear_shopcarts_form_data()
            }

            flash_message("Success")
        });

        ajax.fail(function (res) {
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Search for an Item
    // ****************************************

    $("#search-item-btn").click(function () {

        let shopcart_id = $("#item_shopcart_id").val();
        let product_id = $("#item_product_id").val();
        let quantity = $("#item_quantity").val();
        let queryString = ""

        if (product_id) {
            queryString += 'product_id=' + product_id;
        }

        if (quantity) {
            if (queryString != "") {
                queryString += '&quantity=' + quantity;
            }
            else {
                queryString += 'quantity=' + quantity;
            }
        }

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: `/shopcarts/${shopcart_id}/items?${queryString}`,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function (res) {
            //alert(res.toSource())
            $("#item_search_results").empty();
            let table = '<table class="table table-striped" cellpadding="10">'
            table += '<thead><tr>'
            table += '<th class="col-md-3">Shopcart ID</th>'
            table += '<th class="col-md-1">Item ID</th>'
            table += '<th class="col-md-3">Product name</th>'
            table += '<th class="col-md-3">Product ID</th>'
            table += '<th class="col-md-2">Product Price</th>'
            table += '<th class="col-md-2">Quantity</th>'
            table += '<th class="col-md-3">Subtotal</th>'
            table += '</tr></thead><tbody>'
            let firstItem = "";
            for (let i = 0; i < res.length; i++) {
                let item = res[i];
                table += `<tr id="row_${i}"><td>${item.cart_id}</td><td>${item.id}</td><td>${item.product_name}</td><td id="product-id-${item.product_id}">${item.product_id}</td><td>${item.product_price}</td><td>${item.quantity}</td><td>${item.subtotal}</td></tr>`;
                if (i == 0) {
                    firstItem = item;
                }
            }
            table += '</tbody></table>';
            $("#item_search_results").append(table);

            // copy the first result to the form
            if (firstItem != "") {
                update_items_form_data(firstItem)
            }
            else {
                clear_items_form_data()
            }

            flash_message("Success")
        });

        ajax.fail(function (res) {
            flash_message(res.responseJSON.message)
        });

    });

})
