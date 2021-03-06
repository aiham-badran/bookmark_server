# Generated by Django 3.1.7 on 2021-06-10 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookmarks', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookmarks',
            name='important',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='folders',
            name='color',
            field=models.CharField(blank=True, default=None, max_length=30, null=True),
        ),
    ]
