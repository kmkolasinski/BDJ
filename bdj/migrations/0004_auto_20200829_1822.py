# Generated by Django 3.0.3 on 2020-08-29 18:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bdj', '0003_auto_20200829_1820'),
    ]

    operations = [
        migrations.RenameField(
            model_name='foodplace',
            old_name='fb_place_id',
            new_name='fb_page_id',
        ),
    ]