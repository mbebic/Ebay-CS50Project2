# Generated by Django 4.0.4 on 2022-05-25 22:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_alter_auctionitem_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionitem',
            name='image',
            field=models.ImageField(upload_to='uploads/'),
        ),
    ]
