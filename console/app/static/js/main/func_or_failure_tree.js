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
                    var node = obj.part.adornedPart;
                    var thisemp = node.data;

                    var type = thisemp['category'];
                    var name_number = thisemp['name_number'];
                    var type_name = (type === "FuncNode") ? 'func' : 'failure';

                    $.get('/tree/attr?product_id=' + product_id + '&type_name=' + type_name + '&name_number=' + name_number, function (resp) {
                        console.log(resp);
                        var data = resp['data'];
                        var content = resp['content'];
                        $.attr_html(data, '', name_number, type_name, content);

                    });
                    // if (product_id) {
                    // action = $.getUrlParam('action');
                    // if (action !== 'edit_attr')
                    //     window.location.href = window.location.href + '?action=edit_attr'
                    // }

                }),
            makeButton("新增失效",
                function (e, obj) {
                    var node = obj.part.adornedPart;
                    if (node !== null) {
                        var thisemp = node.data;
                        var func_id = thisemp['key'];
                        var product_relation_id = thisemp['product_relation_id'];
                    }
                    console.log(thisemp);
                    var add_process = $("#add-process");
                    var add_content = $("#add-content");
                    jqclass.show_modal(add_process, $(this));

                     // tree 参数 product_relation_id-， parent_id -， level
                    add_content.find('[name="parent_id"]').val(func_id);
                    add_content.find('[name="product_relation_id"]').val(product_relation_id);
                    add_content.find('[name="level"]').val('');
                })
        );


    var failureContextMenu =
        $$(go.Adornment, "Vertical",
            makeButton("编辑属性",
                function (e, obj) {


                }),
            makeButton("编辑评估",
                function (e, obj) {
                    var node = obj.part.adornedPart;
                    if (node !== null) {
                        var thisemp = node.data;
                    }
                    var add_process = $("#add-process");
                    jqclass.show_modal(add_process, $(this));
                    add_process.find('[name="level"]').val(-1);
                })
        );

    myDiagram.nodeTemplateMap.add("FuncNode",
        $$(go.Node, "Auto",
            $$(go.Shape, "RoundedRectangle", {strokeWidth: 1, fill: 'white', stroke: "green"}),
            $$(go.TextBlock, {margin: 8, stroke: "green"}, new go.Binding("text", "name")),
            {
                toolTip: $$(go.Adornment, "Auto",
                    $$(go.Shape, {fill: '#FFFFCC', stroke: "#ddd"}),
                    $$(go.TextBlock, {margin: 8}, new go.Binding("text", "name_number", function (val) {
                        return val ? '编号: ' + val : '---'
                    }))
                )
            },
            {
                contextMenu: partContextMenu
            }
        ));

    myDiagram.nodeTemplateMap.add("FailureNode",
        $$(go.Node, "Auto",
            $$(go.Shape, "RoundedRectangle", {strokeWidth: 1, fill: 'white', stroke: "red"}),
            $$(go.TextBlock, {margin: 8, stroke: "red"}, new go.Binding("text", "name")),
            {
                toolTip: $$(go.Adornment, "Auto",
                    $$(go.Shape, {fill: '#FFFFCC', stroke: "#ddd"}),
                    $$(go.TextBlock, {margin: 8}, new go.Binding("text", "name_number", function (val) {
                        return val ? '编号: ' + val : '---'
                    }))
                )
            },
            {
                contextMenu: failureContextMenu
            }
        ));

    // myDiagram.linkTemplateMap.add("FuncLink",
    //     $$(go.Link, {
    //             selectionAdorned: false,
    //             routing: go.Link.Orthogonal,
    //             corner: 10,
    //             fromSpot: new go.Spot(0, 0.5),
    //             toSpot: new go.Spot(0, 0.5)
    //         },
    //         $$(go.Shape, {strokeWidth: 2, stroke: "#666"})
    //     ));

    myDiagram.linkTemplateMap.add("FailureLink",
        $$(go.Link, {selectionAdorned: false},
            $$(go.Shape, {strokeWidth: 2, stroke: "#666"}),
            $$(go.Shape, {fill: '#666', stroke: null, toArrow: "Standard", segmentFraction: 0})
        ));


    // $.myDiagramFunc = myDiagram;

    $.get_func_or_failure_tree = function (relation_id) {
        $.get('/file/func/failure/tree?product_relation_id=' + relation_id).done(function (resp) {
            if (resp.success) {
                var data = resp['data'];
                var nodedata = data['nodedata'];
                var linkdata = data['linkdata'];
                myDiagram.model = new go.GraphLinksModel(nodedata, linkdata);
            } else
                toastr.error(resp.message)
        });
    };

});