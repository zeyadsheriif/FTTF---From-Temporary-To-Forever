# Generated by Django 5.1.3 on 2024-12-21 08:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_alter_product_rate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='rate',
            field=models.DecimalField(decimal_places=1, default=0, max_digits=10),
        ),
    ]