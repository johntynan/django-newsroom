
def create_profile(sender, instance, signal, created, **kwargs):
    """When user is created also create a profile."""
    from core.models import Person
    if created:
        Person(user = instance).save()

