# Generated by Django 2.1.7 on 2019-04-18 16:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0004_admincoupon_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='coupon',
            name='book',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='books.Book'),
        ),
    ]
