# Generated by Django 4.2.2 on 2023-06-15 15:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0017_alter_issue_assignee'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='issue_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.issue'),
        ),
    ]
