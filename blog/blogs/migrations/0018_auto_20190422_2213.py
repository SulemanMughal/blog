# Generated by Django 2.2 on 2019-04-22 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0017_auto_20190422_2129'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscribe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=254)),
                ('date_added', models.DateField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Subscribe',
                'verbose_name_plural': 'Subscribers',
            },
        ),
        migrations.AlterField(
            model_name='blogcomment',
            name='post_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
