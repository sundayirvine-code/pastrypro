// Get the "Create Product" button element
const createProductBtn = document.getElementById("createProductBtn");

// Add event listener for the button click
createProductBtn.addEventListener("click", function(event) {
    event.preventDefault(); // Prevent the default form submission behavior

    // Collect the form data
    const name = document.getElementById("inputName").value;
    const price = parseFloat(document.getElementById("inputPrice").value);
    const quantity = parseInt(document.getElementById("inputQuantity").value);
    const category = document.getElementById("inputCategory").value;
    const image = document.getElementById("inputImage").value;
    const description = document.getElementById("inputDescription").value;
    const unit = document.getElementById("inputUnit").value;

    // Perform validation on the data
    if (!name || !price || !quantity || !category || !description || !unit) {
        alert("Please fill in all the required fields.");
        return;
    }

    // Create an object with the form data
    const formData = {
        name: name,
        price: price,
        quantity: quantity,
        category: category,
        image: image,
        description: description,
        unit_id: unit
    };

    // Send an AJAX request to the server to create a new product
    fetch("/create_product", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(formData)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error("Error creating the product.");
        }
        return response.json();
    })
    .then(data => {
        // Check for any error messages from the server
        if (data.error) {
            alert(data.error);
            return;
        }

        // Access the new product data from the response
        const newProduct = data.product;

        // Get the table rows
        const tableRows = document.querySelectorAll(".table-group-divider tr");

        // Get the number of existing products
        const productCount = tableRows.length + 1;

        // Generate the HTML for the new table row
        const newRowHtml = `
            <tr scope="row">
                <td>${productCount}</td>
                <td><a href="/product_details?name=${newProduct.name}&id=${newProduct.id}">${newProduct.name}</a></td>
                <td>${newProduct.category}</td>
                <td>${newProduct.quantity}</td>
                <td>${newProduct.unit}</td>
                <td>${newProduct.status}</td>
                <td><a href="{{ url_for('delete_product', id=${newProduct.id}) }}" class="btn btn-danger btn-sm delete-product">Delete</a></td>  
            </tr>
        `;

        // Append the new row to the table
        const tableBody = document.querySelector(".table-group-divider");
        tableBody.innerHTML += newRowHtml;

        // Clear the form input fields
        document.getElementById("inputName").value = "";
        document.getElementById("inputPrice").value = "";
        document.getElementById("inputQuantity").value = "";
        document.getElementById("inputCategory").value = "";
        document.getElementById("inputImage").value = "";
        document.getElementById("inputDescription").value = "";
        document.getElementById("inputUnit").value = "";

    })
    .catch(error => {
        console.error("Error:", error);
        alert("An error occurred while creating the product.");
    });

    var offcanvas = document.getElementById('offcanvasWithBothOptionss');
    var offcanvasInstance = bootstrap.Offcanvas.getInstance(offcanvas);

    offcanvasInstance.hide();
});
