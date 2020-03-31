$(function(){
    for (var i=1; i <=4; i++) {
    $("#id_player"+i).keyup(function(){
    var sum = ' '
    for (var n=1; n<=4; n++) {
    var players = $('#id_player' + n).val()
    p = players.replace(' ', '++')
    sum += p + ' '
}
    $('#id_players').val(sum)
});
};
});


