# Generated by Django 4.0.4 on 2022-07-26 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0016_alter_article_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='title',
            field=models.CharField(max_length=32, unique=True),
        ),
    ]
