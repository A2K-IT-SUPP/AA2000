$(document).ready(function() {

    var slides = $('.product-main-slide');
    var btns = $('.product-icon-slide');
    let currentslide = 0;

    var manualNav = function(manual) {

        slides.each(function() {
            $(this).removeClass('active');
        })

        btns.each(function(manual) {
            $(this).removeClass('active');
        })

        $(slides[manual]).addClass('active');
        $(btns[manual]).addClass('active');


    }

    btns.each(function(i) {
        $(this).on('click', function() {
            manualNav(i);
            currentslide = i;
        });
    });



    $('#similar-products-slider-container').scrollLeft = 0;

    const scrollSimilarProductAmount = 300;

    function similarProductScrollLeft() {
        $('#similar-products-slider-container').animate({
            scrollLeft: '-=' + scrollSimilarProductAmount
        }, 500);
    }
    
    function similarProductScrollRight() {
        $('#similar-products-slider-container').animate({
            scrollLeft: '+=' + scrollSimilarProductAmount
        }, 500);
    }

    $('#similar-products-btn-prev').click(function() {
        similarProductScrollLeft();
    })

    
    $('#similar-products-btn-next').click(function() {
        similarProductScrollRight();
    })


    
    $('#same-brand-products-slider-container').scrollLeft = 0;

    const scrollSameBrandProductAmount = 300;

    function sameBrandProductScrollLeft() {
        $('#same-brand-products-slider-container').animate({
            scrollLeft: '-=' + scrollSimilarProductAmount
        }, 500);
    }
    
    function sameBrandProductScrollRight() {
        $('#same-brand-products-slider-container').animate({
            scrollLeft: '+=' + scrollSimilarProductAmount
        }, 500);
    }

    $('#same-brand-products-btn-prev').click(function() {
        sameBrandProductScrollLeft();
    })

    
    $('#same-brand-products-btn-next').click(function() {
        sameBrandProductScrollRight();
    })
})