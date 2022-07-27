from rest_framework.exceptions import ValidationError


def not_me_username_validation(value):
    if value == 'me':
        raise ValidationError(
            'Нельзя использовать "me" в качестве имени пользователя.')
