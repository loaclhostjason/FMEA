$(document).ready(function () {
    var jqclass = $.jqclass;

    var add_content = $("#add-content");
    $('.show-content').click(function () {
        jqclass.show_modal(add_content, $(this));
    });

    var btn;
    add_content.on('show.bs.modal', function (event) {
        btn = $(event.relatedTarget);
    });

    $('.submit-content').click(function () {
        var params = add_content.find('form').serialize();
        var type = btn.data('type');

        params += '&parent_id=' + add_content.find('[name="parent_id"]').val() + '&type=' + type || '';
        $.post('/file/tree/content/add/' + product_id, params, function (resp) {
            if (resp.success) {
                window.location.reload();
            } else
                toastr.error(resp.message)
        })
    });

});