$(document).ready(function () {
    var file = $.product_class;
    var file_modal = $('#select_product');
    $('.add-product').click(function () {
        file.show_modal(file_modal, $(this));
    });
});