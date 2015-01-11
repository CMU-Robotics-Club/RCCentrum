from rest_framework import permissions
from crm.settings import USER_RFID_PROJECTS_TO_USERS, USER_BALANCE_PROJECTS_TO_USERS, USER_EMAIL_PROJECTS_TO_USERS

class UserAuthorizedProjectOrReadOnlyPermission(permissions.BasePermission):
    """
    Anyone authenticated can view.
    Only Project that is authorized for the
    endpoint and user in question can perform
    not safe methods.
    """

    """
    A dictionary of project IDs(public keys) to
    an array of user IDs the project can perform
    the endpoint action on.  If the array is [],
    same as not having the project ID listed.  If array
    is `None` all user IDs are valid.
    """
    project_id_to_user_ids = {}
    
    """
    If a RoboUser can perform the action
    with their own credentials from the
    API documentation.
    """
    user_perform = False

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            # TODO: find better way to work around lazy behavior of user object
            # Unwrap SimpleLazyObject so type is 'User' or 'Project'
            user = request.user._wrapped if hasattr(request.user,'_wrapped') else request.user

            # Check User to RoboUser equality
            if self.user_perform and user == obj.user:
                return True
            else:
                if type(user).__name__ != 'Project':
                    return False
                else:
                    if user.id not in self.project_id_to_user_ids:
                        return False
                    else:
                        users = self.project_id_to_user_ids[user.id]
                        return users is None or obj.id in users 


class UserBalancePermission(UserAuthorizedProjectOrReadOnlyPermission):
    project_id_to_user_ids = USER_BALANCE_PROJECTS_TO_USERS


class UserRFIDPermission(UserAuthorizedProjectOrReadOnlyPermission):
    project_id_to_user_ids = USER_RFID_PROJECTS_TO_USERS


class UserEmailPermission(UserAuthorizedProjectOrReadOnlyPermission):
    project_id_to_user_ids = USER_EMAIL_PROJECTS_TO_USERS

    """
    User can email themselves.
    """
    user_perform = True


class IsAPIRequesterOrReadOnlyPermission(permissions.BasePermission):
    """
    Anyone can view.  Only original Project to request API endpoint
    in first place('project' field) can update request.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            # TODO: find better way to work around lazy behavior of user object
            # Unwrap SimpleLazyObject so type is 'User' or 'Project'
            user = request.user._wrapped if hasattr(request.user,'_wrapped') else request.user

            # Ensure user is a Project and is the same project
            return (type(user).__name__ == 'Project') and (user.id == obj.updater_id)
