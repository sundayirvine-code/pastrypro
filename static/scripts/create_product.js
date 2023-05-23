//create_products.js

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

// Perform validation on the data (you can add your own validation logic here)
if (!name || !price || !quantity || !category || !description) {
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
    description: description
};

// Send an AJAX request to the server to create a new product
fetch("/create_product", {
    method: "POST",
    headers: {
    "Content-Type": "application/json"
    },
    body: JSON.stringify(formData)
})
.then(response => response.json())
.then(data => {
    // Handle the response from the server
    console.log(data); // You can customize the behavior based on the response
})
.catch(error => {
    console.error("Error:", error);
});

var offcanvas = document.getElementById('offcanvasWithBothOptionss');
var offcanvasInstance = bootstrap.Offcanvas.getInstance(offcanvas);
    
offcanvasInstance.hide();
});

