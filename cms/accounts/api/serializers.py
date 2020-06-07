from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from rest_framework import serializers
from rest_framework.authtoken.models import Token


class SignupSerializer(serializers.ModelSerializer):

    confirm_password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model  = User
        fields = ('username', 'password', 'confirm_password')
        extra_kwargs = {
            'password': {'write_only': True} # Security feature
        }

    # Overriding the save method to provide functionality of password confirmation
    # Django REST built-in does not checks password & confirm-password matching
    def save(self):
        user = User(
            username=self.validated_data['username']
        )

        pass1 = self.validated_data['password']
        pass2 = self.validated_data['confirm_password']

        if pass1 != pass2:
            raise serializers.ValidationError({'password':'Passwords must match'})
        user.set_password(pass1) # Defined inside lib/python3.6/site-packages/django/contrib/auth/models.py
        user.save()
        return user


# Post_Save receiver functions perform a certain activity after a save event has occurred
# These act like event listeners
@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)