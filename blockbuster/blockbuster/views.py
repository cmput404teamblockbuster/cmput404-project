from django.shortcuts import render
from django.contrib.auth import authenticate, login


def myStream(request):
    return render(request, 'myStream.html')


def login(request):
    return render(request, 'login.html')


def myFriends(request):
    return render(request, 'myFriends.html')


def profile(request):
    return render(request, 'profile.html')

def singlePost(request):
    return render(request, 'singlePost.html')


# def login_view(request):
#     """
#     from https://docs.djangoproject.com/en/1.10/topics/auth/default/#how-to-log-a-user-in
#     """
#     username = request.POST['username']
#     password = request.POST['password']
#     user = authenticate(username=username, password=password)
#     if user is not None:
#         login(request, user)
#         return render(request, 'index.html')
#     else:
#         pass
#         # TODO raise error or something
