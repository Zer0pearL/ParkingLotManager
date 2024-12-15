# Generated by Django 3.2.25 on 2024-12-15 00:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_parkinglot_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='parkinglot',
            name='revenue',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]