# Generated by Django 4.0.4 on 2022-07-26 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0017_alter_article_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='total_views',
            field=models.IntegerField(default=0),
        ),
    ]
