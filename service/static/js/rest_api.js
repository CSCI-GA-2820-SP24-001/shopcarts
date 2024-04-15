$(function () {

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the SHOPCARTS form with data from the response
    function update_shopcarts_form_data(res) {
        $("#shopcart_id").val(res.shopcart_id);
        $("#shopcart_user_id").val(res.shopcart_user_id);
        $("#shopcart_creation_date").val(res.shopcart_creation_date);
        $("#shopcart_last_update_date").val(res.shopcart_last_update_date);
        $("#shopcart_items").val(res.shopcart_items);
        $("#shopcart_total_price").val(res.shopcart_total_price);
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
        $("#item_id").val(res.item_id);
        $("#item_product_name").val(res.item_product_name);
        $("#item_shopcart_id").val(res.item_shopcart_id);
        $("#item_product_id").val(res.item_product_id);
        $("#item_product_price").val(res.item_product_price);
        $("#item_quantity").val(res.item_quantity);
        $("#item_subtotal_price").val(res.item_subtotal_price);
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
        // let shopcart_id = $("#shopcart_id").val();
        // let shopcart_creation_date = $("#shopcart_creation_date").val();
        // let shopcart_last_update_date = $("#shopcart_last_update_date").val();
        // let shopcart_items = $("#shopcart_items").val();
        // let shopcart_total_price = $("#shopcart_total_price").val();

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
            update_form_data(res)
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
        let item_subtotal_price = $("#item_subtotal_price").val();

        let data = {
            "product_name": item_product_name,
            "cart_id": item_shopcart_id,
            "product_id": item_product_id,
            "product_price": item_product_price,
            "quantity": item_quantity,
            "subtotal": item_subtotal_price
        }

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "POST",
            url: `/shopcarts/${item_shopcart_id}/items`,
            contentType: "application/json",
            data: JSON.stringify(data),
        });


        ajax.done(function (res) {
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function (res) {
            flash_message(res.responseJSON.message)
        });
    });

    // ****************************************
    // Update a Shopcart
    // ****************************************

    $("#update-btn").click(function () {

        let shopcart_id = $("#shopcart_id").val();
        let name = $("#shopcart_name").val();
        let category = $("#shopcart_category").val();
        let available = $("#shopcart_available").val() == "true";
        let gender = $("#shopcart_gender").val();
        let birthday = $("#shopcart_birthday").val();

        let data = {
            "name": name,
            "category": category,
            "available": available,
            "gender": gender,
            "birthday": birthday
        };

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "PUT",
            url: `/shopcarts/${shopcart_id}`,
            contentType: "application/json",
            data: JSON.stringify(data)
        })

        ajax.done(function (res) {
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function (res) {
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Retrieve a Shopcart
    // ****************************************

    $("#retrieve-btn").click(function () {

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
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function (res) {
            clear_form_data()
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Delete a Shopcart
    // ****************************************

    $("#delete-btn").click(function () {

        let shopcart_id = $("#shopcart_id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "DELETE",
            url: `/shopcarts/${shopcart_id}`,
            contentType: "application/json",
            data: '',
        })

        ajax.done(function (res) {
            clear_form_data()
            flash_message("Shopcart has been Deleted!")
        });

        ajax.fail(function (res) {
            flash_message("Server error!")
        });
    });

    // ****************************************
    // Clear the form
    // ****************************************

    $("#clear-btn").click(function () {
        $("#shopcart_id").val("");
        $("#flash_message").empty();
        clear_form_data()
    });

    // ****************************************
    // Search for a Shopcart
    // ****************************************

    $("#search-btn").click(function () {

        let name = $("#shopcart_name").val();
        let category = $("#shopcart_category").val();
        let available = $("#shopcart_available").val() == "true";

        let queryString = ""

        if (name) {
            queryString += 'name=' + name
        }
        if (category) {
            if (queryString.length > 0) {
                queryString += '&category=' + category
            } else {
                queryString += 'category=' + category
            }
        }
        if (available) {
            if (queryString.length > 0) {
                queryString += '&available=' + available
            } else {
                queryString += 'available=' + available
            }
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
            table += '<th class="col-md-2">ID</th>'
            table += '<th class="col-md-2">Name</th>'
            table += '<th class="col-md-2">Category</th>'
            table += '<th class="col-md-2">Available</th>'
            table += '<th class="col-md-2">Gender</th>'
            table += '<th class="col-md-2">Birthday</th>'
            table += '</tr></thead><tbody>'
            let firstShopcart = "";
            for (let i = 0; i < res.length; i++) {
                let shopcart = res[i];
                table += `<tr id="row_${i}"><td>${shopcart.id}</td><td>${shopcart.name}</td><td>${shopcart.category}</td><td>${shopcart.available}</td><td>${shopcart.gender}</td><td>${shopcart.birthday}</td></tr>`;
                if (i == 0) {
                    firstShopcart = shopcart;
                }
            }
            table += '</tbody></table>';
            $("#search_results").append(table);

            // copy the first result to the form
            if (firstShopcart != "") {
                update_form_data(firstShopcart)
            }

            flash_message("Success")
        });

        ajax.fail(function (res) {
            flash_message(res.responseJSON.message)
        });

    });

})
