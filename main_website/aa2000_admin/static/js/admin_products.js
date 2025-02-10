$(document).ready(function() {

    // prepare the csrf token
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


    //   image preview upon selecting image
      $('#productImg1Upload').on('change', function() {
        const file = event.target.files[0];
        if (file && file.type.startsWith('image/')) {
            const reader = new FileReader();
            reader.onload = function(e) {
                $('#productImage1Preview').attr('src', e.target.result);
                $('#preview1Container').removeClass('d-none');
            };
            reader.readAsDataURL(file);
        } else {
            $('#preview1Container').addClass('d-none');
        }
    })

    $('#productImg2Upload').on('change', function() {
        const file = event.target.files[0];
        if (file && file.type.startsWith('image/')) {
            const reader = new FileReader();
            reader.onload = function(e) {
                $('#productImage2Preview').attr('src', e.target.result);
                $('#preview2Container').removeClass('d-none');
            };
            reader.readAsDataURL(file);
        } else {
            $('#preview2Container').addClass('d-none');
        }
    })

    $('#productImg3Upload').on('change', function() {
        const file = event.target.files[0];
        if (file && file.type.startsWith('image/')) {
            const reader = new FileReader();
            reader.onload = function(e) {
                $('#productImage3Preview').attr('src', e.target.result);
                $('#preview3Container').removeClass('d-none');
            };
            reader.readAsDataURL(file);
        } else {
            $('#preview3Container').addClass('d-none');
        }
    })


    $('#productDescImg1Upload').on('change', function() {
        const file = event.target.files[0];
        if (file && file.type.startsWith('image/')) {
            const reader = new FileReader();
            reader.onload = function(e) {
                $('#productDescImg1Preview').attr('src', e.target.result);
                $('#productDescImg1PreviewContainer').removeClass('d-none');
            };
            reader.readAsDataURL(file);
        } else {
            $('#productDescImg1PreviewContainer').addClass('d-none');
        }
    })

    $('#productDescImg2Upload').on('change', function() {
        const file = event.target.files[0];
        if (file && file.type.startsWith('image/')) {
            const reader = new FileReader();
            reader.onload = function(e) {
                $('#productDescImg2Preview').attr('src', e.target.result);
                $('#productDescImg2PreviewContainer').removeClass('d-none');
            };
            reader.readAsDataURL(file);
        } else {
            $('#productDescImg2PreviewContainer').addClass('d-none');
        }
    })


    $('#keyFeatureImg1Upload').on('change', function() {
        const file = event.target.files[0];
        if (file && file.type.startsWith('image/')) {
            const reader = new FileReader();
            reader.onload = function(e) {
                $('#keyFeatureImg1Preview').attr('src', e.target.result);
                $('#keyFeatureImg1PreviewContainer').removeClass('d-none');
            };
            reader.readAsDataURL(file);
        } else {
            $('#keyFeatureImg1PreviewContainer').addClass('d-none');
        }
    })

    $('#keyFeatureImg2Upload').on('change', function() {
        const file = event.target.files[0];
        if (file && file.type.startsWith('image/')) {
            const reader = new FileReader();
            reader.onload = function(e) {
                $('#keyFeatureImg2Preview').attr('src', e.target.result);
                $('#keyFeatureImg2PreviewContainer').removeClass('d-none');
            };
            reader.readAsDataURL(file);
        } else {
            $('#keyFeatureImg2PreviewContainer').addClass('d-none');
        }
    })




    // for technical specifications area

    $('.add-categ-btn').on('click', function() {
        const categCard = `
                    <div class="card tech-spec col-xl-3 col-6 m-1">
                        <div class="card-body">
                            <label class="categ-label form-label fs-3 fw-medium">Category</label>
                            <div class="input-group">
                                <span class="input-group-text"><i class="bi bi-star"></i></span>
                                <input type="text" name="categ-name" class="form-control categ-name" value="New Category" required disabled>
                            </div> 
                            <div class="add-categ-btns mt-1 d-none">
                                <button type="button" class="btn btn-primary p-1 add-btn">Add</button>
                                <button type="button" class="btn btn-secondary p-1 delete-btn">Cancel</button>
                            </div>
                            <div class="edit-categ-btns mt-1 d-none">
                                <button type="button" class="btn btn-primary p-1 edit-btn">Edit</button>
                                <button type="button" class="btn btn-danger p-1 delete-btn">Delete</button>
                            </div> 
                            <div class="edit-active-categ-btns mt-1 d-none">
                                <button type="button" class="btn btn-primary p-1 save-btn">Save</button>
                            </div> 
                            <div class="specs-area mt-3 row"></div> <!-- Area for nested specs -->
                            <div class="add-spec-btn-area mt-2">
                                <button type="button" class="btn btn-secondary p-1 add-spec-btn">Add Specification</button>
                            </div>
                        </div>
                    </div>
        `;
        $('#categ-container').append(categCard);
        const newCard = $('#categ-container').children().last();
        newCard.find('.categ-name').prop('disabled', false);
        newCard.find('.add-categ-btns').removeClass('d-none');
    })


    $('#categ-container').on('click', '.add-btn', function() {
        const cardBody = $(this).closest('.card-body');
        cardBody.find('.categ-name').prop('disabled', true)
        cardBody.find('.add-categ-btns').addClass('d-none')
        cardBody.find('.edit-categ-btns').removeClass('d-none');
    })

    $('#categ-container').on('click', '.delete-btn', function() {
        $(this).closest('.card').remove();
    })

    $('#categ-container').on('click', '.edit-btn', function() {
        const cardBody = $(this).closest('.card-body');
        cardBody.find('.categ-name').prop('disabled', false)
        cardBody.find('.edit-categ-btns').addClass('d-none')
        cardBody.find('.edit-active-categ-btns').removeClass('d-none');
    })

    $('#categ-container').on('click', '.save-btn', function() {
        const cardBody = $(this).closest('.card-body');
        cardBody.find('.categ-name').prop('disabled', true)
        cardBody.find('.edit-categ-btns').removeClass('d-none')
        cardBody.find('.edit-active-categ-btns').addClass('d-none');
    })
    


    // add a spec area
    $('#categ-container').on('click', '.add-spec-btn', function() {
        const cardBody = $(this).closest('.card-body')
        const specCard = `
            <div class="card tech-spec-value mt-2 card-categ-key">
                <div class="card-body">
                    <label class="spec-label form-label">Specification</label>
                    <div class="input-group">
                        <span class="input-group-text"><i class="bi bi-pencil"></i></span>
                        <input type="text" name="spec-name" class="form-control spec-name" value="Spec Name" placeholder="Spec Name" required disabled>
                    </div>
                    <div class="input-group">
                        <span class="input-group-text"><i class="bi bi-file"></i></span>
                        <input type="text" name="spec-val" class="form-control spec-val" value="Value" placeholder="Value" required disabled>
                    </div>
                    <div class="add-spec-val-btns mt-1 d-none">
                        <button type="button" class="add-spec-val-btn btn btn-primary p-1">Add</button>
                        <button type="button" class="delete-spec-val-btn btn btn-secondary p-1">Cancel</button>
                    </div>
                    <div class="edit-spec-val-btns mt-1 d-none">
                        <button type="button" class="edit-spec-val-btn btn btn-primary p-1">Edit</button>
                        <button type="button" class="delete-spec-val-btn btn btn-danger p-1">Delete</button>
                    </div> 
                    <div class="edit-active-spec-val-btns mt-1 d-none">
                        <button type="button" class="save-spec-val-btn btn btn-primary p-1">Save</button>
                    </div> 
                </div>
            </div>
        `;
        // $(this).siblings('.specs-area').append(specCard);
        cardBody.find('.specs-area').append(specCard);
        // const newSpecCard = $('.specs-area').children().last();
        const newSpecCard = cardBody.find('.specs-area').children().last();
        newSpecCard.find('.spec-name').prop('disabled', false);
        newSpecCard.find('.spec-val').prop('disabled', false);
        newSpecCard.find('.add-spec-val-btns').removeClass('d-none');
    })

    $('#categ-container').on('click', '.add-spec-val-btn', function() {
        const cardBody = $(this).closest('.card-body')
        const specCard = cardBody.closest('.specs-area');
        specCard.find('.spec-name').prop('disabled', true)
        specCard.find('.spec-val').prop('disabled', true)
        specCard.find('.add-spec-val-btns').addClass('d-none')
        specCard.find('.edit-spec-val-btns').removeClass('d-none')
    })

    $('#categ-container').on('click', '.edit-spec-val-btn', function() {
        const cardBody = $(this).closest('.card-body')
        const specCard = cardBody.closest('.specs-area');
        specCard.find('.spec-name').prop('disabled', false)
        specCard.find('.spec-val').prop('disabled', false)
        specCard.find('.edit-spec-val-btns').addClass('d-none')
        specCard.find('.edit-active-spec-val-btns').removeClass('d-none')
    })

    $('#categ-container').on('click', '.save-spec-val-btn', function() {
        const cardBody = $(this).closest('.card-body')
        const specCard = cardBody.closest('.specs-area');
        specCard.find('.edit-spec-val-btns').removeClass('d-none')
        specCard.find('.edit-active-spec-val-btns').addClass('d-none')
    })


    $('#categ-container').on('click', '.delete-spec-val-btn', function() {
        $(this).closest('.card').remove();
    })





// adding the product to the server
// get systems values
$('#productSystem').on('change', function() {
    const system = $(this).val(); 

    $.ajax({
        url: '/admin/systems/category', 
        method: 'GET',
        data: {
            system: system,
        },
        success: function(data) {
            console.log(data); 
            $('#productCategory').empty();
            $('#productBrand').empty();
            if (data.success) { 
                $.each(data.categories, function(key, value) { 
                    $('#productCategory').append('<option value="' + value.id + '">' + value.name + '</option>');
                });
                $.each(data.brands, function(key, value) { 
                    $('#productBrand').append('<option value="' + value.id + '">' + value.name + '</option>');
                });
            } else {
                $('#productCategory').append('<option disabled>No categories found.</option>');
            }
        },
        error: function(xhr, status, error) {
            console.log(xhr.responseText);
        }
    });
});

function getTechSpecsData() {
    let categories = [];

    $('.tech-spec').each(function() {
        let categoryCard = $(this);
        let categoryName = categoryCard.find('.categ-name').val();
        let specifications = [];

        categoryCard.find('.specs-area .card-categ-key').each(function() {
            let specCard = $(this);
            let specName = specCard.find('.spec-name').val();
            let specVal = specCard.find('.spec-val').val();

            specifications.push({
                name: specName,
                value: specVal
            });
        });
        categories.push({
            category_name: categoryName,
            specifications: specifications
        });
    });
    return categories;
}


function showLoader() {
    $('#loaderModal').modal('show');
}

// Function to hide loader modal
function hideLoader() {
    $('#loaderModal').modal('hide');
}

$('#productName').on('input', function() {
    const slug = $(this)
        .val()
        .toLowerCase()
        .replace(/[^a-z0-9]+/g, '-') 
        .replace(/^-+|-+$/g, '');  
    
    $('#productSlug').val(slug);
});

$('#add_product').on('submit', function(e) {
    e.preventDefault();
    // showLoader();



    var productData = {
        productName: $('#productName').val(),
        productSlug: $('#productSlug').val(),
        productSystem: $('#productSystem').val(),
        productCategory: $('#productCategory').val(),
        productBrand: $('#productBrand').val(),
        productShortDescription: $('#productShortDescription').val(),
    };
    $.ajax({
        url: '/admin/products/add/product_overview',
        method: 'POST',
        data: productData,
        success: function(response) {
            console.log('Response received:', response);  // Debug log
        
            if (response.status === 'error') {
                if (response.error === 'product slug') {
                    alert('Product Slug already exists!\nPlease enter a unique slug');
                    // hideLoader();
                    $('#productSlug').focus();
                } else {
                    alert(response.message || 'An error occurred');
                }
            } else if (response.status === 'success' && response.product?.id) {
                sendProductPhotos(response.product.id);
            } else {
                console.error('Invalid response format:', response);
                alert('Error: Unexpected response format from server');
            }
        },
        error: function(xhr, status, error) {
            console.error('Error sending product data:', error);
        }, 
        complete: function() {
            hideLoader();
        }
    })


function sendProductPhotos(productId) {
    // send the product photos
    var formData = new FormData();
    formData.append('productId', productId);

    if ($('#productImg1Upload').prop('files').length > 0) {
        formData.append('productImg1Upload', $('#productImg1Upload').prop('files')[0]);
    }

    if ($('#productImg2Upload').prop('files').length > 0) {
        formData.append('productImg2Upload', $('#productImg2Upload').prop('files')[0]);
    }


    if ($('#productImg3Upload').prop('files').length > 0) {
        formData.append('productImg3Upload', $('#productImg3Upload').prop('files')[0]);
    }

    $.ajax({
        url: '/admin/products/add/product_photos',
        method: 'POST',
        data: formData,
        processData: false,
        contentType: false,
        success: function(response) {

            console.log('Data successfully sent: ', response);
            if (response && response.status === 'success') {
                sendProductDescriptions(productId)
            } else {
                console.error('Invalid response format:', response);
                alert('Error: Unexpected response format from server');
            }

        },
        error: function(xhr, status, error) {
            console.error('Error sending product photos', error)
        }
    })
}


function sendProductDescriptions(productId) {
    // Create FormData object
    var formData = new FormData();
    
    // Add product ID
    formData.append('productId', productId);
    
    // Add descriptions and images
    for (let i = 1; i <= 2; i++) {
        // Get TinyMCE content
        const descriptionContent = tinymce.get(`productDescription_${i}`).getContent();
        formData.append(`productDescription_${i}`, descriptionContent);
        
        // Get file if it exists
        const fileInput = document.getElementById(`productDescImg${i}Upload`);
        if (fileInput && fileInput.files.length > 0) {
            formData.append(`productDescImg${i}Upload`, fileInput.files[0]);
        }
    }
    
    // Send AJAX request
    $.ajax({
        url: '/admin/products/add/product_description',
        method: 'POST',
        data: formData,
        processData: false,
        contentType: false,
        success: function(response) {
            console.log('Descriptions successfully sent:', response);
            if (response && response.status === 'success') {
                // Move to next step or show success message
                sendKeyFeatures(response.product.id);
            } else {
                console.error('Invalid response format:', response);
                alert('Error: Unexpected response format from server');
            }
        },
        error: function(xhr, status, error) {
            console.error('Error sending product descriptions:', error);
            console.error('Response:', xhr.responseText);
            alert('Error saving product descriptions. Please try again.');
        }
    });
}      
                        
function sendKeyFeatures(productId) {
    // send the key features

    var featureData = new FormData();
    featureData.append('productId', productId)
    featureData.append('keyFeature_1', $('#keyFeature_1').val())
    featureData.append('keyFeature_2', $('#keyFeature_2').val())

    if ($('#keyFeatureImg1Upload').prop('files').length > 0) {
        featureData.append('keyFeatureImg1Upload', $('#keyFeatureImg1Upload').prop('files')[0])
    }


    if ($('#keyFeatureImg2Upload').prop('files').length > 0) {
        featureData.append('keyFeatureImg2Upload', $('#keyFeatureImg2Upload').prop('files')[0])
    }

    $.ajax({
        url: '/admin/products/add/product_key_features',
        method: 'POST',
        data: featureData,
        processData: false,
        contentType: false,
        success: function(response) {
            console.log('Data successfully sent: ', response);
            if (response && response.status === 'success') {
                sendTechnicalSpecs(productId)
            } else {
                console.error('Invalid response format:', response);
                alert('Error: Unexpected response format from server');
            }
        },
        error: function(xhr, status, error){
            console.error('Error sending key features ', error)
        }
    })

}


                                

function sendTechnicalSpecs(productId) {
    // send the technical features
    let categoriesData = getTechSpecsData();
        
    $.ajax({
        url: '/admin/products/add/product_technical_specs',
        method: 'POST',
        data: JSON.stringify({ categories: categoriesData, productId: productId }),
        contentType: 'application/json',
        success: function(response) {
            console.log('Data successfully sent: ', response);
            if (response && response.status === 'success') {
                window.location.href = '/admin/products';
            } else {
                console.error('Invalid response format:', response);
                alert('Error: Unexpected response format from server');
            }


        },
        error: function(error) {
            console.error('Error in sending data: ', error)
        }
    })
}

})






    var productName = $('#productName');
    var productSlug = $('#productSlug');
    var productSystem = $('#productSystem');
    var productCategory = $('#productCategory');
    var productBrand = $('#productBrand');
    var productShortDescription = $('#productShortDescription');
    var productImg_1 = $('#productImg1Upload');
    var productImg_2 = $('#productImg2Upload');
    var productImg_3 = $('#productImg3Upload');
    var productDescriptionImg_1 = $('#productDescImg1Upload');
    var productDescriptionImg_2 = $('#productDescImg2Upload');
    var keyFeatureImg_1 = $('#keyFeatureImg1Upload');
    var keyFeatureImg_2 = $('#keyFeatureImg2Upload');
    var add_categ_btn = $('.add-categ-btn');

    var currentUrl = window.location.href;

    var currentProductSlug = currentUrl.match(/products\/([\w-]+)\/view/)[1];
    

    // view brands btn
    $('#product-edit-btn').on('click', function() {
        $('#edit-active-btns-area').removeClass('d-none')
        $('#edit-btns-area').addClass('d-none')

        // productName.prop('disabled', false).focus()
        // productSlug.prop('disabled', false)
        productSystem.prop('disabled', false).focus()
        productCategory.prop('disabled', false)
        productBrand.prop('disabled', false)
        productShortDescription.prop('disabled', false)
        productImg_1.prop('disabled', false)
        productImg_2.prop('disabled', false)
        productImg_3.prop('disabled', false)
        productDescriptionImg_1.prop('disabled', false)
        productDescriptionImg_2.prop('disabled', false)
        keyFeatureImg_1.prop('disabled', false)
        keyFeatureImg_2.prop('disabled', false)
        add_categ_btn.removeClass('d-none')
    })

    
    $('#cancel-edit-btn').on('click', function() {
        $('#edit-active-btns-area').addClass('d-none')
        $('#edit-btns-area').removeClass('d-none')
        
        productName.prop('disabled', true)
        productSlug.prop('disabled', true)
        productSystem.prop('disabled', true)
        productCategory.prop('disabled', true)
        productBrand.prop('disabled', true)
        productShortDescription.prop('disabled', true)
        productImg_1.prop('disabled', true)
        productImg_2.prop('disabled', true)
        productImg_3.prop('disabled', true)
        productDescriptionImg_1.prop('disabled', true)
        productDescriptionImg_2.prop('disabled', true)
        keyFeatureImg_1.prop('disabled', true)
        keyFeatureImg_2.prop('disabled', true)
        add_categ_btn.addClass('d-none')
    })


    $('#edit_product_form').on('submit', function(e) {
        e.preventDefault()
        showLoader()


        var productData = {
            "productName": productName.val(),
            "productSlug": productSlug.val(),
            "productSystem": productSystem.val(),
            "productCategory": productCategory.val(),
            "productBrand": productBrand.val(),
            "productShortDescription": productShortDescription.val(),
        }

        $.ajax({
            url: `/admin/products/edit/${currentProductSlug}/product_overview`,
            method: 'POST',
            data: productData,
            success: function(response) {
                console.log(response);
                slug = response.slug
                editProductPhotos(slug)
            },
            error: function(xhr, status, error) {
                console.error('Error sending product data:', error);
            },
            complete: function() {
                hideLoader()
            }
        })
    })


function editProductPhotos(slug) {
    var photoData = new FormData()

    $('.productPhoto input[type="file"]').each(function(index) {
        var fileInput = $(this);
        var file = fileInput.prop('files')[0];
    
        if (file) {
            // Log the closest ancestor to see what is being found
            var imgContainer = fileInput.closest('.productPhoto');
    
            // Check if the data attribute is present
            var photoId = imgContainer.data('photo-id');
            // console.log("Photo ID:", photoId);
    
            if (photoId) {
                photoData.append(`productImg${index + 1}Upload`, file);
                photoData.append(`productImg${index + 1}Id`, photoId);
            } else {
                console.warn("Photo ID is undefined for index:", index);
            }
        } 
    })

    $.ajax({
        url: `/admin/products/edit/${currentProductSlug}/product_photos`,
        method: 'POST',
        data: photoData,
        processData: false,
        contentType: false,
        success: function(response) {
            // console.log(response);
            editProductDescriptions(slug)
        },
        error: function(xhr, status, error) {
            console.error('Error sending product data:', error);
        },
        complete: function() {
        }
    })
}


function editProductDescriptions(slug) {
    var descriptionData = new FormData()

    $('.product_description').each(function(index) {
        var descriptionContainer = $(this)
        var description_id = descriptionContainer.data('description-id')

        var productDesc = descriptionContainer.find('textarea[name^="productDescription_"]').val();

        descriptionData.append(`productDescription_${index + 1}`, productDesc)
        descriptionData.append(`descriptionId_${index + 1}`, description_id)

        var productDescImg = descriptionContainer.find(`input[name="productDescImg${index + 1}Upload"]`);
        var productDescImgFile = productDescImg.prop('files')[0];

        if(productDescImgFile) {
            descriptionData.append(`productDescImg${index + 1}Upload`, productDescImgFile);
            descriptionData.append(`productDescImg${index + 1}Id`, description_id); 
        }
    })

    $.ajax({
        url: `/admin/products/edit/${currentProductSlug}/product_description`,
        method: 'POST',
        data: descriptionData,
        processData: false,
        contentType: false,
        success: function(response) {
            // console.log(response);
            editKeyFeatures(slug)
        },
        error: function(xhr, status, error) {
            console.error('Error sending product data:', error);
        },
        complete: function() {
        }
    })
}


function editKeyFeatures(slug) {
    var keyFeatureData = new FormData()

    $('.key_features').each(function(index) {
        var keyfeatureContainer = $(this)
        var keyfeature_id = keyfeatureContainer.data('key-feature-id')

        var keyfeature = keyfeatureContainer.find('textarea[name^="keyFeature_"]').val();

        keyFeatureData.append(`keyFeature_${index + 1}`, keyfeature)
        keyFeatureData.append(`keyFeatureId_${index + 1}`, keyfeature_id)

        var keyfeatureImg = keyfeatureContainer.find(`input[name="keyFeatureImg${index + 1}Upload"]`);
        var keyfeatureImgFile = keyfeatureImg.prop('files')[0];

        if(keyfeatureImgFile) {
            keyFeatureData.append(`keyFeatureImg${index + 1}Upload`, keyfeatureImgFile);
            keyFeatureData.append(`keyFeatureImg${index + 1}Id`, keyfeature_id); 
        }
    })

    $.ajax({
        url: `/admin/products/edit/${currentProductSlug}/product_key_features`,
        method: 'POST',
        data: keyFeatureData,
        processData: false,
        contentType: false,
        success: function(response) {
            // console.log(response);
            editTechSpecs(slug);
        },
        error: function(xhr, status, error) {
            console.error('Error sending product data:', error);
        },
        complete: function() {
        }
    })
}


function getExistingTechSpecsData() {
    let categories = [];

    $('.tech-spec').each(function() {
        let categoryCard = $(this);
        let categoryName = categoryCard.find('.categ-name').val();
        let categoryId = categoryCard.data('tech-spec-id')
        let specifications = [];

        categoryCard.find('.specs-area .card-categ-key').each(function() {
            let specCard = $(this);
            let specName = specCard.find('.spec-name').val();
            let specVal = specCard.find('.spec-val').val();
            let specCategId = specCard.data('tech-spec-detail-id')

            specifications.push({
                name: specName,
                value: specVal,
                specCategId: specCategId
            });
        });
        categories.push({
            categoryId: categoryId,
            categoryName: categoryName,
            specifications: specifications
        });
    });
    return categories;
}


function editTechSpecs(slug) {
    let categoriesData = getExistingTechSpecsData();

    $.ajax({
        url: `/admin/products/edit/${currentProductSlug}/product_technical_specs`,
        method: 'POST',
        data: JSON.stringify({ categories: categoriesData }),
        contentType: 'application/json',
        success: function(response) {
            // console.log(response);
            window.location.href = `/admin/products/${slug}/view`
            // window.location.reload()
        },
        error: function(xhr, status, error) {
            console.error('Error sending product data:', error);
        },
        complete: function() {
        }
    })
}


$('#delete_product').on('submit', function(e){
    e.preventDefault()
    $.ajax({
        url: `/admin/products/delete/${currentProductSlug}`,
        method: 'POST',
        success: function(response) {
            console.log(response);
            window.location.href = '/admin/products';
        },
        error: function(xhr, status, error) {
            console.error('Error sending product data:', error);
        },
        complete: function() {
        }
    })
})









})