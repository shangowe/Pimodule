# Generated by Django 2.2.4 on 2020-01-22 23:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Pimoduleapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nms_server', models.CharField(max_length=15)),
                ('name', models.CharField(max_length=200)),
                ('btsstatus', models.BooleanField(default=False)),
                ('hvacstatus', models.BooleanField(default=False)),
                ('txnstatus', models.BooleanField(default=False)),
            ],
        ),
        migrations.DeleteModel(
            name='NMS',
        ),
    ]
