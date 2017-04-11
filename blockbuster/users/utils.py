import requests
from nodes.models import Node
from django.contrib.sites.models import Site


def determine_if_request_from_foundbook(request):
    """
    Since foundbook sends friendrequests without friend requests then we need to convert the code for them.
    They dont give displayName, and id is jsut the uuid without the rest of the url
    """
    author = request.get('author')
    friend = request.get('friend')
    if 'http' not in author.get('id'):
        return True
    elif 'http' not in friend.get('id'):
        return True

    return False

def verify_friends(foreign, local):
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
            print("friendship between:", local, "and:", foreign,"verified by host:", foreign.host)
            return result.get('friends')

    print("friendship between:", local, "and:", foreign, "failed to verify with host:", foreign.host, "Response:",
          vars(result))
    return False


def verify_foaf(A, B, C):
    """
    Verifies that author B is friends of A and C. B is just the id of the author
    """

    site_name = Site.objects.get_current().domain

    # print("FOAF verifying author_B:", B)

    # if B is foreign
    if B.host != site_name:
        if verify_friends(B, A) == verify_friends(B, C) == True:
            return True

    # if B is local
    elif B.host == site_name:
        if (A in B.friends) and (C in B.friends):
            return True
    return False

def check_for_foaf(local, foreign):
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

def determine_if_foaf(author_A, author_C):
    """
    Checks if the given author is friends of a friend of post's author making 
    it visible to the author. Assumes that the 2 authors are not friends
    """
    list_B = None
    site_name = Site.objects.get_current().domain

    #print("author C is", author_C)
    #print(vars(author_C))
    # If both are local
    if author_A.host == site_name and author_C.host == site_name:
        # print("FOAF A and C are local")
        for friend in author_A.friends:
            # print("FOAF checking if:", friend, "is a common friend by using its id:", friend.api_id)
            if friend in author_C.friends:
                author_B = friend
                print("FOAF B found!:", author_B, "from host:", author_B.host)
                return verify_foaf(author_A, author_B, author_C)

    local = None
    foreign = None
    if author_A.host == site_name and author_C.host != site_name:
        list_B = check_for_foaf(author_A, author_C)
        local = author_A
        foreign = author_C

    elif author_A.host != site_name and author_C.host == site_name:
        list_B = check_for_foaf(author_C, author_A)
        local = author_C
        foreign = author_A

    else:  # both are not local
        return False

    if len(list_B) < 1:
        return False

    for author_B in list_B:
        for friend in local.friends:
            if friend.api_id == author_B:
                author_B = friend
                continue
        if (author_B.host):
            if verify_foaf(local, author_B, foreign):
                print "FOAF found/verified shared friend:", author_B
                return True

    return False