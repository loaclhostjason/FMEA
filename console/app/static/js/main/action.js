$(document).ready(function () {
    var action_modal = $("#action_modal");
    action_modal.on('hide.bs.modal', function (event) {
        $(this).find('.rest_form input').val('');
    });
    var action_type;
    var type;
    var assess;
    action_modal.on('show.bs.modal', function (event) {
        var btn = $(event.relatedTarget);
        var modal = $(this);
        var name_number = action_modal.find('[name="name_number"]').val();

        action_type = btn.data('action-type');
        type = btn.data('type');
        assess = btn.data('assess');
        console.log(action_type);

        modal.find('input').attr('disabled', 'disabled');
        modal.find('select').attr('disabled', 'disabled');
        if (type === 'current') {
            action_type === 'preventive_action' ? modal.find('.current_preventive_action input').removeAttr('disabled') : modal.find('.current_probe_action input').removeAttr('disabled');
            action_type === 'preventive_action' ? modal.find('.current_preventive_action select').removeAttr('disabled') : modal.find('.current_probe_action input').removeAttr('disabled');
        } else {
            action_type === 'preventive_action' ? modal.find('.optimize_preventive_action input').removeAttr('disabled') : modal.find('.optimize_probe_action input').removeAttr('disabled');
            action_type === 'preventive_action' ? modal.find('.optimize_preventive_action select').removeAttr('disabled') : modal.find('.optimize_probe_action input').removeAttr('disabled');
        }

        if (product_id && name_number) {
            var params = 'product_id=' + product_id + '&name_number=' + name_number + '&type=' + type + '&action_type=' + action_type + '&assess=' + assess;
            $.get('/manage/product/assess/create_edit?' + params, function (resp) {
                var data = resp['data'];
                console.log(data);
                if (!data) return;

                for (var name in data) {
                    $('.' + type + '_' + action_type).find('[name="' + name + '"]').val(data[name]);
                }
            })
        }
    });

    $('.submit_action').click(function () {
        var params = action_modal.find('form').serialize();
        var name_number = action_modal.find('[name="name_number"]').val();
        params += '&product_id=' + product_id + '&name_number=' + name_number + '&type=' + type + '&action_type=' + action_type + '&assess=' + assess;
        console.log(params);
        $.post('/manage/product/assess/create_edit', params, function (resp) {
            if (resp.success) {
                toastr.success(resp.message);
                action_modal.modal('hide');
            } else
                toastr.error(resp.message)
        })
    })
});

