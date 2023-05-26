//update_products.js

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
var productIdElement = document.getElementsByClassName('product_id')[0];
var productUrlIdElement = document.getElementsByClassName('product.url_id')[0];

  // Extract the 'id' attribute value from the elements
  var productId = productIdElement.id;
  var productUrlId = productUrlIdElement.id;

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
    description: description,
    productId: productId,
    urlId: productUrlId
};

// Send an AJAX request to the server to create a new product
fetch("/product_details", {
    method: "PUT",
    headers: {
    "Content-Type": "application/json"
    },
    body: JSON.stringify(formData)
})
.then(response => response.json())
.then(data => {
    // Access the new product data from the response
    console.log(data)
    
    // get elements to update
    const productNameElement = document.getElementById("productName");
    const productCategoryNameElement = document.getElementById("productCategoryName");
    const productPriceElement = document.getElementById("productPrice");
    const productQuantityElement = document.getElementById("productQuantity");
    const productDescriptionElement = document.getElementById("productDescription");
    const productUrlElement = document.getElementById("productUrl");
    const productIdElement = document.getElementsByClassName("product_id");
    const productUrlIdElement = document.getElementsByClassName("product.url_id");

    // Update the elements with the new product data
    productNameElement.textContent = data.name;
    productCategoryNameElement.textContent = data.category_name;
    productPriceElement.textContent = data.price;
    productQuantityElement.textContent = data.quantity;
    productDescriptionElement.textContent = data.description;
    productUrlElement.src = data.image_url;
    // Force the image to reload by appending a timestamp as a query parameter
    productUrlElement.src = productUrlElement.src + '?time=' + new Date().getTime();
    productIdElement.id = data.product_id;
    productUrlIdElement.id = data.url_id;

    // Update the input values in the form
    document.getElementById("inputName").value = data.name;
    document.getElementById("inputPrice").value = data.price;
    document.getElementById("inputQuantity").value = data.quantity;
    document.getElementById("inputImage").value = data.image_url;
    document.getElementById("inputDescription").value = data.description;

    // Update the selected option in the category dropdown
    const categoryDropdown = document.getElementById("inputCategory");
    const selectedCategoryId = data.category_id;
    const selectedCategoryName = data.category_name;

    // Clear existing options
    //categoryDropdown.innerHTML = '';

    // Create and add the selected option
    const selectedOption = document.createElement("option");
    selectedOption.value = selectedCategoryId;
    selectedOption.textContent = selectedCategoryName;
    selectedOption.selected = true;
    categoryDropdown.appendChild(selectedOption);

    /*Add other category options
    const categories = data.categories;
    for (const category of categories) {
        if (category.id !== selectedCategoryId) {
            const option = document.createElement("option");
            option.value = category.id;
            option.textContent = category.name;
            categoryDropdown.appendChild(option);
        }
    }*/

})
.catch(error => {
    console.error("Error:", error);
});

var offcanvas = document.getElementById('offcanvasWithBothOptions');
var offcanvasInstance = bootstrap.Offcanvas.getInstance(offcanvas);
    
offcanvasInstance.hide();
});

