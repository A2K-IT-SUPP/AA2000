$(document).ready(function() {

       
    //   image preview upon selecting image
    $('#brandLogoUpload').on('change', function() {
        const file = event.target.files[0];
        if (file && file.type.startsWith('image/')) {
            const reader = new FileReader();
            reader.onload = function(e) {
                $('#brandImagePreview').attr('src', e.target.result);
                $('#previewContainer').removeClass('d-none');
            };
            reader.readAsDataURL(file);
        } else {
            $('#previewContainer').addClass('d-none');
        }
    })

    $('#brandDescImg1Upload').on('change', function() {
        const file = event.target.files[0];
        if (file && file.type.startsWith('image/')) {
            const reader = new FileReader();
            reader.onload = function(e) {
                $('#brandDescImg1Preview').attr('src', e.target.result);
                $('#brandDescImg1PreviewContainer').removeClass('d-none');
            };
            reader.readAsDataURL(file);
        } else {
            $('#brandDescImg1PreviewContainer').addClass('d-none');
        }
    })

    
    $('#brandDescImg2Upload').on('change', function() {
        const file = event.target.files[0];
        if (file && file.type.startsWith('image/')) {
            const reader = new FileReader();
            reader.onload = function(e) {
                $('#brandDescImg2Preview').attr('src', e.target.result);
                $('#brandDescImg2PreviewContainer').removeClass('d-none');
            };
            reader.readAsDataURL(file);
        } else {
            $('#brandDescImg2PreviewContainer').addClass('d-none');
        }
    })


    $('#brandName').on('input', function() {
        const slug = $(this)
            .val()
            .toLowerCase()
            .replace(/[^a-z0-9]+/g, '-') 
            .replace(/^-+|-+$/g, '');  
        
        $('#brandSlug').val(slug);
    });

    

        // brand edit
        brand_name = $('#brandName')
        system = $('#brandSystem')
        brandSlug = $('#brandSlug')
        logo = $('#brandLogoUpload')
        description_1 = $('#brandDescription_1')
        image_1 = $('#brandDescImg1Upload')
        description_2 = $('#brandDescription_2')
        image_2 = $('#brandDescImg2Upload')
        other_details = $('#brandOtherDescription')
    
        $('#brand-edit-btn').on('click', function() {
            $('#edit-active-btns-area').removeClass('d-none')
            $('#edit-btns-area').addClass('d-none')
    
            brand_name.prop('disabled', false).focus()
            system.prop('disabled', false)
            brandSlug.prop('disabled', false)
            logo.prop('disabled', false)
            description_1.prop('disabled', false)
            image_1.prop('disabled', false)
            description_2.prop('disabled', false)
            image_2.prop('disabled', false)
            other_details.prop('disabled', false)

    
        })
    
        
        $('#cancel-edit-btn').on('click', function() {
            $('#edit-active-btns-area').addClass('d-none')
            $('#edit-btns-area').removeClass('d-none')
                
            brand_name.prop('disabled', true)
            system.prop('disabled', true)
            brandSlug.prop('disabled', true)
            logo.prop('disabled', true)
            description_1.prop('disabled', true)
            image_1.prop('disabled', true)
            description_2.prop('disabled', true)
            image_2.prop('disabled', true)
            other_details.prop('disabled', true)
        })
    


})