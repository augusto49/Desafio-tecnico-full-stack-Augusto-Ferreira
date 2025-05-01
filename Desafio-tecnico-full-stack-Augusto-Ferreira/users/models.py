import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models

# User Model
class User(AbstractUser):
    """
    Extensão do modelo padrão de usuário do Django (AbstractUser).
    A principal modificação é a adição do campo 'role' para definir o papel do usuário.
    Os papéis disponíveis são:
    - 'tecnico': Usuário técnico responsável por realizar as etapas do processo.
    - 'enfermagem': Usuário de enfermagem responsável por verificar a rastreabilidade e consultar falhas.
    - 'administrativo': Usuário administrativo responsável por cadastrar e gerenciar usuários.

    A escolha do papel é realizada com o campo 'role', que é um campo de texto com as opções predeterminadas.
    """

    ROLE_CHOICES = [
        ('tecnico', 'Técnico'),
        ('enfermagem', 'Enfermagem'),
        ('administrativo', 'Administrativo'),
    ]
    
    # Campo para armazenar o papel do usuário
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

# Material Model
class Material(models.Model):
    """
    Modelo para armazenar informações sobre os materiais que serão esterilizados.
    Os campos principais incluem o nome, tipo, data de validade e o serial gerado para cada material.

    O serial é gerado automaticamente no momento do salvamento do material, sendo único para cada item.
    O método `gerar_serial` cria o serial com base no nome do material e um UUID único, garantindo que não existam duplicatas.
    """

    nome = models.CharField(max_length=255)  # Nome do material
    tipo = models.CharField(max_length=255)  # Tipo do material
    data_validade = models.DateField()  # Data de validade do material
    serial = models.CharField(max_length=255, unique=True, blank=True)  # Serial único gerado para o material
    
    def save(self, *args, **kwargs):
        """
        Sobrescreve o método save para gerar automaticamente o serial se não estiver presente.
        """
        if not self.serial:
            self.serial = self.gerar_serial()  # Gera o serial caso não exista
        super().save(*args, **kwargs)

    def gerar_serial(self):
        """
        Gera um serial único para o material, combinando um UUID e as 3 primeiras letras do nome do material.
        """
        serial_base = f"SERIAL-{uuid.uuid4().hex[:8].upper()}-{self.nome[:3].upper()}"
        
        # Garante que o serial seja único no banco de dados
        while Material.objects.filter(serial=serial_base).exists():
            serial_base = f"SERIAL-{uuid.uuid4().hex[:8].upper()}-{self.nome[:3].upper()}"
            
        return serial_base
    
    def __str__(self):
        """
        Retorna o nome do material quando for impresso ou visualizado.
        """
        return self.nome

# Procedimento Model
class Procedimento(models.Model):
    """
    Modelo para representar um procedimento realizado com um material.
    Cada procedimento está vinculado a um material e possui uma data de início.
    Esse modelo será utilizado para rastrear o progresso do material ao longo das etapas do processo.
    """

    material = models.ForeignKey(Material, on_delete=models.CASCADE, related_name='procedimentos')  # Referência ao material
    data_inicio = models.DateTimeField(auto_now_add=True)  # Data e hora em que o procedimento foi iniciado

    def __str__(self):
        """
        Retorna uma representação legível do procedimento com o ID do procedimento e o serial do material.
        """
        return f"Procedimento {self.id} - {self.material.serial}"

# EtapaProcesso Model
class EtapaProcesso(models.Model):
    """
    Modelo para representar uma etapa do processo de esterilização.
    Cada etapa é associada a um procedimento e possui informações sobre o status e a data de realização.
    As etapas são divididas em quatro tipos: Recebimento, Lavagem, Esterilização e Distribuição.
    """

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

    procedimento = models.ForeignKey(Procedimento, on_delete=models.CASCADE, related_name='etapas')  # Referência ao procedimento
    etapa = models.CharField(max_length=20, choices=ETAPAS)  # Tipo de etapa
    status = models.CharField(max_length=20, choices=STATUS, default='pendente')  # Status da etapa
    data_realizacao = models.DateTimeField(auto_now_add=True)  # Data de realização da etapa

    class Meta:
        ordering = ['data_realizacao']  # Ordena as etapas pela data de realização

    def __str__(self):
        """
        Retorna uma descrição da etapa, incluindo o serial do material e o status da etapa.
        """
        return f"{self.procedimento.material.serial} - {self.etapa} - {self.status}"

# Falha Model
class Falha(models.Model):
    """
    Modelo para representar uma falha ocorrida em uma etapa do processo.
    Cada falha é associada a uma etapa e contém uma descrição detalhada do problema.
    """

    etapa = models.ForeignKey(EtapaProcesso, on_delete=models.CASCADE, related_name='falhas')  # Referência à etapa do processo
    descricao = models.TextField()  # Descrição detalhada da falha
    data_ocorrencia = models.DateTimeField(auto_now_add=True)  # Data e hora da falha

    def __str__(self):
        """
        Retorna uma descrição legível da falha, incluindo o tipo da etapa e o serial do material.
        """
        return f"Falha na etapa {self.etapa.etapa} - Serial {self.etapa.procedimento.material.serial}"
