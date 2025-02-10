$(document).ready(function() {
// Define a maximum file size in bytes (e.g., 20 MB)
const MAX_FILE_SIZE = 20 * 1024 * 1024; // 20 MB

$('#files').on('change', function () {
    updateFilePreview();
});

// Update file preview when files are selected
function updateFilePreview() {
    const files = $('#files')[0].files;
    const previewArea = $('#file-preview');
    previewArea.empty(); // Clear previous previews

    if (files.length > 0) {
        previewArea.show(); // Show preview area

        $.each(files, function (index, file) {
            // Check if file size is within the limit
            if (file.size > MAX_FILE_SIZE) {
                alert(`The file "${file.name}" exceeds the 20 MB size limit and won't be uploaded.`);
                return; // Skip this file
            }

            const fileItem = $('<div class="file-item"></div>');
            const fileName = $('<span></span>').text(file.name).addClass('fs-6');

            // Image Preview (for images only)
            if (file.type.startsWith('image/')) {
                const reader = new FileReader();
                reader.onload = function (e) {
                    const img = $('<img>').attr('src', e.target.result).addClass('img-thumbnail');
                    fileItem.prepend(img);
                };
                reader.readAsDataURL(file);
            }

            // Add file name and remove button
            const removeButton = $('<span class="remove-file text-danger">Remove</span>')
                .on('click', function () {
                    removeFile(file);
                });

            fileItem.append(fileName, removeButton);
            previewArea.append(fileItem);
        });
    }
}

// Remove selected file from the input
function removeFile(fileToRemove) {
    const input = $('#files')[0];
    const files = Array.from(input.files);
    const updatedFiles = files.filter(file => file !== fileToRemove);

    // Create new DataTransfer object to set the updated file list
    const dataTransfer = new DataTransfer();
    updatedFiles.forEach(file => dataTransfer.items.add(file));

    input.files = dataTransfer.files;
    updateFilePreview(); // Refresh preview
}

// Drag and Drop functionality
const fileUploadArea = $('.file-upload-area');

fileUploadArea.on('dragover', function (e) {
    e.preventDefault();
    fileUploadArea.addClass('bg-light');
});

fileUploadArea.on('dragleave', function () {
    fileUploadArea.removeClass('bg-light');
});

fileUploadArea.on('drop', function (e) {
    e.preventDefault();
    fileUploadArea.removeClass('bg-light');
    const files = e.originalEvent.dataTransfer.files;
    $('#files')[0].files = files;
    updateFilePreview();
});



    function showLoader() {
        var loaderModal = new bootstrap.Modal(document.getElementById('loaderModal'));
        loaderModal.show();
      }
      
      // Function to hide loader modal
      function hideLoader() {
        var loaderModal = bootstrap.Modal.getInstance(document.getElementById('loaderModal'));
        loaderModal.hide(); // This hides the modal
      }


      function getFormData() {
        var form = $('#reply_inquiry')[0];  
        var formData = new FormData(form);
      
        var reply = $('#reply').val(); 
        // console.log("Reply:", reply);

        var files = $('#files')[0].files;  
        // console.log("Files:", files);
 
        formData.append('reply', reply)
        for (var i = 0; i < files.length; i++) {
            formData.append('files[]', files[i]);
        }
    
        return formData; 
    }
    


    
    var currentUrl = window.location.href;

    var currentInquirySlug = currentUrl.match(/inquiries\/([\w-]+)\/view/)[1];
    




    $(document).ready(function() {
        $('#reply_inquiry').on('submit', function(event) {
            event.preventDefault(); 
            
            var content = tinymce.get('reply').getContent();

            // Check if content is empty
            if (content.trim() === '') {
                alert("Please enter a reply before submitting.");
                return false;
            }

            
            showLoader()
            var formData = getFormData();  
    
           
            $.ajax({
                url: `/admin/inquiries/${currentInquirySlug}/reply`,  
                type: 'POST',
                data: formData,
                processData: false,  
                contentType: false, 
                success: function(response) {
                    console.log(response); 
                    hideLoader()
                    // alert("Reply sent successfully!");
                    if (response && response.status === 'success') {
                        $('#successLoaderModal').modal('show')
                    } else {
                        $('#errorLoaderModal').modal('show')
                    }

                },
                error: function(xhr, status, error) {
                    // Handle error
                    alert("An error occurred. Please try again.");
                    console.log(error);  // Log error for debugging
                }
            });
        });
    });
    

})