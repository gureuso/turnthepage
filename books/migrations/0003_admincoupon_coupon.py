# Generated by Django 2.1.7 on 2019-04-18 16:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import conf.commons


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('books', '0002_book_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdminCoupon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('coupon_url', models.ImageField(upload_to=conf.commons.generate_filename)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('admin_coupon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.AdminCoupon')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
