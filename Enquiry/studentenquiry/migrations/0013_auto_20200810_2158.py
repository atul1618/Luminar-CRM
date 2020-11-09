# Generated by Django 3.1 on 2020-08-10 16:28

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studentenquiry', '0012_auto_20200726_2036'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admission',
            name='date',
            field=models.DateField(default=datetime.date(2020, 8, 10)),
        ),
        migrations.AlterField(
            model_name='batch',
            name='batch_date',
            field=models.DateField(default=datetime.date(2020, 8, 10)),
        ),
        migrations.AlterField(
            model_name='enquiry',
            name='enquirydate',
            field=models.DateField(default=datetime.date(2020, 8, 10)),
        ),
        migrations.AlterField(
            model_name='payment',
            name='payment_date',
            field=models.DateField(default=datetime.date(2020, 8, 10)),
        ),
    ]