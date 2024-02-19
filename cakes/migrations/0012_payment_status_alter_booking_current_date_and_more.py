# Generated by Django 4.2.4 on 2024-02-12 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cakes', '0011_payment_bookingid'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='status',
            field=models.CharField(default='sucessfull', max_length=25),
        ),
        migrations.AlterField(
            model_name='booking',
            name='current_date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='booking',
            name='desc',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='payment',
            name='current_date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='payment',
            name='name',
            field=models.CharField(max_length=50, null=True),
        ),
    ]