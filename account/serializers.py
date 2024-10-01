from rest_framework import serializers
from .models import User

class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    
    class Meta:
        model = User
        fields = ['email', 'name', 'employee_id', 'tc', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }
        
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')

        # Check if password and confirm password match
        if password != password2:
            raise serializers.ValidationError("Password and Confirm Password don't match")
        return attrs
    
    def create(self, validated_data):
        # Remove the password2 from validated_data as it's only used for validation
        validated_data.pop('password2')
        
        # Extract password to hash it
        password = validated_data.pop('password')

        # Create the user without saving yet
        user = User(**validated_data)

        # Set the hashed password
        user.set_password(password)
        
        # Now save the user to the database
        user.save()
        
        return user
