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




    // edit account details
    var adminFname = $('#adminFirstName')
    var adminLname = $('#adminLastName')
    var adminEmail = $('#adminEmail')
    var adminImg = $('#adminImgUpload')
    var username = $('#adminUsername')
    var oldPassword = $('#adminOldPassword')
    var newPassword = $('#adminNewPassword')
    var confirmPassword = $('#adminNewPassword2')
    var adminSecurityCode = $('.admin-access-code-area')

    function getAccessCode() {
        const accessCode = $('#current_digit1').val() +
        $('#current_digit2').val() +
        $('#current_digit3').val() +
        $('#current_digit4').val() +
        $('#current_digit5').val() +
        $('#current_digit6').val();

        return accessCode
    }


    $('#admin-edit-btn').on('click', function() {
        $('#edit-active-btns-area').removeClass('d-none')
        $('#edit-btns-area').addClass('d-none')
        $('#edit-credentials-btns-area').removeClass('d-none')
        $('#edit-code-btns-area').removeClass('d-none')
        
        adminFname.prop('disabled', false).focus()
        adminLname.prop('disabled', false)
        adminEmail.prop('disabled', false)
        adminImg.prop('disabled', false)
        adminSecurityCode.removeClass('d-none')

    })

    
    $('#cancel-edit-btn').on('click', function() {
        $('#edit-active-btns-area').addClass('d-none')
        $('#edit-btns-area').removeClass('d-none')
        $('#edit-credentials-btns-area').addClass('d-none')
        $('#edit-code-btns-area').addClass('d-none')

        adminFname.prop('disabled', true)
        adminLname.prop('disabled', true)
        adminEmail.prop('disabled', true)
        adminImg.prop('disabled', true)

        adminSecurityCode.addClass('d-none')

    })


    function getAdminData() {

        access_code = getAccessCode()
        let formData = new FormData();

        formData.append('admin_fname', adminFname.val());
        formData.append('admin_lname', adminLname.val());
        formData.append('admin_email', adminEmail.val());
        formData.append('admin_photo', adminImg.prop('files')[0])
        formData.append('access_code', access_code);


        return formData;
    }



    $('#edit_account').on('submit', function(e) {
        e.preventDefault();

        let accountData = getAdminData()

        $.ajax({
            url: `/admin/settings/edit`,
            method: 'POST',
            data: accountData,
            processData: false,
            contentType: false,
            success: function(response) {
                if (response && response.status === 'success' && response.type === 'Account Update') {
                    window.location.reload();
                } else if (response && response.status === 'success' && response.type === 'Password Update') {
                    alert('Account Password Updated Successfully')
                } else if (response && response.status === 'error' && response.type === 'Security Code') {
                    alert('Incorrect Security Code')
                    adminSecurityCode.focus()
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



    // edit password
    var isChangePass = 0;

    $('#admin-edit-credentials-btn').on('click', function(){
        isChangePass = 1;
        $('.admin-password-area').removeClass('d-none')
        $('#active-edit-credentials-btns-area').removeClass('d-none')

        oldPassword.prop('disabled', false)
        newPassword.prop('disabled', false)
        confirmPassword.prop('disabled', false)
    })

    $('#admin-canceledit-credentials-btn').on('click', function() {
        isChangePass = 0;
        $('.admin-password-area').addClass('d-none')
        $('#active-edit-credentials-btns-area').addClass('d-none')

        oldPassword.prop('disabled', true).val('')
        newPassword.prop('disabled', true).val('')
        confirmPassword.prop('disabled', true).val('')
    })


    function getAdminCredentialsData() {

        let accountData = {
            isChangePass: isChangePass,
            oldPassword: oldPassword.val(),
            newPassword: newPassword.val(),
        }

        return accountData;
    }


    $('#update_password').on('submit', function(e) {
        e.preventDefault();
        if (newPassword.val() !== confirmPassword.val()) {
            alert('Your Password does not match')
            return
        }

        let accountData = getAdminCredentialsData();
        
        $.ajax({
            url: `/admin/settings/edit/credentials`,
            method: 'POST',
            data: accountData,
            success: function(response) {
                if (response.status === 'success' && response.type === 'Account Update') {
                    alert(response.message)
                    oldPassword.prop('disabled', true).val('')
                    newPassword.prop('disabled', true).val('')
                    confirmPassword.prop('disabled', true).val('')
                    $('#changePasswordModal').modal('hide')
                } else if (response.status === 'error' && response.type === 'Password Update') {
                    alert(response.message)
                    oldPassword.focus()
                } else if (response.status === 'error' && response.type === 'Database' ) {
                    alert(response.message)
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



    // change access code
    
    // edit password
    var isChangeCode = 0;

    $('#admin-edit-code-btn').on('click', function(){
        isChangeCode = 1;
        $('.admin-access-code-area').removeClass('d-none')

        oldPassword.prop('disabled', false)
        newPassword.prop('disabled', false)
        confirmPassword.prop('disabled', false)
    })

    $('#admin-canceledit-code-btn').on('click', function() {
        isChangeCode = 0;
        $('.admin-access-code-area').addClass('d-none')

        oldPassword.prop('disabled', true).val('')
        newPassword.prop('disabled', true).val('')
        confirmPassword.prop('disabled', true).val('')
    })


    function getAdminCodeData() {
        
        const oldAccessCode = 
            $('#old_digit1').val() +
            $('#old_digit2').val() +
            $('#old_digit3').val() +
            $('#old_digit4').val() +
            $('#old_digit5').val() +
            $('#old_digit6').val();

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
            isChangeCode: isChangeCode,
            oldCode: oldAccessCode,
            newCode: newAccessCode,
            confirmCode: confirmNewAccessCode
        }

        return accountData;
    }


    function clearAdminCodeInput() {
                
        for (i=1; i<=6; i++) {
            $('#old_digit' + i).val('')
            $('#new_digit' + i).val('')
            $('#confirm_new_digit' + i).val('')
        }

    }

    $('#update_access_code').on('submit', function(e) {
        e.preventDefault();

        let accountData = getAdminCodeData();

        if (accountData['newCode'] !== accountData['confirmCode']) {
            alert('Your Access Code does not match')
            return
        }

        $.ajax({
            url: `/admin/settings/edit/access_code`,
            method: 'POST',
            data: accountData,
            success: function(response) {
                if (response.status === 'success' && response.type === 'Access Code Update') {
                    alert(response.message)
                    clearAdminCodeInput()
                    $('#changeCodeModal').modal('hide')
                } else if (response.status === 'error' && response.type === 'Access Code Update') {
                    alert(response.message)
                    clearAdminCodeInput()
                    old_digit1.focus()
                } else if (response.status === 'error' && response.type === 'Database' ) {
                    alert(response.message)
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


})