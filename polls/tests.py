import datetime
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.utils import timezone
from models import Poll, Choice, Comment, Vote, Ratings
# Create your tests here.
class PollTestCase(TestCase):
    def test_was_published_recently_with_future_poll(self):
        """
        was_published_recently() should return False for polls whose
        pub_date is in the future
        """
        future_poll = Poll(pub_date=timezone.now() + datetime.timedelta(days=30))
        self.assertEqual(future_poll.was_published_recently(), True)