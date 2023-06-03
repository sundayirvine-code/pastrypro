$(document).ready(function() {
    $('#create-product-form').submit(function(e) {
        e.preventDefault(); // Prevent form submission

        // Get the form data
        var formData = {
            name: $('#product_name').val(),
        };

        // Send a POST request to the create_baked_product route
        $.ajax({
            type: 'POST',
            url: '/create_baked_product',
            data: formData,
            success: function(response) {
                console.log(response)
                // Display success message and update the product list
                alert(response.message);
                appendProduct(response.product);
            },
            error: function(error) {
                // Display error message
                alert('Failed to create baked product. Please try again.');
            }
        });

        // Clear the form inputs
        $('#product_name').val('');
    });

    // Function to append a new product to the product list
    function appendProduct(product) {
        console.log(product)
        // Create a new option element
        var option = $('<option>');
        option.attr('value', product.id);
        option.text(product.name);

        // Append the new option to the select dropdown
        $('#name').append(option);
    }
});
