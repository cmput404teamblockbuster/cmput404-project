from django.contrib import admin
from users.models import Profile, UserRelationship, NewUser

# Re-register UserAdmin
admin.site.register(NewUser)
admin.site.register(Profile)
admin.site.register(UserRelationship)

