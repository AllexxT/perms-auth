from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.utils.translation import gettext_lazy as _

# from django.utils import timezone
# from dateutil.relativedelta import relativedelta


class CustomUserManager(UserManager):
    def create_superuser(self, email, password, **extra_fields):
        return super().create_superuser(email, password, **extra_fields)

    def _create_user(self, email, password, username=None, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractUser):
    class Meta:
        db_table = "user"
        verbose_name = "User"
        verbose_name_plural = "Users"

    email = models.EmailField(
        error_messages={"unique": "A user with that email already exists."},
        blank=False,
        max_length=254,
        verbose_name=_("Email address"),
        unique=True,
    )

    username = models.CharField(
        _("Username"), max_length=150, blank=True, null=True
    )
    al_id = models.CharField(_("AccelerList ID"), max_length=64, null=True)

    is_active = models.BooleanField(
        _('active'),
        default=False,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()


class Role(models.Model):
    user = models.ManyToManyField(to=User, related_name='roles')
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name
