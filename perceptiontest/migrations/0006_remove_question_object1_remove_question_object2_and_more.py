# Generated by Django 5.0.3 on 2024-03-31 00:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('perceptiontest', '0005_alter_testtaker_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='object1',
        ),
        migrations.RemoveField(
            model_name='question',
            name='object2',
        ),
        migrations.RemoveField(
            model_name='question',
            name='object3',
        ),
        migrations.DeleteModel(
            name='Answer',
        ),
        migrations.DeleteModel(
            name='Question',
        ),
    ]
