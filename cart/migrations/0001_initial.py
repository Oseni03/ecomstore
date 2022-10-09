# Generated by Django 4.1.1 on 2022-10-06 10:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("store", "0002_alter_media_alt_text"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Cart",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("total", models.IntegerField(default=0)),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True,
                        help_text="format: y-m-d H:M:S",
                        verbose_name="date cart created",
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now=True,
                        help_text="format: y-m-d H:M:S",
                        verbose_name="date cart updated",
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="cart",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "cart",
                "verbose_name_plural": "carts",
            },
        ),
        migrations.CreateModel(
            name="CartItem",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("quantity", models.IntegerField(default=1)),
                (
                    "added_at",
                    models.DateTimeField(
                        auto_now_add=True,
                        help_text="format: y-m-d H:M:S",
                        verbose_name="date cart-item added",
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now=True,
                        help_text="format: y-m-d H:M:S",
                        verbose_name="date cart-item updated",
                    ),
                ),
                (
                    "price",
                    models.DecimalField(
                        decimal_places=2,
                        default=0.0,
                        error_messages={
                            "name": {
                                "max_length": "the price must be between 0 and 999.99."
                            }
                        },
                        help_text="format: maximum price 999.99",
                        max_digits=5,
                        verbose_name="total price",
                    ),
                ),
                (
                    "cart",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="items",
                        to="cart.cart",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="cart_items",
                        to="store.product",
                    ),
                ),
            ],
            options={
                "verbose_name": "cart item",
                "verbose_name_plural": "cart items",
            },
        ),
    ]