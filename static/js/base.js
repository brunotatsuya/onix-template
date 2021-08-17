function responsiveShowSidebar(){
    if (($(window).width() < 600) || (/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent))){
        $("#sidebar").addClass("side-hidden");
        $("#topbar").addClass("side-hidden");
        $("#principalContainer").addClass("side-hidden");
        $("body").addClass("side-hidden");
    }
    else {
        $("#sidebar").removeClass("side-hidden");
        $("#topbar").removeClass("side-hidden");
        $("#principalContainer").removeClass("side-hidden");
        $("body").removeClass("side-hidden");
    }
}

window.onload = function() {
    responsiveShowSidebar();
    
    window.addEventListener('resize', function(event) {
        if (!(/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent))){
            responsiveShowSidebar();
        }
    }, true);

    $(".hidder").click(function(e) {
        e.preventDefault();
        $("#sidebar").toggleClass("side-hidden");
        $("#topbar").toggleClass("side-hidden");
        $("#principalContainer").toggleClass("side-hidden");
        $("body").toggleClass("side-hidden");
    });

    $('#logout').on('click', function () {
        $.ajax({
            type: "GET",
            url: '/api/logout',
            success: response => {
                setTimeout(function(){
                    location.reload();
               }, 1); 
            }
        });
    });
};