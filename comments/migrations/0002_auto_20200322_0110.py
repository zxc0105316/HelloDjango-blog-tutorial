# Generated by Django 2.2.3 on 2020-03-21 17:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['-create_time'], 'verbose_name': '评论', 'verbose_name_plural': '评论'},
        ),
    ]