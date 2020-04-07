Array.from(document.getElementsByClassName("pos")).forEach(
    function(element, index, array) {
        for (var i = 0; i <= array.length; i++) {
        array[i].innerHTML = i+1
    }
    }
);