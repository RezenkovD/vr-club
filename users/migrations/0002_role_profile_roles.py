# Generated by Django 4.2.1 on 2023-06-15 21:27

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Role",
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
                ("title", models.CharField(max_length=32, unique=True)),
                ("description", models.CharField(max_length=64)),
            ],
        ),
        migrations.AddField(
            model_name="profile",
            name="roles",
            field=models.ManyToManyField(to="users.role"),
        ),
    ]
