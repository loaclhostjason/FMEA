$(document).ready(function () {
    var action_modal = $("#action_modal");
    action_modal.on('show.bs.modal', function (event) {
        var btn = $(event.relatedTarget);
        var modal = $(this);

        var action_type = btn.data('action-type');
        var type = btn.data('type');
        console.log(action_type)

        modal.find('input').attr('disabled', 'disabled');
        if (type === 'current') {
            action_type === 'preventive_action' ? modal.find('.current_action_01 input').removeAttr('disabled') : modal.find('.current_action_02 input').removeAttr('disabled');
        } else {
            action_type === 'preventive_action' ? modal.find('.optimize_action_01 input').removeAttr('disabled') : modal.find('.optimize_action_02 input').removeAttr('disabled');
        }

        console.log(type)
    })
});