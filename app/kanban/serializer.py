from rest_framework import serializers
from email_validator import validate_email as validEmail, EmailNotValidError
from django.core.validators import MinValueValidator
from kanban.models import Column

class MemberSerializer(serializers.Serializer):
    name = serializers.CharField()
    email = serializers.EmailField()
    phone = serializers.CharField(required=False)

    def validate_email(self, value, **kwargs):
        errors = kwargs.get('errors', [])
        
        try:
            emailinfo = validEmail(value, check_deliverability=True)
            value = emailinfo.normalized

        except EmailNotValidError as err:
            errors.append(str(err))
        if len(errors) > 0:
            print(errors)
            raise serializers.ValidationError(errors)
        return value

class KanbanSerializer(serializers.Serializer):
    name = serializers.CharField()
    imagem = serializers.CharField(required=False)

class ColumnSerializer(serializers.Serializer):
    uuid = serializers.CharField()
    name = serializers.CharField(required=False)
    position = serializers.IntegerField(required=False, validators=[MinValueValidator(0)])
    idKanban = serializers.IntegerField(validators=[MinValueValidator(0)])

class CardSerializer(serializers.Serializer):
    uuid = serializers.CharField()
    title = serializers.CharField(max_length=255)
    column = serializers.IntegerField(validators=[MinValueValidator(0)])
    position = serializers.IntegerField(required=False, validators=[MinValueValidator(0)])
    textDescription = serializers.CharField(allow_blank=True, required=False)
    concluded = serializers.BooleanField(required=False)

class FilterSerializer(serializers.Serializer):
    nome = serializers.CharField(required=False)
    id_label = serializers.IntegerField(required=False, validators=[MinValueValidator(0)])

class LabelSerializer(serializers.Serializer):
    text = serializers.CharField()
    color = serializers.CharField()
    idKanban = serializers.IntegerField(required=False, validators=[MinValueValidator(0)])
    
class CommentSerializer(serializers.Serializer):
    text = serializers.CharField(required=False)
    idCard = serializers.IntegerField(validators=[MinValueValidator(0)])

class CardLabelSeriaizer(serializers.Serializer):
    id_card = serializers.IntegerField(validators=[MinValueValidator(0)])
    id_label = serializers.IntegerField(validators=[MinValueValidator(0)])

class CardMemberSeriaizer(serializers.Serializer):
    id_card = serializers.IntegerField(validators=[MinValueValidator(0)])
    member_email = serializers.CharField()
