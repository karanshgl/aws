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
					team = Team.objects.get(team_name = team_name) if team_name else None

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
 



	return render(request, 'workflow/create.html')

