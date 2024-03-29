# Generated by Django 4.0.1 on 2022-03-05 16:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.DateTimeField()),
                ('end', models.DateTimeField(blank=True, null=True)),
                ('allday', models.BooleanField(default=True)),
                ('title', models.CharField(max_length=15)),
                ('description', models.CharField(blank=True, max_length=10000, null=True)),
                ('url', models.URLField(blank=True, null=True)),
                ('background_color', models.CharField(default='#03a9f3', max_length=7)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to=settings.AUTH_USER_MODEL)),
                ('groups', models.ManyToManyField(to='auth.Group')),
            ],
        ),
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('days', models.CharField(max_length=13)),
                ('meeting_id', models.CharField(max_length=42)),
                ('subject', models.CharField(max_length=50)),
                ('event', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='classes', to='classes.event')),
            ],
        ),
    ]
