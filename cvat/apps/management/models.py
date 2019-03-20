from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    assignee = models.ManyToManyField(User)
    name = models.CharField(max_length=45)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def assignees(self):
        return self.assignee.all().count()
    
    def datasets(self):
        return Dataset.objects.filter(project_id=self.id).count()


class Dataset(models.Model):
    assignee = models.ManyToManyField(User)
    project =  models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=45)
    due_date = models.DateField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def assignees(self):
        return self.assignee.all().count()
