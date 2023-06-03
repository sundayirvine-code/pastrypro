$(function() {
  $("#ingredients").autocomplete({
    source: "/ingredients/search",
    minLength: 1,
    select: function(event, ui) {
      addIngredient(ui.item);
      $(this).val('');
      return false;
    }
  });

  var totalPrice = 0;
  var costPrice = 0;
  var sellingPrice = 0;

  function addIngredient(ingredient) {
    var quantity = parseFloat(prompt("Enter quantity for ingredient " + ingredient.label));
    if (!quantity) {
      alert("Please fill in all the required fields.");
      return;
    }

    var ingredientCostPrice = ingredient.price * quantity;
    costPrice += ingredientCostPrice;
    sellingPrice = calculateSellingPrice(costPrice);

    var li = '<li data-id="' + ingredient.id + '" data-quantity="' + quantity + '">' + ingredient.label + ' @ ' + ingredient.price + ' x ' + quantity + ' = ' + ingredientCostPrice + '</li>';
    $("#ingredientList").append(li);

    calculateTotalPrice(quantity, ingredient.price);
    $("#sellingPrice").val(sellingPrice.toFixed(2));
  }

  function calculateTotalPrice(quantity, price) {
    totalPrice += price * quantity;
    $("#totalPrice").val(totalPrice.toFixed(2));
  }

  function calculateSellingPrice(costPrice) {
    var laborCost = $("#laborCost").val();
    var electricityCost = $("#electricityCost").val();
    var transportationCost = $("#transportationCost").val();
    if (!laborCost || !electricityCost || !transportationCost) {
      alert("Please fill in all the required fields.");
      return;
    }
    var taxPercentage = 0.16;
    var totalCost = costPrice + parseFloat(laborCost) + parseFloat(electricityCost) + parseFloat(transportationCost);
    var sellingPrice = totalCost / (1 - taxPercentage);
    
    return sellingPrice.toFixed(2);
  }

  $("#finishBaking").click(function() {
    var name_id = $("#name").val();
    var quantity = $("#quantity").val();
    var unit = $("#inputUnit").val();  
    var ingredients = [];

    $("#ingredientList li").each(function() {
      var id = $(this).data("id");
      var quantity = $(this).data("quantity");

      ingredients.push({
        id: id,
        quantity: quantity
      });
    });

    if (!name_id || !quantity || !unit || !ingredients) {
      alert("Please fill in all the required fields.");
      return;
    }

    // ...

    var data = {
      name_id: name_id,
      quantity: quantity,
      ingredients: ingredients,
      totalPrice: costPrice.toFixed(2),
      selling_price: sellingPrice.toFixed(2),
      unit: unit
    };

    console.log(data)
    $.ajax({
      url: '/bake',
      type: 'POST',
      data: JSON.stringify(data),
      contentType: 'application/json',
      success: function(response) {
        console.log(response)
        alert(response.message);  
      },
      error: function(xhr, status, error) {
        var errorMessage = xhr.responseJSON.error;
        alert(errorMessage);
      }
    });
  });
});
