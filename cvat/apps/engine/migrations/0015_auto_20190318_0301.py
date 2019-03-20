# Generated by Django 2.1.5 on 2019-03-18 03:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0001_initial'),
        ('engine', '0014_job_max_shape_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='label',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='management.Project'),
        ),
        migrations.AddField(
            model_name='task',
            name='dataset',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='management.Dataset'),
        ),
        migrations.AlterField(
            model_name='label',
            name='task',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='engine.Task'),
        ),
    ]