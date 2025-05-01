import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models

# User
class User(AbstractUser):
    ROLE_CHOICES = [
        ('tecnico', 'Técnico'),
        ('enfermagem', 'Enfermagem'),
        ('administrativo', 'Administrativo'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

# Material
class Material(models.Model):
    # Campos do modelo de material
    nome = models.CharField(max_length=255)
    tipo = models.CharField(max_length=255)
    data_validade = models.DateField()
    serial = models.CharField(max_length=255, unique=True, blank=True)  # O serial será gerado automaticamente
    
    def save(self, *args, **kwargs):
        # Se o serial não for preenchido, geramos automaticamente com base no nome
        if not self.serial:
            self.serial = self.gerar_serial()
        super().save(*args, **kwargs)

    def gerar_serial(self):
        # Gerar o serial baseado no nome do material e no UUID
        serial_base = f"SERIAL-{uuid.uuid4().hex[:8].upper()}-{self.nome[:3].upper()}"
        
        # Garantir que o serial seja único no banco
        while Material.objects.filter(serial=serial_base).exists():
            serial_base = f"SERIAL-{uuid.uuid4().hex[:8].upper()}-{self.nome[:3].upper()}"
            
        return serial_base
    
    def __str__(self):
        return self.nome

# Procedimento para as Etapas
class Procedimento(models.Model):
    material = models.ForeignKey(Material, on_delete=models.CASCADE, related_name='procedimentos')
    data_inicio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Procedimento {self.id} - {self.material.serial}"
    
# Etapas 4
class EtapaProcesso(models.Model):
    ETAPAS = [
        ('recebimento', 'Recebimento'),
        ('lavagem', 'Lavagem'),
        ('esterilizacao', 'Esterilização'),
        ('distribuicao', 'Distribuição'),
    ]
    STATUS = [
        ('pendente', 'Pendente'),
        ('em andamento', 'Em andamento'),
        ('concluida', 'Concluída'),
    ]


    procedimento = models.ForeignKey(Procedimento, on_delete=models.CASCADE, related_name='etapas')
    etapa = models.CharField(max_length=20, choices=ETAPAS)
    status = models.CharField(max_length=20, choices=STATUS, default='pendente')  # Status da etapa
    data_realizacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['data_realizacao']

    def __str__(self):
        return f"{self.procedimento.material.serial} - {self.etapa} - {self.status}"


class Falha(models.Model):
    etapa = models.ForeignKey(EtapaProcesso, on_delete=models.CASCADE, related_name='falhas')
    descricao = models.TextField()
    data_ocorrencia = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Falha na etapa {self.etapa.etapa} - Serial {self.etapa.procedimento.material.serial}"