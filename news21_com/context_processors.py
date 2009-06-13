from django.conf import settings

def google_analytics(request):
        return {'google_analytics_key': settings.GOOGLE_ANALYTICS_KEY}


