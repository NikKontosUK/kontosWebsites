# # import hashlib
# # import uuid
# # from django.db import models
# # from django.core.validators import RegexValidator
# # from django.contrib.auth.models import AbstractUser, BaseUserManager
# # from django.utils.timezone import now
# # from django.core.exceptions import ValidationError
# # from django.db import IntegrityError
# # from django.utils.translation import gettext_lazy as _
# # from userauths.validators import PhoneNumberValidator

# # # Custom User Manager
# # class CustomUserManager(BaseUserManager):
# #     def create_user(self, email, phone, password, **extra_fields):
# #         if not email:
# #             raise ValueError("The Email field must be set")
# #         if not phone:
# #             raise ValueError("The Phone field must be set")
# #         if not password:
# #             raise ValueError("The Password field must be set")
     
# #         email = self.normalize_email(email)
# #         unique_id = self.generate_unique_id()
       
     
        

# #         user = self.model(email=email, phone=phone, unique_id=unique_id, **extra_fields)
# #         user.set_password(password)
# #         user.full_clean()
# #         user.save(using=self._db)
# #         return user



# #     def create_superuser(self, email, phone, password=None, **extra_fields):
# #         extra_fields.setdefault("is_staff", True)
# #         extra_fields.setdefault("is_superuser", True)

# #         return self.create_user(email=email, phone=phone, password=password, **extra_fields)

# #     def generate_unique_id(self):
   
# #         """Generates an 8-character unique ID using UUID"""
# #         return uuid.uuid4().hex[:8]

# # # Custom User Model
# # class User(AbstractUser):
# #     phone_validator = RegexValidator(
# #         regex=r'^\d{10,15}$',
# #         message="Phone number must contain only digits and be 10-15 characters long."
# #     )
    

# #     email = models.EmailField(unique=True, max_length=100)
# #     phone = models.CharField(
# #         unique=True,
# #         max_length=15,
# #         validators=[phone_validator],
# #         blank=False,
# #         null=False
# #     )
    

# #     unique_id = models.CharField(
# #         max_length=8, unique=True, editable=False, blank=False, null=False
# #     )  # Hash-based unique ID

# #     username = None  # Remove default username field

# #     USERNAME_FIELD = "email"
# #     REQUIRED_FIELDS = ["phone"]  # Add required fields for superuser creation

# #     objects = CustomUserManager()  # Use custom user manager

    
# #     def __str__(self):
# #         return f"{self.email} - {self.unique_id} - {self.phone}"
# #     def clean(self):
# #         """Apply custom phone validators."""
# #         validator = PhoneNumberValidator()
# #         validator.validate(self.phone, user=self)
# #         super().clean()
# #     def save(self, *args, **kwargs):
# #         """Ensure unique_id is assigned before saving."""
# #         if not self.unique_id:  # Only generate if unique_id is empty
# #             self.unique_id = CustomUserManager().generate_unique_id()
# #         super().save(*args, **kwargs)


# from django.db import IntegrityError

# import uuid
# from django.db import models
# from django.core.validators import RegexValidator
# from django.contrib.auth.models import AbstractUser, BaseUserManager
# from django.core.exceptions import ValidationError
# from django.utils.translation import gettext_lazy as _
# from userauths.validators import PhoneNumberValidator  # Ensure this exists

# # Custom User Manager
# # Custom User Manager
# class CustomUserManager(BaseUserManager):
#     def create_user(self, email, phone, password=None, **extra_fields):
#         if not email:
#             raise ValueError("The Email field must be set")
#         if not phone:
#             raise ValueError("The Phone field must be set")
#         if not password:
#             raise ValueError("The Password field must be set")
        
#         email = self.normalize_email(email)
       
#         user = self.model(email=email, phone=phone, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)  # `save()` will handle unique_id generation
        
#         return user

#     def create_superuser(self, email, phone, password=None, **extra_fields):
#         """Ensure phone is required for createsuperuser"""
#         extra_fields.setdefault("is_staff", True)
#         extra_fields.setdefault("is_superuser", True)

#         if not phone:
#             raise ValueError("The Phone field must be set for superusers")

#         return self.create_user(email=email, phone=phone, password=password, **extra_fields)

# # Custom User Model
# class User(AbstractUser):
    

#     email = models.EmailField(unique=True, max_length=100)
#     phone = models.CharField(
#         max_length=15,
#         unique=True,
#         validators=[
#             RegexValidator(
#                 regex=r'^\d{10,15}$',  
#                 message="Enter a valid phone number (10-15 digits)."
#             )
#         ],
#         error_messages={"unique": "A user with this phone number already exists."}
#     )

#     unique_id = models.CharField(
#         max_length=8, unique=True, editable=False, blank=False, null=False
#     )  # Hash-based unique ID

#     username = None  # Remove default username field

#     USERNAME_FIELD = "email"
#     REQUIRED_FIELDS = ["phone"]  # Required fields for superuser creation

#     objects = CustomUserManager()  # Use custom user manager

#     def __str__(self):
#         return f"{self.email} - {self.unique_id} - {self.phone}"

#     def clean(self):
#         super().clean()
        
#     def save(self, *args, **kwargs):
#         """Ensure unique_id is assigned before saving."""
#         if not self.unique_id:  # Generate only if it's empty
#             self.unique_id = uuid.uuid4().hex[:8]
#         super().save(*args, **kwargs)

import re
import uuid
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.core.validators import RegexValidator, MinLengthValidator
from django.core.exceptions import ValidationError


# Email Validator
email_regex = RegexValidator(
    regex=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$",
    message="Enter a valid email address."
)

# Phone Number Validator
phone_regex = RegexValidator(
    regex=r'^\+?1?\d{9,15}$',
    message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
)

class CustomUserManager(BaseUserManager):
    def validate_email(self, email):
        """Validate email format and uniqueness."""
        if not email:
            raise ValidationError("The Email field is required.")
        
        # Email regex pattern
        email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

        # Validate email format with regex
        if not re.match(email_regex, email):
            raise ValidationError("Enter a valid email address.")

        # Normalize the email
        email = self.normalize_email(email)

        # Check if email is unique
        if User.objects.filter(email=email).exists():
            raise ValidationError("A user with this email already exists.")
        
        return email

    def validate_phone_number(self, phone_number):
        """Validate phone number format and uniqueness."""
        if not phone_number:
            raise ValidationError("The Phone Number field is required.")
        phone_regex=r"^\+?1?\d{9,15}$"

        # Validate email format with regex
        if not re.match(phone_regex, phone_number):
            raise ValidationError("Enter a valid email address.")



        if User.objects.filter(phone_number=phone_number).exists():
            raise ValidationError("A user with this phone number already exists.")
        
        return phone_number

    def validate_password(self, password):
        """Validate password."""
        if not password:
            raise ValidationError("The Password field is required.")

        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long.")
        
        return password

    def create_user(self, email, phone_number, password, **extra_fields):
        """Create and return a regular user with email, phone, and password."""
        
        print("Step 1: Validating email")
        email = self.validate_email(email)
        
        print("Step 2: Validating phone number")
        phone_number = self.validate_phone_number(phone_number)
        
        print("Step 3: Validating password")
        password = self.validate_password(password)

        # Create user instance
        print("Step 4: Creating user instance")
        user = self.model(email=email, phone_number=phone_number, **extra_fields)

        print("Step 5: Setting password")
        user.set_password(password)

        print("Step 6: Running clean method for final validations")
        user.full_clean()

        print("Step 7: Saving user to database")
        user.save(using=self._db)

        print("User created successfully!")
        return user

    def create_superuser(self, email, phone_number, password, **extra_fields):
        """Create and return a superuser with all permissions."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        while True:  # Keep asking for a valid phone number
            try:
                phone_number = self.validate_phone_number(phone_number)
                break  # If validation passes, exit loop
            except ValidationError:
                print("Error: Phone Number is Taken")
                phone_number = input("Enter a new phone number: ")

        while True:  # Keep asking for a valid email
            try:
                email = self.validate_email(email)
                break  # If validation passes, exit loop
            except ValidationError:
                print("Error: Email Address is Taken or Invalid")
                email = input("Enter a valid email address: ")  # Ensure email input is proper

        return self.create_user(email, phone_number, password, **extra_fields)


# Custom User Model
class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)

    email = models.EmailField(
        unique=True,
        validators=[MinLengthValidator(5), email_regex],
        max_length=100
    )

    phone_number = models.CharField(
        max_length=15,
        unique=True,
        validators=[phone_regex]
    )

    password = models.CharField(max_length=128)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number',]

    def __str__(self):
        return f"{self.email} - {self.phone_number}"

    def clean(self):
        """Ensure email and phone number are unique before saving."""
        super().clean()
        if User.objects.exclude(pk=self.pk).filter(email=self.email).exists():
            raise ValidationError({"email": "A user with this email already exists."})
        if User.objects.exclude(pk=self.pk).filter(phone_number=self.phone_number).exists():
            raise ValidationError({"phone_number": "A user with this phone number already exists."})

    def save(self, *args, **kwargs):
        """Ensure validation before saving."""
        self.full_clean()  # Calls `clean()` and runs model field validators
        super().save(*args, **kwargs)
