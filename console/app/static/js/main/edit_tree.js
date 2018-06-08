function doubleTreeLayout(diagram) {
    // Within this function override the definition of '$' from jQuery:
    var $$ = go.GraphObject.make;  // for conciseness in defining templates
    diagram.startTransaction("Double Tree Layout");

    // split the nodes and links into two Sets, depending on direction
    var leftParts = new go.Set(go.Part);
    var rightParts = new go.Set(go.Part);
    separatePartsByLayout(diagram, leftParts, rightParts);
    // but the ROOT node will be in both collections

    // create and perform two TreeLayouts, one in each direction,
    // without moving the ROOT node, on the different subsets of nodes and links
    var layout1 =
        $$(go.TreeLayout,
            {
                angle: 180,
                arrangement: go.TreeLayout.ArrangementFixedRoots,
                setsPortSpot: false
            });

    var layout2 =
        $$(go.TreeLayout,
            {
                angle: 0,
                arrangement: go.TreeLayout.ArrangementFixedRoots,
                setsPortSpot: false
            });

    layout1.doLayout(leftParts);
    layout2.doLayout(rightParts);

    diagram.commitTransaction("Double Tree Layout");
}

function separatePartsByLayout(diagram, leftParts, rightParts) {
    var root = diagram.findNodeForKey("Root");
    if (root === null) return;
    // the ROOT node is shared by both subtrees!
    leftParts.add(root);
    rightParts.add(root);
    // look at all of the immediate children of the ROOT node
    root.findTreeChildrenNodes().each(function (child) {
        // in what direction is this child growing?
        var dir = child.data.dir;
        var coll = (dir === "left") ? leftParts : rightParts;
        // add the whole subtree starting with this child node
        coll.addAll(child.findTreeParts());
        // and also add the link from the ROOT node to this child node
        coll.add(child.findTreeParentLink());
    });
}

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

                console.log(data);
                myDiagram.model = new go.TreeModel(data);
                doubleTreeLayout(myDiagram)
            } else
                toastr.error(resp.message)
        });
    });


    var $$ = go.GraphObject.make;

    var myDiagram =
        $$(go.Diagram, "edit-tree",
            {
                initialContentAlignment: go.Spot.Center
            });

    myDiagram.nodeTemplate =
        $$(go.Node, "Auto",
            $$(go.Shape, "RoundedRectangle", {strokeWidth: 1, fill: 'white'}, new go.Binding("stroke", "color")),
            $$(go.TextBlock, {margin: 8}, new go.Binding("text", "name"), new go.Binding("stroke", "color")),
            {
                click: function (e, obj) {

                    var node = obj.part.data;
                    if (node !== null) {
                        var type_name = node['type'];
                        var id = edit_tree_modal.find('[name="id"]').val();

                        $.post('/manage/edit/tree?product_id=' + product_id + '&type=' + type_name + '&id=' + id + '&is_show=true', '', function (resp) {
                            if (resp.success) {
                                var data = resp['data'];
                                console.log(data)
                                myDiagram.model = new go.TreeModel(data);
                                doubleTreeLayout(myDiagram)
                            } else
                                toastr.error(resp.message)
                        });
                    }
                }
            }
        );

    myDiagram.linkTemplate =
        $$(go.Link, {selectionAdorned: false},
            $$(go.Shape, {strokeWidth: 2, stroke: "#666"}, new go.Binding("stroke", "is_show", function (val) {
                return val ? '#666' : 'white';
            })))


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