# Generated by Django 3.0.5 on 2020-08-31 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_auto_20200831_1926'),
    ]

    operations = [
        migrations.AlterField(
            model_name='title',
            name='description',
            field=models.CharField(blank=True, default=0, max_length=500),
            preserve_default=False,
        ),
    ]
