from django.db import models


class Lead(models.Model):
    CATEGORIAS = [
        ("comercial", "Comercial"),
        ("suporte", "Suporte"),
        ("geral", "Geral"),
    ]
    URGENCIAS = [
        ("alta", "Alta"),
        ("normal", "Normal"),
    ]

    nome = models.CharField(max_length=120)
    email = models.EmailField()
    mensagem = models.TextField()
    origem = models.CharField(max_length=40, default="site")

    categoria = models.CharField(max_length=20, choices=CATEGORIAS, blank=True)
    urgencia = models.CharField(max_length=10, choices=URGENCIAS, blank=True)
    score = models.PositiveSmallIntegerField(default=0)

    recebido_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-score", "-recebido_em"]

    def __str__(self):
        return f"{self.nome} ({self.categoria}/{self.urgencia} score={self.score})"
