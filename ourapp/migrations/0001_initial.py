# Generated by Django 3.1.7 on 2021-04-26 04:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(default=None, max_length=100)),
                ('last_name', models.CharField(default=None, max_length=100)),
                ('password', models.CharField(default=None, max_length=100)),
                ('address', models.CharField(default=None, max_length=100)),
                ('email', models.EmailField(default=None, max_length=254)),
                ('phone_number', models.CharField(default=None, max_length=15)),
                ('role', models.CharField(default=None, max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='SectionOne',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('teacher', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='ourapp.myuser')),
            ],
        ),
        migrations.CreateModel(
            name='MyCourse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=None, max_length=100)),
                ('number', models.IntegerField(default=None)),
                ('people', models.ManyToManyField(blank=True, default=None, to='ourapp.MyUser')),
            ],
        ),
        migrations.CreateModel(
            name='Joke',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('var', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='ourapp.myuser')),
            ],
        ),
    ]
