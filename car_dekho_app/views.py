from django.shortcuts import render
from django.http import JsonResponse

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from .models import CarList, ShowroomList, Review
from .api_file.serializers import CarSerializer, ShowroomListSerializer, ReviewSerializer
from .api_file.permissions import AdminOrReadOnlyPermission, ReviewUserOrReadOnlyPermission
from .api_file.throttling import ReviewListThrottle, ReviewDetailThrottle
from .api_file.pagination import ReviewListPagination, ReviewListLimitOffset

from rest_framework.response import Response
from rest_framework import generics, mixins
from rest_framework.authentication import BasicAuthentication, SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser, DjangoModelPermissions
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle


# Create your views here.

@api_view(['GET','POST'])
def car_list_view(request):
    if request.method == 'GET':
        car = CarList.objects.all()
        serializer = CarSerializer(car, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = CarSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors)
        serializer.save()
        return Response(serializer.data)

@api_view(['GET','PUT','DELETE'])
def car_detail_view(request, pk):
    if request.method == 'GET':
        try:
            car = CarList.objects.get(pk=pk)
            serialize = CarSerializer(car)
            return Response(serialize.data)
        except Exception as e:
            return Response({'message':'car not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'PUT':
        car = CarList.objects.get(pk=pk)
        serialize = CarSerializer(car, request.data)
        if serialize.is_valid():
            serialize.save()
            return Response(serialize.data)
        return Response(serialize.data)

    if request.method == 'DELETE':
        car = CarList.objects.get(pk=pk)
        car.delete()
        return Response({'message':'car deleted successfully'}, status=status.HTTP_200_OK)

class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    authentication_classes = [TokenAuthentication]
    
    def get_queryset(self):
        return Review.objects.all()
    
    def perform_create(self, serializer):
        pk = self.kwargs['pk']
        cars = CarList.objects.get(pk=pk)
        created_by = self.request.user
        review_queryset = Review.objects.filter(car = cars, api_user=created_by)
        if review_queryset.exists():
            raise ValidationError('Review already exists')
        serializer.save(CarList=cars)   

class ReviewList(generics.ListAPIView):
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    authentication_classes = [TokenAuthentication]
    # throttle_classes = [ReviewListThrottle]
    pagination_class = ReviewListLimitOffset
    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(car=pk)
    
class ReviewDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [ReviewUserOrReadOnlyPermission]
    authentication_classes = [TokenAuthentication]
    throttle_classes = [ReviewDetailThrottle]
    
    
# class ReviewList(mixins.ListModelMixin,
#                  mixins.CreateModelMixin,
#                  generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
#     authentication_classes = [SessionAuthentication]
    
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
    
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
    
# class ReviewDetails(mixins.RetrieveModelMixin
#                     ,generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
    
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)
    
    
# class ShowroomViewset(viewsets.ViewSet):
#     def list(self, request):
#         queryset = ShowroomList.objects.all()
#         serializer = ShowroomListSerializer(queryset, many=True)
#         return Response(serializer.data)
     
#     def retrieve(self, request, pk=None):
#         queryset = ShowroomList.objects.all()
#         showroom = get_object_or_404(queryset, pk=pk)
#         serializer = ShowroomListSerializer(showroom)
#         return Response(serializer.data)
    
#     def create(self, request):
#         serializer = ShowroomListSerializer(data = request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors)
        
class ShowroomViewset(viewsets.ModelViewSet):
    queryset = ShowroomList.objects.all()
    serializer_class = ShowroomListSerializer
    

class ShowroomView(APIView):
    
    # authentication_classes = [SessionAuthentication]
    # permission_classes = [ IsAuthenticated]
    
    def get(self, request):
        showrooms = ShowroomList.objects.all()
        serialize = ShowroomListSerializer(showrooms, many=True)
        return Response(serialize.data)
    
    def post(self, request):
        serializer = ShowroomListSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
        
class ShowroomDetails(APIView):
    
    def get(self, request, pk):
        try:
            showrooms = ShowroomList.objects.get(pk=pk)
        except ShowroomList.DoesNotExist:
            return Response({"message":"showroom not found"},status=status.HTTP_404_NOT_FOUND)
        serializer = ShowroomListSerializer(showrooms)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    def put(self, request, pk):
        showroom = ShowroomList.objects.get(pk=pk)
        serializer = ShowroomListSerializer(showroom, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        showroom = ShowroomList.objects.get(pk=pk)
        showroom.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)