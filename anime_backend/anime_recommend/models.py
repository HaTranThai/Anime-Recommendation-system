from datetime import timezone
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

# Custom manager
class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', True)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if not extra_fields.get('is_staff'):
            raise ValueError('Superuser must have is_staff=True.')
        if not extra_fields.get('is_superuser'):
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

# Custom User model
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10, blank=True)

    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    class Meta:
        db_table = 'user'

class Anime(models.Model):
    id = models.AutoField(primary_key=True)  # mặc định
    anime_code = models.CharField(max_length=20, unique=True, blank=True, null=True)
    title = models.CharField(max_length=255)
    image_link = models.URLField(blank=True)
    subtitle = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    new_episode = models.CharField(max_length=100, blank=True)
    latest_episode = models.CharField(max_length=100, blank=True)
    release_schedule = models.CharField(max_length=100, blank=True)
    genre = models.CharField(max_length=255, blank=True)
    director = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=100, blank=True)
    duration = models.CharField(max_length=50, blank=True)
    rating = models.FloatField(null=True, blank=True)

    class Meta:
        db_table = 'anime'
        

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    watched_animes = models.ManyToManyField(Anime, through="UserWatchHistory", related_name="watched_by")

    def __str__(self):
        return f"Profile of {self.user.email}"

    class Meta:
        db_table = "user_profile"

class UserWatchHistory(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE)
    last_watched = models.DateTimeField(default=timezone.now)
    progress = models.CharField(max_length=50, blank=True, help_text="e.g. 'Tập 12/24'")

    class Meta:
        db_table = "user_watch_history"
        unique_together = ("user_profile", "anime")

    def __str__(self):
        return f"{self.user_profile.user.email} watched {self.anime.title}"