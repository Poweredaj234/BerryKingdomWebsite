from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.contrib.auth.models import BaseUserManager

class CustomUser(AbstractUser):
    balance = models.FloatField(default=0.0)
    nobility = models.IntegerField(
        choices=[
            (0, 'King'),
            (1, 'Archduke'),
            (2, 'Prince'),
            (3, 'Duke'),
            (4, 'Marquess'),
            (5, 'Count'),
            (6, 'Viscount'),
            (7, 'Baron'),
            (8, 'Citizen'),
            (9, 'Stateless'),
        ],
        default=7
    )
    house = models.CharField(max_length=100, blank=True, null=True)

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, nobility=7, house=None, created_by=None):
        """
        Create a new user. Handles self-registration and admin creation.

        Args:
            username (str): Username of the new user.
            email (str): Email of the new user.
            password (str): Password for the new user.
            nobility (int): Nobility level (defaults to Citizen).
            house (str): House name (only if created by a high-ranking user).
            created_by (CustomUser): The user creating this account (None for self-registration).

        Returns:
            CustomUser: The newly created user.
        """
        if created_by:
            # Admin/privileged user creation
            if created_by.nobility > 1:  # Only Duke or higher
                if nobility < created_by.nobility:
                    raise ValueError("You cannot create a user with higher nobility than yourself.")
            else:
                raise PermissionError("Only users with nobility of Duke or higher can create users.")

            # Assign house if provided
            if house:
                if created_by.house != house:
                    raise ValueError("You can only assign users to your own house.")

        else:
            # Self-registration
            nobility = 8  # Default to Citizen
            house = None  # Default to no house

        user = self.model(username=username, email=email, nobility=nobility, house=house)
        user.set_password(password)
        user.save(using=self._db)
        return user