$(document).ready(function () {
    var $$ = go.GraphObject.make;
    var jqclass = $.jqclass;

    var myDiagram =
        $$(go.Diagram, "myDiagramFunc",
            {
                initialContentAlignment: go.Spot.Center,
                "undoManager.isEnabled": true,
                draggingTool: new NonRealtimeDraggingTool(),
                "draggingTool.isEnabled": false,
                layout: $$(go.TreeLayout,
                    {
                        angle: 90,
                        setsPortSpot: false,
                        setsChildPortSpot: false,
                        arrangement: go.TreeLayout.ArrangementVertical
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

    myDiagram.linkTemplateMap.add("FuncLink",
        $$(go.Link, {
                selectionAdorned: false,
                routing: go.Link.Orthogonal,
                corner: 10,
                fromSpot: new go.Spot(0, 0.5),
                toSpot: new go.Spot(0, 0.5)
            },
            $$(go.Shape, {strokeWidth: 2, stroke: "#666"})
        ));


    $.myDiagramFunc = myDiagram;
});