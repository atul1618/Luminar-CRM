# Generated by Django 3.0.6 on 2020-07-08 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studentenquiry', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enquiry',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]