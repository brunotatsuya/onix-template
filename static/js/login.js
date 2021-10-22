window.onload = function () {
    $("#inputUsername").on("keyup", function (event) {
        if (event.keyCode === 13) {
            $('#buttonLogin').click();
        }
    });

    $("#inputConfirmPassword").on("keyup", function (event) {
        if (event.keyCode === 13) {
            $('#buttonLogin').click();
        }
    });

    $('#buttonLogin').on('click', function () {

        $('#buttonLogin').toggle();
        $('#buttonLoginLoading').toggle();
        $.ajax({
            type: "POST",
            url: '/api/auth',
            data: {
                login: $("#inputLogin").val(),
                password: $("#inputConfirmPassword").val()
            },
            dataType: 'json',
            success: response => {
                setTimeout(function(){
                    location.reload();
               }, 1); 
            },
            error: response => {
                $('#buttonLogin').toggle();
                $('#buttonLoginLoading').toggle();
                $('#messageFailedLogin').show();
            }
        });
    });
};