# Generated by Django 5.0.3 on 2024-04-01 21:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('perceptiontest', '0007_question_answer'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestTakerQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answered', models.BooleanField(default=False)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='perceptiontest.question')),
                ('test_taker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='perceptiontest.testtaker')),
            ],
        ),
    ]
