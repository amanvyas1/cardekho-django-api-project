from rest_framework import serializers

from ..models import CarList, Review, ShowroomList

class ReviewSerializer(serializers.ModelSerializer):
    api_user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Review
        exclude = ('car',)
        # fields = '__all__'

class CarSerializer(serializers.ModelSerializer):
    discounted_price = serializers.SerializerMethodField()
    Reviews = ReviewSerializer(many=True,read_only=True)
    class Meta:
        model = CarList
        fields = '__all__'
        
    def get_discounted_price(self, object):
        if object.price is not None:
            return object.price - 1000
        
    def validate_price(self, value):
        if value <= 20000:
            raise serializers.ValidationError('Price must be greater than 20000')
        return value
    
    def validate(self, data):
        if data['name'] == data['description']:
            raise serializers.ValidationError('Name and description cannot be same')
        return data
    
class ShowroomListSerializer(serializers.ModelSerializer):
    # showrooms = CarSerializer(many=True, read_only=True)
    # showrooms = serializers.StringRelatedField(many=True)
    class Meta:
        model = ShowroomList
        fields = '__all__'


        