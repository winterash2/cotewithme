# Generated by Django 3.1 on 2020-08-26 10:52

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0003_post_created_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='chat',
            name='created_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='code',
            name='created_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='commentcode',
            name='created_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='commentproblem',
            name='created_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
