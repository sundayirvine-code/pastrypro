// Function to update the product table based on the selected category
function updateProductTable(categoryId) {
const data = { 
    id: categoryId, 
};

// Fetch the product data for the selected category asynchronously
fetch('/category_products', {
    method: 'POST',
    headers: {
    'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
})
    .then(response => response.json())
    .then(data => {
    const productTableBody = document.getElementById('product-table-body');
    productTableBody.innerHTML = ''; // Clear existing table rows

    // Iterate over the fetched product data and generate table rows dynamically
    data.forEach(product => {
        const row = document.createElement('tr');
        row.setAttribute('scope', 'row');

        const indexCell = document.createElement('td');
        indexCell.textContent = product.index;
        row.appendChild(indexCell);

        const nameCell = document.createElement('td');
        const nameLink = document.createElement('a');
        nameLink.setAttribute('href', `/product_details?id=${product.id}`);
        nameLink.textContent = product.name;
        nameCell.appendChild(nameLink);
        row.appendChild(nameCell);

        const categoryCell = document.createElement('td');
        categoryCell.textContent = product.category;
        row.appendChild(categoryCell);

        const quantityCell = document.createElement('td');
        quantityCell.textContent = product.quantity;
        row.appendChild(quantityCell);

        const unitCell = document.createElement('td');
        unitCell.textContent = product.unit;
        row.appendChild(unitCell);

        const statusCell = document.createElement('td');
        statusCell.textContent = product.status;
        row.appendChild(statusCell);

        //<td><a href="{{ url_for('delete_product', id=${newProduct.id}) }}" class="btn btn-danger btn-sm delete-product">Delete</a></td> 
        const actionCell = document.createElement('td');
        const actionLink = document.createElement('a');
        actionLink.setAttribute('href', `url_for('delete_product', id=${product.id}) }}`);
        actionLink.setAttribute('class', `btn btn-danger btn-sm delete-product`);
        actionLink.textContent = 'Delete';
        actionCell.appendChild(actionLink);
        row.appendChild(actionCell);

        productTableBody.appendChild(row);
    });
    })
    .catch(error => console.log(error));
}

// Event listeners for category selection
const categoryItems = document.querySelectorAll('.categories');
categoryItems.forEach(category => {
category.addEventListener('click', function () {
    // Get the selected category ID from the data attribute
    const categoryId = parseInt(category.getAttribute('id'));
    console.log(categoryId)
    updateProductTable(categoryId);
});
});