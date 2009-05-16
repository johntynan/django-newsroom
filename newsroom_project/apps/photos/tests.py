from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.template.defaultfilters import slugify
from stories.models import Story

def create_story():
    story = Story()
    story.headline = "This Is A Test Story"
    #normally slugify will be handled by the UI
    story.slug = slugify(story.headline)
    story.summary = "Like I said in the headline, this is a test story."
    #TODO add an author(s)
    story.save()
    return story

def create_user():
    user =  User.objects.create_user("user", "user@mail.com", "secret")
    return user

class PhotoUrlTests(TestCase):
    """
    These tests exercise the views.
    """
    def setUp(self):
        self.story = create_story()
        self.user = create_user()
        self.client.login(username="user", password="secret")
    def tearDown(self):
        self.client.logout()


    def test_add_photo_get_url(self):
        self.response = self.client.get(
            reverse("stories_story_add_media",
            kwargs={"story_id" : self.story.id,
                "media_type" : "photo"}))
        self.assertEqual(self.response.status_code, 200)
