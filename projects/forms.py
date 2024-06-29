from django import forms
from .models import Project, Task
from django.contrib.auth.models import User


class ProjectForm(forms.ModelForm):
    members = forms.ModelMultipleChoiceField(queryset=User.objects.all(), widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Project
        fields = ['name', 'description', 'members']


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'assigned_to', 'project']


class UserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class TaskProgressForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['progress', 'completed']


class AddMemberForm(forms.Form):
    user = forms.ModelChoiceField(queryset=User.objects.all(), label="Add Member")