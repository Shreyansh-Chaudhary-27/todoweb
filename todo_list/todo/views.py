from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Todo
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required()
def index(request):
    if request.method == 'POST':
        task = request.POST.get('task', 'NA')
        Todo.objects.create(user=request.user, task=task)
        return redirect('index')

    all_todo = Todo.objects.filter(user=request.user)
    context = {
        'all_todo': all_todo
    }
    return render(request, 'todo/index.html', context)


@login_required()
def complete_todo(request, todo_id):
    todo = Todo.objects.get(id=todo_id)
    todo.status = True
    todo.save()
    return redirect('index')


@login_required()
def delete_todo(request, todo_id):
    todo = Todo.objects.get(id=todo_id)
    todo.delete()
    return redirect('index')

def update_todo(request, todo_id):
    todo = Todo.objects.get(id=todo_id, user=request.user)
    if request.method == 'POST':
        task = request.POST.get('task', 'NA')
        if not task:
            # messages.error(request, 'Task cannot be empty')
            return redirect('update_todo')
        todo.task = task
        todo.save()
        # messages.success(request, 'Task updated successfully!')
        return redirect('index')

    context = {
        'todo' : todo
    }

    return render(request, 'todo/update.html', context)

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', 'NA')
        email = request.POST.get('email', 'NA')
        password = request.POST.get('password', 'NA')

        if len(password) < 3:
            messages.error(request, 'Password must be atleast 3 characters')
            return redirect('register_view')

        get_all_users_by_username = User.objects.filter(username=username)
        if get_all_users_by_username:
            messages.error(request, 'Username already exists, use another username')
            return redirect('register_view')

        new_user = User.objects.create_user(username=username, email=email, password=password)
        new_user.save()

        return redirect('login_view')
    return render(request, 'todo/register.html')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        username = request.POST.get('username', 'NA')
        password = request.POST.get('password', 'NA')

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Error, Wrong user details..')
            return redirect('login_view')
    return render(request, 'todo/login.html')


def logout_view(request):
    logout(request)
    return redirect('login_view')
