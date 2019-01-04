# Generated by Django 2.1.4 on 2018-12-30 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lowlevel', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='alarm',
            old_name='activated',
            new_name='enabled',
        ),
        migrations.RemoveField(
            model_name='alarm',
            name='datetime',
        ),
        migrations.AddField(
            model_name='alarm',
            name='day',
            field=models.CharField(default='*', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='alarm',
            name='day_of_week',
            field=models.CharField(default='*', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='alarm',
            name='hour',
            field=models.CharField(default='*', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='alarm',
            name='minute',
            field=models.CharField(default=(0, 15, 30, 60), max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='alarm',
            name='month',
            field=models.CharField(default='*', max_length=255),
            preserve_default=False,
        ),
    ]
