# Generated by Django 4.1.7 on 2023-02-20 04:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_alter_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(default='static/images/placeholder.png', upload_to=''),
        ),
    ]
