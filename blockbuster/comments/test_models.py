from django.test import TestCase
from comments.factories import CommentModelFactory


class CommentModelTestCase(TestCase):
    def test__created_date_saves_correctly(self):
        # GIVEN a comment is created
        # WHEN it is created/saved
        comment = CommentModelFactory()

        # THEN the created time is set
        self.assertTrue(comment.created)