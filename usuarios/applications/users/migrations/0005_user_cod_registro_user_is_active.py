# Generated by Django 4.1 on 2022-09-09 07:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_user_managers_remove_user_date_joined_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='cod_registro',
            field=models.CharField(blank=True, max_length=6),
        ),
        migrations.AddField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
