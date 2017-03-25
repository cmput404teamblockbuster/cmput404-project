from rest_framework.test import APIRequestFactory, force_authenticate, APITestCase, APIClient
from users.factories import ProfileModelFactory, UserModelFactory
from rest_framework import status
from posts.factories import BasePostModelFactory
from comments.models import Comment
from posts.constants import PRIVATE_TO_ME


class CommentViewSetTestCase(APITestCase):
    client = APIClient()

    # from example http://www.django-rest-framework.org/api-guide/testing/#example

    def test__create_comment_success(self):
        # GIVEN an authenticated user chooses to make a comment on a post
        post_author = UserModelFactory()
        post_obj = BasePostModelFactory(author=post_author.profile)
        comment_author = UserModelFactory()
        self.client.force_authenticate(
            user=comment_author)  # http://www.django-rest-framework.org/api-guide/testing/#force_authenticateusernone-tokennone
        body = 'This is a comment on the post!'
        data = dict(
            author=dict(
                id=str(comment_author.profile.api_id),
                displayName='bradley',
            ),
            comment=body,
            post=dict(
                uuid=post_obj.uuid,
            )
        )
        url = '/api/posts/%s/comments/' % post_obj.uuid

        # WHEN the comment is posted
        response = self.client.post(url, data, format='json')

        # THEN the comment should be created, and a successful response message returned
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('message'), "Comment Added")
        self.assertTrue(response.data.get('success'))
        comment = Comment.objects.all()[0]
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(comment.author, comment_author.profile)
        self.assertEqual(comment.body, body)
        self.assertEqual(comment.post, post_obj)

    def test__create_comment__unviewable_post_fails(self):
        # GIVEN an authenticated user chooses to make a comment on a post that is not viewable to them
        post_author = UserModelFactory()
        post_obj = BasePostModelFactory(privacy=PRIVATE_TO_ME, author=post_author.profile)
        comment_author = UserModelFactory()
        self.client.force_authenticate(
            user=comment_author)  # http://www.django-rest-framework.org/api-guide/testing/#force_authenticateusernone-tokennone
        body = 'This is a comment to myself'
        data = dict(
            author=dict(
                id=str(comment_author.profile.api_id),
                displayName='bradley',
            ),
            comment=body,
            post=dict(
                uuid=post_obj.uuid,
            )
        )
        url = '/api/posts/%s/comments/' % post_obj.uuid

        # WHEN the comment is posted
        response = self.client.post(url, data, format='json')

        # THEN the comment should not be created, and a forbidden response message returned
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data.get('message'), "Comment not allowed")
        self.assertFalse(response.data.get('success'))
        self.assertEqual(Comment.objects.count(), 0)

    def test__create_comment__unauthed_author_fails(self):
        # GIVEN an unauthenticated user chooses to make a comment on a post
        post_author = UserModelFactory()
        post_obj = BasePostModelFactory(author=post_author.profile)
        comment_author = UserModelFactory()
        body = 'This is a comment!'
        data = dict(
            author=dict(
                id=str(comment_author.profile.api_id),
                displayName='bradley',
            ),
            comment=body,
            post=dict(
                uuid=post_obj.uuid,
            )
        )
        url = '/api/posts/%s/comments/' % post_obj.uuid

        # WHEN the comment is posted
        response = self.client.post(url, data, format='json')

        # THEN the comment should not be created, and an error status code raised
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data.get('detail'), "Authentication credentials were not provided.")
        self.assertEqual(Comment.objects.count(), 0)

    def test__create_comment__empty_body_text_fails(self):
        # GIVEN an authenticated user chooses to make a comment on a post
        post_author = UserModelFactory()
        post_obj = BasePostModelFactory(author=post_author.profile)
        comment_author = UserModelFactory()
        self.client.force_authenticate(user=comment_author)

        # AND the comment has no text body
        body = ''
        data = dict(
            author=dict(
                id=str(comment_author.profile.api_id),
                displayName='bradley',
            ),
            comment=body,
            post=dict(
                uuid=post_obj.uuid,
            )
        )
        url = '/api/posts/%s/comments/' % post_obj.uuid

        # WHEN the comment is posted
        response = self.client.post(url, data, format='json')

        # THEN the comment should not be created, and an error status code raised
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('comment')[0], "This field may not be blank.")
        self.assertEqual(Comment.objects.count(), 0)
