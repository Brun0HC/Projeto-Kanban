from rest_framework.response import Response
from rest_framework import status


def BadRequest(message='abstence of parameters'):
    return Response(status=status.HTTP_400_BAD_REQUEST, data={'message':message})

def InternalError(error='error'):
    return Response(data={'message': error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def CreatedRequest(message = 'created'):
    return Response(data={'message':message}, status=status.HTTP_201_CREATED)

def ResponseDefault(message='ok', data={}):
    data['message'] = message
    return Response(status=status.HTTP_200_OK, data=data)