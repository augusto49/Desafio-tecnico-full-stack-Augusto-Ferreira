from rest_framework import serializers
from .models import EtapaProcesso, Falha, Material, Procedimento, User

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo User, utilizado para criar, visualizar e atualizar usuários.
    
    Campos:
        - id: Identificador único do usuário.
        - username: Nome de usuário.
        - email: Endereço de e-mail.
        - password: Senha do usuário (somente para escrita).
        - role: Função do usuário (ex: técnico, enfermagem, administrativo).

    Métodos:
        - create: Cria um novo usuário, utilizando a função `create_user` do modelo User para criar o usuário com senha segura.
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'role']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """
        Cria um usuário utilizando os dados validados.
        A senha do usuário será tratada com segurança usando o método `create_user`.
        """
        user = User.objects.create_user(**validated_data)
        return user


class UserRoleUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer para atualizar apenas o campo 'role' (função) de um usuário.
    Utilizado em operações onde o papel de um usuário precisa ser alterado.

    Campos:
        - role: Função do usuário.
    """
    class Meta:
        model = User
        fields = ['role']


class MaterialSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo Material, utilizado para manipular informações de materiais.

    Campos:
        - id: Identificador único do material.
        - nome: Nome do material.
        - tipo: Tipo do material.
        - data_validade: Data de validade do material.
        - serial: Serial único do material.

    Esse serializer permite criar e visualizar os materiais.
    """
    class Meta:
        model = Material
        fields = ['id', 'nome', 'tipo', 'data_validade', 'serial']


class EtapaProcessoSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo EtapaProcesso, utilizado para manipular as etapas do processo de esterilização dos materiais.

    Campos:
        - id: Identificador único da etapa.
        - serial: Serial do material (campo somente de escrita).
        - etapa: Etapa do processo (ex: recebimento, lavagem, esterilização, distribuição).
        - status: Status da etapa (pendente, em andamento, concluída).
        - data_realizacao: Data e hora de realização da etapa.

    Métodos:
        - validate: Valida as etapas do processo, garantindo que a ordem das etapas seja respeitada.
        - create: Cria uma nova etapa para o processo de esterilização.
    """
    serial = serializers.CharField(write_only=True)

    class Meta:
        model = EtapaProcesso
        fields = ['id', 'serial', 'etapa', 'status', 'data_realizacao']
        read_only_fields = ['status', 'data_realizacao']

    def validate(self, data):
        """
        Valida as informações antes de criar ou atualizar a etapa do processo.
        
        A validação verifica:
            - Se o serial informado existe na base de dados.
            - Se a etapa do processo está na ordem correta.
            - Se a etapa pode ser realizada, de acordo com a etapa anterior.
        """
        serial = data.get('serial')
        etapa = data.get('etapa')

        # Verifica se o material existe com o serial informado
        try:
            material = Material.objects.get(serial=serial)
        except Material.DoesNotExist:
            raise serializers.ValidationError({'serial': 'Material não encontrado com esse serial.'})

        # Recupera o procedimento mais recente do material
        procedimento = material.procedimentos.order_by('-data_inicio').first()

        # Caso o procedimento não exista ou já tenha passado por todas as etapas, cria um novo procedimento
        if not procedimento or procedimento.etapas.count() >= 4:
            procedimento = Procedimento.objects.create(material=material)

        # Define a ordem das etapas
        ordem_etapas = ['recebimento', 'lavagem', 'esterilizacao', 'distribuicao']
        etapas_realizadas = list(procedimento.etapas.values_list('etapa', flat=True))

        # Define a próxima etapa esperada com base nas etapas já realizadas
        proxima_etapa = ordem_etapas[len(etapas_realizadas)] if len(etapas_realizadas) < 4 else None

        # Verifica se a etapa fornecida é a próxima etapa na ordem
        if etapa != proxima_etapa:
            raise serializers.ValidationError({'etapa': f'A próxima etapa deve ser: {proxima_etapa}'})

        # Define o status com base na etapa
        if etapa == 'recebimento':
            status = 'pendente'
        elif etapa in ['lavagem', 'esterilizacao']:
            status = 'em_andamento'
        elif etapa == 'distribuicao':
            status = 'concluida'
        else:
            status = 'pendente'

        data['status'] = status
        data['procedimento'] = procedimento
        return data

    def create(self, validated_data):
        """
        Cria uma nova etapa, removendo o serial do validated_data antes de chamar o método `create`.
        """
        validated_data.pop('serial')
        return super().create(validated_data)


class FalhaSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo Falha, utilizado para registrar falhas nas etapas do processo de esterilização.

    Campos:
        - id: Identificador único da falha.
        - descricao: Descrição da falha ocorrida.
        - data_ocorrencia: Data e hora em que a falha ocorreu.
        - etapa: Etapa do processo onde a falha ocorreu.
    """
    class Meta:
        model = Falha
        fields = ['id', 'descricao', 'data_ocorrencia', 'etapa']
