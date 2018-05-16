$(document).ready(function () {
    var jqclass = $.jqclass;

    var add_content = $("#add-content");
    $('.show-content').click(function () {
        jqclass.show_modal(add_content, $(this));
    });

    $('.submit-content').click(function () {
        var params = add_content.find('form').serialize();
        $.post('/file/tree/content/add/' + product_id, params, function (resp) {
            if (resp.success) {
                window.location.reload();
            } else
                toastr.error(resp.message)
        })
    });

});