# exhibition/serializers.py

from rest_framework import serializers
from .models import Breed, Kitten, Rating

class BreedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Breed
        fields = ['id', 'name']

class KittenSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Kitten
        fields = ['id', 'breed', 'color', 'age', 'description', 'owner', 'average_rating']

    def get_average_rating(self, obj):
        return obj.get_average_rating()

class RatingSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Rating
        fields = ['id', 'kitten', 'user', 'score']

    def validate_score(self, value):
        if 1 <= value <= 5:
            return value
        raise serializers.ValidationError('Оценка должна быть от 1 до 5')
