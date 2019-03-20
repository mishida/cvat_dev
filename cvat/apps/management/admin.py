from django.contrib import admin

from .models import Project, Dataset
from cvat.apps.engine.models import Task, Segment, Job, Label, AttributeSpec


class LabelInline(admin.TabularInline):
    model = Label
    show_change_link = True
    exclude = ('task',)
    readonly_fields = ('name',)
    can_delete = False

    # Don't show extra lines to add an object
    def has_add_permission(self, request, object=None):
        return False


class TaskInline(admin.TabularInline):
    model = Task
    show_change_link = True
    exclude = ('size', 'path', 'mode', 'owner', 'assignee', 
        'bug_tracker', 'overlap', 'z_order', 'flipped', 'source', 'status')
    readonly_fields = ('name',)
    show_change_link = True
    can_delete = False

    # Don't show extra lines to add an object
    def has_add_permission(self, request, object=None):
        return False


class DatasetInline(admin.TabularInline):
    model = Dataset
    show_change_link = True
    # exclude = ('assignee',)
    readonly_fields = ('name', 'assignee','due_date')
    can_delete = False

    # Don't show extra lines to add an object
    def has_add_permission(self, request, object=None):
        return False


class DatasetAdmin(admin.ModelAdmin):
    filter_horizontal = ('assignee',)
    fields = ['name', 'project', 'assignee','due_date']
    list_display = ('name', 'project', 'assignees', 'due_date')
    inlines = [TaskInline]


class ProjectAdmin(admin.ModelAdmin):
    filter_horizontal = ('assignee',)
    fields = ['name', 'assignee']
    list_display = ('name', 'assignees','datasets', 'updated_date')
    inlines = [LabelInline, DatasetInline]
    

admin.site.register(Project, ProjectAdmin)
admin.site.register(Dataset, DatasetAdmin)
