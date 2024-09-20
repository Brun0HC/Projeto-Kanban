from django.forms import model_to_dict
from kanban.models import Card, Comment, Kanban, Member, MemberInKanban

# DJANGO 
from django.conf import settings
import os
import requests

# settings
from datetime import datetime


def listComments() -> dict:
    return {'comments': Comment.objects.all().values()}

def visualizeComment(request,email, pk) -> dict:
    comment = Comment.objects.filter(id=pk).first()
    if not comment:
        return {'error': 'comment not found'}
    kanban_id = request.query_params.get('kanban')
    member = Member.objects.filter(email=email).first()
    if not member:
        return {'error':'You are not a member'}
    kanban=Kanban.objects.filter(id=kanban_id).first()
    if not kanban:
        return {"error":'Kanban not found'}
    is_member_in_kanban = MemberInKanban.objects.filter(idMember=member, idKanban=kanban).exists()
    if not is_member_in_kanban:
        return {'error':"member does not have access to this kanban"}
    
    return model_to_dict(comment)

def changeComment(request, email, pk):
    kanban_id = request.query_params.get('kanban')
    text = request.data.get('text')
    
    belongs = Member.objects.filter(email=email).first()
    kanban = Kanban.objects.filter(id=kanban_id).first()
    if not kanban:
        return {'error':"You are not in this kanban"}
    
    is_member_in_kanban = MemberInKanban.objects.filter(idMember=belongs, idKanban=kanban).exists()
    if not is_member_in_kanban:
        return {"error": "member does not have access to this kanban"}
    comment = Comment.objects.filter(id=pk).first()
    if comment.idMember != belongs:
        return {'error':"You can't change this comment"}
    if not comment:
        return {"error":'comment not found'}

    try:
        comment.text = text if text != None else comment.text       
        comment.save()
    except Exception as e:
        return {"error":str(e)}
    return {'seccess': 'changed'}

def createComment(request, email) -> dict:
    text = request.data.get('text')
    member = Member.objects.filter(email=email).first()
    if not member:
        return {"error":'Member not found'}
    cardId = request.data.get('idCard')
    card = Card.objects.filter(id=cardId).first()
    if not card:
        return {"error":'card not found'}
    try:
        comment = Comment.objects.create(text=text, idMember= member, idCard=card)
        return {'success': 'created'}
    except Exception as e:
        return {"error":str(e)}
    
def deleteComment(request, email, pk) -> dict:
    kanban_id = request.query_params.get('kanban')
    belongs = Member.objects.filter(email=email).first()
    kanban = Kanban.objects.filter(id=kanban_id).first()
    if not kanban:
        return {'error':"You are not in this kanban"}
    
    is_member_in_kanban = MemberInKanban.objects.filter(idMember=belongs, idKanban=kanban).exists()
    if not is_member_in_kanban:
        return {"error": "member does not have access to this kanban"}
    comment = Comment.objects.filter(pk=pk).first()
    if comment.idMember != belongs:
        return {'error':"You can't delete this comment"}
    if not comment:
        return {'error':'comment not found'}
    comment.delete()
    return {'success':'deleted'}


