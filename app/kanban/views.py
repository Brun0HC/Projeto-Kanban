from django.shortcuts import render

# settings
from project.settings import EMAIL_USER

# services
from kanban.services.member import *

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
