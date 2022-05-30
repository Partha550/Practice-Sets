// If user clicks anywhere outside of the modal, Modal will close

var modal1 = document.getElementById('concentrated-loads');
window.addEventListener("click", function(event) {
    if (event.target == modal1) {
        modal1.style.display = "none";
    }
});

var modal2 = document.getElementById('distributed-loads');
window.addEventListener("click", function(event) {
    if (event.target == modal2) {
        modal2.style.display = "none";
    }
});

var modal3 = document.getElementById('varying-loads');
window.addEventListener("click", function(event) {
    if (event.target == modal3) {
        modal3.style.display = "none";
    }
});

var modal4 = document.getElementById('concentrated-moments');
window.addEventListener("click", function(event) {
    if (event.target == modal4) {
        modal4.style.display = "none";
    }
});

var modal5 = document.getElementById('distributed-moments');
window.addEventListener("click", function(event) {
    if (event.target == modal5) {
        modal5.style.display = "none";
    }
});

var modal6 = document.getElementById('varying-moments');
window.addEventListener("click", function(event) {
    if (event.target == modal6) {
        modal6.style.display = "none";
    }
});