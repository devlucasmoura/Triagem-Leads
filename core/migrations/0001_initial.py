from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True
    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Lead",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("nome", models.CharField(max_length=120)),
                ("email", models.EmailField(max_length=254)),
                ("mensagem", models.TextField()),
                ("origem", models.CharField(default="site", max_length=40)),
                (
                    "categoria",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("comercial", "Comercial"),
                            ("suporte", "Suporte"),
                            ("geral", "Geral"),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "urgencia",
                    models.CharField(
                        blank=True,
                        choices=[("alta", "Alta"), ("normal", "Normal")],
                        max_length=10,
                    ),
                ),
                ("score", models.PositiveSmallIntegerField(default=0)),
                ("recebido_em", models.DateTimeField(auto_now_add=True)),
            ],
            options={"ordering": ["-score", "-recebido_em"]},
        ),
    ]
