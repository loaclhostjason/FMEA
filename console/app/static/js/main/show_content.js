$(document).ready(function () {
    var jqclass = $.jqclass;

    var add_content = $("#add-content");
    var add_process = $("#add-process");


    $(document).on('click', '.show-content', function () {
        jqclass.show_modal(add_content, $(this));
    });

    var btn;
    add_content.on('show.bs.modal', function (event) {
        btn = $(event.relatedTarget);
        $(this).find('form')[0].reset();
    });

    $('.submit-content').click(function () {
        var params = add_content.find('form').serialize();
        var type = btn.data('type');

        var type_name = (!type || typeof(type) === "undefined") ? '' : type;
        params += '&type=' + type_name;
        $.post('/file/tree/content/add/' + product_id, params, function (resp) {
            if (resp.success) {
                var type = resp['type'];
                if (type) {
                    $.get_func_or_failure_tree(resp['product_relation_id']);
                } else {
                    $.get_tree(product_id);
                }


                add_content.modal('hide');
                add_process.modal('hide');
            } else
                toastr.error(resp.message)
        })
    });

});