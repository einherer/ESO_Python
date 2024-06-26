# Generated by Django 5.0.6 on 2024-06-05 09:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Account",
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
                ("name", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="Server",
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
                ("name", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="Character",
            fields=[
                (
                    "character_id",
                    models.CharField(max_length=20, primary_key=True, serialize=False),
                ),
                ("name", models.CharField(max_length=100)),
                (
                    "faction_name",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                ("race_name", models.CharField(blank=True, max_length=100, null=True)),
                ("class_name", models.CharField(blank=True, max_length=100, null=True)),
                ("level", models.IntegerField(default=0)),
                ("champion_points", models.IntegerField(default=0)),
                ("is_werewolf", models.BooleanField(default=False)),
                ("is_vampire", models.BooleanField(default=False)),
                (
                    "account",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="django_app.account",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ActiveBuff",
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
                ("buff_id", models.IntegerField()),
                ("name", models.CharField(max_length=100)),
                ("description", models.TextField()),
                ("icon", models.TextField()),
                (
                    "character",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="django_app.character",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ActiveAbility",
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
                ("ability_id", models.IntegerField()),
                ("name", models.CharField(max_length=100)),
                ("description", models.TextField()),
                ("icon", models.TextField()),
                (
                    "character",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="django_app.character",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Equipment",
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
                ("slot", models.CharField(max_length=50)),
                ("name", models.CharField(max_length=100)),
                ("item_link", models.TextField()),
                ("quality", models.CharField(max_length=50)),
                ("icon", models.TextField()),
                ("set_info", models.TextField()),
                ("set_bonus_info", models.TextField()),
                ("enchant_info", models.TextField()),
                (
                    "character",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="django_app.character",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="account",
            name="server",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="django_app.server"
            ),
        ),
    ]
