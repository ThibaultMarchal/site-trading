# Generated by Django 4.2 on 2023-05-05 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppTrading', '0005_action_variation'),
    ]

    operations = [
        migrations.AddField(
            model_name='titre',
            name='graphe',
            field=models.FileField(default='', upload_to='documents/'),
            preserve_default=False,
        ),
    ]
