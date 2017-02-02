from datetime import date

from django.db import models


class Project(models.Model):
    """
    Project database model. This is class to interact with database
    """
    name = models.CharField(max_length=1024, null=True)

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


def get_statuses():
    """
    Get all statuses, not repeating, alphabetically ordered
    """
    statuses = []
    for t in Task.objects.order_by('name'):
        statuses.append({t: t.status})

    return statuses


def get_tasks_counts_amount_sorted():
    """
    Get the count of all tasks in each project, order by tasks count descending
    """
    projects = []
    for p in Project.objects.annotate(num_tasks=models.Count('tasks')).order_by('-num_tasks'):
        projects.append({p: p.tasks.count()})

    return projects


def get_tasks_counts_name_sorted():
    """
    Get the count of all tasks in each project, order by projects names
    """
    projects = []
    for p in Project.objects.order_by('name'):
        projects.append({p: p.tasks.count()})

    return projects


def get_tasks_for_project_name_starting_with(name):
    """
    Get the tasks for all projects having the name beginning with 'name' letter
    """
    return list(Project.objects.filter(name__startswith=name))


def get_tasks_for_project_name_contains(char):
    """
    Get the list of all projects containing the 'char' in the name,
    """
    projects = []
    for p in Project.objects.filter(name__contains=char):
        projects.append({p: p.tasks.count()})

    return projects


def get_duplicated_tasks():
    """
    Get the list of tasks with duplicate names. Order alphabetically.
    """
    dups = (
        Task.objects.values('name')
            .annotate(count=models.Count('id'))
            .values('name')
            .order_by()
            .filter(count__gt=1)
    )

    return list(Task.objects.filter(name__in=dups).order_by('name'))


def get_tasks_by_name_status(project, name, status):
    """
    Get the list of tasks having several exact matches of both name and status,
    """
    l = lambda t: (t.name == name) + (t.status == status) # lambda - is a little function, good to store in variable
    return sorted(project.tasks.filter(models.Q(name=name) | models.Q(status=status)), key=l)[::-1]


def get_project_names_by_complited_tasks(amount):
    """
    get the list of project names having more than 10 tasks in status ‘completed’(True)
    """
    projects = []
    # get all projects with more than 'amount' tasks, and order it by id
    for p in Project.objects.annotate(num_tasks=models.Count('tasks')).filter(tasks__gte=amount).order_by('id'):
        if p.tasks.filter(status=True).count() > amount:
            projects.append(p.name)

    return projects
