from rest_framework.permissions import BasePermission


class BaseRolePermission(BasePermission):
    """
    Checking if User have roles
    """

    def __getattribute__(self, attr):
        if attr == "has_permission":
            original = super().__getattribute__(attr)
            if callable(original):
                def has_permission_wrapper(*args, **kwargs):
                    if not bool(getattr(args[0].user, 'roles', None)):
                        return False
                    return original(*args, **kwargs)
                return has_permission_wrapper
            return original


class IsSuperUser(BaseRolePermission):
    """
    Allows access only to Super users.
    """

    def has_permission(self, request, view):

        return all([
            request.user,
            request.user.is_authenticated,
            'SUPER_ADMIN' in [role.name for role in request.user.roles.all()]
        ])


class IsManagerUser(BaseRolePermission):
    """
    Allows access only to Manager users.
    """

    def has_permission(self, request, view):

        return all([
            request.user,
            request.user.is_authenticated,
            'MANAGER' in [role.name for role in request.user.roles.all()]
        ])


class IsOperatorUser(BaseRolePermission):
    """
    Allows access only to Operator users.
    """

    def has_permission(self, request, view):

        return all([
            request.user,
            request.user.is_authenticated,
            'OPERATOR' in [role.name for role in request.user.roles.all()]
        ])
