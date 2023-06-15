# Generated by Django 4.2.2 on 2023-06-14 02:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0013_alter_contributor_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contributor',
            name='role',
            field=models.CharField(choices=[('author', 'AUTHOR'), ('contributor', 'CONTRIBUTOR')], max_length=11),
        ),
    ]