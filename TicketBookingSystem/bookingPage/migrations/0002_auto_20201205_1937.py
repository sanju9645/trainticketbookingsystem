# Generated by Django 3.1.3 on 2020-12-05 19:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookingPage', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookings',
            name='passenger_gender',
            field=models.CharField(choices=[('F', 'F'), ('M', 'M')], max_length=1),
        ),
    ]