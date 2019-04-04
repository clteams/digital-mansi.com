function disripp(el) {
    try {
      $(el).find('div').remove();
    } catch (e) {};
}
audio = new Audio('sable.mp3');
$('.navbar-brand').click(function () {
    audio.play();
    setTimeout(function(){audio.pause();}, 5000);
});