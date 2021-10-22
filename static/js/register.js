window.onload = function () {
    $("#inputConfirmPassword").on("keyup", function (event) {
        if (event.keyCode === 13) {
            $('#buttonRegister').click();
        }
    });

    $('#buttonRegister').on('click', function () {
        $('#buttonRegister').toggle();
        $('#buttonRegisterLoading').toggle();
        $.ajax({
            type: "POST",
            url: '/api/register',
            data: {
                username: $("#inputUsername").val(),
                email: $("#inputEmail").val(),
                password: $("#inputPassword").val(),
                confirmPassword: $("#inputConfirmPassword").val()
            },
            dataType: 'json',
            success: response => {
                setTimeout(function(){
                    location.reload();
               }, 1); 
            },
            error: response => {
                $('#buttonRegister').toggle();
                $('#buttonRegisterLoading').toggle();
                $('#textFailedRegister').text(response.responseJSON.message);
                $('#messageFailedRegister').show();
            }
        });
    });
};