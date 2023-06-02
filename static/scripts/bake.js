//bake.js

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

    function addIngredient(ingredient) {
        var quantity = parseFloat(prompt("Enter quantity for ingredient " + ingredient.label));
        if (!quantity) {
          alert("Please fill in all the required fields.");
          return;
        }
        var li = '<li data-id="' + ingredient.id + '" data-quantity="' + quantity+ '">' + ingredient.label + ' @ ' + ingredient.price +  ' x ' + quantity + ' = '+ ingredient.price * quantity + '</li>';
        $("#ingredientList").append(li);
      calculateTotalPrice(quantity, ingredient.price);
    }

    function calculateTotalPrice(quantity, price) {
        totalPrice += price * quantity;
        $("#totalPrice").val(totalPrice.toFixed(2));
    }

    $("#finishBaking").click(function() {
      var name = $("#name").val();
      var quantity = $("#quantity").val();
      var totalPrice = $("#totalPrice").val();
      var laborCost = $("#laborCost").val();
      var electricityCost = $("#electricityCost").val();
      var rentCost = $("#rentCost").val();
      var waterCost = $("#waterCost").val();
      var transportationCost = $("#transportationCost").val();
      var unit = $("#inputUnit").val();
      var ingredients = [];
 
      $("#ingredientList li").each(function() {
        var id = $(this).data("id");
        var quantity =$(this).data("quantity");

        ingredients.push({
          id: id,
          quantity: quantity
        });
      });

      if (!name || !quantity || !totalPrice || !unit || !ingredients || !laborCost || !electricityCost || !transportationCost) {
        alert("Please fill in all the required fields.");
        return;
      }

      var data = {
        name: name,
        quantity: quantity,
        ingredients: ingredients,
        totalPrice: totalPrice,
        unit: unit,
        laborCost: laborCost,
        electricityCost: electricityCost,
        rentCost: rentCost,
        waterCost: waterCost,
        transportationCost: transportationCost
      };

      console.log(data)
      $.ajax({
        url: '/bake',
        type: 'POST',
        data: JSON.stringify(data),
        contentType: 'application/json',
        success: function(response) {
          console.log(response)
          $("#sellPrice").val(response.selling_price);
          alert(response.message);  
        },
        error: function(xhr, status, error) {
          var errorMessage = xhr.responseJSON.error;
          alert(errorMessage);
        }
      });
    });
  });