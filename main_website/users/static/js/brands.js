$(document).ready(function() {

    const scrollBrandCategAmount = 200;

    function brandCategoryScrollLeft() {
        $('#brands-systems-slider-container').animate({
            scrollLeft: '-=' + scrollBrandCategAmount
        }, 500);
    }

    function brandCategoryScrollRight() {
        $('#brands-systems-slider-container').animate({
            scrollLeft: '+=' + scrollBrandCategAmount
        },500);
    }

    $('#brands-system-btn-prev').click(function() {
        brandCategoryScrollLeft();
    })

    $('#brands-system-btn-next').click(function() {
        brandCategoryScrollRight();
    })


})
