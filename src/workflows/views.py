from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def create_workflow(request):
	if request.method == 'POST':
		form_data = request.POST
		count = int(form_data['count'][0])
		for i in range(count):
			print(form_data['node_{}_role'.format(i+1)])
	return render(request, 'workflow/create.html')

