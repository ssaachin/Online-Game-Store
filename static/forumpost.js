$(document).ready(function() { 
    $('form').on('submit', function(event) { 
        $.ajax({ 
            data : { 
                name : $('#name').val(), 
                email : $('#email').val(),
                gamename : $('#gamename').val(),

            }, 
            type : 'POST', 
            url : '/createpost'
        }).done(function(data) { 
            if (data.error) { 
                $('#errorAlert').text(data.error).show(); 
                $('#successAlert').hide(); 
            } else { 
                $('#successAlert').text(data.message).show(); 
                $('#errorAlert').hide(); 
            } 
        }); 

        event.preventDefault(); 
    }); 
}); 