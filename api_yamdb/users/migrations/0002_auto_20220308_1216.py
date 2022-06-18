# Generated by Django 3.2.3 on 2022-03-08 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={},
        ),
        migrations.AddConstraint(
            model_name='user',
            constraint=models.UniqueConstraint(fields=('username', 'email'), name='unique_email'),
        ),
        migrations.AddConstraint(
            model_name='user',
            constraint=models.CheckConstraint(check=models.Q(('username', 'me'), _negated=True), name='me_no_create_user'),
        ),
    ]