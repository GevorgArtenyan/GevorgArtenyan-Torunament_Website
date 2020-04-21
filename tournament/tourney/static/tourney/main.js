$(function () {

  /* Functions */

  var loadForm = function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-game .modal-content").html("");
        $("#modal-game").modal("show");
      },
      success: function (data) {
        $("#modal-game .modal-content").html(data.html_form);
      }
    });
  };

  var saveForm = function () {
    var form = $(this);
    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      success: function (data) {
        if (data.form_is_valid) {
        var all_players = data.html_game_list
        var tourney_id = $('#tourney_id').text()
        var this_games = $(all_players).filter('.from_tourney'+tourney_id.trim())
        console.log(this_games)
          $("#game-table tbody").html(this_games);
          $("#modal-game").modal("hide");
        }
        else {
          $("#modal-game .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  };


  /* Binding */

  // Create game
  $(".js-create-game").click(loadForm);
  $("#modal-game").on("submit", ".js-game-create-form", saveForm);

  // Update game
  $("#game-table").on("click", ".js-update-game", loadForm);
  $("#modal-game").on("submit", ".js-game-update-form", saveForm);

  // Delete game
  $("#game-table").on("click", ".js-delete-game", loadForm);
  $("#modal-game").on("submit", ".js-game-delete-form", saveForm);

});

document.addEventListener('DOMContentLoaded', function(){
    Array.from(document.getElementsByClassName("pos")).forEach(
        function(element, index, array) {
            for (var i = 0; i <= array.length; i++) {
            array[i].innerHTML = i+1
        }
        }
    );
})


function openPage(pageName, elmnt, color) {
  var i, tabcontent, tablinks;
  tabcontent = document.getElementsByClassName("tabcontent");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }
  tablinks = document.getElementsByClassName("tablink");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].style.backgroundColor = "";
  }
  document.getElementById(pageName).style.display = "block";
  elmnt.style.backgroundColor = color;
}
document.getElementById("defaultOpen").click();
