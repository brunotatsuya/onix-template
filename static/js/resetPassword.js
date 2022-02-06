window.onload = function () {
    $("#inputEmail").on("keyup", function (event) {
        if (event.keyCode === 13) {
            $('#buttonSendEmail').click();
        }
    });

    $('#buttonSendEmail').on('click', function () {
        $('#buttonSendEmail').toggle();
        $('#buttonSendEmailLoading').toggle();
        $.ajax({
            type: "POST",
            url: '/api/request_password_reset',
            data: {
                email: $("#inputEmail").val()
            },
            dataType: 'json',
            success: response => {
                setTimeout(function(){
                    location.reload();
               }, 1); 
            },
            error: response => {
                $('#buttonSendEmail').toggle();
                $('#buttonSendEmailLoading').toggle();
                $('#textFailedSendEmail').text(response.responseJSON.message);
                $('#messageFailedSendEmail').show();
            }
        });
    });
};