var matchList = []
var gameList = []
var playerList = []
var playerResultList = []
var tournament_id = $('#tourney_id').text()
var thisTournamentGamesClass = '.from_tourney'+tournament_id.trim()
var playersWithEqualPoints = []
var headToHeadWins = []
var nameAndPoints = {}

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
    var sorted_list = []
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
        var these_games = $(all_players).filter('.from_tourney'+tourney_id.trim())
        $(these_games).each(function(a, b ){
           sorted_list.push(this)
        });
          $("#game-table tbody").html(sorted_list);
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
        function(element, detail, array) {
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


var playerUrl = 'http://127.0.0.1:8000/playerapi/'
var matchUrl = 'http://127.0.0.1:8000/matchapi/'

function ajax(api){
    $.ajax({
        method: 'GET',
        url: api,
        success: function(data){
        },
        error: function(error_data){
        }
    })
}

function request_(api, renderHtmlFunction){
    var ourRequest = new XMLHttpRequest();
    ourRequest.open('GET', api);
    ourRequest.onload = function(){
        var ourData = JSON.parse(ourRequest.responseText)
        renderHtmlFunction(ourData)
    }
    ourRequest.send();
}



function renderHTML(data){
    playerList.length = 0
    for (i=0; i < data.length; i++){
        if (data[i].tournament == tournament_id){
       playerList.push({'id':data[i].id, 'name':data[i].name, 'games_played':0,
                'wins':0, 'draws':0, 'defeats':0,
                'goals_scored':0, 'goals_conceded':0,
                'goal_difference':0, 'points':0})
       nameAndPoints[data[i].name] = data[i].points
}
}
}

ajax(playerUrl)
ajax(matchUrl)
request_(matchUrl, renderHTML2)

function renderHTML2(data){
    for (i=0; i < data.length; i++){
        matchList.push({'id':data[i].id, 'player1': data[i].player1, 'player2':data[i].player2, 'score1':data[i].score1, 'score2':data[i].score2})
}
}





function gamesToList(){
    gameList.length = 0
    $(thisTournamentGamesClass).each(function(){
        var game_match = $(this).find('.game_match').text()
        var game_id = $(this).find('.game_id').text()
        var game_home_player = $(this).find('.home_player').text()
        var game_away_player = $(this).find('.away_player').text()
        var game_home_score = $(this).find('.h_score').text()
        var game_away_score = $(this).find('.a_score').text()
        gameList.push({'match':game_match, 'game_id':game_id, 'home_player':game_home_player, 'away_player':game_away_player, 'h_score':game_home_score, 'a_score':game_away_score})
    });
};

request_(playerUrl, renderHTML);


$('body').on('DOMSubtreeModified', '#games', function(){
    countingStats()
});


function countingStats(){
  for (var i = 0; i < playerList.length; i++) {
    playerList[i].games_played = 0
    playerList[i].wins = 0
    playerList[i].draws = 0
    playerList[i].defeats = 0
    playerList[i].goals_scored = 0
    playerList[i].goals_conceded = 0
    playerList[i].goal_difference = 0
    playerList[i].points = 0
    nameAndPoints[playerList[i].name] = 0
  }


  gamesToList()
  for (var m=0; m < matchList.length; m++) {
        matchList[m].score1 = 0
        matchList[m].score2 = 0
    for (var g=0; g < gameList.length; g++) {
        if (matchList[m].id == gameList[g].match){
            if (gameList[g].h_score != "" && gameList[g].a_score != "") {
            if (gameList[g].home_player == matchList[m].player1 && gameList[g].away_player == matchList[m].player2) {
                matchList[m].score1 += parseInt(gameList[g].h_score)
                matchList[m].score2 += parseInt(gameList[g].a_score)
            } else if (gameList[g].home_player == matchList[m].player2 && gameList[g].away_player == matchList[m].player1){
                matchList[m].score1 += parseInt(gameList[g].a_score)
                matchList[m].score2 += parseInt(gameList[g].h_score)
            }
            }
            for (var p=0; p < playerList.length; p++) {


            if (gameList[g].h_score != "" && gameList[g].a_score != "") {
            if (gameList[g].home_player == playerList[p].name) {
                if (gameList[g].h_score > gameList[g].a_score) {
                    playerList[p].games_played +=1
                    playerList[p].points +=3
                    playerList[p].wins +=1
                    playerList[p].goals_scored += parseInt(gameList[g].h_score)
                    playerList[p].goals_conceded += parseInt(gameList[g].a_score)
                    playerList[p].goal_difference += parseInt(gameList[g].h_score)
                    playerList[p].goal_difference -= parseInt(gameList[g].a_score)
                    nameAndPoints[playerList[p].name] += 3

                } else if (gameList[g].h_score == gameList[g].a_score){
                    playerList[p].games_played +=1
                    playerList[p].points +=1
                    playerList[p].draws +=1
                    playerList[p].goals_scored += parseInt(gameList[g].h_score)
                    playerList[p].goals_conceded += parseInt(gameList[g].a_score)
                    playerList[p].goal_difference += parseInt(gameList[g].h_score)
                    playerList[p].goal_difference -= parseInt(gameList[g].a_score)
                    nameAndPoints[playerList[p].name] += 1
                } else if (gameList[g].h_score < gameList[g].a_score){
                    playerList[p].games_played +=1
                    playerList[p].defeats +=1
                    playerList[p].goals_scored += parseInt(gameList[g].h_score)
                    playerList[p].goals_conceded += parseInt(gameList[g].a_score)
                    playerList[p].goal_difference += parseInt(gameList[g].h_score)
                    playerList[p].goal_difference -= parseInt(gameList[g].a_score)
                }




            } else if (gameList[g].away_player == playerList[p].name) {
                if (gameList[g].h_score < gameList[g].a_score) {
                    playerList[p].games_played +=1
                    playerList[p].points +=3
                    playerList[p].wins +=1
                    playerList[p].goals_scored += parseInt(gameList[g].a_score)
                    playerList[p].goals_conceded += parseInt(gameList[g].h_score)
                    playerList[p].goal_difference += parseInt(gameList[g].a_score)
                    playerList[p].goal_difference -= parseInt(gameList[g].h_score)
                    nameAndPoints[playerList[p].name] += 3
                 } else if (gameList[g].h_score == gameList[g].a_score){
                    playerList[p].games_played +=1
                    playerList[p].points +=1
                    playerList[p].draws +=1
                    playerList[p].goals_scored += parseInt(gameList[g].a_score)
                    playerList[p].goals_conceded += parseInt(gameList[g].h_score)
                    playerList[p].goal_difference += parseInt(gameList[g].a_score)
                    playerList[p].goal_difference -= parseInt(gameList[g].h_score)
                    nameAndPoints[playerList[p].name] += 1
                }   else if (gameList[g].h_score > gameList[g].a_score){
                    playerList[p].games_played +=1
                    playerList[p].defeats +=1
                    playerList[p].goals_scored += parseInt(gameList[g].a_score)
                    playerList[p].goals_conceded += parseInt(gameList[g].h_score)
                    playerList[p].goal_difference += parseInt(gameList[g].a_score)
                    playerList[p].goal_difference -= parseInt(gameList[g].h_score)
                }

            }

        }
        }
     }
  playersWithEqualPoints = []
  for (var z = 0; z < playerList.length; z++) {
    for (var y = 0; y < playerList.length; y++) {
        if (playerList[z].name != playerList[y].name && playerList[z].points == playerList[y].points) {
            if (playersWithEqualPoints.includes(playerList[z].name) == false){
            playersWithEqualPoints.push(playerList[z].name)
            }
        }
    }
  }
}

}

    headToHeadWins = []
    for (var n = 0; n < matchList.length; n++) {
         if (playersWithEqualPoints.includes(matchList[n].player1) == true &&
         playersWithEqualPoints.includes(matchList[n].player2) == true) {
            if (nameAndPoints[matchList[n].player1] == nameAndPoints[matchList[n].player2]) {
            if (matchList[n].score1 > matchList[n].score2) {
                headToHeadWins.push(matchList[n].player1)
            } else if (matchList[n].score1 < matchList[n].score2) {
                headToHeadWins.push(matchList[n].player2)
            }
          }
     }
  }


  playerList.sort(function(first, second) {
        if ($('#poistion_priority').text() == 'Head to Head Matches') {
        return second.points - first.points || countInArray(headToHeadWins, second.name) - countInArray(headToHeadWins, first.name) || second.goal_difference - first.goal_difference || second.goals_scored - first.goals_scored  ||  second.wins - first.wins;
        } else if ($('#poistion_priority').text() == 'Goal Difference') {
        return second.points - first.points || second.goal_difference - first.goal_difference || countInArray(headToHeadWins, second.name) - countInArray(headToHeadWins, first.name) || second.goals_scored - first.goals_scored  ||  second.wins - first.wins;
        }
    });


  $('.player_stats').remove()
  for (var x = 0; x < playerList.length; x++) {
    $('#player_list').append(
    '<tbody class="player_stats">' +
        '<tr class="top">' +
            '<td class="pos">' + (parseInt(x)+1) + '</td>' +
            '<td class="name">' + playerList[x].name + '</td>' +
            '<td>' + playerList[x].games_played + '</td>' +
            '<td>' + playerList[x].wins + '</td>'+
            '<td>' + playerList[x].draws + '</td>' +
            '<td>' + playerList[x].defeats + '</td>'+
            '<td class="goals_scored" id="gs-39">' + playerList[x].goals_scored + '</td>' +
            '<td class="goals_conceded" id="gc-39">' + playerList[x].goals_conceded + '</td>' +
            '<td class="goal_difference" id="gd-39">' + playerList[x].goal_difference + '</td>' +
            '<td class="points" id="points-39">' + playerList[x].points + '</td>' +
        '</tr>' +
    '</tbody>'
    )
  }
  playerResultList.length = 0
  $('.name').each(function(){
    var playerName = $(this).text()
    playerResultList.push(playerName.trim())
});
  $('#results').empty()
  createTables(playerResultList.length-1,playerResultList.length-1);
}


function countInArray(array, what) {
    var count = 0;
    for (var i = 0; i < array.length; i++) {
        if (array[i] === what) {
            count++;
        }
    }
    return count;
}


$('.name').each(function(){
    var playerName = $(this).text()
    playerResultList.push(playerName.trim())
});


function createTables(maxNum,limit){
	const table = document.createElement('table');
	table.setAttribute('class', 'result_table');
	for(let i = 0;i<maxNum + 1;i++){
		const row = document.createElement('tr');
		row.setAttribute('class', 'result_tr');
		for(let j = 0;j<limit + 1;j++){
			const td = document.createElement('td');
			td.setAttribute('class', 'result_td');
			//Below four lines are new
			if(i === 0 && j === 0) {td.innerHTML = '';
            td.setAttribute('class', 'left_name');
			}
			else if (i === j) {
			    $(td).css("background-color", "black")
			}
			else if(i === 0){ td.innerHTML = j;
			td.setAttribute('class', 'top_name');
			}
			else if(j === 0) {td.innerHTML = i + '. ' + playerResultList[i]
            td.setAttribute('class', 'left_name');
			}
			else td.innerHTML = calculationResults(playerResultList[i], playerResultList[j])
			row.appendChild(td);
		}
		table.appendChild(row)
	}
	$('#results').append(table)
}
createTables(playerResultList.length-1,playerResultList.length-1);


function calculationResults(team1, team2){
    var game1 = '<div class="not_played">0:0</div>'
    var game2 = '<div class="not_played">0:0</div>'
    $('.from_tourney2').each(function(){
        if ( team1 == $(this).find('.home_player').text() && team2 == $(this).find('.away_player').text()){
            if (parseInt($(this).find('.h_score').text()) > parseInt($(this).find('.a_score').text())) {
                game1 = '<div class="table_score" style="color:green;">' + $(this).find('.h_score').text() + ':' + $(this).find('.a_score').text() + '</div>'
            } else if (parseInt($(this).find('.h_score').text()) == parseInt($(this).find('.a_score').text())) {
                game1 = '<div class="table_score" style="color:black;">' + $(this).find('.h_score').text() + ':' + $(this).find('.a_score').text() + '</div>'
            } else if (parseInt($(this).find('.h_score').text()) < parseInt($(this).find('.a_score').text())) {
                game1 = '<div class="table_score" style="color:red;">' + $(this).find('.h_score').text() + ':' + $(this).find('.a_score').text() + '</div>'
            }

        } if ( team2 == $(this).find('.home_player').text() && team1 == $(this).find('.away_player').text()){
            if (parseInt($(this).find('.h_score').text()) < parseInt($(this).find('.a_score').text())) {
                game2 = '<div class="table_score" style="color:green;">' + $(this).find('.a_score').text() + ':' + $(this).find('.h_score').text() + '</div>'
            } else if (parseInt($(this).find('.h_score').text()) == parseInt($(this).find('.a_score').text())) {
                game2 = '<div class="table_score" style="color:black;">' + $(this).find('.a_score').text() + ':' + $(this).find('.h_score').text() + '</div>'
            } else if (parseInt($(this).find('.h_score').text()) > parseInt($(this).find('.a_score').text())) {
                game2 = '<div class="table_score" style="color:red;">' + $(this).find('.a_score').text() + ':' + $(this).find('.h_score').text() + '</div>'
            }


        }
    })
return game1 + '<br>' + game2

}


$(window).scroll(function() {
    if ($(document).scrollTop() > 50) {
        $('.nav').addClass('affix');
    } else {
        $('.nav').removeClass('affix');
    }
});

$('.navTrigger').click(function () {
    $(this).toggleClass('active');
    $("#mainListDiv").toggleClass("show_list");
    $("#mainListDiv").fadeIn();

});




var targetNode = document.getElementById('modal-game');
var observer = new MutationObserver(function(){
    if(targetNode.style.display != 'none'){
        $('#team1').text(( $("#id_home_player option:selected" ).text()));
        $('#team2').text(( $("#id_away_player option:selected" ).text()));
    }
});
observer.observe(targetNode, { attributes: true, childList: true });





