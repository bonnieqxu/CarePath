# Generated by Django 5.1 on 2024-09-20 08:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CarePath', '0009_customuser_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='username',
        ),
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='status',
            field=models.CharField(default='Active', max_length=20),
        ),
    ]
