$(document).ready(function() {




    $('#jobImageUpload').on('change', function(event) {
        const file = event.target.files[0];
        if (file && file.type.startsWith('image/')) {
            const reader = new FileReader();
            reader.onload = function(e) {
                $('#jobImgPreview').attr('src', e.target.result);
                $('#jobImgPreviewContainer').removeClass('d-none');
            };
            reader.readAsDataURL(file);
        } else {
            $('#jobImgPreviewContainer').addClass('d-none');
        }
    })


    $('#jobTitle').on('input', function() {
        const slug = $(this)
            .val()
            .toLowerCase()
            .replace(/[^a-z0-9]+/g, '-') 
            .replace(/^-+|-+$/g, '');  
        
        $('#jobSlug').val(slug);
    });



    function showLoader() {
        $('#loaderModal').modal('show');
    }
    
    // Function to hide loader modal
    function hideLoader() {
        $('#loaderModal').modal('hide');
    }

    // add new job

    var title = $('#jobTitle');
    var slug = $('#jobSlug');
    var shortDescription = $('#shortDescription');
    var jobImageUpload = $('#jobImageUpload');
    var jobDescription = $('#jobDescription');
    var keyResponsibilities_1 = $('#keyResponsibilities_1');
    var keyResponsibilities_2 = $('#keyResponsibilities_2');
    var qualifications_1 = $('#qualifications_1');
    var qualifications_2 = $('#qualifications_2');
    var preferredSkills_1 = $('#preferredSkills_1');
    var preferredSkills_2 = $('#preferredSkills_2');
    var compensations = $('#compensations');
    var benefits = $('#benefits');
    
    function getJobData() {
        let keyResponsibilities = [
            { responsibility: keyResponsibilities_1.val() },
            { responsibility: keyResponsibilities_2.val() }
        ];
    
        let qualifications = [
            { qualifications: qualifications_1.val() },
            { qualifications: qualifications_2.val() }
        ];
    
        let preferredSkills = [
            { preferredSkills: preferredSkills_1.val() },
            { preferredSkills: preferredSkills_2.val() }
        ];
    
        // Create FormData object
        let formData = new FormData();
        formData.append('title', title.val());
        formData.append('slug', slug.val());
        formData.append('shortDescription', shortDescription.val());
        formData.append('jobImageUpload', jobImageUpload.prop('files')[0]);
        formData.append('jobDescription', jobDescription.val());
        formData.append('keyResponsibilities', JSON.stringify(keyResponsibilities));
        formData.append('qualifications', JSON.stringify(qualifications));
        formData.append('preferredSkills', JSON.stringify(preferredSkills));
        formData.append('compensations', compensations.val());
        formData.append('benefits', benefits.val());
    
        return formData;
    }



    function getExistingJobData() {
        let keyResponsibilities = [
            { responsibility: keyResponsibilities_1.val(), responsibility_id: keyResponsibilities_1.data('responsibility-id') },
            { responsibility: keyResponsibilities_2.val(), responsibility_id: keyResponsibilities_2.data('responsibility-id') }
        ];
    
        let qualifications = [
            { qualifications: qualifications_1.val(), qualifications_id: qualifications_1.data('qualifications-id') },
            { qualifications: qualifications_2.val(), qualifications_id: qualifications_2.data('qualifications-id') }
        ];
    
        let preferredSkills = [
            { preferredSkills: preferredSkills_1.val(), preferredSkills_id: preferredSkills_1.data('preferred-skills-id') },
            { preferredSkills: preferredSkills_2.val(), preferredSkills_id: preferredSkills_2.data('preferred-skills-id') }
        ];
    
        // Create FormData object
        let formData = new FormData();
        formData.append('title', title.val());
        formData.append('slug', slug.val());
        formData.append('shortDescription', shortDescription.val());
        formData.append('jobImageUpload', jobImageUpload.prop('files')[0]);
        formData.append('jobDescription', jobDescription.val());
        formData.append('keyResponsibilities', JSON.stringify(keyResponsibilities));
        formData.append('qualifications', JSON.stringify(qualifications));
        formData.append('preferredSkills', JSON.stringify(preferredSkills));
        formData.append('compensations', compensations.val());
        formData.append('benefits', benefits.val());
    
        return formData;
    }
    
    $('#add_job').on('submit', function(e) {
        e.preventDefault();
        // showLoader();
        let jobData = getJobData();
    
        $.ajax({
            url: '/admin/jobs/processadd',
            method: 'POST',
            data: jobData,
            processData: false, // Important: Don't process data as a query string
            contentType: false, // Important: Let jQuery set the content type to multipart/form-data
            success: function(response) {
                if (response && response.status === 'success') {
                    window.location.href = '/admin/jobs';
                } else if(response && response.status == 'error' && response.error == 'Duplicate Slug') {
                    alert('Job with this slug already exists');
                    slug.focus();
                } else {
                    console.error('Invalid response format:', response);
                    alert('Error: ' + (response.message || 'Unexpected response format from server'));
                }
            },
            error: function(error) {
                console.error('Error in sending data: ', error);
                alert('Error: ' + (error.responseJSON?.message || 'Failed to send data'));
            },
            complete: function() {
                hideLoader();
            }
        });
    });
    
    


// edit job
    var currentUrl = window.location.href;

    var currentJobsSlug = currentUrl.match(/jobs\/([\w-]+)\/view/)[1];


    $('#job-edit-btn').on('click', function() {
        $('#edit-active-btns-area').removeClass('d-none')
        $('#edit-btns-area').addClass('d-none')

        title.prop('disabled', false).focus()
        slug.prop('disabled', false)
        jobImageUpload.prop('disabled', false)

    })


    $('#cancel-edit-btn').on('click', function() {
        $('#edit-active-btns-area').addClass('d-none')
        $('#edit-btns-area').removeClass('d-none')
        
        title.prop('disabled', true)
        slug.prop('disabled', true)
        jobImageUpload.prop('disabled', true)
    })



    $('#edit_job').on('submit', function(e) {
        e.preventDefault();

        let jobData = getExistingJobData();

    
        $.ajax({
            url: `/admin/jobs/${currentJobsSlug}/edit`,
            method: 'POST',
            data: jobData,
            processData: false, 
            contentType: false,
            success: function(response) {
                if (response && response.status === 'success') {
                    window.location.href = `/admin/jobs/${response.slug}/view`
                    // window.location.reload();
                } else if(response && response.status == 'error' && response.error == 'Duplicate Slug') {
                    alert('Job with this slug already exists');
                    slug.focus();
                } else {
                    console.error('Invalid response format:', response);
                    alert('Error: ' + (response.message || 'Unexpected response format from server'));
                }
            },
            error: function(error) {
                console.error('Error in sending data: ', error);
                alert('Error: ' + (error.responseJSON?.message || 'Failed to send data'));
            },
            complete: function() {
                hideLoader();
            }
        });
    })


    $('#delete_job').on('submit', function(e){
        e.preventDefault()
        $.ajax({
            url: `/admin/jobs/delete/${currentJobsSlug}`,
            method: 'POST',
            success: function(response) {
                console.log(response);
                window.location.href = '/admin/jobs';
            },
            error: function(xhr, status, error) {
                console.error('Error sending product data:', error);
            },
            complete: function() {
            }
        })
    })
    








})