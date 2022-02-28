# Generated by Django 4.0.1 on 2022-02-07 07:54

from django.db import migrations, models
import user.models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='avatar',
            field=models.ImageField(default='static/images/default_avatar.jpg', upload_to=user.models.filename_generator),
        ),
        migrations.AddField(
            model_name='user',
            name='user_id',
            field=models.CharField(default=1, editable=False, max_length=10, unique=True),
            preserve_default=False,
        ),
    ]
