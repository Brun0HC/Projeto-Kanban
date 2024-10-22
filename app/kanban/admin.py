from django.contrib import admin
from kanban.models import *
# Register your models here.

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('pk','name', 'email')
    search_fields = ('name', 'email')

@admin.register(Kanban)
class KanbanAdmin(admin.ModelAdmin):
    list_display = ('pk','name', 'idMemberCreator')
    search_fields = ('name',)
    list_filter = ('idMemberCreator',)

@admin.register(MemberInKanban)
class MemberInKanbanAdmin(admin.ModelAdmin):
    list_display = ('idKanban', 'idMember', 'role')
    list_filter = ('role',)

@admin.register(Column)
class ColumnAdmin(admin.ModelAdmin):
    list_display = ('pk','name', 'idKanban', 'position')
    list_filter = ('idKanban',)
    search_fields = ('name','idKanban')

@admin.register(Label)
class LabelAdmin(admin.ModelAdmin):
    list_display = ('pk', 'idKanban', 'text', 'color')
    search_fields = ('text','idKanban',)

@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('pk','title', 'idMemberCreator','column', 'position', 'created_at')
    search_fields = ('title', 'textDescription')
    list_filter = ('column__idKanban', 'idMemberCreator')

@admin.register(CardMember)
class CardMemberAdmin(admin.ModelAdmin):
    list_display = ('card', 'member')
    search_fields = ('card', 'member')

@admin.register(CardLabel)
class CardLabelAdmin(admin.ModelAdmin):
    list_display = ('card', 'label')
    search_fields = ('card','label')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk','text', 'idMember', 'idCard')
    search_fields = ('text','idMember')
    list_filter = ('idMember',)

