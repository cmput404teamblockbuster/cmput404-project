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