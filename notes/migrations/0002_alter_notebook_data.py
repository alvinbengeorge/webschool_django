# Generated by Django 4.0.1 on 2022-01-28 23:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notebook',
            name='data',
            field=models.TextField(default={'blocks': [{'html': '', 'id': 'kyysw8ccau2pi34yw2c', 'tag': 'p'}]}),
        ),
    ]
