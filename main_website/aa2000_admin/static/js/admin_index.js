$(document).ready(function() {
    // Setup CSRF token for all AJAX requests
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Setup CSRF token for all jQuery AJAX requests
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
            }
        }
    });


    // Focus on the next input field when typing
    $('.access-code-area input[type="password"]').on('input', function() {
        // If the entered character is not a digit, clear the input
        if (!/^\d$/.test(this.value)) {
            this.value = ''; // Clear the non-digit character
        } else if (this.value.length === 1) {
            // Move to the next input only if a digit is entered
            $(this).next('input[type="password"]').focus();
        }
    });

    // Handle backspace to focus on the previous input field
    $('.access-code-area input[type="password"]').on('keydown', function(event) {
        if (event.key === 'Backspace' && $(this).val() === '') {
            // Move focus to the previous input if the field is empty
            $(this).prev('input[type="password"]').focus();
        }
    });


    var login_phase = "credentials"
    var username = $('#username')
    var password = $('#password')

    function getAccessCode() {

        accessCode = 
        $('#digit1').val() + 
        $('#digit2').val() + 
        $('#digit3').val() + 
        $('#digit4').val() + 
        $('#digit5').val() + 
        $('#digit6').val();

        return accessCode
    }


    $('#login_now').on('submit', function(e){
        e.preventDefault()

        var loginData;

        if (login_phase == 'credentials') {
            loginData = {
                login_phase: login_phase,
                username: username.val(),
                password: password.val(),
            }
        } else {
            loginData = {
                login_phase: login_phase,
                accessCode: getAccessCode()
            }
        }
        

        $.ajax({
            url: `/admin/login`,
            method: 'POST',
            data: loginData,
            success: function(response) {
                if(login_phase == 'credentials' && response && response.status == 'success' && response.nextPhase == 'accessCode') {
                    login_phase = 'accessCode'
                    $('.credentials-area').addClass('d-none')
                    $('.access-code-area').removeClass('d-none')
                    
                    welcome_banner = `<span class="fs-1 text-muted"> ${response.username}!</span>`;

                    $('#welcome_area').append(welcome_banner);

                    $('#digit1').prop('required', true).focus();
                    $('#digit2').prop('required', true);
                    $('#digit3').prop('required', true);
                    $('#digit4').prop('required', true);
                    $('#digit5').prop('required', true);
                    $('#digit6').prop('required', true);

                } else if (login_phase == 'accessCode' && response && response.status == 'success' && response.nextPhase == 'dashboard') {
                    // alert('login successful')
                    window.location.href = '/admin/home'
                } else if (login_phase == 'credentials' && response && response.status == 'error' && response.nextPhase == 'credentials') {
                    error_msg = `<span class="fs-4 text-danger"> ${response.message}!</span>`;

                    $('.login_credentials_error').empty();
                    $('.login_credentials_error').append(error_msg);
                    $('#password').val('').focus();
                } else if (login_phase == 'accessCode' && response && response.status == 'error' && response.nextPhase == 'accessCode') {
                    error_msg = `<span class="fs-4 text-danger"> ${response.message}!</span>`;

                    $('.login_access_code_error').empty();
                    $('.login_access_code_error').append(error_msg);

                    $('#digit1').val('').focus();
                    $('#digit2').val('');
                    $('#digit3').val('');
                    $('#digit4').val('');
                    $('#digit5').val('');
                    $('#digit6').val('');
                } else {
                    alert(response.message)
                }
            },
            error: function(error){
                console.error('Error in sending Data: ', error)
                alert('Error: ' + (error.responseJSON?.message || 'Failed to send data'));
            }
        })

    })
});