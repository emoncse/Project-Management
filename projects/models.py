from django.contrib.auth.models import User
from django.db import models


class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    members = models.ManyToManyField(User, related_name='member_projects')
    progress = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def update_progress(self):
        total_tasks = self.tasks.count()
        if total_tasks > 0:
            completed_tasks = self.tasks.filter(completed=True).count()
            self.progress = int((completed_tasks / total_tasks) * 100)
        else:
            self.progress = 0
        self.save()


class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    name = models.CharField(max_length=255)
    description = models.TextField()
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    completed = models.BooleanField(default=False)
    progress = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.project.update_progress()
