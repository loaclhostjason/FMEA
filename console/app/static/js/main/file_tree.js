$(document).ready(function () {
    var $$ = go.GraphObject.make;
    var jqclass = $.jqclass;

    var myDiagram =
        $$(go.Diagram, "myDiagramStructure",
            {
                initialContentAlignment: go.Spot.Center,
                "undoManager.isEnabled": true,
                draggingTool: new NonRealtimeDraggingTool(),
                "draggingTool.isEnabled": false,
                layout: $$(go.TreeLayout,
                    {
                        setsPortSpot: false,
                        setsChildPortSpot: false,
                        arrangement: go.TreeLayout.ArrangementHorizontal
                    }
                )
            });

    function makeButton(text, action, visiblePredicate) {
        return $$("ContextMenuButton",
            $$(go.TextBlock, text),
            {click: action},
            visiblePredicate ? new go.Binding("visible", "", function (o, e) {
                return o.diagram ? visiblePredicate(o, e) : false;
            }).ofObject() : {});
    }

    var partContextMenu =
        $$(go.Adornment, "Vertical",
            makeButton("编辑属性",
                function (e, obj) {
                    if (product_id) {
                        action = $.getUrlParam('action');
                        if (action !== 'edit_attr')
                            window.location.href = window.location.href + '?action=edit_attr'
                    }

                }),
            makeButton("新增过程",
                function (e, obj) {
                    var node = obj.part.adornedPart;
                    if (node !== null) {
                        var thisemp = node.data;
                        var parent_id = thisemp['key'];
                        var level = thisemp['level'];
                    }
                    var add_process = $("#add-process");
                    var add_content = $("#add-content");
                    jqclass.show_modal(add_process, $(this));
                    add_content.find('[name="parent_id"]').val(parent_id);
                    add_content.find('[name="level"]').val(level);
                })
        );

    myDiagram.nodeTemplate =
        $$(go.Node, "Auto",
            $$(go.Shape, "RoundedRectangle", {strokeWidth: 1, fill: 'white'}),
            $$(go.TextBlock, {margin: 8}, new go.Binding("text", "name")),
            {
                contextMenu: partContextMenu
            }
        );

    myDiagram.linkTemplate =
        $$(go.Link, {selectionAdorned: false},
            $$(go.Shape, {strokeWidth: 2, stroke: "#666"}),
            $$(go.Shape, {fill: '#666', stroke: null, toArrow: "Standard", segmentFraction: 0})
        );

    if (product_id)
        $.get('/file/tree?product_id=' + product_id).done(function (resp) {
            if (resp.success) {
                var data = resp['data'];
                var nodedata = data['nodedata'];
                var linkdata = data['linkdata'];
                myDiagram.model = new go.GraphLinksModel(nodedata, linkdata);
            } else
                toastr.error(resp.message)
        });


});