# Generated by Django 5.0.3 on 2024-03-14 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userauth', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='about_me',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='user',
            name='employee',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='full_name',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='user',
            name='major',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='user',
            name='profile_photo',
            field=models.ImageField(blank=True, null=True, upload_to='profile_photos/'),
        ),
        migrations.AddField(
            model_name='user',
            name='university_name',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
