from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from rest_framework import status
from user_app.api.serializers import RegisterSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.tokens import RefreshToken


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
def registration_view(request):
    if request.method == 'POST':
        serializer = RegisterSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            account = serializer.save()
            print('------------', account)
            data['username'] = account.username
            data['email'] = account.email
            refresh = RefreshToken.for_user(account)

            data['token'] = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        else:
            data = serializer.errors
            
        return Response(data, status=status.HTTP_201_CREATED)
        
@api_view(['POST'])
def logout_view(request):
    if request.method == 'POST':
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)



