from django.core.exceptions import ValidationError
import re

class PhoneNumberValidator:
    """Custom validator to enforce phone number constraints."""

    def validate():
        """
        Validate the phone number.
        :param phone_number: The phone number to validate.
        :param user: Optional user instance.
        """
        # Ensure phone number contains only digits
        if not re.match(r'^\d{10,15}$', self):
            raise ValidationError("Phone number must be 10-15 digits long and contain only numbers.")

        # Prevent duplicate phone numbers
        from userauths.models import User  # Import inside function to avoid circular import
        if User.objects.filter(phone=self).exists():
            raise ValidationError("A user with this phone number already exists.")

    def get_help_text(self):
        return "Your phone number must be unique and contain only digits (10-15 characters)."
