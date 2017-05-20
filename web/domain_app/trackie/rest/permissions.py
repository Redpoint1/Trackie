from django.utils.translation import ugettext_lazy as _

from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        if hasattr(view, "trackie_owner"):
            fields = view.trackie_owner.split(".")
            owner = obj
            for field in fields:
                owner = getattr(owner, field)
        else:
            owner = getattr(obj, "owner")

        return owner == request.user


class IsNotPublicOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        if hasattr(view, "trackie_public"):
            field = view.trackie_public
            public = getattr(obj, field)
        else:
            public = getattr(obj, "public")

        return not public


class NotProtectedOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):

        check_methods = getattr(view, "trackie_protect_methods", ["DELETE"])

        if request.method not in check_methods:
            return True

        assert hasattr(view, "trackie_protect"), _(
            "trackie_protect attribute is not set"
        )

        field = view.trackie_protect
        protected = getattr(obj, field)

        return not protected.count()


class ReadOnly(BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        return False
