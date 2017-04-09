import requests
from users.models import Profile
from users.models import UserRelationship
from users.constants import *
from nodes.models import Node
from django.contrib.sites.models import Site
import uuid
from users.utils import determine_if_foaf



def foreign_post_viewable_for_author(post, profile):
    """
    will check to see if the post is viewable to the given author
    Args:
        post: a json dict representation of a post object. It is expected that this is from another server
        author: a local Profile object

    Returns: boolean

    WARNING: This needs to follow the docs of other groups *precisely* in order to work
    """
    print("checking viewablility for foreign post with title:", post.get('title'), "and visibility:",
          post.get('visibility'))
    post_viewable_to = post.get('visibleTo')
    if post_viewable_to and profile.uuid in post_viewable_to:
        return True
    post_visibility = post.get('visibility')
    post_author = post.get('author')
    author_username = post_author.get('displayName')
    author_host = post_author.get('host')
    foreign_profile = Profile.objects.filter(host=author_host, username=author_username)
    if foreign_profile:
        foreign_profile = foreign_profile[0]
    if not foreign_profile:  # Then there is no relationship with that author and no chance of visibility at this point
        if post_visibility == 'FOAF': # Can still be visible to FOAF?
            return check_if_viewable_as_FOAF(post, profile)
        else:
            return False
    elif post_visibility == 'FOAF':
        return check_if_viewable_as_FOAF(post, profile, foreign_profile)

    friends1 = UserRelationship.objects.filter(initiator=foreign_profile, receiver=profile,
                                               status=RELATIONSHIP_STATUS_FRIENDS)
    friends2 = UserRelationship.objects.filter(receiver=foreign_profile, initiator=profile,
                                               status=RELATIONSHIP_STATUS_FRIENDS)
    following = UserRelationship.objects.filter(receiver=foreign_profile, initiator=profile,
                                                status=RELATIONSHIP_STATUS_FOLLOWING)
    pending = UserRelationship.objects.filter(receiver=foreign_profile, initiator=profile,
                                              status=RELATIONSHIP_STATUS_PENDING)
    relationship_exists = friends1 | friends2 | following | pending
    if relationship_exists and post_visibility in ['FRIENDS', 'PUBLIC', 'FOAF']:
        return True

    return False


def get_foreign_posts_by_author(author_uuid):
    """
    This will search all nodes for posts by the specified author uuid
    WARNING: This will return all posts by the author. You must filter them out yourself
    """
    host = find_authors_host(author_uuid)
    if not host:
        return None
    for node in Node.objects.filter(host=host, is_allowed=True):
        url = '%sauthor/%s/posts/' % (node.host, author_uuid)
        try:
            response = requests.get(url, auth=(node.username_for_node, node.password_for_node))
        except requests.ConnectionError:
            print ('ERROR: could not connect to host %s' % node.host)
            continue
        if 199 < response.status_code < 300:
            try:
                return response.json().get('posts')
            except AttributeError:
                return response.json()
        continue
    return None


def find_authors_host(author_uuid):
    """
    This will search all nodes for the host of a given uuid
    """
    # First we look for the host of the user by asking all nodes. The issue is some nodes might have local copies
    for node in Node.objects.filter(is_allowed=True):
        url = '%sauthor/%s/' % (node.host, author_uuid)
        try:
            response = requests.get(url, auth=(node.username_for_node, node.password_for_node))
        except requests.ConnectionError:
            print ('WARNING - could not connect to host %s. Continuing...' % node.host)
            continue
        if 199 < response.status_code < 300:
            host = response.json().get('host')
            return host

    return None


def check_if_viewable_as_FOAF(post, profile, foreign_profile=None):
    print("FOAF ATTEMPTING FOAF for post with title:", post.get('title'))

    if not foreign_profile:
        try:
            identifier = post.get('author').get('id').split('/')[-1]
            if len(identifier) <= 1:
                identifier = post.get('author').get('id').split('/')[-2]
            # create a user if it is remote user
            foreign_profile = Profile.objects.get(uuid=identifier)
        except Profile.DoesNotExist:
            author = post.get('author')
            foreign_profile = Profile.objects.create(uuid=uuid.UUID(identifier).hex, username=author.get('displayName'),
                                         host=author.get('host'))
            if foreign_profile:
                foreign_profile = foreign_profile[0]

    if not foreign_profile:
        return False
    elif determine_if_foaf(profile, foreign_profile):
        return True
    else:
        return False