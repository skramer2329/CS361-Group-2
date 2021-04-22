# Generated by Django 3.1.7 on 2021-04-22 05:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ourapp', '0003_auto_20210422_0015'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='instructor',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='ourapp.instructor'),
        ),
        migrations.AddField(
            model_name='section',
            name='course',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='ourapp.course'),
        ),
    ]
