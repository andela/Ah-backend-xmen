
import re
from rest_framework import serializers

def validate_password(password):
    if password is None:
        raise serializers.ValidationError("A new password is required to request reset password.")
    elif len(password)<8:
       raise serializers.ValidationError("Password must be longer than 8 characters.")
    elif re.search(r'(?=.*[\d])(?=.*[A-Z])(?=.*[a-z])', password) is None:
        raise serializers.ValidationError("Password should at least contain a number, capital and small letter.")
    return password