$(document).ready(function() {
    
    const scrollBrandCategAmount = 200;

    function brandCategoryScrollLeft() {
        $('#same-brand-products-slider').animate({
            scrollLeft: '-=' + scrollBrandCategAmount
        }, 500);
    }

    function brandCategoryScrollRight() {
        $('#same-brand-products-slider').animate({
            scrollLeft: '+=' + scrollBrandCategAmount
        },500);
    }

    $('#same-brand-products-btn-prev').click(function() {
        brandCategoryScrollLeft();
    })

    $('#same-brand-products-btn-next').click(function() {
        brandCategoryScrollRight();
    })


})
