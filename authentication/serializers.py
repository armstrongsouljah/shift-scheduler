import re
import uuid

from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from utils.messages import error_messages
from utils.validators.validation_helpers import (
        validate_password,
        validate_username,
        validate_field_exists,
        find_email_by_username)

from .models import User


class RegistrationSerializer(serializers.ModelSerializer):
    """Serializers registration requests and creates a new user."""

    # Ensure passwords are at least 8 characters long, no longer than 128
    # characters, and can not be read by the client.
    password = serializers.CharField(
        max_length=128,
        write_only=True
    )
    email = serializers.EmailField()
    username = serializers.CharField()

    # The client should not be able to send a token along with a registration
    # request. Making `token` read-only handles that for us.
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        # List all of the fields that could possibly be included in a request
        # or response, including fields specified explicitly above.
        fields = ['email', 'username', 'password', 'token', 'phone', 'address']

    def validate_password(self, password):
        """ 
        This function validates the password input by a new user signing up
        It ensures that the password length is longer than 8 characters to be considered valid.
        The password should also contain at least a letter and number. 
        Args: 
            password (str): This is password string received from user
        Returns: 
            Returns the validated password
        Raises: 
            ValidationError: 
            - ("Password must be longer than 8 characters."): for very short passwords
            - ("Password should at least contain a number, capital and small letter."): for non alphanumeric paaswords  
        """
        return validate_password(password)

    def validate_email(self, email):
        """ 
        A function to validate the email input by a new user signing up
        It ensures that the email being used for signing up was not already used by another user.
        Args: 
            email(str): This is the email string received from user
        Returns: 
            Returns the validated email
        Raises: 
            ValidationError: 
            - "Email already exists." : for an already existing email
        """

        check_email = User.objects.filter(email=email)
        if check_email.exists():
            raise serializers.ValidationError("Email already exists.")
        return email

    def validate_username(self, username):
        """ 
        Validation function of the username input by a new user signing up
        It ensures that the username being used for signing up was not already used by another user.
        It also ensures the username only contains numbers and letters.
        Args: 
            username (str): username
        Returns: 
            Returns the validated username
        Raises: 
            ValidationError: 
            - "Username already exists." : for an already existing username
            - "Username can only contain letters and numbers." : for an invalid username
        """
        return validate_username(username)

    def create(self, validated_data):
        # Use the `create_user` method we wrote earlier to create a new user.
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255, required=False)
    username = serializers.CharField(max_length=255, required=False)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        # The `validate` method is where we make sure that the current
        # instance of `LoginSerializer` has "valid". In the case of logging a
        # user in, this means validating that they've provided an email
        # and password and that this combination matches one of the users in
        # our database.
        email = data.get('email', None)
        username = data.get('username', None)
        password = data.get('password', None)
   
        # As mentioned above, an email is required. Raise an exception if an
        # email is not provided.
        if email is None and username is None:
            raise serializers.ValidationError(
                error_messages['field required'].format('Email or Username')
            )

        # As mentioned above, a password is required. Raise an exception if a
        # password is not provided.
        validate_field_exists(
            password, error_messages['field required'].format('Password'))   

        # The `authenticate` method is provided by Django and handles checking
        # for a user that matches this email/password combination. Notice how
        # we pass `email` as the `username` value. Remember that, in our User
        # model, we set `USERNAME_FIELD` as `email`.
        if username is not None:
            email = find_email_by_username(username)

        user = authenticate(username=email, password=password)
        # If no user was found matching this email/password combination then
        # `authenticate` will return `None`. Raise an exception in this case.
        validate_field_exists(
            user, 'A user with this email and password was not found.')

        # Django provides a flag on our `User` model called `is_active`. The
        # purpose of this flag to tell us whether the user has been banned
        # or otherwise deactivated. This will almost never be the case, but
        # it is worth checking for. Raise an exception in this case.
        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )

        # The `validate` method should return a dictionary of validated data.
        # This is the data that is passed to the `create` and `update` methods
        # that we will see later on.
        return {
            'email': user.email,
            'username': user.username,
            'token': user.token
        }


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255, required=True)

    def validate(self, data):

        email = data.get('email', None)

        if email is None:
            raise serializers.ValidationError(
                error_messages['field required'].format('Email'))

        return {
            'email': email
        }


class PasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=128, required=True)

    def validate(self, data):
        new_password = data.get('password', None)
        return {
            'password': validate_password(new_password)
        }


class UserSerializer(serializers.ModelSerializer):
    """Handles serialization and deserialization of User objects."""

    # Passwords must be at least 8 characters, but no more than 128
    # characters. These values are the default provided by Django. We could
    # change them, but that would create extra work while introducing no real
    # benefit, so let's just stick with the defaults.
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )
    token = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'token',)

        # The `read_only_fields` option is an alternative for explicitly
        # specifying the field with `read_only=True` like we did for password
        # above. The reason we want to use `read_only_fields` here is because
        # we don't need to specify anything else about the field. For the
        # password field, we needed to specify the `min_length` and
        # `max_length` properties too, but that isn't the case for the token
        # field.
        read_only_fields = ('token',)

    def update(self, instance, validated_data):
        """Performs an update on a User."""

        # Passwords should not be handled with `setattr`, unlike other fields.
        # This is because Django provides a function that handles hashing and
        # salting passwords, which is important for security. What that means
        # here is that we need to remove the password field from the
        # `validated_data` dictionary before iterating over it.
        password = validated_data.pop('password', None)
        for (key, value) in validated_data.items():
            # For the keys remaining in `validated_data`, we will set them on
            # the current `User` instance one at a time.
            setattr(instance, key, value)

        if password is not None:
            # `.set_password()` is the method mentioned above. It handles all
            # of the security stuff that we shouldn't be concerned with.
            instance.set_password(password)

        # Finally, after everything has been updated, we must explicitly save
        # the model. It's worth pointing out that `.set_password()` does not
        # save the model.
        instance.save()

        return instance

    def get_token(self,user):
        """ Create a token for a user who logs in """

        # Overriding the token creation method in the User serializer class so that
        # we can generate our own valid token from the credentials of the user
        token = user.generate_jwt_token()
        return token

