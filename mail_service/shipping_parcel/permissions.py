from rest_framework import permissions


class ParcelPermissions(permissions.BasePermission):
    __doc__ = """
    post master have a only read access and the parcel owner have all access.
    """

    def has_permission(self, request, view):
        if request.user.user_type in ["PARCEL_OWNER", "POST_MASTER"]:
            if request.method == "GET":
                return True
            elif (
                request.method == "POST" or request.method == "PATCH"
            ) and request.user.user_type == "PARCEL_OWNER":
                return True
            else:
                return False
        else:
            return False


class TrainPermissions(permissions.BasePermission):
    __doc__ = """
    post master have a only read access and the Train operator have all access.
    """

    def has_permission(self, request, view):
        if request.user.user_type in ["TRAIN_OPERATOR", "POST_MASTER"]:
            if request.method == "GET":
                return True
            elif (
                request.method == "POST" or request.method == "PATCH"
            ) and request.user.user_type == "TRAIN_OPERATOR":
                return True
            else:
                return False
        else:
            return False


class PostMasterPermissions(permissions.BasePermission):
    __doc__ = """
    Only post master have a access.
    """

    def has_permission(self, request, view):
        if request.user.user_type == "POST_MASTER":
            return True
        else:
            return False