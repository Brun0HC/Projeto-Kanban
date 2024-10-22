from django.urls import path, include

# VIEW
from .views import *
from rest_framework import routers

def getRouter():
    # middleware
    return routers.DefaultRouter(trailing_slash=False)

router = getRouter()
router.register(r'member', MemberView)
router.register(r'kanban', KanbanView)
router.register(r'column', ColumnView)
router.register(r'label', LabelView)
router.register(r'card', CardView)
router.register(r'comment', CommentView)


urlpatterns = [
    path('', include(router.urls)),
]