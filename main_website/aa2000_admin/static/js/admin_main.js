$(document).ready(function () {

//   tinymce.init({
//     selector: '.text-area',
//     plugins: 'image link code lists advlist fontselect fontsizeselect',
//     toolbar: 'undo redo | formatselect | bold italic | alignleft aligncenter alignright | bullist numlist outdent indent | link image | code | fontselect fontsizeselect | header 1 header 2 header 3',
//     advlist_bullet_styles: 'default circle disc square',
//     advlist_number_styles: 'default lower-alpha lower-roman upper-alpha upper-roman',    
//     height: 400,
//     images_upload_url: '/admin/upload',  // Ensure this is the correct URL
//     automatic_uploads: true,
//     file_picker_types: 'image',
//     images_upload_handler: function (blobInfo, success, failure) {
//         let formData = new FormData();
//         formData.append('file', blobInfo.blob(), blobInfo.filename());

//         fetch('/admin/upload', {  
//             method: 'POST',
//             body: formData
//         })
//         .then(response => {
//             console.log("Upload Response Status:", response.status);
//             return response.json();  // Ensure response is converted to JSON
//         })
//         .then(data => {
//             console.log("Upload Response JSON:", data); // Debugging

//             if (data && data.location) {
//                 console.log("Image URL received:", data.location);
//                 success(data.location);  // ✅ Show image in TinyMCE
//             } else {
//                 console.error("Error: Missing 'location' in response.");
//                 failure('Image upload failed: No "location" in response.');
//             }
//         })
//         .catch(error => {
//             console.error('Upload Error:', error);
//             failure('Image upload failed: Network error.');
//         });
//     }
// });


tinymce.init({
    selector: '.text-area',
    plugins: 'image link code lists advlist fontselect fontsizeselect',
    toolbar: 'undo redo | formatselect | bold italic | alignleft aligncenter alignright | bullist numlist outdent indent | link image | code | fontselect fontsizeselect',
    height: 400,
    images_upload_url: '/admin/upload',
    automatic_uploads: true,
    file_picker_types: 'image',
    images_upload_handler: function (blobInfo, success, failure) {
        let formData = new FormData();
        formData.append('file', blobInfo.blob(), blobInfo.filename());

        console.log("📤 Uploading file:", blobInfo.filename());  // Debugging log

        fetch('/admin/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            console.log("✅ Upload Response Status:", response.status);
            return response.json();
        })
        .then(data => {
            console.log("✅ Upload Response JSON:", data);

            if (data && data.location) {
                console.log("✅ Image URL received:", data.location);
                success(data.location);
            } else {
                console.error("❌ Missing 'location' in response:", data);
                failure('Image upload failed: No "location" in response.');
            }
        })
        .catch(error => {
            console.error("❌ Upload Error:", error);
            failure('Image upload failed: Network error.');
        });
    }
});


      



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


});