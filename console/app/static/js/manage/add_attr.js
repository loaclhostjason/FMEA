$(document).ready(function () {
    var html_tr = '';

    html_tr += '<tr>';
    html_tr += '<td><input name="field" class="td-input" required/></td>';
    html_tr += '<td><input name="field_zh" class="td-input" required/></td>';
    html_tr += '<td><input name="required" type="checkbox" class="td-input" value="y"/></td>';
    html_tr += '<td><a href="javascript:void(0);" class="td-remove">移除</a></td>';

    html_tr += '</tr>';


    $('.td-add').click(function () {
        $(this).parents('tr').before(html_tr);
    });
    $(document).on('click', '.td-remove', function () {
        $(this).parents('tr').remove();
    });


});