from users.models import Profile
from users.models import UserRelationship
from users.constants import *


def foreign_post_viewable_for_author(post, profile):
    """
    will check to see if the post is viewable to the given author
    Args:
        post: a json dict representation of a post object. It is expected that this is from another server
        author: a local Profile object

    Returns: boolean

    WARNING: This needs to follow the docs of other groups *precisely* in order to work
    """
    post_viewable_to = post.get('visibleTo')
    if profile.uuid in post_viewable_to:
        return True
    post_visibility = post.get('visibility')
    post_author = post.get('author')
    author_username = post_author.get('displayName')
    author_host = post_author.get('host')
    foreign_profile = Profile.objects.filter(host=author_host, username=author_username)
    if not foreign_profile:  # Then there is no relationship with that author and no chance of visibility at this point
        return False

    friends1 = UserRelationship.objects.filter(initiator=foreign_profile, receiver=profile,
                                               status=RELATIONSHIP_STATUS_FRIENDS)
    friends2 = UserRelationship.objects.filter(receiver=foreign_profile, initiator=profile,
                                               status=RELATIONSHIP_STATUS_FRIENDS)
    following = UserRelationship.objects.filter(receiver=foreign_profile, initiator=profile,
                                                status=RELATIONSHIP_STATUS_FOLLOWING)
    pending = UserRelationship.objects.filter(receiver=foreign_profile, initiator=profile,
                                              status=RELATIONSHIP_STATUS_PENDING)
    relationship_exists = friends1 | friends2 | following | pending
    if relationship_exists and post_visibility in ['FRIENDS', 'PUBLIC']:
        return True

    return False
