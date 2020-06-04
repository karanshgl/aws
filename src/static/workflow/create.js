$(document).ready(function() {

    var template = $("#cloneIt");
    const template_clone = template.clone();
    //console.log(template)
	// Base Variables
    var node_count = 1;
    var headNode = "div[id='node_1_head'";
    var baseTitle = ".card-title";
    var baseInputRole = "select[name='node_1_role'";
    var baseInputTeam = "select[name='node_1_team'";
    var baseInputRoleId = "select[id='node_1_role'";
    var baseInputTeamId = "select[id='node_1_team'";
    // Format function
    String.prototype.format = String.prototype.f = function() {
        var s = this,
            i = arguments.length;

        while (i--) {
            s = s.replace(new RegExp('\\{' + i + '\\}', 'gm'), arguments[i]);
        }
        return s;
    };


    $("#node_1_role").select2({  //giving searchable feature to dropdown

    });
    $("#node_1_team").select2({

    });

    $("#btnAddNode").click(function() {
        // Increase the node count


        node_count = node_count + 1;


        var new_node = template_clone.clone();

        // Update the template
        // console.log(node_count)
        new_node.find(baseTitle).text("Node {0}".f(node_count));
        new_node.find(baseInputRole).attr("name", "node_{0}_role".f(node_count));
        //new_node.find(baseInputRole).attr("class", "");
        new_node.find(baseInputTeam).attr("name", "node_{0}_team".f(node_count));
        new_node.find(headNode).attr("id", "node_{0}_head".f(node_count));
        new_node.find(headNode).attr("name", "node_{0}_head".f(node_count));
        new_node.find(baseInputRoleId).attr("id", "node_{0}_role".f(node_count));
        new_node.find(baseInputTeamId).attr("id", "node_{0}_team".f(node_count));

        $("#node_list").append(new_node);
        //$("#node_{0}_role".f(node_count)).select2('enable');
        $("#node_{0}_role".f(node_count)).select2({

        });
        $("#node_{0}_team".f(node_count)).select2({

        });
        //console.log(new_node);
        populate_dropdown(node_count, 'role');
        populate_dropdown(node_count, 'team');

    });

    $("#btnSubmit").click(function() {
    	var form = $("#workflow_form");
    	var hidden_input = "<input type = 'hidden' name = 'count' value = '{0}'>".f(node_count);
    	form.append(hidden_input).submit();
    });

    $("#btnDeleteNode").click(function() {
      if(node_count > 1){
        $("#node_{0}_head".f(node_count)).remove();
        node_count = node_count - 1;
      }
    });

    populate_dropdown(1, 'role');
    populate_dropdown(1, 'team');


    $("[id=node_list]").on('change', "[id^=node_][id$=_role]",function() {
        var node_id = $(this)[0].id;
        var role_name = $(this).val().replace(/ /g, "-");
        var url = "http://127.0.0.1:8000/forms/api/teams_have_role/" + role_name + "/teams/";
        var teams = [];
        var node_select_id = node_id.replace("role", "team");
        var options = '<option value="None">None</option>';

        var selected_team = $("select#{0}".format(node_select_id)).val();

        $.ajax({url: url, success: function(result){
            $.each(result, function (index, value) {
                teams.push(value.team);
            });
            for (var i = 0; i < teams.length; i++) {
                options += '<option value="' + teams[i] + '">' + teams[i] + '</option>';
            }
            $("select#{0}".format(node_select_id)).html(options);
            $("select#{0}".format(node_select_id)).val(selected_team);
        }});
    });

    $("[id=node_list]").on('change', "[id^=node_][id$=_team]",function() {
        var node_id = $(this)[0].id;
        var team_name = $(this).val().replace(/ /g, "-");
        var url = "http://127.0.0.1:8000/forms/api/roles_in_team/" + team_name + "/roles/";
        var roles = [];
        var node_select_id = node_id.replace("team", "role");
        var options = '<option value="None">None</option>';

        var selected_role = $("select#{0}".format(node_select_id)).val();

        $.ajax({url: url, success: function(result){
            $.each(result, function (index, value) {
                roles.push(value.role);
            });
            for (var i = 0; i < roles.length; i++) {
                options += '<option value="' + roles[i] + '">' + roles[i] + '</option>';
            }
            $("select#{0}".format(node_select_id)).html(options)
            $("select#{0}".format(node_select_id)).val(selected_role);
        }});
    });
});

function populate_dropdown(node_id, list_name) {
    let dropdown = $('select#node_{0}_{1}'.format(node_id,list_name));
    dropdown.empty();
    dropdown.append('<option selected="true" disabled>Choose {0}</option>'.format(list_name));
    dropdown.prop('selectedIndex', 0);

    const role_api_url = 'http://127.0.0.1:8000/forms/api/roles_in_team/None/roles/';
    const team_api_url = 'http://127.0.0.1:8000/forms/api/teams_have_role/None/teams/';

    if(list_name === 'role'){
        $.ajax({url: role_api_url, success: function(result){
            $.each(result, function (index, value) {
                dropdown.append($('<option></option>').attr('value', value.role).text(value.role));
            });
        }});
    }
    else{
        $.ajax({url: team_api_url, success: function(result){
            $.each(result, function (index, value) {
                dropdown.append($('<option></option>').attr('value', value.team).text(value.team));
            });
        }});
    }
}
