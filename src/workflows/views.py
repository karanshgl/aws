from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db import transaction

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
		count = int(form_data['count'][0])
		print(form_data)
		title = form_data['title']
		user = Profile.objects.get(user = request.user)

		try:
			with transaction.atomic():
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

			return HttpResponse('Success')

		except Exception as e:
			print(e)
			return HttpResponse('Fail')
 
	#making a list of roles and teams for rendering in searchable dropdown
	total_number_of_roles=Role.objects.count()
	role_list=[]
	for i in range (0,total_number_of_roles):
		role_list.append(Role.objects.get(id=i+1))						#TODO : check impact of inactive roles on this list
	
	total_number_of_teams=Team.objects.count()
	team_list=[]
	for i in range (0,total_number_of_teams):
		team_list.append(Team.objects.get(id=i+1))


	context={
		"role_list":role_list,
		"team_list":team_list
	}


	return render(request, 'workflow/create.html',context)

