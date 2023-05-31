// Add event listener for the delete buttons
const deleteButtons = document.querySelectorAll('.delete-product');
deleteButtons.forEach(button => {
    button.addEventListener('click', function(event) {
        event.preventDefault();

        const deleteUrl = this.getAttribute('href');
        const tableRow = this.closest('tr');

        fetch(deleteUrl, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Error deleting the product.');
            }
            return response.json();
        })
        .then(data => {
            // Check for any error messages from the server
            if (data.error) {
                alert(data.error);
                return;
            }

            // Get the table body element
            const tableBody = document.getElementById("product-table-body");

            // Animate the table row removal
            tableRow.style.opacity = '0';
            setTimeout(() => {
                tableRow.remove();
                // Recalibrate the table row numbers
                const tableRows = tableBody.getElementsByTagName("tr");
                for (let i = 0; i < tableRows.length; i++) {
                    tableRows[i].getElementsByTagName("td")[0].innerText = i + 1;
                }
            }, 500);
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while deleting the product.');
        });
    });
});
