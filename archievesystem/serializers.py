from rest_framework import serializers
from .models import InternalEntity, InternalDepartment, ExternalEntity, ExternalDepartment, Document


class EntityTypeSerializer(serializers.Serializer):
    entity_type = serializers.ChoiceField(choices=[('internal', 'Internal'), ('external', 'External')])

class InternalEntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = InternalEntity
        fields = ['name']

class InternalDepartmentSerializer(serializers.ModelSerializer):
    internal_entity = serializers.CharField()

    class Meta:
        model = InternalDepartment
        fields = ['name','internal_entity']

class ExternalEntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExternalEntity
        fields = ['name']

class ExternalDepartmentSerializer(serializers.ModelSerializer):
    external_entity = serializers.CharField()
    class Meta:
        model = ExternalDepartment
        fields = ['name','external_entity']





class GetDocumentSerializer(serializers.ModelSerializer):
    internal_entity = InternalEntitySerializer()
    internal_department= InternalDepartmentSerializer()
    external_entity = ExternalEntitySerializer()
    external_department = ExternalDepartmentSerializer()
    
    class Meta:
        model = Document
        fields = '__all__'


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'

    def validate(self, data):
        entity_type = data.get('entity_type')
        internal_entity = data.get('internal_entity')
        internal_department = data.get('internal_department')
        external_entity = data.get('external_entity')
        external_department = data.get('external_department')

        # التحقق من صحة البيانات بناءً على entity_type
        if entity_type == 'internal':
            if not internal_entity or not internal_department:
                raise serializers.ValidationError("Internal entity and internal department are required for internal documents.")
            if external_entity or external_department:
                raise serializers.ValidationError("External entity and external department are not allowed for internal documents.")
        elif entity_type == 'external':
            if not external_entity or not external_department:
                raise serializers.ValidationError("External entity and external department are required for external documents.")
            if internal_entity or internal_department:
                raise serializers.ValidationError("Internal entity and internal department are not allowed for external documents.")

        return data