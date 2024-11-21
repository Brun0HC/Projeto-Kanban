# Models
from django.forms import model_to_dict
from kanban.models import Kanban, Label

def findLabel(id):
    try:
        label = Label.objects.filter(id=id).first()
        return label
    except Label.DoesNotExist:
        return None

def createLabel(dictionary:dict) -> dict:
    text = dictionary.get('text')
    color = dictionary.get('color')
    idKanban = dictionary.get('idKanban')
    kb = Kanban.objects.filter(pk=idKanban).first()
    if not kb:
        return {'error': 'Kanban not found'}
    try:
        lb = Label.objects.create(
            text = text,
            color = color,
            idKanban=kb
        )
        
    except Exception as e:
        return {'error':f'Error while creating Label: {str(e)}'}
    return {'id': lb.pk}

def updateLabel(dictionary: dict, id: int) -> dict:
    text = dictionary.get('text')
    color = dictionary.get('color')

    label = findLabel(id)
    if not label:
        return {"error": "label not found"}

    try:
        label.text = text if text != None else label.text
        label.color = color if color != None else label.color
        label.save()
    except Exception as e:
        return {'error': str(e)}
    return {'success': 'updated'}

def listLabel(kanban_id: int) -> dict:

    kanban=Kanban.objects.filter(id=kanban_id).first()
    if not kanban:
        return {"error":'Kanban not found'}
    labels= Label.objects.filter(idKanban=kanban).values(
        "id",
        "text",
        "color"
    )
    return {
        "labels": labels
    }

def retrieveLabel(id: int) -> dict:
    label = findLabel(id)

    if not label:
        return {"error": "label not found"}
    
    return {'label': model_to_dict(label)}

def deleteLabel(id: int, kanban_id: int) -> dict:
    label = findLabel(id)
    kanban = Kanban.objects.filter(id=kanban_id).first()
    if not kanban:
        return {'error':"kanban not found"}
    if not label:
        return {"error": "label not found"}

    try:
        label.delete()
    except Exception as e:
        return {'error': f'Error when trying to delete label: {str(e)}'}
    
    return {'success': 'deleted'}