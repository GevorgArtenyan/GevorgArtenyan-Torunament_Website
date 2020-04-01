$(function(){
    for (var i=1; i <=132; i++) {
    $("#id_player"+i).keyup(function(){
    var sum = ' '
    for (var n=1; n<=132; n++) {
    var players = $('#id_player' + n).val()
    p = players.replace(' ', '++')
    sum += p + ' '
}
    $('#id_players').val(sum)
});
};
});

var a = 5

$(function(){
$('#add_player').click(function(){
    $("#div_id_player"+a).show()
    a += 1
});
});

$(function(){
$('#remove_player').click(function(){
    if (a > 132) {
    a = 133}
    if (a >= 6){
    $("#div_id_player"+ String(parseInt(a - 1))).hide()
    a -= 1
}
});
});