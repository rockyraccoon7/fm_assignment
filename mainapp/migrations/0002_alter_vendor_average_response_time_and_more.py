# Generated by Django 4.2.11 on 2024-05-03 05:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendor',
            name='average_response_time',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='fulfillment_rate',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='on_time_delivery_rate',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='quality_rating_avg',
            field=models.FloatField(null=True),
        ),
    ]
