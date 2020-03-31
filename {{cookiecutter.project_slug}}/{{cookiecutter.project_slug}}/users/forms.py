from django_sso_app.core.apps.users.forms import (UserCreationForm as DjangoSsoAppUserCreationForm,
                                                  UserChangeForm as DjangoSsoAppUserChangeForm)


class UserChangeForm(DjangoSsoAppUserChangeForm):
    pass


class UserCreationForm(DjangoSsoAppUserCreationForm):
    pass
