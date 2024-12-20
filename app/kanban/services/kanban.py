# Models
from kanban.models import *
from django.forms.models import model_to_dict
from datetime import date

# DJANGO
from django.conf import settings
import os

# settings
from datetime import datetime

from django.db.models import Count, Q
from typing import Optional, Dict, Set, List

def createKanban(dictionary:dict, email:str) -> dict:
    name = dictionary.data.get('name')
    imagem = dictionary.data.get('imagem')
    member = Member.objects.filter(email=email).first()
    if not member:
        return {'error': 'Member not found'}

    try:
        kb = Kanban.objects.create(
            name = name,
            imagem = imagem,
            idMemberCreator = member
        )
        MemberInKanban.objects.create(
            idKanban = kb,
            idMember = member,
            role = "ADMIN"
        )
    except Exception as e:
        return {'error': str(e)}
    return {}

def updateKanban(dictionary: dict, pk: int, email: str):
    member = Member.objects.filter(email=email).first()
    if not member:
        return {'error': 'Member not found'}
    kanban = Kanban.objects.filter(id=pk).first()
    if not kanban:
        return {"error": "kanban not found"}
    if not MemberInKanban.objects.filter(idKanban=kanban, idMember=member).exists:
        return {'errro':'You do not have access to this kanban'}

    name = dictionary.data.get('name')
    imagem = dictionary.data.get('imagem')
    kanban.name = name if name != None else kanban.name
    kanban.imagem = imagem if imagem != None else kanban.imagem
    kanban.save()
    return {'success': 'changed'}

def listKanbans(email) -> dict:
    member = Member.objects.filter(email=email).first()
    if not member:
        return {'error': 'Member not found'}
    # Obtém todos os kanbans do membro
    kanbans = Kanban.objects.filter(memberinkanban__idMember=member)

    kanbans_list = []

    for kanban in kanbans:
        # Converte o kanban em dicionário
        kanban_dict = model_to_dict(kanban, fields=['id', 'name', 'imagem','idMemberCreator'])

        kanban_dict['memberCreator'] = kanban.idMemberCreator.name
        kanban_dict['emailCreator'] = kanban.idMemberCreator.email

        kanbans_list.append(kanban_dict)

    return {"kanbans": kanbans_list}

def get_kanban_with_access_check(kanban_id: int, email: str) -> Optional[Dict]:
    """Verifica se o Kanban e o membro existem e se o membro tem acesso ao Kanban."""
    member = Member.objects.filter(email=email).first()
    if not member:
        return {'error': 'Member not found'}
    kanban = Kanban.objects.filter(id=kanban_id).first()
    if not kanban:
        return {"error": "Kanban not found"}
    exist = MemberInKanban.objects.filter(idKanban=kanban, idMember=member).first()
    if not exist:
        return {'error': 'You do not have access to this Kanban'}
    return {"member": member, "kanban": kanban}

def get_kanban_base_info(kanban: Kanban, member: Member) -> Dict:
    """Retorna as informações base do Kanban."""
    retorno = {
        "kanban": model_to_dict(kanban, fields=['id', 'name', 'imagem', 'idMemberCreator']),
        "columns": []
    }
    retorno["kanban"]["memberCreator"] = kanban.idMemberCreator.name
    retorno["kanban"]["emailCreator"] = kanban.idMemberCreator.email
    retorno["kanban"]["memberRole"] = MemberInKanban.objects.filter(idKanban=kanban, idMember=member).values('role')
    retorno["kanban"]["labels"] = Label.objects.filter(idKanban=kanban).values()


    return retorno

def get_columns_and_cards(kanban: Kanban, card_ids: Optional[Set[int]] = None) -> List[Dict]:
    """Obtém as colunas e os cartões do Kanban, filtrando se necessário."""
    columns = Column.objects.filter(idKanban=kanban).order_by("position")
    columns_list = []

    for column in columns:
        column_dict = model_to_dict(column, fields=["uuid",'id', 'name', "position"])
        column_dict['idKanban'] = column.idKanban_id

        # Obter todos os cartões da coluna, filtrando se card_ids estiver definido
        cards_query = Card.objects.filter(column=column)
        if card_ids is not None:
            cards_query = cards_query.filter(id__in=card_ids)

        cards = cards_query.select_related('idMemberCreator').order_by('position')
        card_dicts = []

        for card in cards:
            card_dict = model_to_dict(card, fields=["uuid", "id", "title", "textDescription", 'position'])
            card_dict["creator"] = card.idMemberCreator.name if card.idMemberCreator else None
            card_dict["creator_email"] = card.idMemberCreator.email if card.idMemberCreator else None

            # Labels dos cartões
            card_labels = CardLabel.objects.filter(card=card).select_related('label').values(
                "label__id", "label__text", "label__color"
            )
            card_dict["labels"] = list(card_labels)

            # Membros dos cartões
            card_members = CardMember.objects.filter(card=card).select_related('member').values(
                "member__name", "member__email"
            )
            card_dict["members"] = list(card_members)
            card_dict["comments"] = Comment.objects.filter(idCard=card).values()

            card_dicts.append(card_dict)

        column_dict['items'] = card_dicts
        columns_list.append(column_dict)

    return columns_list

def retrieveKanban(id: int, email:str) -> dict:
    """Recupera o Kanban com todos os dados relevantes."""
    access_check = get_kanban_with_access_check(id, email)
    if 'error' in access_check:
        return access_check

    kanban = access_check["kanban"]
    member = access_check["member"]

    retorno = get_kanban_base_info(kanban, member)
    retorno["columns"] = get_columns_and_cards(kanban)

    return retorno

def filterCards(dictionary: dict) -> set:
    nome = dictionary.get('nome')
    id_label = dictionary.get('id_label')
    member = Member.objects.filter(name=nome).first()
    label = Label.objects.filter(id=id_label).first()

    card_ids = set()

    if nome is not None:
        member = Member.objects.filter(name=nome).first()
        if member is not None:
            member_card_ids = set(CardMember.objects.filter(member=member).values_list('card', flat=True))
            card_ids = member_card_ids if not card_ids else card_ids.intersection(member_card_ids)

    if id_label is not None:
        label = Label.objects.filter(id=id_label).first()
        if label is not None:
            label_card_ids = set(CardLabel.objects.filter(label=label).values_list('card', flat=True))
            card_ids = label_card_ids if not card_ids else card_ids.intersection(label_card_ids)

    return card_ids

def retrieveFilteredKanban(kanban_id: int, filters: dict, email) -> dict:
    """Recupera o Kanban com filtragem de cards."""
    access_check = get_kanban_with_access_check(kanban_id, email)
    if 'error' in access_check:
        return access_check

    kanban = access_check["kanban"]
    member = access_check["member"]

    card_ids = filterCards(filters)
    retorno = get_kanban_base_info(kanban, member)
    retorno["columns"] = get_columns_and_cards(kanban, card_ids)

    return retorno

def deleteKanban(pk: int) -> dict:
    kanban = Kanban.objects.filter(pk=pk).first()
    if kanban:
        kanban.delete()
        return {'success': 'deleted'}
    return {'error': 'kanban not found'}