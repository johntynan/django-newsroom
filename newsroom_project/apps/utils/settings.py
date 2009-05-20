from django.conf import settings

NEWSROOM_TEST_SUITE =getattr(settings,
    "UTILS_NEWSROOM_TEST_SUITE",
    ["stories", "multimedia"])