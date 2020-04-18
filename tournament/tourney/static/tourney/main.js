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
    $('.games').each(function(){
    $('#game'+String(this.id).substring(4)).click(function(){
    window.open("/game/"+String(this.id).substring(4), "myWindow", 'width=400,height=300', 'resize=no');
    window.close();
});
})
});

$('.save').click(function(){
    window.close();
    window.opener.location.reload(true);
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



$(window).resize(function(){
    if ($(window).width() <= 320) {
       window.resizeTo(300 ,$(window).height());
    }
});