# Generated by Django 2.2.10 on 2022-12-25 20:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0007_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='rate',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]
