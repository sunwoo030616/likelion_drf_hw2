# Generated by Django 5.0.7 on 2024-07-12 22:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("post", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Comment",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("writer", models.CharField(max_length=50)),
                ("content", models.TextField(max_length=200)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "movie",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="post.movie"
                    ),
                ),
            ],
        ),
    ]
