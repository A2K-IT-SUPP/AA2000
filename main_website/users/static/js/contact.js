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



    $('#typeOfConcern').on('change', function() {
      var projectDetails = $('#projectDetails');
      if ($(this).val() === '1') {
        projectDetails.show(); // Show the project details section
      } else {
        projectDetails.hide(); // Hide the project details section
      }
    });




    var fname = $('#firstName')
    var lname = $('#lastName')
    var email = $('#email')
    var phone = $('#contactNumber')
    var concernType = $('#typeOfConcern')
    var details = $('#inquiry')
    var contactMethod = $('#preferredContactMethod')
    var contactTime = $('#preferredContactTime')

    var projectName = $('#projectName')
    var projectLocation = $('#projectLocation')
    var estimatedBudget = $('#estimatedBudget')
    var timeline = $('#timeline')
    var additionalDetails = $('#additionalDetails')



    function getInquiryDetails() {
      let inquiryData = {}

      fname = fname.val()
      lname = lname.val()
      email = email.val()
      phone = phone.val()
      concernType = concernType.val()
      details = details.val()
      contactMethod = contactMethod.val()
      contactTime = contactTime.val()

      if (concernType == '1') {
        projectName = projectName.val()
        projectLocation = projectLocation.val()
        estimatedBudget = estimatedBudget.val()
        timeline = timeline.val()
        additionalDetails = additionalDetails.val()        

        inquiryData = {
          "firstName": fname,
          "lastName": lname,
          "email": email,
          "contactNumber": phone,
          "typeOfConcern": concernType,
          "inquiry": details,
          "preferredContactMethod": contactMethod,
          "preferredContactTime": contactTime,
          "projectName": projectName,
          "projectLocation": projectLocation,
          "estimatedBudget": estimatedBudget,
          "timeline": timeline,
          "additionalDetails": additionalDetails
        }
        return inquiryData
      }

      inquiryData = {
        "firstName": fname,
        "lastName": lname,
        "email": email,
        "contactNumber": phone,
        "typeOfConcern": concernType,
        "inquiry": details,
        "preferredContactMethod": contactMethod,
        "preferredContactTime": contactTime
      }

      return inquiryData;
    }



    function showLoader() {
      var loaderModal = new bootstrap.Modal(document.getElementById('loaderModal'));
      loaderModal.show();
    }
    
    // Function to hide loader modal
    function hideLoader() {
      var loaderModal = bootstrap.Modal.getInstance(document.getElementById('loaderModal'));
      loaderModal.hide(); // This hides the modal
    }
    
    $('#inquire-form').on('submit', function(e) {
      e.preventDefault();
      showLoader(); // Show the loader modal
      let inquiryData = getInquiryDetails();
    
      $.ajax({
        url: '/inquiry/submit',
        method: 'POST',
        data: inquiryData,
        success: function(data) {
          console.log(data);
          hideLoader(); // Hide the loader modal
          if (data.status === 'success') {
            $('#ticket_area').text(data.ticket); // Use .text to set the ticket
            var successModal = new bootstrap.Modal(document.getElementById('successLoaderModal'));
            successModal.show(); // Show the success modal
          } else {
            var errorModal = new bootstrap.Modal(document.getElementById('errorLoaderModal'));
            errorModal.show(); // Show the error modal
          }
        },
        error: function(xhr, status, error) {
          console.log(xhr.responseText);
          // alert("Error submitting inquiry");
        }, 
        complete: function() {
          hideLoader(); // Hide the loader modal
        }
      });
    });




    // $('#check_ticket_status').on('submit', function(e) {
    //   e.preventDefault();

    //   var ticket_id = $('#ticket_id').val()

    //   $.ajax({
    //     url: `/inquiry/submit?ticket=${ticket_id}`,
    //     method: 'POST',
    //     data: {
    //       ticket_id: ticket_id
    //     },
    //     success: function(data) {
    //       console.log(data);
    //     },
    //     error: function(xhr, status, error) {
    //       console.log(xhr.responseText);
    //       // alert("Error submitting inquiry");
    //     }
    //   });
    // })
    
});