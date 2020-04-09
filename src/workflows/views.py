from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db import transaction
import collections

# GET MODELS
from .models import Workflow, Node
from employees.models import Role, Profile
from teams.models import Team



# Create your views here.
@login_required
def create_workflow(request):
	if request.method == 'POST':
		form_data = request.POST
		print(form_data)
		form_values_list = list(form_data.values())
		values_length = len(form_values_list)

		# CREATING DICT FOR ROLE-TEAM PAIR
		roles = []
		teams = []
		j = 2
		while j < (values_length - 1):
			if (j % 2) == 0:
				roles.append(form_values_list[j])
			else:
				teams.append(form_values_list[j])
			j += 1

		merged_list = tuple(zip(roles, teams))
		nested_merged_list = []

		for pair in merged_list:
		    a = []
		    a.append(tuple(pair))
		    nested_merged_list.append(a)

		output = collections.defaultdict(int)
		for elem in nested_merged_list:
			output[elem[0]] += 1

		count = int(form_data['count'][0])
		title = form_data['title']
		user = Profile.objects.get(user = request.user)

		try:
			with transaction.atomic():
				# CHECK FOR LOOP IN WORKFLOW
				for i in output.values():
					if i > 1:
						raise ValueError('Loop is present in the workflow')
				# CREATE WORKFLOW
				workflow = Workflow(creator = user, title = title)
				workflow.save()
				# CREATE NODES
				prev = None
				for i in range(count):
					role_name = form_data['node_{}_role'.format(i+1)]
					team_name = form_data['node_{}_team'.format(i+1)]

					role = Role.objects.get(role_name = role_name)
					team = Team.objects.get(team_name = team_name) if team_name != "None" else None

					cur_node = Node(prev_node = prev, assosiated_role = role, assosiated_team = team, workflow = workflow)
					cur_node.save()

					if prev:
						prev.next_node = cur_node
						prev.save()

					prev = cur_node

			return redirect('forms_blueprint_edit', fb_id = workflow.formblueprint.id)

		except ValueError as err:
			print(err)
			return HttpResponse('Fail - Loop present')

		except Exception as e:
			print(e)
			return HttpResponse('Fail')

	#making a list of roles and teams for rendering in searchable dropdown
	role_list=list(Role.objects.all())
	team_list=list(Team.objects.all())

	context={
		"role_list":role_list,
		"team_list":team_list
	}


	return render(request, 'workflow/create.html',context)
