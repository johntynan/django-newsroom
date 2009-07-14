from django.shortcuts import _get_queryset



def user_objects_qs(klass, user):
    """
    Returns a filtered QuerySet from a Model or QuerySet.
    If the user is_staff the queryset contains all the object
    else it contains only the object where the user is in the
    authors list.
    """
    queryset = _get_queryset(klass)
    if user.is_staff:
        return queryset
    else:
        queryset = queryset.filter(submitter=user)
        return queryset
    