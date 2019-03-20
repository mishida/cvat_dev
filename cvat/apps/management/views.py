from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.utils import six
from django.views.generic import CreateView, DeleteView, ListView, TemplateView, UpdateView
from django.contrib.auth.models import User
from .models import Project, Dataset
from cvat.apps.engine.models import Task, Segment
from .forms import CustomUserForm, LabelForm


class UsersView(ListView):
    """ユーザ一覧画面"""
    model = User
    context_object_name = 'users'
    template_name = 'management/users/users.html'


class UserCreateView(CreateView):
    """ユーザ作成画面"""
    model = User
    form_class = CustomUserForm
    template_name = 'management/users/users_create.html'
    success_url = "/management/users"


class UserUpdateView(UpdateView):
    """ユーザ設定画面"""
    model = User
    form_class = CustomUserForm
    template_name = 'management/users/users_create.html'
    success_url = "/management/users"


class UserDeleteView(DeleteView):
    """ユーザ削除画面"""
    model = User
    template_name = 'management/users/users_delete.html'
    success_url = "/management/users"


def assigned_projects(request, pk):
    user = User.objects.get(id=pk)
    assigned_projects = Project.objects.filter(assignee=pk)
    projects = Project.objects.all()
    context = {
        'user': user,
        'assigned_projects': assigned_projects,
        'projects': projects,
    }
    
    if (request.method == 'POST'):
        user = User.objects.get(id=pk)
        for project_id in request.POST.getlist('projects'):
            project = Project.objects.get(id=project_id)
            project.assignee.add(user)

        return redirect('assigned_projects', pk=pk)

    return render(request, 'management/users/assigned_projects.html', context)


def dessign_user_project(request, pk):
    user = User.objects.get(id=pk)
    project_id = request.POST['project_id']
    project = Project.objects.get(id=project_id)
    project.assignee.remove(user)

    return redirect('assigned_projects', pk=pk)


class ProjectsView(ListView):
    """プロジェクト一覧画面"""
    model = Project
    context_object_name = 'projects'
    template_name = 'management/projects/projects.html'


class ProjectCreateView(CreateView):
    """プロジェクト作成画面"""
    model = Project
    fields = ['name']
    template_name = 'management/projects/projects_create.html'
    success_url = "/management/projects"


class ProjectUpdateView(UpdateView):
    """プロジェクト設定画面"""
    model = Project
    fields = ['name']
    template_name = 'management/projects/projects_create.html'
    success_url = "/management/projects"


class ProjectDeleteView(DeleteView):
    """プロジェクト削除画面"""
    model = Project
    context_object_name = 'project'
    template_name = 'management/projects/projects_delete.html'
    success_url = "/management/projects"


class DatasetsView(TemplateView):
    """データセット一覧画面"""
    template_name = 'management/projects/datasets.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['datasets'] = Dataset.objects.filter(project_id=kwargs['pk'])
        context['project'] = Project.objects.get(id=kwargs['pk'])
        return context


class DatasetCreateView(CreateView):
    """データセット作成画面"""
    model = Dataset
    fields = ['project', 'name', 'due_date']
    template_name = 'management/projects/datasets_create.html'

    def get_initial(self):
        print(self.kwargs['pk'])
        return {'project': Project.objects.get(id=self.kwargs['pk'])}

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.project_id = self.kwargs['pk']
        self.object.save()
        return response

    def get_success_url(self, **kwargs):
        return reverse_lazy('datasets', kwargs = {'pk': self.kwargs['pk']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = Project.objects.get(id=self.kwargs['pk'])
        return context


class DatasetUpdateView(UpdateView):
    """データセット設定画面"""
    model = Dataset
    fields = ['project', 'name', 'due_date']
    template_name = 'management/projects/datasets_create.html'

    def get_success_url(self, **kwargs):
        return reverse_lazy('datasets', kwargs = {'pk': self.kwargs['project_id']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = Project.objects.get(id=self.kwargs['project_id'])
        print(context)
        return context


class DatasetDelateView(DeleteView):
    """データセット削除画面"""
    model = Dataset
    context_object_name = 'dataset'
    template_name = 'management/projects/datasets_delete.html'
   
    def get_success_url(self, **kwargs):
        return reverse_lazy('datasets', kwargs = {'pk': self.kwargs['project_id']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = Project.objects.get(id=self.kwargs['project_id'])
        print(context)
        return context


class TasksView(ListView):
    """タスク一覧画面(仮)"""
    model = Segment
    template_name = 'management/projects/tasks.html'


def labels(request, pk):
    """ラベルの設定画面(仮)
    vehicle @select=type:__undefined__,car,truck,bus,train ~radio=quality:good,bad ~checkbox=parked:false
    Label.name = 'vehicle' 
    AttributeSpec.text = [
        '@select=type:__undefined__,car,truck,bus,train', 
        '~radio=quality:good,bad', 
        '~checkbox=parked:false']
    """
    project = Project.objects.get(id=pk)
    params = {
        'project': project,
        'form': LabelForm()
    }
    
    if (request.method == 'POST'):
        post_dict = dict(six.iterlists(request.POST))
        params['form'] = LabelForm(request.POST)
        print(post_dict)
        # return HttpResponse('successed!!')
        return redirect('projects')

    return render(request, 'management/projects/labels.html', params)
