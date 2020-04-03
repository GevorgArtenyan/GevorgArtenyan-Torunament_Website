function playerList(){
    for (var i=1; i <=132; i++) {
    $("#id_player"+i).keyup(function(){
    var sum = ''
    for (var n=1; n<=132; n++) {
    var players = $('#id_player' + n).val()
    if ($('#id_player' + n).is(":visible")){
    p = players.replace(' ', '++')
    if (p == '') {
        sum += ''
    } else {
    sum += p + ' '
}
}
}
    $('#id_players').val(sum)
});
};
};



playerList()

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
    $('#id_player' + String(parseInt(a-1))).val('')
    $('#div_id_player' + String(parseInt(a-1))).hide('')
    a -= 1
}
});
});

$(function(){
    $('#remove_player').click(function(){
    var summary = ''
    for (var x=1; x<=132; x++) {
    var players = $('#id_player' + x).val()
    if ($('#id_player' + x).is(":visible")){
    y = players.replace(' ', '++')
    summary += y + ' '
}
}
    $('#id_players').val(summary)
});
});

