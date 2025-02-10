$(document).ready(function() {

    $('#adminImgUpload').on('change', function() {
        const file = event.target.files[0];
        if (file && file.type.startsWith('image/')) {
            const reader = new FileReader();
            reader.onload = function(e) {
                $('#adminImgPreview').attr('src', e.target.result);
                $('#adminImgPreviewContainer').removeClass('d-none');
            };
            reader.readAsDataURL(file);
        } else {
            $('#adminImgPreviewContainer').addClass('d-none');
        }
    })


    // admin edit
    var fname = $('#adminFirstName')
    var lname = $('#adminLastName')
    var email = $('#adminEmail')
    var photo = $('#adminImgUpload')
    var level = $('#adminLevel')
    var username = $('#adminUsername')
    var password = $('#adminPassword')
    var password2 = $('#adminPassword2')


    // Focus on the next input field when typing and accept only digits
    $('.access-code-area input[type="password"], .old-access-code-area input[type="password"], .new-access-code-area input[type="password"], .confirm-new-access-code-area input[type="password"]').on('input', function() {
        // If the entered character is not a digit, clear the input
        if (!/^\d$/.test(this.value)) {
            this.value = ''; // Clear the non-digit character
        } else if (this.value.length === 1) {
            // Move to the next input only if a digit is entered
            $(this).next('input[type="password"]').focus();
        }
    });

    // Handle backspace to focus on the previous input field
    $('.access-code-area input[type="password"], .old-access-code-area input[type="password"], .new-access-code-area input[type="password"], .confirm-new-access-code-area input[type="password"]').on('keydown', function(event) {
        if (event.key === 'Backspace' && $(this).val() === '') {
            // Move focus to the previous input if the field is empty
            $(this).prev('input[type="password"]').focus();
        }
    });


    function getAccessCode() {
        const accessCode = $('#current_digit1').val() +
        $('#current_digit2').val() +
        $('#current_digit3').val() +
        $('#current_digit4').val() +
        $('#current_digit5').val() +
        $('#current_digit6').val();

        return accessCode
    }

    function getAdminData() {
        
        let formData = new FormData()
        accessCode = getAccessCode();
        formData.append('adminFirstName', fname.val())
        formData.append('adminLastName', lname.val())
        formData.append('adminEmail', email.val())
        formData.append('adminLevel', level.val())
        formData.append('adminImgUpload', photo.prop('files')[0])
        formData.append('adminUsername', username.val())
        formData.append('adminPassword', password.val())
        formData.append('adminAccessCode', accessCode)


        return formData;
    }



    $('#add_admin').on('submit', function(e) {
        e.preventDefault()
        
        if (password.val() !== password2.val()) {
            alert('Passwords do not match')
            password2.focus()
            return
        }

        let adminData = getAdminData();
        console.log(adminData);
        

        $.ajax({
            url: `/admin/admins/processadd`,
            method: 'POST',
            data: adminData,
            processData: false,
            contentType: false,
            success: function(response) {
                if (response && response.status == 'success') {
                    window.location.href = '/admin/admins'
                } else if (response && response.status == 'error' && response.type == 'Duplicate Username') {
                    alert(response.message)
                }  else if (response && response.status == 'error' && response.type == 'Duplicate Email') {
                    alert(response.message)
                } else {
                    console.error('Invalid response format:', response);
                    alert('Error: ' + (response.message || 'Unexpected response format from server'));
                } 

            },
            error: function(error){
                console.error('Error in sending Data: ', error)
                alert('Error: ' + (error.responseJSON?.message || 'Failed to send data'));
            },
            complete: function() {
                hideLoader();
            }
        })


    })

















// edit admin data

    $('#admin-edit-btn').on('click', function() {
        $('#edit-active-btns-area').removeClass('d-none')
        $('#edit-btns-area').addClass('d-none')

        $('#edit-credentials-btns-area').removeClass('d-none')
        $('#edit-code-btns-area').removeClass('d-none')


        fname.prop('disabled', false).focus()
        lname.prop('disabled', false)
        email.prop('disabled', false)
        photo.prop('disabled', false)
        level.prop('disabled', false)

    })


    $('#cancel-edit-btn').on('click', function() {
        $('#edit-active-btns-area').addClass('d-none')
        $('#edit-btns-area').removeClass('d-none')
        $('#edit-credentials-btns-area').addClass('d-none')
        $('#edit-code-btns-area').addClass('d-none')
    })


    // edit admin details
    function getEditAdminData() {
        let formData = new FormData();

        formData.append('adminFirstName', fname.val())
        formData.append('adminLastName', lname.val())
        formData.append('adminEmail', email.val())
        formData.append('adminLevel', level.val())
        formData.append('adminImgUpload', photo.prop('files')[0])


        return formData;
    }

        
    var currentUrl = window.location.href;

    var currentAdminsSlug = currentUrl.match(/admins\/([\w-]+)\/view/)[1];



    $('#edit_admin').on('submit', function(e) {
        e.preventDefault();

        let adminEditData = getEditAdminData();


        $.ajax({
            url: `/admin/admins/${currentAdminsSlug}/edit`,
            method: 'POST',
            data: adminEditData,
            processData: false,
            contentType: false,
            success: function(response) {
                if (response && response.status === 'success') {
                    window.location.reload();
                } else {
                    console.error('Invalid response format:', response);
                    alert('Error: ' + (response.message || 'Unexpected response format from server'));
                }
            },
            error: function(error){
                console.error('Error in sending Data: ', error)
                alert('Error: ' + (error.responseJSON?.message || 'Failed to send data'));
            },
            complete: function() {
                hideLoader();
            }
        })
    })





    // update credentials area

    $('#admin-edit-credentials-btn').on('click' , function() {
        $('.admin-password-area').removeClass('d-none')

        $('#adminNewPassword').prop('disabled', false).focus()
        $('#adminNewPassword2').prop('disabled', false)
    })

    $('#cancel_edit_password_btn').on('click', function() {
        $('.admin-password-area').addClass('d-none')

        $('#adminNewPassword').prop('disabled', true).val('')
        $('#adminNewPassword2').prop('disabled', true).val('')
    })

    $('#admin-edit-code-btn').on('click' , function() {
        $('.admin-access-code-area').removeClass('d-none')
    })

    $('#cancel_edit_code_btn').on('click', function() {
        $('.admin-access-code-area').addClass('d-none')
    })

    var adminNewPassword = $('#adminNewPassword')
    var adminNewPassword2 = $('#adminNewPassword2')

    function getAdminCodeData() {
        const newAccessCode = 
        $('#new_digit1').val() +
        $('#new_digit2').val() +
        $('#new_digit3').val() +
        $('#new_digit4').val() +
        $('#new_digit5').val() +
        $('#new_digit6').val();

    const confirmNewAccessCode = 
        $('#confirm_new_digit1').val() +
        $('#confirm_new_digit2').val() +
        $('#confirm_new_digit3').val() +
        $('#confirm_new_digit4').val() +
        $('#confirm_new_digit5').val() +
        $('#confirm_new_digit6').val();
    
    let accountData = {
        newCode: newAccessCode,
        confirmCode: confirmNewAccessCode
    }

    return accountData;
    }


    $('#update_password').on('submit', function(e) {
        e.preventDefault()

        if (adminNewPassword.val() !== adminNewPassword2.val()) {
            alert('Passwords do not match')
            return
        }

        credentialsData = {
            password: adminNewPassword.val(),
        }

        $.ajax({
            url: `/admin/admins/${currentAdminsSlug}/edit/credentials`,
            method: 'POST',
            data: credentialsData,
            success: function(response) {
                if (response.status === 'success') {
                    alert(response.message)
                    adminNewPassword.prop('disabled', true).val('')
                    adminNewPassword2.prop('disabled', true).val('')
                    $('#changePasswordModal').modal('hide')
                } else {
                    alert(response.message)
                }
            },
            error: function(error){
                console.error('Error in sending Data: ', error)
                alert('Error: ' + (error.responseJSON?.message || 'Failed to send data'));
            }
        })
        // execute the ajax in here
    })


    $('#update_access_code').on('submit', function(e) {
        e.preventDefault()

        let adminCodeData = getAdminCodeData()

        if (adminCodeData['newCode'] !== adminCodeData['confirmCode']) {
            alert('Your Access Code does not match')
            return
        }
        
        $.ajax({
            url: `/admin/admins/${currentAdminsSlug}/edit/access_code`,
            method: 'POST',
            data: adminCodeData,
            success: function(response) {
                if (response.status === 'success') {
                    alert(response.message)
                    $('#changeCodeModal').modal('hide')
                } else {
                    alert(response.message)
                }
            },
            error: function(error){
                console.error('Error in sending Data: ', error)
                alert('Error: ' + (error.responseJSON?.message || 'Failed to send data'));
            }
        })
        // execute the ajax in here
    })


    $('#delete_admin').on('submit', function(e) {
        e.preventDefault()
        $.ajax({
            url: `/admin/admins/${currentAdminsSlug}/delete`,
            method: 'POST',
            success: function(response) {
                console.log(response);
                window.location.href = '/admin/admins';
            },
            error: function(xhr, status, error) {
                console.error('Error sending product data:', error);
            },
            complete: function() {
            }
        })
    })
})