# Generated by Django 4.0.5 on 2023-04-21 07:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app3', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('Result', models.CharField(max_length=30)),
                ('Probability', models.CharField(max_length=30)),
            ],
        ),
    ]
