# Generated by Django 5.1.3 on 2024-11-18 16:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_answer_question'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='question',
        ),
    ]
