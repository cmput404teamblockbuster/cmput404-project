from django.test import TestCase

# Create your tests here.
from comments.factories import CommentModelFactory


class CommentModelTestCase(TestCase):
    # TODO get factory boy working and test this
    def test__created_date_saves_correctly(self):
        # GIVEN a comment is created
        # WHEN it is created/saved
        comment = CommentModelFactory()

        # THEN the correct time is displayed
        print comment.created
        self.assertTrue(comment.created)