import json
from django.urls import reverse
from django.http import JsonResponse
from django.http.response import HttpResponseBadRequest
from django.shortcuts import get_object_or_404

from .models import User, Hobby, FriendRequest


def user_api(request):
    """
        API entry point for a getting user's info
    """
    return JsonResponse({
        'users': [
            user.to_dict()
            for user in User.objects.all() if user.username == request.session['username']
        ]})

def users_api(request):
    """
        API entry point for a getting all users info.
    """
    return JsonResponse({
        'users': [
            user.to_dict()
            for user in User.objects.all()
        ]})


def hobbies_api(request):
    """
        API entry point for a list of hobbies.
        On POST: create a new student.
    """
    return JsonResponse({
        'hobbies': [
            hobby.to_dict()
            for hobby in Hobby.objects.all()
        ]
    })

def create_hobby(request):
    """API for creating a hobby"""
    if request.method == "POST":
        PUT = json.loads(request.body)
        hobby = Hobby(name=PUT['name'])
        hobby.save()
        return JsonResponse(hobby.to_dict())

    return HttpResponseBadRequest("Invalid method")

def update_user_api(request, id):
    """ API for updating a user. """

    user = get_object_or_404(User, id=id)


    if request.method == "PUT":
        PUT = json.loads(request.body)
        user.username = PUT['username']
        user.email = PUT['email']
        user.dob = PUT['dob']
        user.city = PUT['city']
        user.hobbies.clear()
        hobbies_list = PUT['hobbies']
        for i in range(len(hobbies_list)):
            try:
                hobby = get_object_or_404(Hobby, id=hobbies_list[i])
                user.hobbies.add(hobby)
            except:
                pass
        user.save()
        return JsonResponse(user.to_dict())

    return HttpResponseBadRequest("Invalid method")

def update_profile_pic(request):
    if request.method == "POST":
        user = User.objects.get(username=request.user.username)
        user.profile_pic = request.FILES['profile_pic']
        user.save()
        return JsonResponse(user.to_dict())
    return HttpResponseBadRequest("Invalid method")

# Friend Request
def get_friend_api(request):
    friends = {
        "sent": [],
        "received": [],
        "friends": []
    }
    for friendship in FriendRequest.objects.all():
        if friendship.are_friends:
            if friendship.sender.username == request.session["username"]:
                friends["friends"].append(friendship.receiver.to_dict())
            elif friendship.receiver.username == request.session["username"]:
                friends["friends"].append(friendship.sender.to_dict())
        else:
            if friendship.sender.username == request.session["username"]:
                friends["sent"].append(friendship.receiver.to_dict())
            elif friendship.receiver.username == request.session["username"]:
                temp_user = friendship.sender.to_dict()
                temp_user["accept"] = reverse("accept_friend_api", kwargs={
                    "id":friendship.id
                })
                temp_user["decline"] = reverse("decline_friend_api", kwargs={
                    "id":friendship.id
                })
                friends["received"].append(temp_user)
    return JsonResponse(friends)

def accept_friend_api(request, id):
    user = get_object_or_404(User, username=request.session["username"])
    friendship = FriendRequest.objects.get(id=id)

    if friendship.receiver.username == user.username:
        friendship.are_friends = True
        friendship.save()

        return JsonResponse({})

    return HttpResponseBadRequest("Invalid method")

def decline_friend_api(request, id):
    user = get_object_or_404(User, username=request.session["username"])
    friendship = FriendRequest.objects.get(id=id)

    if friendship.receiver.username == user.username:
        friendship.delete()
        return JsonResponse({})

    return HttpResponseBadRequest("Invalid method")


def send_friend_api(request, id):
    user = get_object_or_404(User, username=request.session["username"])

    friendship = FriendRequest()
    friendship.sender = User.objects.get(username=request.user.username)
    friendship.receiver = User.objects.get(id=id)
    friendship.save()

    return JsonResponse({})


# Get list of users.
def users_list_api(request):
    # Return the set of User objects back to the client.
    return JsonResponse({
        'users': [
            user.to_dict()
            for user in User.objects.all()
        ],
    })
