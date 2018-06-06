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
                    var node = obj.part.adornedPart;
                    if (node !== null) {
                        var thisemp = node.data;
                        var level = thisemp['level'] - 1;
                        var name_number = thisemp['name_number'];
                        console.log(thisemp)
                    }
                    $.get('/tree/attr?product_id=' + product_id + '&level=' + level + '&name_number=' + name_number, function (resp) {
                        console.log(resp);
                        if (resp.success) {
                            var data = resp['data'];
                            var content = resp['content'];
                            $.attr_html(data, level, name_number, 'structure', content);
                        } else {
                            toastr.error(resp.messgae)
                        }


                    });
                    // alert(level)

                }),
            makeButton("新增过程",
                function (e, obj) {
                    var node = obj.part.adornedPart;
                    if (node !== null) {
                        var thisemp = node.data;
                        var key = thisemp['key'];
                        var level = thisemp['level'];
                    }
                    var add_process = $("#add-process");
                    var add_content = $("#add-content");
                    jqclass.show_modal(add_process, $(this));

                    console.log(thisemp);

                    // 添加 process level 1，2，3
                    add_process.find('[name="level"]').val(level);

                    // tree 参数 product_relation_id， parent_id-， level-
                    add_content.find('[name="product_relation_id"]').val(key);
                    add_content.find('[name="parent_id"]').val(key);
                    add_content.find('[name="level"]').val(level);

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
                        $.get_func_or_failure_tree(product_relation_id);

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
        $.get_tree(product_id);

    function required_html(required) {
        var html = '';
        if (required)
            html = '<span class="text-danger">*</span>';
        return html

    }

    function required_input(field, required, content) {
        var html = '<input class="form-control pull-left" name="' + field + '" type="text" value="' + (content ? content[field] : "") + '">';
        if (required)
            html = '<input class="form-control pull-left" name="' + field + '" type="text" value="' + (content ? content[field] : "") + '" required>';

        return html

    }

    $.attr_html = function (data, level, name_number, type, content) {
        var attr_form = $('#attr-form');
        if (!data || !data.length) {
            attr_form.html('');
            return false
        }
        var form_html = '';

        form_html += '<input name="level" type="hidden" value="' + level + '">';
        form_html += '<input name="type_name" type="hidden" value="' + type + '">';
        form_html += '<input name="name_number" type="hidden" value="' + name_number + '">';

        data.forEach(function (value) {
            form_html += '<div class="form-group">';
            form_html += '<div class="col-sm-2"><label class="control-label pull-right">' + required_html(value['required']) + value['field_zh'] + '</label></div>';
            form_html += '<div class="col-sm-8">' + required_input(value['field'], value['required'], content) + '</div>';
            form_html += '</div>';
        });
        form_html += '<div class="form-group"><div class="col-sm-2"><button type="button" class="btn btn-primary submit-add-attr">保存</button></div></div>';
        attr_form.html(form_html);

    };

    $(document).on('click', '.submit-add-attr', function () {
        var form_data = $('form#attr-form').serialize();
        $.post('/manage/attr/content/add?product_id=' + product_id, form_data, function (resp) {
            if (resp.success) {
                toastr.success(resp['message'])
            } else
                toastr.error(resp['message'])
        })
    })

});

//
// process  html
//

$(document).ready(function () {
    function content_html(content) {
        var html = '';
        if (!content || !content.length) {
            return html
        }
        content.forEach(function (value) {
            html += '<div></i><label class="label-border-default add-action" style="width: 125px;cursor: pointer"><i class="glyphicon glyphicon-triangle-right"></i>' + value['name_zh'] + '</label></div>'
        });
        return html
    }

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
                var id = info[key]['id'];

                html += '<tr><td>' + info[key]['name_zh'] + '</td>';
                html += '<td>';
                info[key]['content'].forEach(function (value) {
                    switch (key) {
                        case "functional_analysis":
                            html += '<div><a class="label-a" href="javascript:void(0)">';
                            if ($.inArray(level, value['show_level']) > -1) {
                                html += '<label data-type="func" class="label-border text-center show-content" style="width: 125px;cursor: pointer">';
                            } else
                                html += '<label data-type="failure" class="label-border text-center disabled" style="width: 125px;cursor: pointer">';

                            html += value['name_zh'] + '</label></a></div>';

                            break;
                        case "failure_analysis":
                            html += '<div><a class="label-a" href="javascript:void(0)">';
                            if ($.inArray(level, value['show_level']) > -1) {
                                html += '<label data-type="failure" class="label-border text-center show-content" style="width: 125px;cursor: pointer">';
                            } else
                                html += '<label data-type="failure" class="label-border text-center disabled" style="width: 125px;cursor: pointer">';

                            html += value['name_zh'] + '</label></a></div>';
                            break;

                        case 'current_action':
                            html += '<div>';
                            if ($.inArray(level, value['show_level']) > -1) {
                                html += '<a class="label-a" data-toggle="collapse" data-parent="#accordion" href="#' + id + '_' + value['name'] + '">';
                                html += '<label class="label-border text-center" style="width: 125px;cursor: pointer">';
                            }
                            else {
                                html += '<a class="label-a" data-toggle="collapse" data-parent="#accordion" href="#' + id + '_' + value['name'] + '">';
                                html += '<label class="label-border text-center disabled" style="width: 125px;cursor: pointer">';
                            }

                            html += value['name_zh'] + '</label></a></div>';
                            html += '<div id="' + id + '_' + value['name'] + '" class="panel-collapse collapse">' + content_html(value['content']) + '</div>';

                            break;

                        case 'optimize_action':
                            html += '<div>';
                            if ($.inArray(level, value['show_level']) > -1) {
                                html += '<a class="label-a" data-toggle="collapse" data-parent="#accordion" href="#' + id + '_' + value['name'] + '">';
                                html += '<label class="label-border text-center" style="width: 125px;cursor: pointer">';
                            }
                            else {
                                html += '<a class="label-a" data-toggle="collapse" data-parent="#accordion" href="#' + id + '_' + value['name'] + '">';
                                html += '<label class="label-border text-center disabled" style="width: 125px;cursor: pointer">';
                            }

                            html += value['name_zh'] + '</label></a></div>';
                            html += '<div id="' + id + '_' + value['name'] + '" class="panel-collapse collapse">' + content_html(value['content']) + '</div>';

                            break;

                        default:
                            html += '<div><a class="label-a" href="javascript:void(0)">';
                            if ($.inArray(level, value['show_level']) > -1)
                                html += '<label class="label-border text-center show-content" style="width: 125px;cursor: pointer">';
                            else
                                html += '<label class="label-border text-center disabled" style="width: 125px;cursor: pointer">';

                            html += value['name_zh'] + '</a></div>';
                    }

                });
                html += '</td></tr>';
            }
        });
        process_table.html(html);

    }
});


//
$(document).ready(function () {
    var action_modal = $('#action_modal');
    $(document).on('click', '.add-action', function () {
        $.jqclass.show_modal(action_modal, $(this));
        var text = $(this).parents('.panel-collapse').prev().find('label').text();
        action_modal.find('.modal-title').text(text);

    });
});