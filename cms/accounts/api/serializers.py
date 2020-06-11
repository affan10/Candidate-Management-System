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


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    """
        - This Receiver function creates a token whenever a User object is saved to the database.
        - Post_Save Receiver functions perform a certain activity after a save event has occurred.
        - These act like event listeners or Receivers and receive Signals from a Sender.

        :param sender: The event that caused this Receiver function to activate.
        :param instance: The instance associated with that event.
        :param created: Flag specifying if something got saved to the database.
        :param kwargs: optional argument containing all arguments.
        :return: just creates an associates a token with its corresponding user instance.
    """
    if created:
        Token.objects.create(user=instance)