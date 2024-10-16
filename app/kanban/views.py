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
