from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Library, Seat, UserProfile
import logging

logger = logging.getLogger(__name__)

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



# class LibrarySerializer(serializers.ModelSerializer):
#     total_seats = serializers.SerializerMethodField()
#     class Meta:
#         model = Library
#         fields = ['id', 'name', 'location', 'total_seats', 'owner', 'latitude', 'longitude']

#     def create(self, validated_data):
#         # Custom logic can be added here if necessary
#         return Library.objects.create(**validated_data)

#     def update(self, instance, validated_data):
#         instance.name = validated_data.get('name', instance.name)
#         instance.location = validated_data.get('location', instance.location)
#         instance.total_seats = validated_data.get('total_seats', instance.total_seats)
#         instance.latitude = validated_data.get('latitude', instance.latitude)
#         instance.longitude = validated_data.get('longitude', instance.longitude)
#         # instance.available_seats = validated_data.get('available_seats', instance.available_seats)
#         instance.save()
#         return instance
    
#     def get_total_seats(self, obj):
#         return obj.seats.filter(is_occupied=False).count()



# class LibrarySerializer(serializers.ModelSerializer):
#     total_seats = serializers.SerializerMethodField()

#     class Meta:
#         model = Library
#         fields = ['id', 'name', 'location', 'total_seats', 'owner', 'latitude', 'longitude']

#     def create(self, validated_data):
#         return Library.objects.create(**validated_data)

#     def update(self, instance, validated_data):
#         instance.name = validated_data.get('name', instance.name)
#         instance.location = validated_data.get('location', instance.location)
#         instance.total_seats = validated_data.get('total_seats', instance.total_seats)
#         instance.latitude = validated_data.get('latitude', instance.latitude)
#         instance.longitude = validated_data.get('longitude', instance.longitude)
#         instance.save()
#         return instance

#     # Return count of available seats (unoccupied seats) as 'total_seats'
#     def get_total_seats(self, obj):
#         return obj.seats.filter(is_occupied=False).count()




class LibrarySerializer(serializers.ModelSerializer):
    total_seats = serializers.SerializerMethodField()

    class Meta:
        model = Library
        fields = ['id', 'name', 'location', 'total_seats', 'owner', 'latitude', 'longitude']

    def get_total_seats(self, obj):
        try:
            occupied_seats = obj.seats.filter(is_occupied=True).count()
            total_seats = obj.total_seats - occupied_seats
            return total_seats
        except Exception as e:
            logger.error(f"Error calculating total seats: {e}")
            raise serializers.ValidationError("Error calculating total seats")

    def create(self, validated_data):
        logger.debug(f"Creating Library with data: {validated_data}")
        try:
            library = Library.objects.create(**validated_data)
            logger.info(f"Library created successfully: {library}")
            return library
        except Exception as e:
            logger.error(f"Error creating Library: {e}")
            raise serializers.ValidationError("Failed to create library")
        
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.location = validated_data.get('location', instance.location)
        instance.total_seats = validated_data.get('total_seats', instance.total_seats)
        instance.latitude = validated_data.get('latitude', instance.latitude)
        instance.longitude = validated_data.get('longitude', instance.longitude)
        instance.save()
        return instance



# class UserProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserProfile
#         fields = '__all__' 

# class LibrarySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Library
#         fields = '__all__'  # Adjust fields as needed

# class LibrarySerializer(serializers.ModelSerializer):
#     seat_availability = serializers.SerializerMethodField()

#     class Meta:
#         model = Library
#         fields = ['id', 'name', 'location', 'seat_availability', 'owner']

#     def get_seat_availability(self, obj):
#         return obj.seats.filter(is_occupied=False).count()




# Serializer for User model to include in UserProfile
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']  # Include fields you need

# UserProfileSerializer updated to include nested User details
class UserProfileSerializer(serializers.ModelSerializer):
    # user = UserSerializer(read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    first_name = serializers.CharField(source='user.first_name', required=False)
    last_name = serializers.CharField(source='user.last_name', required=False)

    class Meta:
        model = UserProfile
        fields = ['id', 'role', 'dob', 'hobbies', 'contact_number', 'location', 'latitude', 'longitude', 'approved', 'library', 'email', 'username', 'first_name', 'last_name']


    def update(self, instance, validated_data):
        # Update the User model fields for email, username, first_name, last_name
        user_data = validated_data.pop('user', {})
        instance.user.email = user_data.get('email', instance.user.email)
        instance.user.username = user_data.get('username', instance.user.username)
        instance.user.first_name = user_data.get('first_name', instance.user.first_name)
        instance.user.last_name = user_data.get('last_name', instance.user.last_name)
        instance.user.save()

        # Update the UserProfile model fields
        return super().update(instance, validated_data)




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
