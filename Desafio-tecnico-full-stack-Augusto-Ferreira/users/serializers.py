from rest_framework import serializers
from .models import EtapaProcesso, Falha, Material, Procedimento, User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'role']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class UserRoleUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['role']

class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = ['id', 'nome', 'tipo', 'data_validade', 'serial']


class EtapaProcessoSerializer(serializers.ModelSerializer):
    serial = serializers.CharField(write_only=True)

    class Meta:
        model = EtapaProcesso
        fields = ['id', 'serial', 'etapa', 'status', 'data_realizacao']
        read_only_fields = ['status', 'data_realizacao']

    def validate(self, data):
        serial = data.get('serial')
        etapa = data.get('etapa')

        try:
            material = Material.objects.get(serial=serial)
        except Material.DoesNotExist:
            raise serializers.ValidationError({'serial': 'Material não encontrado com esse serial.'})

        # Busca o último procedimento
        procedimento = material.procedimentos.order_by('-data_inicio').first()

        # Se não existir ou estiver completo, inicia novo
        if not procedimento or procedimento.etapas.count() >= 4:
            procedimento = Procedimento.objects.create(material=material)

        # Define qual é a próxima etapa obrigatória
        ordem_etapas = ['recebimento', 'lavagem', 'esterilizacao', 'distribuicao']
        etapas_realizadas = list(procedimento.etapas.values_list('etapa', flat=True))

        proxima_etapa = ordem_etapas[len(etapas_realizadas)] if len(etapas_realizadas) < 4 else None

        if etapa != proxima_etapa:
            raise serializers.ValidationError({'etapa': f'A próxima etapa deve ser: {proxima_etapa}'})

        # Definir status baseado na etapa atual
        if etapa == 'recebimento':
            status = 'pendente'
        elif etapa in ['lavagem', 'esterilizacao']:
            status = 'em_andamento'
        elif etapa == 'distribuicao':
            status = 'concluida'
        else:
            status = 'pendente'  # fallback seguro

        # Adiciona manualmente ao validated_data
        data['status'] = status
        data['procedimento'] = procedimento
        return data

    def create(self, validated_data):
        validated_data.pop('serial')  # Já usamos
        return super().create(validated_data)

class FalhaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Falha
        fields = ['id', 'descricao', 'data_ocorrencia', 'etapa']