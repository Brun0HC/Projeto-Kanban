# Models
from kanban.models import *
from django.db.models import Max

# Django
from django.forms.models import model_to_dict

def findColumn(id: int) -> Column:
    try:
        return Column.objects.get(pk=id)
    except Column.DoesNotExist:
        return None
    
def createColumn(dictionary: dict) -> dict:
    uuid = dictionary.get('uuid')
    name = dictionary.get('name')
    idKanban = dictionary.get('idKanban')
    kanban = Kanban.objects.filter(id=idKanban).first()

    max_position = Column.objects.filter(idKanban=kanban).aggregate(Max('position'))['position__max']
    # Define o `position` da nova coluna
    new_position = 0 if max_position is None else max(max_position + 1, 0)

    try:
        Column.objects.create(
            uuid=uuid,
            name = name,
            idKanban = kanban,
            position = new_position
            )
    except Exception as e:
        return {'error': f'Failed to create Column: {str(e)}'}
    return {'success': 'created'}

def listColumn() -> dict:
    return {
        "items": Column.objects.all().values()
    }

def updateColumn(dictionary: dict, id: int) -> dict:
    column = findColumn(id)
    if not column:
        return {"error": "Column not found"}
    
    name = dictionary.get('name')
    new_position = dictionary.get('position')

    try:
        if new_position != None:
            if new_position > Column.objects.filter(idKanban=column.idKanban).count():
                return {"error": "position is bigger than total of columns"}
            # Alterar todos que estão naquela posição
            old_position = column.position #1
            column.position = new_position #2
            column.save()
            if new_position > old_position:
                columns = Column.objects.filter(idKanban=column.idKanban, position__lte=new_position, position__gte=old_position).exclude(pk=column.pk).order_by('position')
            else:
                columns = Column.objects.filter(idKanban=column.idKanban, position__gte=new_position, position__lte=old_position).exclude(pk=column.pk).order_by('position')
            
            for col in columns:
                col.position += 1 if new_position < old_position else -1
                col.save()

        column.name = name if name != None else column.name
        column.save()
    except Exception as e:
        return {'error': str(e)}
    return {"success": "changed"}

def retrieveColumn(id: int) -> dict:
    column = findColumn(id)
    if not column:
        return {"error": "Column not found"}

    column_data = model_to_dict(column, fields=['uuid','name', 'idKanban'])
    column_data['idKanban'] = column.idKanban_id

    # Obter os cartões (cards) na coluna
    cards = Card.objects.filter(column=column).values(
        'id', 'title', 'idMemberCreator_id', 'textDescription', 'position'
    ).order_by('position')

    # Adicionar informações detalhadas para cada cartão
    detailed_cards = []
    for card in cards:
        card_id = card['id']
        card_labels = Label.objects.filter(cardlabel__card_id=card_id).values('id', 'text', 'color')
        card_members = Member.objects.filter(cardmember__card_id=card_id).values('id', 'name', 'email')
        
        detailed_card = {
            'id': card['id'],
            'uuid': card['uuid'],
            'title': card['title'],
            'idMemberCreator': card['idMemberCreator_id'],
            'textDescription': card['textDescription'],
            'labels': list(card_labels),
            'members': list(card_members),
            'position':card['position']
        }
        detailed_cards.append(detailed_card)

    column_data['cards'] = detailed_cards

    return {"item": column_data}


def deleteColumn(id: int) -> dict:
    column = findColumn(id)
    if not column:
        return {"error": "Column not found"}
    try:
        column.delete()
        return {'success': 'Column deleted'}
    except Exception as e:
        return {'internalerror': f'Error while deleting Column: {str(e)}'}