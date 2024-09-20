# MODELS
from kanban.models import Member, MemberInKanban
from django.forms import model_to_dict

# DJANGO
from django.conf import settings
import os
import requests

# settings
from datetime import datetime

def createMember(dictionary: dict) -> dict:
    name = dictionary.data.get('name')
    email = dictionary.data.get('email')
    phone = dictionary.data.get('phone')

    member = Member.objects.filter(email=email).first()
    if member:
        return {'error': 'Member already exists'}
    
    try:
        member = Member.objects.create(
            name=name,
            email=email,
            phone=phone
        )
    except Exception as e:
        return {'error': str(e)}
    return {'success': 'created'}

def listMember():
    return {
        'members': Member.objects.all().values()
    }

def listMembersByKanban(email, pk: int) -> dict:
    user = Member.objects.filter(email=email).first()
    in_kanban = MemberInKanban.objects.filter(idMember=user).first()
    if not in_kanban:
        return {'error': 'You are not a member of this Kanban'}

    member_ids_in_kanban = MemberInKanban.objects.filter(idKanban=pk).values_list('idMember', flat=True)
    members = Member.objects.filter(id__in=member_ids_in_kanban).values('id', 'name', 'email',"image")
    return {'members': list(members)}

def updateMember(dictionary: dict, email: str) -> dict:
    name = dictionary.data.get('name')
    phone = dictionary.data.get('phone')
    member = Member.objects.filter(email=email).first()
    if not member:
        return {'error': 'Member not found'}
    try:
        member.name = name if name != None else member.name
        member.phone = phone if phone != None else member.phone
        member.save()
    except Exception as e:
        
        return {'error': str(e)}
    return {'success': 'updated'}

def retrieveMember(email: str) -> dict:
    member = Member.objects.filter(email=email).first()

    if not member:
        return {"error": "member not found"}
    
    return {'member': model_to_dict(member)}

def deleteMember(email: str) -> dict:
    member = Member.objects.filter(email=email).first()

    if not member:
        return {"error": "member not found"}
    
    try:
        member.delete()
    except Exception as e:
        
        return {'error': f'Error when trying to delete member: {str(e)}'}
    
    return {'success': 'deleted'}