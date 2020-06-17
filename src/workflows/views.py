from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db import transaction
import collections

# GET MODELS
from .models import Workflow, Node
from employees.models import Role, Profile
from teams.models import Team, TeamHasEmployees
from forms.models import TeamHasBlueprintPersmission, FormBlueprint


# Create your views here.
@login_required
def create_workflow(request):
	if request.method == 'POST':
		form_data = request.POST
		print(form_data)

		count = int(form_data['count'][0])

		# CREATING DICT FOR ROLE-TEAM PAIR
		NODE_ROLE_FORMAT = 'node_{}_role'
		NODE_TEAM_FORMAT = 'node_{}_team'

		# LOOP DETECTION
		role_team_pairs = []

		is_loop = False

		for i in range(1, count+1):
			role_input = NODE_ROLE_FORMAT.format(i)
			team_input = NODE_TEAM_FORMAT.format(i)

			if team_input != 'None':
				role_team_pair = (role_input, team_input)
				if role_team_pair in role_team_pairs:
					is_loop = True
				role_team_pairs.append(role_team_pair)


		title = form_data['title']
		user = Profile.objects.get(user = request.user)

		try:
			with transaction.atomic():
				# CHECK FOR LOOP IN WORKFLOW
				if is_loop:
					raise ValueError('Loop is present in the workflow')

				# CHECK IF HEAD IS EMPLOYEE AND IT DOES NOT BELONGS ANY TEAM
				# if roles[0].lower() == 'employee' and teams[0] != 'None':
				#	raise ValueError('Employee should not belong to any team')

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

					cur_node = Node(prev_node = prev, associated_role = role, associated_team = team, workflow = workflow)
					cur_node.save()

					if prev:
						prev.next_node = cur_node
						prev.save()

					prev = cur_node

			return redirect('fb_edit', fb_id = workflow.formblueprint.id)

		except ValueError as err:
			print(err)
			return HttpResponse('Fail - ' + str(err))
			context={
				'message': 'Fail - ' + str(err)
			}
			return render(request, 'forms/redirect_to_dashboard.html', context = context)

		except Exception as e:
			print(e)
			context={
				'message': "Failed"
			}
			return render(request, 'forms/redirect_to_dashboard.html', context = context)

    #check if the team of the user is present in TeamHasBlueprintPermissions
	user_team=TeamHasEmployees.objects.get(employee=request.user.profile).team
	try:
		check=TeamHasBlueprintPersmission.objects.get(team = user_team)
		if(check):
			context ={
				'form_blueprints':FormBlueprint.objects.all()
			}
			return render(request, 'workflow/create.html',{})
		else:
			context={
                        'message': "Your team doesn't have permission to manage blueprints"
                    }
			return render(request, 'forms/redirect_to_dashboard.html', context = context)
	except:
		context={
                        'message': "Your team doesn't have permission to manage blueprints"
                    }
		return render(request, 'forms/redirect_to_dashboard.html', context = context)
	
