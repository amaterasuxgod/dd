# Generated by Django 4.0.3 on 2022-05-29 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('module1', '0012_alter_services_available'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderservice',
            name='paper_type',
            field=models.CharField(help_text='Required', max_length=255, null=True, verbose_name='paper type'),
        ),
        migrations.AlterField(
            model_name='orderservice',
            name='photo_format',
            field=models.CharField(help_text='Required', max_length=255, null=True, verbose_name='photo format'),
        ),
        migrations.AlterField(
            model_name='orderservice',
            name='urgency_rate',
            field=models.IntegerField(null=True),
        ),
    ]
