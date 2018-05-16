$(document).ready(function () {
    var file = $.product_class;
    var file_modal = $('#select_product');
    $('.add-product').click(function () {
        file.show_modal(file_modal, $(this));
    });

    $('.submit_product').click(function () {
        var params = file_modal.find('form').serialize();
        $.post('/file/product/create', params, function (resp) {
            if (resp.success) {
                file_modal.modal('hide');
                sessionStorage.setItem('success', resp.message);
                window.location.href = '/file/edit/' + resp.product_id
            } else
                toastr.error(resp.message)
        })
    });
});