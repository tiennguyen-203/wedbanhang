# Generated by Django 5.0.3 on 2024-05-05 01:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_alter_orderitem_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='product',
            field=models.CharField(max_length=200),
        ),
    ]