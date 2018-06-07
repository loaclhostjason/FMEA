$(document).ready(function () {

    var edit_tree_modal = $("#edit-tree-modal");
    $(document).on('click', '.show-edit-tree', function () {
        $.jqclass.show_modal(edit_tree_modal, $(this));
        edit_tree_modal.find('.modal-title').text($(this).data('message'))
    });
});


$(document).ready(function () {
    var update_name = $('#update-name-modal');
    update_name.on('hide.bs.modal', function () {
        $(this).find('form')[0].reset();
    });

    update_name.find('.submit_update_name').click(function () {
        var params = (this).find('form').serialize();
        $.post('/tree/edit/name', params, function (resp) {
            if (resp.success) {
                toastr.success(resp.message);
                resp['product_relation_id'] ? $.get_func_or_failure_tree(resp['product_relation_id']) : $.get_tree(product_id);
                update_name.modal('hide');
            } else {
                toastr.error(resp.message)
            }
        })
    })
});