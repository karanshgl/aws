$(document).ready(function() {


	// Base Variables
    var node_count = 1;
    var baseTitle = ".card-title";
    var baseInputRole = "input[name='node_1_role'";
    var baseInputTeam = "input[name='node_1_team'";

    // Format function
    String.prototype.format = String.prototype.f = function() {
        var s = this,
            i = arguments.length;

        while (i--) {
            s = s.replace(new RegExp('\\{' + i + '\\}', 'gm'), arguments[i]);
        }
        return s;
    };


    $("#btnAddNode").click(function() {
        // Increase the node count
        node_count = node_count + 1;

        var template = $("#headNode");
        var new_node = template.clone();

        // Update the template
        new_node.find(baseTitle).text("Node {0}".f(node_count));
        new_node.find(baseInputRole).attr("name", "node_{0}_role".f(node_count));
        new_node.find(baseInputTeam).attr("name", "node_{0}_team".f(node_count));

        $("#node_list").append(new_node);

        console.log(new_node);

    });

    $("#btnSubmit").click(function() {
    	var form = $("#workflow_form");
    	var hidden_input = "<input type = 'hidden' name = 'count' value = '{0}'>".f(node_count);
    	form.append(hidden_input).submit();
    });
});