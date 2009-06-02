from videos.models import Video
import os.path
import os
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from stories.tests import create_draft_story, create_user



class VideoUrlTests(TestCase):
    """
    These tests exercise the views.
    """
    def setUp(self):
        self.user = create_user("user")
        self.story_draft = create_draft_story(
                headline="draft story",
                user=self.user)


        self.client.login(username="user", password="secret")
    def tearDown(self):
        self.client.logout()

    def test_add_video_get_url(self):
        self.response = self.client.get(
            reverse("stories_story_add_media",
            kwargs={"story_id" : self.story_draft.id,
                "media_type" : "video"}))
        self.assertEqual(self.response.status_code, 200)

    def test_add_video_post_url(self):
        try:
            TESTS_DIR = os.path.abspath(os.path.dirname(__file__))
            frame = open(os.path.join(TESTS_DIR, "test_frame.jpg"))
            video =  open(os.path.join(TESTS_DIR, "test_video.flv"))
            self.response = self.client.post(
                reverse("stories_story_add_media",
                kwargs={"story_id" : self.story_draft.id,
                    "media_type" : "video"}),
                    {
                        "title":"test video",
                        "status":"D",
                        "license":"http://creativecommons.org/licenses/by/2.0/",
                         "authors" : (self.user.id,),
                         "sites" : (1,),
                         "video":video,
                         "image":frame,
                    })
        finally:
            frame.close()
            video.close()
        self.assertEqual(self.response.status_code, 302)
        # Check if the video as been created
        self.assertEqual(1, Video.objects.count())
        self.assertEqual(self.story_draft.get_relatedcontent(),
            {'video': [Video.objects.all()[0]]})
