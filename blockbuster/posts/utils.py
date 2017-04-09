import requests
from users.models import Profile
from users.models import UserRelationship
from users.constants import *
from nodes.models import Node
from django.contrib.sites.models import Site
import uuid

from posts.models import Post


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

def F_verify(foreign, local):
    """
    Verifies that the given ids are friends by sending a /author/{author_id}/friends/{author_id}/ request
    """
    node = Node.objects.filter(host=foreign.host, is_allowed=True)
    if node:
        node = node[0]

        api_url = '%s%sauthor/%s/friends/%s' % (foreign.host, node.api_endpoint, foreign.uuid, local.uuid)

        try:
            # print("Attempting to verify friendship between:", author_B, "and", author)
            response = requests.get(api_url, auth=(
                node.username_for_node, node.password_for_node))
        except requests.ConnectionError:
            response = None

        result = response.json() if response and 199 < response.status_code < 300 else None
        if (result and result.get('friends') != False):
            # print("friendship verified by host:", author_B.host)
            return result.get('friends')

    return False


def FOAF_verify(A, B, C):
    """
    Verifies that author B is friends of A and C. B is just the id of the author
    """

    site_name = Site.objects.get_current().domain

    # print("FOAF verifying author_B:", B)

    # if B is foreign
    if B.host != site_name:
        if F_verify(B, A) == F_verify(B, C) == True:
            return True

    # if B is local
    elif B.host == site_name:
        if (A in B.friends) and (C in B.friends):
            return True
    return False

def check_for_FOAF(local, foreign):
    """
    Sends an api POST request to author/{author_id}/friends/ to get a list of common friends
    """
    list_local = []

    for friend in local.friends:
        list_local.append(friend.api_id)

    if len(list_local) < 1:
        return []

    node = Node.objects.filter(host=foreign.host, is_allowed=True)
    if node:
        node = node[0]

        data = dict(
            query="friends",
            author=foreign.api_id,
            authors=list_local
        )
        api_url = '%s%sauthor/%s/friends/' % (foreign.host, node.api_endpoint, foreign.uuid)

        try:
            # print("Attempting to retrieve common freinds from foreign author= ", foreign)
            response = requests.post(api_url, json=data, auth=(
                node.username_for_node, node.password_for_node))
        except requests.ConnectionError:
            response = None

        result = response.json() if response and 199 < response.status_code < 300 else None
        if (result and result.get('authors') != False):
            # print("found common friends!:", result.get('authors'))
            return result.get('authors')

    return []

def viewable_to_FOAF(author_A, author_C):
    """
    Checks if the given author is friends of a friend of post's author making 
    it visible to the author. Assumes that the 2 authors are not friends
    """
    list_B = None
    site_name = Site.objects.get_current().domain

    #print("author C is", author_C)
    print(vars(author_C))
    # If both are local
    if author_A.host == site_name and author_C.host == site_name:
        # print("FOAF A and C are local")
        for friend in author_A.friends:
            # print("FOAF checking if:", friend, "is a common friend by using its id:", friend.api_id)
            if friend in author_C.friends:
                author_B = friend
                print("FOAF B found!:", author_B, "from host:", author_B.host)
                return FOAF_verify(author_A, author_B, author_C)

    local = None
    foreign = None
    if author_A.host == site_name and author_C.host != site_name:
        list_B = check_for_FOAF(author_A, author_C)
        local = author_A
        foreign = author_C

    elif author_A.host != site_name and author_C.host == site_name:
        list_B = check_for_FOAF(author_C, author_A)
        local = author_C
        foreign = author_A

    else:  # both are not local
        return False

    if len(list_B) < 1:
        return False

    for author_B in list_B:
        try:
            identifier = author_B.split('/')[-1]
            if len(identifier) <= 1:
                identifier = author_B.split('/')[-2]
            author_B = Profile.objects.get(uuid=identifier)
        except Profile.DoesNotExist:
            print "in-between author of FOAF relation apparently does not have a profile"

        if (author_B.host):
            if FOAF_verify(local, author_B, foreign):
                print "FOAF found shared friend:", author_B
                return True

    return False

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
    elif viewable_to_FOAF(profile, foreign_profile):
        return True
    else:
        return False