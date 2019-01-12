from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six


class EmailVerificationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return(
            six.text_type(user.id)+six.text_type(timestamp)
        )


email_verification_token = EmailVerificationTokenGenerator()
