from rest_framework import permissions

class IsAPIRequesterOrReadOnly(permissions.BasePermission):
    """
    Anyone can view.  Only original Project to request API endpoint
    in first place('project' field) can update request.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # TODO: find better way to work around lazy behavior of user object
        # Unwrap SimpleLazyObject so type is 'User' or 'Project'
        user = request.user._wrapped if hasattr(request.user,'_wrapped') else request.user

        # Ensure user is a Project and is the same project
        return (type(user).__name__ == 'Project') and (user.id == obj.updater_id)
