$(document).ready(function() {

    $('#authorImgUpload').on('change', function() {
        const file = event.target.files[0];
        if (file && file.type.startsWith('image/')) {
            const reader = new FileReader();
            reader.onload = function(e) {
                $('#authorImgPreview').attr('src', e.target.result);
                $('#authorImgPreviewContainer').removeClass('d-none');
            };
            reader.readAsDataURL(file);
        } else {
            $('#authorImgPreviewContainer').addClass('d-none');
        }
    })

    $('#articleCoverImg').on('change', function() {
        const file = event.target.files[0];
        if (file && file.type.startsWith('image/')) {
            const reader = new FileReader();
            reader.onload = function(e) {
                $('#articleCoverImgPreview').attr('src', e.target.result);
                $('#articleCoverImgPreviewContainer').removeClass('d-none');
            };
            reader.readAsDataURL(file);
        } else {
            $('#articleCoverImgPreviewContainer').addClass('d-none');
        }
    })


    

    function showLoader() {
        $('#loaderModal').modal('show');
    }
    
    // Function to hide loader modal
    function hideLoader() {
        $('#loaderModal').modal('hide');
    }


    $('#articleTitle').on('input', function() {
        const slug = $(this)
            .val()
            .toLowerCase()
            .replace(/[^a-z0-9]+/g, '-') 
            .replace(/^-+|-+$/g, '');  
        
        $('#articleSlug').val(slug);
    });


    var title = $('#articleTitle')
    var slug = $('#articleSlug')
    var keywords = $('#keyword')
    var cover = $('#articleCoverImg')
    var author = $('#authorName')
    var author_img = $('#authorImgUpload')
    var author_description = $('#authorDescription')
    var content = $('#articleContent')

    // add article


    function getArticleData() {
        let formData = new FormData()

        formData.append('title', title.val())
        formData.append('slug', slug.val())
        formData.append('keywords', keywords.val())
        formData.append('author', author.val())
        formData.append('cover', cover.prop('files')[0])
        formData.append('author_img', author_img.prop('files')[0])
        formData.append('author_description', author_description.val())
        formData.append('content', content.val())


        return formData;
    }



    $('#add_article').on('submit', function(e) {
        e.preventDefault()

        let articleData = getArticleData()


        $.ajax({
            url: '/admin/articles/processadd',
            method: 'POST',
            data: articleData,
            processData: false, // Important: Don't process data as a query string
            contentType: false, // Important: Let jQuery set the content type to multipart/form-data
            success: function(response) {
                if (response && response.status === 'success') {
                    window.location.href = '/admin/articles';
                } else if(response && response.status == 'error' && response.error == 'Duplicate Slug') {
                    alert('Article with this slug already exists');
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


// edit article

    
$('#article-edit-btn').on('click', function() {
    $('#edit-active-btns-area').removeClass('d-none')
    $('#edit-btns-area').addClass('d-none')

    // title.prop('disabled', false).focus()
    // slug.prop('disabled', false)
    keywords.prop('disabled', false).focus()
    author.prop('disabled', false)
    author_img.prop('disabled', false)
})


$('#cancel-edit-btn').on('click', function() {
    $('#edit-active-btns-area').addClass('d-none')
    $('#edit-btns-area').removeClass('d-none')
    
    title.prop('disabled', true)
    slug.prop('disabled', true)
    keywords.prop('disabled', true)
    author.prop('disabled', true)
    author_img.prop('disabled', true)
})


var currentUrl = window.location.href;

var currentArticlesSlug = currentUrl.match(/articles\/([\w-]+)\/view/)[1];



$('#edit_article').on('submit', function(e) {
    e.preventDefault();

    let articleData = getArticleData()


    $.ajax({
        url: `/admin/articles/${currentArticlesSlug}/edit`,
        method: 'POST',
        data: articleData,
        processData: false, // Important: Don't process data as a query string
        contentType: false, // Important: Let jQuery set the content type to multipart/form-data
        success: function(response) {
            if (response && response.status === 'success') {
                window.location.reload()
            } else if(response && response.status == 'error' && response.error == 'Duplicate Slug') {
                alert('Article with this slug already exists');
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




$('#delete_article').on('submit', function(e){
    e.preventDefault()
    $.ajax({
        url: `/admin/articles/${currentArticlesSlug}/delete`,
        method: 'POST',
        success: function(response) {
            console.log(response);
            window.location.href = '/admin/articles';
        },
        error: function(xhr, status, error) {
            console.error('Error sending product data:', error);
        },
        complete: function() {
        }
    })
})







})
