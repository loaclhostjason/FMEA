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
                        angle: 90,
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
            makeButton("新增失效",
                function (e, obj) {
                    var node = obj.part.adornedPart;
                    if (node !== null) {
                        var thisemp = node.data;
                        var parent_id = thisemp['key'];
                        var product_relation_id = thisemp['product_relation_id'];
                    }
                    console.log(thisemp);
                    var add_process = $("#add-process");
                    var add_content = $("#add-content");
                    jqclass.show_modal(add_process, $(this));

                    // tree 参数 product_relation_id-， parent_id -， level
                    add_content.find('[name="parent_id"]').val(parent_id);
                    add_content.find('[name="product_relation_id"]').val(product_relation_id);
                    add_content.find('[name="level"]').val(-1);

                    add_process.find('[name="level"]').val(-1);

                    var action_modal = $("#action_modal");
                    action_modal.find('[name="name_number"]').val(thisemp['name_number']);
                }),
            makeButton('修改名称', function (e, obj) {
                var node = obj.part.adornedPart;
                if (node !== null) {
                    var thisemp = node.data;
                    var id = thisemp['key'];
                }
                var update_name = $('#update-name-modal');
                $.jqclass.show_modal(update_name);
                update_name.find('[name="id"]').val(id);
                update_name.find('[name="type"]').val('func');
            }),
            makeButton('复制', function (e, obj) {
                var node = obj.part.adornedPart;
                if (node !== null) {
                    var thisemp = node.data;
                    var key = thisemp['key'];
                    var name = thisemp['name'];
                    var product_relation_id = thisemp['product_relation_id'];
                }
                console.log(thisemp);
                if (key) {
                    var params = {
                        'parent_id': null,
                        'level': -1,
                        'content': name,
                        'product_relation_id': product_relation_id,
                        'type': 'func'
                    };
                    $.post('/file/tree/content/add/' + product_id + '?action=copy&key=' + key, params, function (resp) {
                        if (resp.success) {
                            toastr.success('复制成功');
                            $.get_func_or_failure_tree(product_relation_id);
                        } else {
                            toastr.error(resp.message || 'error: func Tree')
                        }
                    })
                }
            }),
            makeButton('删除', function (e, obj) {
                var node = obj.part.adornedPart;
                if (node !== null) {
                    var thisemp = node.data;
                    var id = thisemp['key'];
                }
                if (id) {
                    $.post('/tree/delete/' + id + '?type=func', '', function (resp) {
                        if (resp.success) {
                            toastr.success(resp.message);
                            var product_relation_id = resp ['product_relation_id'];
                            $.get_func_or_failure_tree(product_relation_id);
                        } else {
                            toastr.error(resp.message)
                        }
                    })
                }
            })
        );


    var failureContextMenu =
        $$(go.Adornment, "Vertical",
            makeButton("编辑评估",
                function (e, obj) {
                    var node = obj.part.adornedPart;
                    if (node !== null) {
                        var thisemp = node.data;
                    }
                    $.g_name_number = thisemp['name_number'];
                    var add_process = $("#add-process");
                    jqclass.show_modal(add_process, $(this));
                    add_process.find('[name="level"]').val(-2);

                    var action_modal = $("#action_modal");
                    action_modal.find('[name="name_number"]').val(thisemp['name_number']);
                }),
            makeButton('修改名称', function (e, obj) {
                var node = obj.part.adornedPart;
                if (node !== null) {
                    var thisemp = node.data;
                    var id = thisemp['key'];
                }
                var update_name = $('#update-name-modal');
                $.jqclass.show_modal(update_name);
                update_name.find('[name="id"]').val(id);
                update_name.find('[name="type"]').val('failure');
            }),
            makeButton('复制', function (e, obj) {
                var node = obj.part.adornedPart;
                if (node !== null) {
                    var thisemp = node.data;
                    var key = thisemp['key'];
                    var name = thisemp['name'];
                    var product_relation_id = thisemp['product_relation_id'];
                }
                console.log(thisemp);
                if (key) {
                    var params = {
                        'level': -2,
                        'content': name,
                        'product_relation_id': product_relation_id,
                        'type': 'failure'
                    };
                    $.post('/file/tree/content/add/' + product_id + '?key=' + key, params, function (resp) {
                        if (resp.success) {
                            toastr.success('复制成功');
                            $.get_func_or_failure_tree(product_relation_id);
                        } else {
                            toastr.error(resp.message || 'error: failure Tree')
                        }
                    })
                }
            }),
            makeButton('删除', function (e, obj) {
                var node = obj.part.adornedPart;
                if (node !== null) {
                    var thisemp = node.data;
                    var id = thisemp['key'];
                }
                if (id) {
                    $.post('/tree/delete/' + id + '?type=failure', '', function (resp) {
                        if (resp.success) {
                            toastr.success(resp.message);
                            var product_relation_id = resp ['product_relation_id'];
                            $.get_func_or_failure_tree(product_relation_id);
                        } else {
                            toastr.error(resp.message)
                        }
                    })
                }
            })
        );

    myDiagram.nodeTemplateMap.add("ProductNode",
        $$(go.Node, "Auto",
            $$(go.Shape, "RoundedRectangle", {strokeWidth: 1, fill: 'white'}),
            $$(go.TextBlock, {margin: 8}, new go.Binding("text", "name")),
            {
                click: function (e, obj) {
                    var node = obj.part.data;
                    var level = node['level'];
                    var name_number = node['name_number'];

                    $.get('/tree/attr?product_id=' + product_id + '&level=' + level + '&name_number=' + name_number, function (resp) {
                        if (resp.success) {
                            var data = resp['data'];
                            var content = resp['content'];
                            $.attr_html(data, level, name_number, 'structure', content);
                        } else {
                            toastr.error(resp.messgae)
                        }


                    });

                }
            },
            {
                toolTip: $$(go.Adornment, "Auto",
                    $$(go.Shape, {fill: '#FFFFCC', stroke: "#ddd"}),
                    $$(go.TextBlock, {margin: 8}, new go.Binding("text", "name_number", function (val) {
                        return val ? '编号: ' + val : '---'
                    }))
                )
            }
        ));

    myDiagram.nodeTemplateMap.add("FuncNode",
        $$(go.Node, "Auto",
            $$(go.Shape, "RoundedRectangle", {strokeWidth: 1, fill: 'white', stroke: "green"}),
            $$(go.TextBlock, {margin: 8, stroke: "green"}, new go.Binding("text", "name")),
            {
                click: function (e, obj) {
                    var node = obj.part.data;
                    var name_number = node['name_number'];

                    $.get('/tree/attr?product_id=' + product_id + '&type_name=func' + '&name_number=' + name_number, function (resp) {
                        console.log(resp);
                        var data = resp['data'];
                        var content = resp['content'];
                        $.attr_html(data, -1, name_number, 'func', content);

                    });

                }
            },
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
                click: function (e, obj) {
                    var node = obj.part.data;
                    var name_number = node['name_number'];
                    $.attr_html('', -2, name_number, 'failure', '');

                    // $.get('/tree/attr?product_id=' + product_id + '&type_name=failure' + '&name_number=' + name_number, function (resp) {
                    //     console.log(resp);
                    //     var data = resp['data'];
                    //     var content = resp['content'];
                    //     $.attr_html(data, -2, name_number, 'failure', content);
                    //
                    // });

                }
            },
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

    myDiagram.linkTemplateMap.add("ProductLink",
        $$(go.Link, {selectionAdorned: false},
            $$(go.Shape, {strokeWidth: 2, stroke: "#666"})
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