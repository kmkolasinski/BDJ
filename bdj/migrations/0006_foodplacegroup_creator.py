# Generated by Django 3.0.3 on 2020-08-30 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bdj', '0005_foodplacegroup'),
    ]

    operations = [
        migrations.AddField(
            model_name='foodplacegroup',
            name='creator',
            field=models.CharField(default='admin', max_length=512),
        ),
    ]
