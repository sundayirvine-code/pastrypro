document.getElementById('catBtn').addEventListener('click', function() {
    var categoryInput = document.getElementById('catAdd');
    var category = categoryInput.value.trim();
    
    // Validate category input
    if (category === '' || category.length > 20) {
        var errorElement = document.querySelector('.error');
        if (category === '') {
        errorElement.textContent = 'Category cannot be empty.';
        } else if (category.length > 20) {
        errorElement.textContent = 'Category must be 20 characters or less.';
        }
        else{
            errorElement.textContent = '';
        }
        return;
    }

  
    // Make an AJAX request to the /category route
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/category', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onreadystatechange = function() {
      if (xhr.readyState === 4 && xhr.status === 200) {
        // Category creation successful
        var newCategory = JSON.parse(xhr.responseText);

        // Access the category attributes
        var categoryId = newCategory.id;
        var categoryName = newCategory.name;
        var categoryUserId = newCategory.user_id;

        // Add the new category to the list dynamically
        var categoryList = document.getElementById('categoryList');
        categoryList.innerHTML += '<li class="categories">' + categoryName + '</li>';

        // Add the new category as an option to the select element
        var inputCategory = document.getElementById('inputCategory');
        var newOption = document.createElement('option');
        newOption.value = categoryId;
        newOption.textContent = categoryName;
        inputCategory.appendChild(newOption);
  
        // Close the offcanvas
        var offcanvas = document.getElementById('offcanvasWithBothOptions');
        var offcanvasInstance = bootstrap.Offcanvas.getInstance(offcanvas);
        offcanvasInstance.hide();
  
        // Clear the category input field
        categoryInput.value = '';
      }
    };
    xhr.send(JSON.stringify({ category: category }));
  });
  
  // Close offcanvas when close button is clicked
  document.querySelector('#offcanvasWithBothOptions .btn-close').addEventListener('click', function() {
    var offcanvas = document.getElementById('offcanvasWithBothOptions');
    var offcanvasInstance = bootstrap.Offcanvas.getInstance(offcanvas);
    offcanvasInstance.hide();
  });
  