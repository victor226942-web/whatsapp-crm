from django.db import models


class InstanceStatus(models.Model):
    """
    Guarda o último status conhecido de cada instância Evolution.
    Atualizado pelo evento `connection.update` do webhook — o resto do
    sistema consulta esse registro em vez de perguntar direto pra
    Evolution, que é a parte instável.
    """

    instance_name = models.CharField(max_length=100, unique=True)
    state = models.CharField(max_length=30, default="unknown")
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.instance_name}: {self.state}"
