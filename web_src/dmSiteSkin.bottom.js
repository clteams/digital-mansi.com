$(document).ready(function() { $('body').bootstrapMaterialDesign(); });
window.onload = function () {
    $('.ornament').height($('.jumbotron').height() + $('.sobol').height() + 80);
    audio = new Audio('sable.mp3');
    $('.navbar-brand').click(function () {
        audio.play();
        setTimeout(function(){audio.pause();}, 1700);
    });
};