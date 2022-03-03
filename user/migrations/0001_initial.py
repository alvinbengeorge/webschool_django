# Generated by Django 4.0.1 on 2022-03-03 20:46

from django.db import migrations, models
import user.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email address')),
                ('avatar', models.ImageField(default='default/images/default_avatar.png', upload_to=user.models.avatar_filename_generator)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('user_id', models.CharField(editable=False, max_length=10, unique=True)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('user_type', models.CharField(blank=True, choices=[('S', 'Student'), ('T', 'Teacher')], default='S', max_length=2)),
                ('is_active', models.BooleanField(blank=True, default=True)),
                ('is_admin', models.BooleanField(blank=True, default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
