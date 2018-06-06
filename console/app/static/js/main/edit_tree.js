$(document).ready(function () {

    var edit_tree_modal = $("#edit-tree-modal");
    $(document).on('click', '.show-edit-tree', function () {
        $.jqclass.show_modal(edit_tree_modal, $(this));
        edit_tree_modal.find('.modal-title').text($(this).data('message'))
    });
});