from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Library, Seat, UserProfile

# class StudentSignupSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True)

#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password']

#     def create(self, validated_data):
#         user = User(
#             username=validated_data['username'],
#             email=validated_data['email']
#         )
#         user.set_password(validated_data['password'])
#         user.save()
#         return user


# class UserProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserProfile
#         fields = ['user', 'role', 'approved']  # Add other fields as necessary

# class LibrarySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Library
#         fields = ['id', 'name', 'location']


class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = ['id', 'number', 'status']


# ==================================================



class LibrarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Library
        fields = ['id', 'name', 'location', 'total_seats']

    def create(self, validated_data):
        # Custom logic can be added here if necessary
        return Library.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.location = validated_data.get('location', instance.location)
        instance.total_seats = validated_data.get('total_seats', instance.total_seats)
        # instance.available_seats = validated_data.get('available_seats', instance.available_seats)
        instance.save()
        return instance
    


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'  # Adjust fields as needed

class LibrarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Library
        fields = '__all__'  # Adjust fields as needed




class UserSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class ApproveUserSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=['admin', 'student'], required=True)

    class Meta:
        model = UserProfile
        fields = ['role']
