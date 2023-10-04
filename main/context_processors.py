from django.contrib.auth import get_user


def user_info(request):
    user = get_user(request)

    user_info = {
        'user': user,
    }

    return user_info
