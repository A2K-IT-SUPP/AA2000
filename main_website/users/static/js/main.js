$(document).ready(function() {


    document.querySelectorAll('.carousel-buttons .btn').forEach(button => {
        button.addEventListener('mouseenter', () => {
            const icon = button.querySelector('i');
            if (icon.classList.contains('bi-arrow-left-circle')) {
                icon.classList.replace('bi-arrow-left-circle', 'bi-arrow-left-circle-fill');
            } else if (icon.classList.contains('bi-arrow-right-circle')) {
                icon.classList.replace('bi-arrow-right-circle', 'bi-arrow-right-circle-fill');
            }
        });
    
        button.addEventListener('mouseleave', () => {
            const icon = button.querySelector('i');
            if (icon.classList.contains('bi-arrow-left-circle-fill')) {
                icon.classList.replace('bi-arrow-left-circle-fill', 'bi-arrow-left-circle');
            } else if (icon.classList.contains('bi-arrow-right-circle-fill')) {
                icon.classList.replace('bi-arrow-right-circle-fill', 'bi-arrow-right-circle');
            }
        });
    });



    // scroll function in the trusted brands
    const scrollBrandAmount = 200; 
    let autoBrandScrollInterval;


    function brandScrollLeft() {
        $('#brand-slider-container').animate({
            scrollLeft: '-=' + scrollBrandAmount
        }, 500);
    }


    function brandScrollRight() {
        $('#brand-slider-container').animate({
            scrollLeft: '+=' + scrollBrandAmount
        }, 500);
    }


    $('.btn-prev').click(function() {
        brandScrollLeft();
        resetAutoBrandScroll(); 
    });

    $('.btn-next').click(function() {
        brandScrollRight();
        resetAutoBrandScroll(); 
    });


    function startAutoBrandScroll() {
        autoBrandScrollInterval = setInterval(function() {
            brandScrollRight(); 
        }, 3000);
    }

    function resetAutoBrandScroll() {
        clearInterval(autoBrandScrollInterval);
        startAutoBrandScroll(); 
    }

    startAutoBrandScroll();




    // scroll function in the trusted brands
    const clientScrollAmount = 200; 
    let autoClientScrollInterval;


    function clientScrollLeft() {
        $('#clients-slider-container').animate({
            scrollLeft: '-=' + clientScrollAmount
        }, 500);
    }


    function clientScrollRight() {
        $('#clients-slider-container').animate({
            scrollLeft: '+=' + clientScrollAmount
        }, 500);
    }


    $('#client-btn-left').click(function() {
        clientScrollLeft();
        resetAutoClientScroll(); 
    });

    $('#client-btn-right').click(function() {
        clientScrollRight();
        resetAutoClientScroll(); 
    });


    function startAutoClientScroll() {
        autoClientScrollInterval = setInterval(function() {
            clientScrollRight(); 
        }, 3000);
    }

    function resetAutoClientScroll() {
        clearInterval(autoClientScrollInterval);
        startAutoClientScroll(); 
    }

    startAutoClientScroll();
})





