$(document).ready(function () {
    var $$ = go.GraphObject.make;

    var myDiagram =
        $$(go.Diagram, "temp",
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

    myDiagram.nodeTemplate =
        $$(go.Node, "Auto",
            $$(go.Shape, "RoundedRectangle", {strokeWidth: 1, fill: 'white'}),
            $$(go.TextBlock, {margin: 8}, new go.Binding("text", "name")),
            {
                toolTip: $$(go.Adornment, "Auto",
                    $$(go.Shape, {fill: '#FFFFCC', stroke: "#ddd"}),
                    $$(go.TextBlock, {margin: 8}, new go.Binding("text", "name_number", function (val) {
                        return val ? '编号: ' + val : '---'
                    }))
                )
            }
        );

    myDiagram.linkTemplate =
        $$(go.Link, {selectionAdorned: false},
            $$(go.Shape, {strokeWidth: 2, stroke: "#666"}),
            $$(go.Shape, {fill: '#666', stroke: null, toArrow: "Standard", segmentFraction: 0})
        );


    var get_temp_tree = function () {
        $.get('/temps/view/info/' + temp_id).done(function (resp) {
            if (resp.success) {
                var data = resp['data'];
                var nodedata = data['nodedata'];
                console.log(nodedata);
                var linkdata = data['linkdata'];
                myDiagram.model = new go.GraphLinksModel(nodedata, linkdata);
            } else
                toastr.error(resp.message)
        });
    };

    get_temp_tree();
});

