# Generated by Django 4.2.11 on 2024-05-16 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0002_remove_order_articles_remove_order_total_price_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="order_date",
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
    ]