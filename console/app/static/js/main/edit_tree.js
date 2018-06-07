$(document).ready(function () {

    var edit_tree_modal = $("#edit-tree-modal");
    $(document).on('click', '.show-edit-tree', function () {
        $.jqclass.show_modal(edit_tree_modal, $(this));
        edit_tree_modal.find('.modal-title').text($(this).data('message'));
    });
    // edit_tree_modal.on('hide.bs.modal', function () {
    //     $(this).find('input').val('');
    // });

    edit_tree_modal.on('shown.bs.modal', function () {
        var type_name = $(this).find('.modal-title').text() === '编辑功能网' ? 'func' : 'failure';
        var id = $(this).find('[name="id"]').val();

        $.get('/manage/edit/tree?product_id=' + product_id + '&type=' + type_name + '&id=' + id).done(function (resp) {
            if (resp.success) {
                var data = resp['data'];
                var nodedata = data['nodedata'];
                console.log(nodedata);
                var linkdata = data['linkdata'];
                myDiagram.model = new go.GraphLinksModel(nodedata, linkdata);
            } else
                toastr.error(resp.message)
        });
    });


    var $$ = go.GraphObject.make;

    var myDiagram =
        $$(go.Diagram, "edit-tree",
            {
                initialContentAlignment: go.Spot.Center,
                "undoManager.isEnabled": true,
                draggingTool: new NonRealtimeDraggingTool(),
                "draggingTool.isEnabled": false,
                // layout: $$(go.TreeLayout,
                //     {
                //         setsPortSpot: false,
                //         setsChildPortSpot: false,
                //         arrangement: go.TreeLayout.ArrangementHorizontal
                //     }
                // )
            });

    myDiagram.nodeTemplateMap.add("ParentNode",
        $$(go.Node, "Auto",
            $$(go.Shape, "RoundedRectangle", {strokeWidth: 1, fill: 'white'}, new go.Binding("stroke", "color")),
            $$(go.TextBlock, {margin: 8}, new go.Binding("text", "name"), new go.Binding("stroke", "color")),
            {
                click: function (e, obj) {

                }
            }
        ));

    myDiagram.nodeTemplateMap.add("SelfNode",
        $$(go.Node, "Auto",
            $$(go.Shape, "RoundedRectangle", {strokeWidth: 1, fill: 'white'}, new go.Binding("stroke", "color")),
            $$(go.TextBlock, {margin: 8}, new go.Binding("text", "name"), new go.Binding("stroke", "color")),
            {
                click: function (e, obj) {

                }
            }
        ));

    myDiagram.nodeTemplateMap.add("ChilrenNode",
        $$(go.Node, "Auto",
            $$(go.Shape, "RoundedRectangle", {strokeWidth: 1, fill: 'white'}, new go.Binding("stroke", "color")),
            $$(go.TextBlock, {margin: 8}, new go.Binding("text", "name"), new go.Binding("stroke", "color")),
            {
                click: function (e, obj) {

                }
            }
        ));


    myDiagram.linkTemplate =
        $$(go.Link, {selectionAdorned: false},
            $$(go.Shape, {strokeWidth: 2, stroke: "#666"}),
            $$(go.Shape, {fill: '#666', stroke: null, toArrow: "Standard", segmentFraction: 0}));


});


$(document).ready(function () {
    var update_name = $('#update-name-modal');
    update_name.on('hide.bs.modal', function () {
        $(this).find('form')[0].reset();
    });

    update_name.find('.submit_update_name').click(function () {
        var params = update_name.find('form').serialize();
        $.post('/tree/edit/name', params, function (resp) {
            if (resp.success) {
                toastr.success(resp.message);
                resp['product_relation_id'] ? $.get_func_or_failure_tree(resp['product_relation_id']) : $.get_tree(product_id);
                update_name.modal('hide');
            } else {
                toastr.error(resp.message)
            }
        })
    })
});