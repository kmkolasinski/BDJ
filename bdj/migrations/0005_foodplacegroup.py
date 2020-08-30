# Generated by Django 3.0.3 on 2020-08-30 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bdj', '0004_auto_20200829_1822'),
    ]

    operations = [
        migrations.CreateModel(
            name='FoodPlaceGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateField(auto_created=True, auto_now=True)),
                ('name', models.CharField(max_length=512)),
                ('food_places', models.ManyToManyField(to='bdj.FoodPlace')),
            ],
        ),
    ]
