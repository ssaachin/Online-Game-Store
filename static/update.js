$(document).ready(function() { 
    // Handle form submission
    $('form').on('submit', function(event) { 
        event.preventDefault(); // Prevent the default form submission behavior
        
        // Get the values from the form fields
        var email = $('#email').val();
        var gamename = $('#gamename').val();

        // Make an AJAX PUT request to the server
        $.ajax({
            type: 'PUT',
            url: '/updatepost',
            data: {
                email: email,
                gamename: gamename
            }
        }).done(function(data) {
            if (data.error) {
                // Display error message
                $('#errorAlert').text(data.error).show();
                $('#successAlert').hide();
            } else {
                // Display success message
                $('#successAlert').text(data.message).show();
                $('#errorAlert').hide();
            }
        });
    });
});
