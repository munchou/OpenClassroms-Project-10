# Generated by Django 4.2.2 on 2023-06-18 13:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0018_alter_comment_issue_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='issue_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='issue_id', to='projects.issue'),
        ),
    ]