# Generated by Django 3.0.7 on 2020-06-08 14:29

import candidates.models
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CandidateModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('contact', models.CharField(blank=True, max_length=13)),
                ('resume', models.FileField(null=True, upload_to=candidates.models.rename_and_save, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf', 'docx'])])),
                ('job_applied_to', models.CharField(choices=[('Backend Engineer', 'Backend Engineer'), ('Frontend Engineer', 'Frontend Engineer'), ('Python Developer', 'Python Developer'), ('Business Analyst', 'Business Analyst'), ('ML Engineer', 'ML Engineer'), ('Data Engineer', 'Data Engineer'), ('Technical Recruiter', 'Technical Recruiter')], max_length=100)),
            ],
        ),
    ]
