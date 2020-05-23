# TODO: WRITE THE FORM ROUTING LOGIC
from .models import FormBlueprint, FormInstance
from workflows.models import Workflow, Node
from teams.models import TeamHasEmployees, Team
from employees.models import Role

def get_node_user(node, sender):
	# Returns the user assossitated with the given node and the sender

	# TODO: DEAL WITH MULTIPLE POSSIBLE USERS
	role = node.associated_role
	team = node.associated_team

	if role and team:
		# Both are present
		the_instance = TeamHasEmployees.objects.get(role = role, team = team)
		user = the_instance.employee
		return user
	elif team is None:
		# You just have the role, assume same team
		s_the = TeamHasEmployees.objects.get(employee = sender)
		s_team = s_the.team
		s_role = s_the.role

		d_team = s_team
		d_role = role
		if s_role.default_head:
			# If the sender is the head of its team, send it to parent team
			if s_team.parent is None:
				# Sender and do whatever they want, returns sender themself
				return sender
			d_team = s_team.parent

		d_the = TeamHasEmployees.objects.get(team = d_team, role = d_role)

		return d_the.employee

	else:
		# ERROR
		return None



def get_workflow_user_list(form_instance):
	# Returns the list of users in order for the workflow
	blueprint = form_instance.blueprint
	workflow = blueprint.workflow
	head = Workflow.objects.get(workflow = workflow, prev_node = None)

	og_sender = form_instance.sender
	user_list = [og_sender]

	cur_node = head

	while cur_node.next_node:
		cur_node = cur_node.next_node
		sender = user_list[-1]
		receiver = get_node_user(cur_node, sender)
		user_list.append(receiver)

	return user_list

