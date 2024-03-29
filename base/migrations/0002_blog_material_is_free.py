# Generated by Django 4.1.7 on 2023-07-19 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('body', models.TextField(max_length=500)),
            ],
        ),
        migrations.AddField(
            model_name='material',
            name='is_free',
            field=models.BooleanField(default=False),
        ),
    ]
