from django.db import models
from employees.models import Profile, Role
from teams.models import Team


# Create your models here.

class Node(models.Model):
    """ Represents a node of a workflow """
    next_node = models.ForeignKey('Node', on_delete = models.SET_NULL, null = True, related_name = 'next')
    prev_node = models.ForeignKey('Node', on_delete = models.CASCADE, null = True, related_name = 'prev') # If HEAD is deleted, deleted them all
    assosiated_role = models.ForeignKey(Role, on_delete = models.CASCADE, null = False)
    assosiated_team = models.ForeignKey(Team, on_delete = models.SET_NULL, null = True)

    # Workflow it belongs to
    workflow = models.ForeignKey('Workflow', on_delete = models.CASCADE, null = False) # If no workflow, no node

    def __str__(self):
        return "{} - {}".format(self.workflow, self.assosiated_role)


class Workflow(models.Model):
    
    creator = models.ForeignKey(Profile, on_delete = models.CASCADE, null = False)
    title = models.CharField(max_length = 255, null = False, unique = True, blank = False)
    # For head node, we can filter with prev_node = NULL

    def __str__(self):
        return self.title

    def get_flow(self):
        # Returns the nodes in the workflow
        head = Node.objects.get(prev_node = None, workflow = self)
        workflow_nodes = [head]
        cur = head.next_node
        # Loop through the nodes
        while cur:
            workflow_nodes.append(cur)
            cur = cur.next_node

        return workflow_nodes

