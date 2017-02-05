from datetime import date

from django.test import TestCase, RequestFactory, Client
from django.contrib.auth.models import User, AnonymousUser

from rest_framework.test import APITestCase

from .models import Project, Task


class ModelsTetCase(TestCase):
    """
    Tests for models
    """
    def setUp(self):
        user = User.objects.create_user(username='test_user',
                                 password='password')
        project = Project.objects.create(name='Test project', user=user)
        Task.objects.create(project=project, name='Test task 1')
        Task.objects.create(project=project, name='Test task 2')

    def test_models_relations(self):
        user = User.objects.get(username='test_user')
        project = user.projects.get(name='Test project')
        task1 = project.tasks.get(name='Test task 1')
        task2 = project.tasks.get(name='Test task 2')

        self.assertEqual(user.username, 'test_user')
        self.assertEqual(project.name, 'Test project')
        self.assertEqual(task1.name, 'Test task 1')
        self.assertEqual(task2.name, 'Test task 2')

    def test_task_fields(self):
        task = Task.objects.get(name='Test task 1')
        day = date.today()
        task.deadline = day

        self.assertEqual(task.name, 'Test task 1')
        self.assertEqual(task.status, False)
        self.assertEqual(task.priority, 0)
        self.assertEqual(task.deadline, day)


class ProjectTestCase(APITestCase):
    """
    Tests for projects REST API
    """
    def setUp(self):
        self.user = User.objects.create_user(username='test_user', password='password')
        self.client.login(username='test_user', password='password')

    def test_project_api(self):
        # post test
        response = self.client.post('/projects/',
                                    {'name': 'Test post project',
                                     'user': self.user.id})

        self.assertEqual(response.status_code, 201)

        # get list test
        response = self.client.get('/projects/')

        self.assertEqual(response.status_code, 200)

        id = response.data[0].get('id')

        # get test
        response = self.client.get('/projects/{}/'.format(id))

        self.assertEqual(response.status_code, 200)

        # patch test
        response = self.client.patch('/projects/{}/'.format(id),
                                     {'name': 'Test patch project'})

        self.assertEqual(response.status_code, 200)

        # delete test
        response = self.client.delete('/projects/{}/'.format(id))

        self.assertEqual(response.status_code, 204)


class TaskTestCase(APITestCase):
    """
    Tests for tasks REST API
    """

    def setUp(self):
        self.user = User.objects.create_user(username='test_user', password='password')
        self.client.login(username='test_user', password='password')
        self.project = Project.objects.create(name='Task test project', user=self.user)

    def test_task_api(self):
        # post test
        response = self.client.post('/tasks/',
                                    {'name': 'Test post task',
                                     'project': self.project.id})

        self.assertEqual(response.status_code, 201)

        # get list test
        response = self.client.get('/tasks/')

        self.assertEqual(response.status_code, 200)

        id = response.data[0].get('id')

        # get test
        response = self.client.get('/tasks/{}/'.format(id))

        self.assertEqual(response.status_code, 200)

        # patch test
        response = self.client.patch('/tasks/{}/'.format(id), {'name': 'Test patch task'})

        self.assertEqual(response.status_code, 200)

        # delete test
        response = self.client.delete('/tasks/{}/'.format(id))

        self.assertEqual(response.status_code, 204)

