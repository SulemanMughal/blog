# Generated by Django 2.2 on 2019-04-22 16:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0016_auto_20190421_2044'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blogcomment',
            options={'ordering': ['-post_date']},
        ),
    ]