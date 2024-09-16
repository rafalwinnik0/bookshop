# Generated by Django 5.1 on 2024-09-16 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0014_genres_book_genres"),
    ]

    operations = [
        migrations.AlterField(
            model_name="genres",
            name="genre",
            field=models.CharField(
                choices=[
                    ("akcja", "Akcja"),
                    ("przygoda", "Przygoda"),
                    ("historia", "Historia"),
                    ("komedia", "Komedia"),
                ],
                default="Akcja",
                max_length=15,
            ),
        ),
    ]
