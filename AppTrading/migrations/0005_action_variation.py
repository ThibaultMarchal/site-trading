# Generated by Django 4.2 on 2023-05-04 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppTrading', '0004_titre_difference'),
    ]

    operations = [
        migrations.AddField(
            model_name='action',
            name='variation',
            field=models.FloatField(default=0.0),
            preserve_default=False,
        ),
    ]
