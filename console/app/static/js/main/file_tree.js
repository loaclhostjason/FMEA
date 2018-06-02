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
                    add_process.find('[name="level"]').val(level);
                })
        );

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
            },
            {
                click: function (e, obj) {
                    var node = obj.part.data;
                    if (node !== null) {
                        var product_relation_id = node['key'];
                        $.get_func_or_failure_tree('func', product_relation_id);

                    }

                }
            },
            {
                contextMenu: partContextMenu
            }
        );

    myDiagram.linkTemplate =
        $$(go.Link, {selectionAdorned: false},
            $$(go.Shape, {strokeWidth: 2, stroke: "#666"}),
            $$(go.Shape, {fill: '#666', stroke: null, toArrow: "Standard", segmentFraction: 0})
        );

    $.get_tree = function (product_id) {
        $.get('/file/tree?product_id=' + product_id).done(function (resp) {
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

    if (product_id)
        $.get_tree(product_id)

});


$(document).ready(function () {
    var add_process = $("#add-process");
    add_process.on('hide.bs.modal', function () {
        $(this).find('input').val("");
    });
    add_process.on('show.bs.modal', function () {
        var modal = $(this);
        $.get('/process', function (resp) {

            var data = resp['data'];
            var level = modal.find('input').val();
            level = Number(level);
            console.log(data);
            get_process_table(data, level);

        })
    });


    function get_process_table(data, level) {
        var process_table = $('.table-process tbody');
        var html = '';

        // console.log(data);
        data.forEach(function (info) {
            for (var key in info) {

                html += '<tr><td>' + info[key]['name_zh'] + '</td>';
                html += '<td>';
                info[key]['content'].forEach(function (value) {
                    switch (key) {
                        case "functional_analysis":
                            if ($.inArray(level, value['show_level']) > -1) {
                                html += '<div><label data-type="func" class="label-border text-center show-content" style="width: 125px;cursor: pointer">' + value['name_zh'] + '</label></div>';
                            } else
                                html += '<div><label data-type="failure" class="label-border text-center disabled" style="width: 125px;cursor: pointer">' + value['name_zh'] + '</label></div>';

                            break;
                        case "failure_analysis":
                            if ($.inArray(level, value['show_level']) > -1) {
                                html += '<div><label data-type="failure" class="label-border text-center show-content" style="width: 125px;cursor: pointer">' + value['name_zh'] + '</label></div>';
                            } else
                                html += '<div><label data-type="failure" class="label-border text-center disabled" style="width: 125px;cursor: pointer">' + value['name_zh'] + '</label></div>';

                            break;
                        default:
                            if ($.inArray(level, value['show_level']) > -1)
                                html += '<div><label class="label-border text-center show-content" style="width: 125px;cursor: pointer">' + value['name_zh'] + '</label></div>';
                            else
                                html += '<div><label class="label-border text-center disabled" style="width: 125px;cursor: pointer">' + value['name_zh'] + '</label></div>';

                    }

                });
                html += '</td></tr>';
            }
        });
        process_table.html(html);

    }
});