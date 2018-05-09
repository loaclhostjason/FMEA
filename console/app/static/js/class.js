$(document).ready(function () {
    function ProductClass() {
        this.show_modal = function (dom, btn) {
            dom.modal({
                backdrop: "static"
            }, btn);
        };
    }

    $.product_class = new ProductClass();
});