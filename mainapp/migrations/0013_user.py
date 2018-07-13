# Generated by Django 2.0.5 on 2018-05-23 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0012_goods'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userName', models.CharField(max_length=50)),
                ('userPasswd', models.CharField(max_length=32)),
                ('phone', models.CharField(max_length=12)),
                ('address', models.CharField(default='', max_length=100)),
                ('city', models.CharField(default='', max_length=50)),
                ('nickName', models.CharField(max_length=50, verbose_name='昵称')),
                ('imgpath', models.CharField(default='', max_length=100)),
                ('token', models.CharField(default='', max_length=32)),
                ('state', models.BooleanField(default=True, verbose_name='用户状态')),
            ],
            options={
                'db_table': 'axf_user',
            },
        ),
    ]