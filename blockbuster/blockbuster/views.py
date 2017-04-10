from django.shortcuts import render


def myStream(request):
    return render(request, 'myStream.html')

def login(request):
    return render(request, 'login.html')

def myFriends(request):
    return render(request, 'myFriends.html')

def profile(request):
    return render(request, 'profile.html')

def singlePost(request, uuid):
    return render(request, 'singlePost.html')

def public(request):
    return render(request, 'publicPosts.html')
