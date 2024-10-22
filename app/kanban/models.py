from django.db import models
from django.utils import timezone
from datetime import timedelta


def get_default_due_date():
    return timezone.now() + timedelta(days=2)


# Create your models here.
class Member(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    phone = models.CharField(max_length=15 ,default='99999999999')
    
    def __str__(self):
        return self.name

class Kanban(models.Model):
    name = models.CharField(max_length=255)
    imagem = models.CharField(max_length=255, null=True, blank=True, default=None)
    image_file = models.CharField(max_length=255, null=True, blank=True, default=None)
    idMemberCreator = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

class MemberInKanban(models.Model):
    idKanban = models.ForeignKey(Kanban, on_delete=models.CASCADE)
    idMember = models.ForeignKey(Member, on_delete=models.CASCADE)
    role = models.CharField(choices=[("GUEST","Guest"), ("ADMIN","Admin")], default="GUEST", max_length=6)

    def __str__(self):
        return f"{self.idMember.name} in {self.idKanban.name} as {self.role}"

class Column(models.Model):
    name = models.CharField(max_length=255)
    idKanban = models.ForeignKey(Kanban, on_delete=models.CASCADE)
    position = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Label(models.Model):
    text = models.CharField(max_length=255)
    color = models.CharField(max_length=255)
    idKanban = models.ForeignKey(Kanban, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.text

class Card(models.Model):
    title = models.CharField(max_length=255)
    idMemberCreator = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True)
    textDescription = models.TextField(blank=True, null=True)
    column = models.ForeignKey(Column, on_delete=models.CASCADE, default=None)
    created_at = models.DateTimeField(auto_now=True)
    position = models.IntegerField(default=0)
    start = models.DateField(auto_now_add=True)
    due = models.DateField(auto_now_add=get_default_due_date)
    concluded = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class CardLabel(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    label = models.ForeignKey(Label, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.card.title} - {self.label.text}"

class CardMember(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.member.name} in {self.card.title}"

class Comment(models.Model):
    text = models.TextField(default=None, null=True, blank=True)
    idMember = models.ForeignKey(Member, on_delete=models.CASCADE)
    idCard = models.ForeignKey(Card, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment by {self.idMember.name} on {self.idCard.title}"

