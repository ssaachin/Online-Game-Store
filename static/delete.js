$(document).ready(function() { 
    $('form').on('submit', function(event) { 
        event.preventDefault();

        // getting the values from the form
        var name = $('#name').val();
        var email = $('#email').val();
        var gamename = $('#gamename').val();

        // make an ajax DELETE request to the server
        $.ajax({
            type: 'DELETE',
            url: '/deletepost',
            data: {
                name: name,
                email: email,
                gamename: gamename
            }
        }).done(function(data) {
            if (data.error) { 
                // Displays error message
                $('#errorAlert').text(data.error).show(); 
                $('#successAlert').hide(); 
            } else { 
                // Displays success message
                $('#successAlert').text(data.message).show(); 
                $('#errorAlert').hide(); 
            } 
        }); 
    }); 
});
