document.addEventListener('DOMContentLoaded', function(){
    Array.from(document.getElementsByClassName("pos")).forEach(
        function(element, index, array) {
            for (var i = 0; i <= array.length; i++) {
            array[i].innerHTML = i+1
        }
        }
    );
})

$(function(){
    $('.matches').each(function(){
    $('#match'+String(this.id).substring(5)).click(function(){
    window.open("/match/"+String(this.id).substring(5), "myWindow", 'width=400,height=300');
    window.close();
});
})
});

$('.save').click(function(){
    window.close();
})


