# Generated by Django 3.1.3 on 2020-12-03 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profileUpdate', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='agent',
            name='email',
        ),
        migrations.AddField(
            model_name='agent',
            name='address',
            field=models.CharField(max_length=500, null=True),
        ),
    ]