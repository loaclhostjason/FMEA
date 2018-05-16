$(document).ready(function () {
    var jqclass = $.jqclass;

    var add_content = $("#add-content");
    $('.show-content').click(function () {
        jqclass.show_modal(add_content, $(this));
    });

    $('.submit-content').click(function () {
        var params = add_content.find('form').serialize();
        params += '&parent_id=' + add_content.find('[name="parent_id"]').val();
        $.post('/file/tree/content/add/' + product_id, params, function (resp) {
            if (resp.success) {
                window.location.reload();
            } else
                toastr.error(resp.message)
        })
    });

});