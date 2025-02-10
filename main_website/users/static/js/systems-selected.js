$(document).ready(function() {

    const scrollProductAmount = 200;

    function productScrollLeft() {
        $('#slider-container').animate({
            scrollLeft: '-=' + scrollProductAmount
        }, 500);
    }

    function productScrollRight() {
        $('#slider-container').animate({
            scrollLeft: '+=' + scrollProductAmount
        },500);
    }

    $('#products-btn-prev').click(function() {
        productScrollLeft();
    })

    $('#products-btn-next').click(function() {
        productScrollRight();
    })


})
