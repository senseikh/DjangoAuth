# Generated by Django 4.1.2 on 2023-01-12 07:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_staffuser_delete_systemuser'),
    ]

    operations = [
        migrations.AddField(
            model_name='staffuser',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pictures'),
        ),
    ]