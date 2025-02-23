from rest_framework import serializers

from .models import  User

class UserCSVUploadSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.
    """
    name = serializers.CharField(required = True)
    email = serializers.EmailField()
    age = serializers.IntegerField()
    class Meta:
        model = User
        fields = ['name', 'email',"age"]
    
    def validate_age(self,value):
        """
         Validate the age field.
        """
        # check if age is within valid range (0, 20)
        if not 0 < value < 20:
            # raise a validation error if the age is not in the valid range 0-20
            raise serializers.ValidationError("Value must be in between 0 and 20")
        return value
    
    def validate_email(self,value):
        """
         Validate the email field.
        """
        # check if email already exists in the database
        if User.objects.filter(email__iexact=value).exists():
            # raise a validation error if the email already exists in the database
            raise serializers.ValidationError("Duplicate")
        return value
    



