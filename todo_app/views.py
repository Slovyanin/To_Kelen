from django.shortcuts import render
from rest_framework import viewsets
from django.views.generic import TemplateView

from .models import Project, Task
from .serializers import ProjectSerializer, TaskSerializer


class IndexView(TemplateView):
    template_name = 'index.html'


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get_queryset(self):
        proj_id = self.kwargs.get('proj_id', False)

        if proj_id:
            return Task.objects.filter(project_id=proj_id)
        else:
            return super(TaskViewSet, self).get_queryset()