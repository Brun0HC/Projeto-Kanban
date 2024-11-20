from django.shortcuts import render
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.request import Request

# settings
from project.settings import EMAIL_USER

# services
from kanban.services.member import *
from kanban.services.kanban import *
from kanban.services.column import *
from kanban.services.label import *
from kanban.services.card import *
from kanban.services.comment import *

# responses
from kanban.responses import *

# serializers
from kanban.serializer import *

class MemberView(ViewSet):

    queryset = Member.objects.all()
    serializer_class = MemberSerializer

    def create(self, request, *args, **kwargs):
        serializer = MemberSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        exec = createMember(request)
        if "error" in exec:
            return InternalError(error=exec)
        return CreatedRequest()

    def list(self, request, *args, **kwargs):
        return ResponseDefault(listMember())
    
    @action(detail=False, methods=['get'], url_path=r'(?P<kanban_id>\d+)/members', name='List-Members')
    def list_members(self, request, kanban_id=None):
        email = EMAIL_USER
        members_list = listMembersByKanban(email, kanban_id)
        return ResponseDefault(members_list)
    
    @action(detail=False, methods=['get'], name='Profile')
    def profile(self, request):
        email=EMAIL_USER
        exec = retrieveMember(email)
        if 'error' in exec:
            return BadRequest(exec)
        return ResponseDefault(exec)

    @action(detail=False, methods=['patch'], name='Update Profile')
    def update_profile(self, request, *args, **kwargs):
        
        serializer = MemberSerializer(data=request.data, partial = True)
        serializer.is_valid(raise_exception=True)
        email = EMAIL_USER
        exec = updateMember(request, email)
        if 'error' in exec:
            return BadRequest(exec)
        return ResponseDefault(exec)
        
    @action(detail=False, methods=['delete'], name='Delete Profile')
    def delete(self, request):
        email = EMAIL_USER
        exec = deleteMember(email)
        if 'internalerror' in exec:
            return InternalError(error=exec)
        elif 'error' in exec:
            return BadRequest(exec)
        return ResponseDefault(exec)

class KanbanView(ViewSet):
    queryset = Kanban.objects.all()
    serializer_class = KanbanSerializer

    def create(self, request, *args, **kwargs):
        email = EMAIL_USER

        serializer = KanbanSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        exec = createKanban(request, email)
        if 'error' in exec:
            return InternalError(error=exec)
        return CreatedRequest()

    @action(detail=True, methods=['patch'], url_path='update')
    def change(self, request, pk=None, *args, **kwargs):
        email = EMAIL_USER
        
        exec = updateKanban(request, pk, email)
        if 'error' in exec:
            return BadRequest(exec)
        return ResponseDefault(exec)
        
    def list(self, request):
        email = EMAIL_USER
        exec = listKanbans(email)
        if 'error' in exec:
            return BadRequest(exec)
        return ResponseDefault(data=exec)

    def retrieve(self, request, pk=None):
        email = EMAIL_USER
        exec = retrieveKanban(pk, email)
        if 'error' in exec:
            return BadRequest(exec)
        return ResponseDefault(data=exec)

    @action(detail=True, methods=['get'], url_path='filter', name='Filtered-Cards')
    def filter(self, request: Request, pk=None):
        email = EMAIL_USER
        serializer = FilterSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        
        exec = retrieveFilteredKanban(pk,request.query_params, email)
        if 'error' in exec:
            return BadRequest(exec)
        return ResponseDefault(exec)

class ColumnView(ViewSet):
    queryset = Column.objects.all()
    serializer_class = ColumnSerializer

    def create(self, request, *args, **kwargs):
        serializer = ColumnSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        exec = createColumn(request.data)
        if 'error' in exec:
            return InternalError(error=exec)
        return CreatedRequest()

    def list(self, request, *args, **kwargs):
        return ResponseDefault(listColumn())

    def retrieve(self, request, pk=None):
        exec = retrieveColumn(pk)
        if 'error' in exec:
            return BadRequest(exec)
        return ResponseDefault(exec)

    def partial_update(self, request, pk=None, *args, **kwargs):

        serializer = ColumnSerializer(data=request.data, partial = True)
        serializer.is_valid(raise_exception=True)
        exec = updateColumn(request.data, pk)
        if 'error' in exec:
            return BadRequest(exec)
        return ResponseDefault(exec)

    def destroy(self, request, pk=None):

        exec = deleteColumn(pk)
        if 'internalerror' in exec:
            return InternalError(error=exec)
        elif 'error' in exec:
            return BadRequest(exec)
        return ResponseDefault(exec)

class LabelView(ViewSet):

    queryset = Label.objects.all()
    serializer_class = LabelSerializer

    def create(self, request, *args, **kwargs):
        
        serializer = LabelSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        exec = createLabel(request.data)
        if 'error' in exec:
            return InternalError(error=exec)
        return CreatedRequest(exec)

    @action(detail=False, methods=['get'], url_path='listLabels')
    def listLabels(self, request, *args, **kwargs):
        
        kanban_id = request.query_params.get('kanban')
        return ResponseDefault(listLabel(kanban_id))

    def retrieve(self, request, pk=None):
    
        exec = retrieveLabel(pk)
        if 'error' in exec:
            return BadRequest(exec)
        return ResponseDefault(exec)

    def partial_update(self, request, pk=None, *args, **kwargs):
        
        serializer = ColumnSerializer(data=request.data, partial = True)
        serializer.is_valid(raise_exception=True)
        exec = updateLabel(request.data, pk)
        if 'error' in exec:
            return BadRequest(exec)
        return ResponseDefault(exec)
    
    @action(detail=True, methods=['delete'], url_path='delete')
    def delete(self, request, pk=None):
        
        kanban_id = request.query_params.get('kanban')
        exec = deleteLabel(pk, kanban_id)
        if 'internalerror' in exec:
            return InternalError(error=exec)
        elif 'error' in exec:
            return BadRequest(exec)
        return ResponseDefault(exec)

class CardView(ViewSet):

    queryset = Card.objects.all()
    serializer_class = CardSerializer

    def create(self, request, *args, **kwargs):
        
        serializer = CardSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = EMAIL_USER
        exec = createCard(request.data, email)
        if 'error' in exec:
            return InternalError(error=exec.get('error', 'not found error'))
        return CreatedRequest()
        
    @action(detail=False, methods=['post'], name='Link-Card-Label')
    def linkCardLabel(self, request):
        serializer = CardLabelSeriaizer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        exec = linkCardLabel(request.data)
        if 'error' in exec:
            return BadRequest(exec)
        return ResponseDefault(exec)
    
    @action(detail=False, methods=['post'], name='Link-Card-Member')
    def linkCardMember(self, request):
        serializer = CardMemberSeriaizer(data=request.data)
        serializer.is_valid(raise_exception=True)
        exec = linkCardMember(request.data)
        if 'error' in exec:
            return BadRequest(exec)
        return ResponseDefault(exec)

    def list(self, request, *args, **kwargs):
        cards = listCard()
        return ResponseDefault(cards)
       
    @action(detail=True, methods=['get'], url_path='visualize')
    def visualize(self, request, pk=None):
        kanban_id = request.query_params.get('kanban')
        if not kanban_id:
            return BadRequest({"error": "kanban_id is required"})
        email=EMAIL_USER
        exec = retrieveCard(pk, kanban_id, email)
        if 'error' in exec:
            return BadRequest(exec)
        return ResponseDefault(exec)

    def partial_update(self, request, pk=None, *args, **kwargs):
        serializer = CardSerializer(data=request.data, partial = True)
        serializer.is_valid(raise_exception=True)
        exec = updateCard(request.data, pk)
        if 'error' in exec:
            return BadRequest(exec)
        return ResponseDefault(exec)
    
    def destroy(self, request, pk=None):
        exec = deleteCard(pk)
        if 'internalerror' in exec:
            return InternalError(error=exec)
        elif 'error' in exec:
            return BadRequest(exec)
        return ResponseDefault(exec)
        
class CommentView(ViewSet):

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def list(self, request, *args, **kwargs):
        return ResponseDefault(listComments())

    @action(detail=True, methods=['get'], url_path='visualize')
    def visualize(self, request, pk=None):
        email=EMAIL_USER
        exec = visualizeComment(request, email, pk)
        if 'error' in exec:
            return BadRequest(exec)
        return ResponseDefault(exec)
    
    @action(detail=True, methods=['patch'], url_path='change')
    def change(self, request, pk=None):
        serializer = CommentSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        email=EMAIL_USER
        exec = changeComment(request, email, pk)
        if 'error' in exec:
            return BadRequest(exec)
        return ResponseDefault(exec)

    def create(self, request, *args, **kwargs):
        serializer = CommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email=EMAIL_USER
        exec = createComment(request, email)
        if 'error' in exec:
            return BadRequest(exec)
        return CreatedRequest()
    
    @action(detail=True, methods=['delete'], url_path='delete')
    def delete(self, request, pk=None):
        email=EMAIL_USER
        exec = deleteComment(request, email, pk)
        if 'error' in exec:
            return BadRequest(exec)
        return ResponseDefault('Deleted')