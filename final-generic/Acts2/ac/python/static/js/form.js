$(document).ready(function() {

    $('form').on('submit', function(event) {

        $.ajax({
            data : JSON.stringify({
                name : $('#nameInput').val(),
                password : sha1($('#passwordInput').val())
            }),
            dataType : "json",
            contentType: 'application/json',
            type : 'POST',
            url : '/api/v1/users',
            success : function(data){

            if (data.code == 400) {
                $('#errorAlert').text("UserName or Password missing").show();
                $('#successAlert').hide();
            }
            if (data.code == 405) {
                $('#errorAlert').text("User Already exist").show();
                $('#successAlert').hide();
            }
            if(data.code == 201) {
                $('#successAlert').text("Registration Successful").show();
                $('#errorAlert').hide();
            }
            if(data.code == 600) {
                $('#errorAlert').text("sha1 encode error").show();
                $('#successAlert').hide();
            }


    }});
        event.preventDefault();

});
});