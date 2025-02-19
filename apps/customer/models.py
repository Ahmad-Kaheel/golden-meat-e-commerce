from django.contrib.auth import models as auth_models
from django.db import models
from django.core.mail import send_mail
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class UserManager(auth_models.BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a User with the given email and
        password.
        """
        now = timezone.now()
        if not email:
            raise ValueError("The given email must be set")
        email = UserManager.normalize_email(email)
        user = self.model(
            email=email,
            is_staff=False,
            is_active=True,
            is_superuser=False,
            last_login=now,
            date_joined=now,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        u = self.create_user(email, password, **extra_fields)
        u.is_staff = True
        u.is_active = True
        u.is_superuser = True
        u.save(using=self._db)
        return u


class User(auth_models.AbstractBaseUser, auth_models.PermissionsMixin):
    """

    This is basically a copy of the core AbstractUser model but without a
    username field
    """

    email = models.EmailField(_("email address"), unique=True)
    is_staff = models.BooleanField(
        _("Staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("Active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as "
            "active. Unselect this instead of deleting accounts."
        ),
    )

    is_vendor = models.BooleanField(
        _("Vendor status"),
        default=False,
        help_text=_("Designates whether this user is a vendor.")
    )
    is_blacklisted = models.BooleanField(
        _("Blacklisted"),
        default=False,
        help_text=_("Designates whether this user is blacklisted.")
    )

    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    
    class Meta:
        ordering = ("-date_joined",)
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    @property
    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.profile.first_name, self.profile.last_name)
        return full_name.strip()
    
    @property
    def get_short_name(self):
        """
        Return the short name for the user.
        """
        return self.profile.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Send an email to this user.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)


class Profile(models.Model):
    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
    first_name = models.CharField(_("First name"), max_length=255, blank=True, null=True)
    last_name = models.CharField(_("Last name"), max_length=255, blank=True, null=True)
    gender = models.CharField(_("Gender"), max_length=10, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], blank=True, null=True)
    date_of_birth = models.DateField(_("Date of Birth"), blank=True, null=True)
    phone_number = models.CharField(_("Phone Number"), max_length=15, blank=True, null=True)

    # Fields specific to vendors
    company_name = models.CharField(_("Company Name"), max_length=255, blank=True, null=True)
    company_type = models.CharField(_("Company Type"), max_length=255, blank=True, null=True)
    commercial_registration_number = models.CharField(_("Commercial Registration Number"), max_length=255, blank=True, null=True)
    tax_number = models.CharField(_("Tax Number"), max_length=255, blank=True, null=True)
    manager_name = models.CharField(_("Manager Name"), max_length=255, blank=True, null=True)
    company_email = models.EmailField(_("Company Email"), blank=True, null=True)
    mobile_number = models.CharField(_("Mobile Number"), max_length=15, blank=True, null=True)
    website = models.URLField(_("Website"), blank=True, null=True)
    business_activity = models.CharField(_("Business Activity"), max_length=255, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)
        verbose_name = _("Profile")
        verbose_name_plural = _("Profile")

    def __str__(self):
        return str(self.user.get_full_name)


