# Models
from kanban.models import *
from django.db.models import Max

# Django
from django.forms.models import model_to_dict
from django.db import transaction


def findCard(id):
    try:
        return Card.objects.get(pk=id)
    except Card.DoesNotExist:
        return None

def createCard(dictionary: dict, email) -> dict:
    uuid = dictionary.get('uuid')
    title = dictionary.get('title')
    columnId = dictionary.get('column')
    textDescription = dictionary.get('textDescription')
    id_creator = Member.objects.filter(email=email).first()
    if not id_creator:
        return {'error': 'Member not found'}
    
    column = Column.objects.filter(id=columnId).first()
    if not column:
        return {'error': 'Column not found'}
    
    
    max_position = Card.objects.filter(column=column).aggregate(Max('position'))['position__max']

    # Define o `position` do card
    new_position = 0 if max_position is None else max(max_position + 1, 0)

    try:
        new_card =Card.objects.create(
            uuid=uuid,
            title = title,
            idMemberCreator = id_creator,
            textDescription = textDescription,
            column=column,
            position = new_position
            )      
    except Exception as e:
        return {'error': f'Failed to create Card: {str(e)}'}
    return {"card": new_card.uuid}

def linkCardMember(dictionary: dict) -> dict:
    card_id = dictionary.get('id_card')
    member_email = dictionary.get('member_email')

    card = Card.objects.filter(id=card_id).first()
    member = Member.objects.filter(email=member_email).first()
    card_linked = CardMember.objects.filter(card=card, member=member).first()
    if card_linked:
        card_linked.delete()
        return {'success': 'unlinked'}
    if not card:
        return {'error': "Card not found"}

    if not member:
        return {'error': "Member not found"}
    
    try:
        CardMember.objects.create(
            card=card,
            member=member
        )
    except Exception as e:
        return {'error': f'Internal error: {str(e)}'}
    return {'success': 'card-member updated'}

def listCard() -> dict:
    return {
        "items": Card.objects.all().values()
    }

def updateCard(dictionary: dict, id: int) -> dict:
    title = dictionary.get('title')
    textDescription = dictionary.get('textDescription')
    new_position = dictionary.get('position')
    concluded = dictionary.get('concluded', None)
    if concluded != None:
        concluded = bool(concluded)
    card = findCard(id)

    if not card:
        return {"error": "card not found"}
    
    id_column = dictionary.get('column', card.column.pk)
    if id_column != None:
        column = Column.objects.filter(pk=id_column).first()
        if not column:
            return {'error': 'Column not found'}
    try:
        if new_position is not None:
            if new_position > Card.objects.filter(column=column).count():
                return {"error": "position is bigger than total of cards in the column"}

            if column == card.column:
                # Movendo dentro da mesma coluna
                old_position = card.position

                if new_position > old_position:
                    cards = Card.objects.filter(column=column, position__gte=old_position, position__lte=new_position).exclude(pk=card.pk).order_by('position')
                    for c in cards:
                        c.position -= 1
                        c.save()
                else:
                    cards = Card.objects.filter(column=column, position__lte=old_position, position__gte=new_position).exclude(pk=card.pk).order_by('position')
                    for c in cards:
                        c.position += 1
                        c.save()
            else:
                # Movendo para outra coluna
                old_column = card.column
                old_position = card.position

                cards_in_old_column = Card.objects.filter(column=old_column, position__gte=old_position).exclude(pk=card.pk).order_by('position')
                for c in cards_in_old_column:
                    c.position -= 1
                    c.save()

                cards_in_new_column = Card.objects.filter(column=column, position__gte=new_position).order_by('position')
                for c in cards_in_new_column:
                    c.position += 1
                    c.save()

            card.position = new_position

        card.concluded = concluded if concluded != None else card.concluded
        card.title = title if title != None else card.title
        card.column = column if column != None else card.column
        card.textDescription = textDescription if textDescription != None else card.textDescription           
        card.save()
    except Exception as e:
        return {'error': str(e)}
    return {'success': 'updated'}

def retrieveCard(id: int, kanban_id: int, email: str) -> dict:
    card = findCard(id)
    if not card:
        return {"error": "card not found"}
    
    member = Member.objects.filter(email=email).first()
    if not member:
        return {"error": "member not found"}
    kanban=Kanban.objects.filter(id=kanban_id).first()
    if not kanban:
        return {'error':'kanban not found'}
    
    is_member_in_kanban = MemberInKanban.objects.filter(idMember=member, idKanban=kanban).exists()
    if not is_member_in_kanban:
        return {"error": "member does not have access to this kanban"}
        
    modelCard = model_to_dict(card, fields=['id', 'title', 'idMemberCreator', 'textDescription', 'position', 'concluded'])
    modelCard['created_at'] = card.created_at.isoformat() if card.created_at else None
    modelCard['memberCreator_name'] = card.idMemberCreator.name
    modelCard['column'] = card.column.name
    
    # Labels
    modelCard['labels'] = CardLabel.objects.filter(card=card).values(
        "label__id",
        "label__text",
        "label__color"
    )
    # Members
    modelCard['members'] = CardMember.objects.filter(card=card).values(
        "member__name",
        "member__email"
    )
    # Comments
    modelCard["comments"] = Comment.objects.filter(idCard=card).values(
        'id',
        "idMember__email",
        "idMember__name",
        "text",
        "created_at"
    ).order_by('-created_at')
    return {"item": modelCard} # card

def deleteCard(id: int) -> dict:
    card = findCard(id)
    if not card:
        return {"error": "card not found"}
    try:
        column = card.column

        with transaction.atomic(): 
            # Atualizar as posições dos cards restantes na coluna
            remaining_cards = Card.objects.filter(column=column, position__gt=card.position).order_by('position')
            card.delete()
            for card in remaining_cards:
                card.position -= 1 
                card.save()

        return {"success": "Card deleted"}
    except Exception as e:
        return {'internalerror': f'Error while deleting card: {str(e)}'}

def linkCardLabel(dictionary: dict) -> dict:
    id_card = dictionary.get('id_card')
    id_label = dictionary.get('id_label')

    try:
        card = Card.objects.filter(id=id_card).first()
        label = Label.objects.filter(id=id_label).first()
        exists = CardLabel.objects.filter(card=card, label=label).first()
        if not exists:
            CardLabel.objects.create(card=card, label=label)
        return {'success': 'card-label linked'}
    except Exception as e:
        return {'error': f'Erro to link label with card: {str(e)}'}
    
def unlinkCardLabel(dictionary: dict) -> dict:
    id_card = dictionary.get('id_card')
    id_label = dictionary.get('id_label')

    card = Card.objects.filter(id=id_card).first()
    label = Label.objects.filter(id=id_label).first()
    exists = CardLabel.objects.filter(card=card, label=label).first()
    if exists:
        try:
            exists.delete()
            return {'success':"unlinked"}
        except Exception as e:
            return {'error': str(e)}
    return {}
    
    