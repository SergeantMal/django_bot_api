from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import TGUser
from .serializers import TGUserSerializer

@api_view(['POST'])
def register_user(request):
    data = request.data
    user, created = TGUser.objects.get_or_create(
        user_id=data['user_id'],
        defaults={'username': data.get('username', '')}
    )
    if created:
        serializer = TGUserSerializer(user)
        return Response(serializer.data)
    else:
        return Response({'message': 'Вы уже зарегистрированы!'})

@api_view(['GET'])
def get_user_info(request, user_id):
    try:
        user = TGUser.objects.get(user_id=user_id)
        serializer = TGUserSerializer(user)
        print(serializer.data)
        return Response(serializer.data)
    except TGUser.DoesNotExist:
        return Response({'message': "User not found"}, status=404)