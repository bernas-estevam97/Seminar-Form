$("#savedDistancesForm").on("submit", function (e) {
  e.preventDefault();
  let dataString = $(this).serializeArray();
  

  // var csrfToken = $('[name="csrfmiddlewaretoken"]').val();
  // alert(dataString); return false;

  $.ajax({
    type: "POST",
    url: "saved",
    data: dataString,
    // headers: {
    //   "X-CSRFToken": csrfToken,
    // },
    success: function () {
      savedChoices = document.getElementById("savedChoices");
      savedChoices.options[savedChoices.options.length] = new Option(
        dataString[1].value + " - " + dataString[2].value,
        dataString[1].value
      );
      console.log(dataString);
      alert(
        saveDistance.value +
          " saved! If you want to use it you can select it on the option box above."
      );
      $("#saveDistance").val("");
      $("#imgSizeInfo").val("");
    },
    error: function () {
      alert("Value already in the database or of invalid input.");
    },
  });
  
});

// This functon is for dynamic deletion of options ---- NOT WORKING YET

// $('#removeOption').on('click', function(e){
//   var savedChoices = document.getElementById("savedChoices");
//   var dataStringtoDelete = savedChoices.options[savedChoices.selectedIndex].value;
//   var csrfToken = $('[name="csrfmiddlewaretoken"]').val();
//   $.ajax({
//     type: 'GET',
//     url: "deleted",
//     data: dataStringtoDelete,
//     processData: false,
//     headers: {
//         "X-CSRFToken": csrfToken,
//       },
//     success: function() {
//         alert('Entry deleted successfully!');
//         savedChoices.options[savedChoices.selectedIndex].remove();
//         console.log(dataStringtoDelete)
//     },
//     error: function(){
//       alert("Something went wrong!");
//     }
//   });

// })