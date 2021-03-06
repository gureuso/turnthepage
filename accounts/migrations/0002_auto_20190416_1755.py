# Generated by Django 2.1.7 on 2019-04-16 08:55

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Token',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('expiry_date', models.DateTimeField(default=datetime.datetime(2019, 4, 16, 17, 55, 5, 553476))),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='verified_email',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='token',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
