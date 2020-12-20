window.onload = function() {
    if ($(window).width() < 600) {
        $('#hidder').trigger('click');
    }
};

$("#hidder").click(function(e) {
    e.preventDefault();
    $("#sidebar").toggleClass("side-hidden");
    $("#content").toggleClass("side-hidden");
});

