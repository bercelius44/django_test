# Generated by Django 4.1.3 on 2022-11-03 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('time', models.CharField(max_length=5)),
                ('pick_up_place', models.CharField(max_length=7)),
                ('delivery_place', models.CharField(max_length=7)),
                ('driver', models.IntegerField()),
            ],
        ),
    ]
