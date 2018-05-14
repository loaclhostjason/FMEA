function JClass() {
    this.show_modal = function (dom, btn) {
        dom.modal({
            backdrop: "static"
        }, btn);
    };
}


JClass.prototype.get_chk = function (name) {
    var chk_value = [];
    $('input[name="' + name + '"]:checked').each(function () {
        chk_value.push($(this).val());
    });
    return chk_value;
};

JClass.prototype.get_no_checked_chk = function (name) {
    var chk_value = [];
    $('input[name="' + name + '"]').each(function () {
        chk_value.push($(this).val());
    });
    return chk_value;
};


$(document).ready(function () {
    $.jqclass = new JClass();
});