$(document).ready(function() {

    $('#slider-container').scrollLeft = 0;

    const scrollProductAmount = 300;

    function productScrollLeft() {
        $('#slider-container').animate({
            scrollLeft: '-=' + scrollProductAmount
        }, 500);
    }

    function productScrollRight() {
        $('#slider-container').animate({
            scrollLeft: '+=' + scrollProductAmount
        }, 500);
    }


    $('#products-btn-prev').click(function() {
        productScrollLeft();
    })

    $('#products-btn-next').click(function() {
        productScrollRight();
    })
})