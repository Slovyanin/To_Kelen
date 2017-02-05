from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from django.contrib.auth import forms, views
from django.template.response import TemplateResponse
from django.contrib.auth.models import User

from rest_framework import viewsets

from .models import Project, Task
from .serializers import ProjectSerializer, TaskSerializer


def login_or_signup(request):
    login_response = views.login(request)
    if isinstance(login_response, TemplateResponse):
        if request.method == 'POST':
            # create user if don't exist
            user = User.objects.create_user(username=request.POST.get('username'),
                                            password=request.POST.get('password'))

            return views.login(request)

    return login_response


class IndexView(TemplateView):
    template_name = 'index.html'


class RenderTask(TemplateView):
    template_name = 'task.html'

    def get_context_data(self, **kwargs):
        context = super(RenderTask, self).get_context_data(**kwargs)
        context['task'] = get_object_or_404(Task, pk=self.kwargs.get('pk'))

        return context


class RenderProject(TemplateView):
    template_name = 'project.html'

    def get_context_data(self, **kwargs):
        context = super(RenderProject, self).get_context_data(**kwargs)
        context['project'] = get_object_or_404(Project, pk=self.kwargs.get('pk'))

        return context


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def get_queryset(self):
        return Project.objects.filter(user=self.request.user)


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get_queryset(self):
        proj_id = self.kwargs.get('proj_id', False)

        if proj_id:
            return Task.objects.filter(project_id=proj_id)
        else:
            return super(TaskViewSet, self).get_queryset()