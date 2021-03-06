# Generated by Django 4.0.3 on 2022-04-24 18:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('module1', '0002_alter_userbase_is_professional'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='services',
            name='order',
        ),
        migrations.CreateModel(
            name='OrderService',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order', to='module1.order')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='service', to='module1.services')),
            ],
        ),
    ]
