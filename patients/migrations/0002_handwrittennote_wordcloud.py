# Generated by Django 5.1.4 on 2025-01-04 04:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='HandwrittenNote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='notes/images/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('digitized_text', models.TextField(blank=True)),
                ('corrected_text', models.TextField(blank=True)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='handwritten_notes', to='patients.patient')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='WordCloud',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cloud_type', models.CharField(choices=[('individual', 'Individual'), ('global', 'Global')], max_length=10)),
                ('image', models.ImageField(upload_to='word_clouds/')),
                ('data', models.JSONField(default=dict)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('patient', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='word_clouds', to='patients.patient')),
            ],
            options={
                'unique_together': {('patient', 'cloud_type')},
            },
        ),
    ]
