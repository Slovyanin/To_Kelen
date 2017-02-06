from datetime import date

from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    """
    Project database model. This is class to interact with database
    """
    name = models.CharField(max_length=1024, null=True)
    user = models.ForeignKey(User, related_name='projects')

    def __str__(self):
        """
        This function called when python "str()" function used on this class
        :return: name of project
        """
        return self.name


class Task(models.Model):
    """
    Task database model
    """
    project = models.ForeignKey(Project, related_name='tasks', null=True)  # ForeignKey is a "link" to other parent model
    name = models.CharField(max_length=1024, null=True)
    status = models.BooleanField(default=False)
    priority = models.IntegerField(default=0)
    deadline = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.project.name})"

    @property
    def is_past_deadline(self):
        return self.deadline < date.today()

