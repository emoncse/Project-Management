import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from ..forms import ProjectForm, TaskForm, UserCreationForm, TaskProgressForm, AddMemberForm
from ..models import Project, Task
from django.contrib.auth.forms import UserCreationForm as AuthUserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User

logger = logging.getLogger(__name__)


def signup(request):
    if request.method == 'POST':
        form = AuthUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            logger.info(f'User {user.username} signed up and logged in.')
            return redirect('dashboard')
        else:
            logger.warning('User signup failed. Invalid form data.')
    else:
        form = AuthUserCreationForm()
    return render(request, 'signup.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            logger.info(f'User {user.username} logged in.')
            return redirect('dashboard')
        else:
            logger.warning('User login failed. Invalid form data.')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


@login_required
def dashboard(request):
    if request.user.is_superuser:
        projects = Project.objects.all()
        logger.info(f'Admin {request.user.username} accessed the dashboard.')
    else:
        projects = Project.objects.filter(members=request.user)
        logger.info(f'User {request.user.username} accessed the dashboard.')
    return render(request, 'dashboard.html', {'projects': projects})


@login_required
def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.created_by = request.user
            project.save()
            form.save_m2m()  # Save the many-to-many data for the form
            logger.info(f'User {request.user.username} created project {project.name}.')
            return redirect('dashboard')
        else:
            logger.warning('Project creation failed. Invalid form data.')
    else:
        form = ProjectForm()
    return render(request, 'create_project.html', {'form': form})


@login_required
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.user.is_superuser or request.user in project.members.all():
        tasks = project.tasks.all()
        logger.info(f'User {request.user.username} accessed details for project {project.name}.')
        return render(request, 'project_detail.html', {'project': project, 'tasks': tasks})
    else:
        logger.warning(f'User {request.user.username} tried to access forbidden project {project.name}.')
        return HttpResponseForbidden()


@login_required
def user_list(request):
    users = User.objects.all()
    logger.info(f'User {request.user.username} accessed the user list.')
    return render(request, 'user_list.html', {'users': users})


@login_required
def create_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            logger.info(f'User {request.user.username} created new user {user.username}.')
            return redirect('user_list')
        else:
            logger.warning('User creation failed. Invalid form data.')
    else:
        form = UserCreationForm()
    return render(request, 'create_user.html', {'form': form})


@login_required
def user_detail(request, pk):
    user = get_object_or_404(User, pk=pk)
    logger.info(f'User {request.user.username} accessed details for user {user.username}.')
    return render(request, 'user_detail.html', {'user': user})


@login_required
def update_task_progress(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.user != task.assigned_to:
        logger.warning(f'User {request.user.username} tried to update forbidden task {task.name}.')
        return HttpResponseForbidden("You are not allowed to update this task.")
    if request.method == 'POST':
        form = TaskProgressForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            logger.info(f'User {request.user.username} updated progress for task {task.name}.')
            return redirect('project_detail', pk=task.project.pk)
        else:
            logger.warning('Task progress update failed. Invalid form data.')
    else:
        form = TaskProgressForm(instance=task)
    return render(request, 'update_task_progress.html', {'form': form, 'task': task})


@login_required
def create_task(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.user != project.created_by:
        logger.warning(f'User {request.user.username} tried to add task to forbidden project {project.name}.')
        return HttpResponseForbidden("You are not allowed to add tasks to this project.")
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = project
            task.save()
            logger.info(f'User {request.user.username} created task {task.name} in project {project.name}.')
            return redirect('project_detail', pk=project.pk)
        else:
            logger.warning('Task creation failed. Invalid form data.')
    else:
        form = TaskForm()
    return render(request, 'create_task.html', {'form': form, 'project': project})


@login_required
def add_member(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.user != project.created_by:
        logger.warning(f'User {request.user.username} tried to add member to forbidden project {project.name}.')
        return HttpResponseForbidden("You are not allowed to add members to this project.")
    if request.method == 'POST':
        form = AddMemberForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            project.members.add(user)
            logger.info(f'User {request.user.username} added member {user.username} to project {project.name}.')
            return redirect('project_detail', pk=project.pk)
        else:
            logger.warning('Add member failed. Invalid form data.')
    else:
        form = AddMemberForm()
    return render(request, 'add_member.html', {'form': form, 'project': project})
