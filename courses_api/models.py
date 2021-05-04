from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.conf import settings


class UserProfileManager(BaseUserManager):
    """Manager for users"""

    def create_user(self, name, email, password=None, phone=None, gender=None, about=None, photo=None):
        """Create a new user"""
        if not email:
            raise ValueError("User must enter email address")

        email = self.normalize_email(email)
        user = self.model(name=name, email=email, phone=phone,
                          gender=gender, about=about, photo=photo)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, name, email, password, phone=None, gender=None, about=None, photo=None):
        """Create superuser with given details"""
        user = self.create_user(name, email, password,
                                phone, gender, about, photo)

        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Database model for users in the system"""
    name = models.CharField(max_length=255)
    email = models.EmailField(
        max_length=255, unique=True)
    phone = models.CharField(
        max_length=20, default=None, blank=True, null=True)
    gender = models.BooleanField(default=None, blank=True, null=True)
    about = models.TextField(default=None, blank=True, null=True)
    photo = models.ImageField(
        upload_to='users', default=None, blank=True, null=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        """Return string represenation for user"""
        return self.name


class Category(models.Model):
    """Handle categories in the system"""

    name = models.CharField(max_length=255)

    def __str__(self):
        """Return string representation of the model"""
        return self.name


class Course(models.Model):
    """Handle Courses in the system"""
    user_profile = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
    )

    title = models.CharField(max_length=255)
    description = models.TextField()
    overview = models.TextField()
    price = models.FloatField()
    currency = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return string representation of the model"""
        return self.title


class Chapter(models.Model):
    """Handle Chapters in the system"""
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
    )

    title = models.CharField(max_length=255)

    def __str__(self):
        """Return string representation of the model"""
        return self.title


class Tutorial(models.Model):
    """Handle Tutorials in the system"""
    chapter = models.ForeignKey(
        Chapter,
        on_delete=models.CASCADE,
    )

    title = models.CharField(max_length=255)
    description = models.TextField()
    summary = models.TextField()
    video = models.FileField(upload_to='course_videos', blank=True, null=True)
    mins_count = models.FloatField()

    def __str__(self):
        """Return string representation of the model"""
        return self.title


class Review(models.Model):
    """Handle Reviews in the system"""
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
    )

    reviewer_name = models.CharField(max_length=255)
    score = models.IntegerChoices('score', 'Hate Dislike Ok Like Love')
    content = models.CharField(max_length=255)

    def __str__(self):
        """Return string representation of the model"""
        return self.content
