from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.conf import settings
from django.utils import six
from django.views.generic import CreateView, DeleteView, ListView, TemplateView, UpdateView
from django.contrib.auth.models import User
from .models import Project, Dataset
from cvat.apps.engine.models import Task, Segment, Job, Label, AttributeSpec
from .forms import CustomUserForm, LabelForm
from cvat.settings.base import JS_3RDPARTY
import os

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
    """プロジェクト割当処理(ユーザ管理画面)"""
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


def deassign_user_project(request, pk):
    """プロジェクト割当解除処理(ユーザ管理画面)"""
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


def set_project_assignees(request, pk):
    """プロジェクト割当処理(プロジェクト管理画面)"""
    project = Project.objects.get(id=pk)
    assignees = project.assignee.all()
    users = User.objects.all()

    context = {
        'project': project,
        'assignees': assignees,
        'users': users,
    }

    if (request.method == 'POST'):
        project = Project.objects.get(id=pk)
        for user_id in request.POST.getlist('users'):
            user = User.objects.get(id=user_id)
            project.assignee.add(user)
        
        return redirect('project_assignees', pk=pk)

    return render(request, 'management/projects/project_assignees.html', context)


def deassign_project_assignees(request, pk):
    """プロジェクト割当解除処理(プロジェクト管理画面)"""
    project = Project.objects.get(id=pk)
    user_id = request.POST['user_id']
    user = User.objects.get(id=user_id)
    project.assignee.remove(user)

    return redirect('project_assignees', pk=pk)


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
        return context


def set_dataset_assignees(request, project_id ,dataset_id):
    """データセット割当処理"""
    dataset = Dataset.objects.get(id=dataset_id)
    assignees = dataset.assignee.all()

    project = Project.objects.get(id=project_id)
    users = project.assignee.all()

    context = {
        'project': project,
        'dataset': dataset,
        'assignees': assignees,
        'users': users,
    }

    if (request.method == 'POST'):
        dataset = Dataset.objects.get(id=dataset_id)
        for user_id in request.POST.getlist('users'):
            user = User.objects.get(id=user_id)
            dataset.assignee.add(user)
        
        return redirect('dataset_assignees',project_id=project_id ,dataset_id=dataset_id)
    
    return render(request, 'management/projects/dataset_assignees.html', context)


def deassign_dataset_assignees(request, project_id ,dataset_id):
    """データセット割当解除処理"""
    dataset = Dataset.objects.get(id=dataset_id)
    user_id = request.POST['user_id']
    user = User.objects.get(id=user_id)
    dataset.assignee.remove(user)

    return redirect('dataset_assignees',project_id=project_id ,dataset_id=dataset_id)


# class TasksView(TemplateView):
#     """タスク一覧画面"""
#     template_name = 'management/projects/tasks.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['project'] = Project.objects.get(pk=kwargs['project_id'])
#         context['dataset'] = Dataset.objects.get(pk=kwargs['dataset_id'])

#         tasks = Task.objects.filter(dataset_id=kwargs['dataset_id'])
#         segments = Segment.objects.filter(task_id__in=[i.id for i in tasks])
#         jobs = Job.objects.filter(segment_id__in=[i.id for i in segments])

#         context['segments'] = segments
#         context['jobs'] = jobs
        
#         return context


def TasksView(request, project_id, dataset_id):
    """タスク一覧画面"""
    parent_project = Project.objects.get(pk=project_id)
    parent_dataset = Dataset.objects.get(pk=dataset_id)
    task_list = list(Task.objects.filter(dataset_id=dataset_id)
        .prefetch_related('segment_set__job_set').order_by('-created_date').all())

    return render(request, 'management/projects/tasks.html', {
        'project': parent_project,
        'dataset': parent_dataset,
        'data': task_list,
        'max_upload_size': settings.LOCAL_LOAD_MAX_FILES_SIZE,
        'max_upload_count': settings.LOCAL_LOAD_MAX_FILES_COUNT,
        'base_url': "{0}://{1}/".format(request.scheme, request.get_host()),
        'share_path': os.getenv('CVAT_SHARE_URL', default=r'${cvat_root}/share'),
        'js_3rdparty': JS_3RDPARTY.get('dashboard', []),
    })


def labels(request, pk):
    """現行のLabel仕様
    e.g:
    vehicle @select=type:__undefined__,car,truck,bus,train ~radio=quality:good,bad ~checkbox=parked:false
    Label.name = 'vehicle' 
    AttributeSpec.text = [
        '@select=type:__undefined__,car,truck,bus,train', 
        '~radio=quality:good,bad', 
        '~checkbox=parked:false']
    """
    
    # 要)すでに作成されたLabelがあれば表示する
    # 要)動的に表示項目を増やす
    project = Project.objects.get(id=pk)
    params = {
        'project': project,
        # 'form': LabelForm()
    }
    
    if (request.method == 'POST'):
        # for debug
        post_dict = dict(six.iterlists(request.POST))
        print(post_dict)

        db_label = Label()
        db_label.project = project

        label = request.POST.get('label')
        db_label.name = label

        # 後で追加 -> Projectに紐づいたTaskのみ表示
        # 後で追加 -> Taskが一つも存在しなかった場合の処理
        tasks = Task.objects.all()
        for task in tasks:
            db_label.task = task
            db_label.save()

        # attributeの数だけループを回す
        try: 
            attr_spec_list = []
            i = 0
            
            while request.POST.get('attr_name[' + str(i) +']'):
                attr_list = []
                attr_list.append(request.POST.get('prefix[' + str(i) +']'))
                attr_list.append(request.POST.get('input_type[' + str(i) +']'))
                attr_list.append(request.POST.get('attr_name[' + str(i) +']'))
                attr_list = map(str, attr_list)
                
                attributes = ''.join(attr_list)
                
                value_list = []
                value_list.append(request.POST.get('attr_value1[' + str(i) +']'))
                value_list.append(request.POST.get('attr_value2[' + str(i) +']'))
                value_list.append(request.POST.get('attr_value3[' + str(i) +']'))
                # 空の項目をオミット
                value_list =  [i for i in value_list if i]

                values = ','.join(value_list)

                # atrributesが空の場合、文字連結に":"を使用しない
                if attributes:
                    attr_spec = attributes + ":" + values
                
                # バグ回避用(nullが入ると削除・作成どちらも不可能になるため)
                attr_spec = "@select=type:__undefined__,car,truck,bus,train"

                db_attrspec = AttributeSpec()
                db_attrspec.label = db_label
                db_attrspec.text = attr_spec
                db_attrspec.save()

                i += 1

        except KeyError:
            return redirect('projects')

    return render(request, 'management/projects/labels.html', params)
