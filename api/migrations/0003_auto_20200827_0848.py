# Generated by Django 3.0.5 on 2020-08-27 05:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20200827_0842'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('user', 'user'), ('moderator', 'moderator'), ('admin', 'admin'), ('djadmin', 'djadmin')], default='user', max_length=30),
        ),
    ]