from rest_framework import serializers
from posts.models import Post
from comments.api.serializers import CommentSerializer

from users.api.serializers import UserSerializer


class PostSerializer(serializers.ModelSerializer):
    # http://www.django-rest-framework.org/api-guide/relations/#nested-relationships
    author = UserSerializer()
    comments = CommentSerializer(many=True, read_only=True)

    def validate(self, attrs):
        attrs = super(PostSerializer, self).validate(attrs)
        if not self._errors:
            print attrs
            # if not attrs['venue'].public_twilio_phone_number:
            #     self._errors['venue'] = 'You must purchase a twilio phone number to use this feature.'
            #     return
            #
            # attrs['recipient_list'] = Campaign.generate_campaign_recipients(self.venue_users.all())
            #
            # attrs['sms_recipient_count'] = len(attrs['recipient_list'])
            # if attrs['sms_recipient_count'] <= 0:
            #     self._errors['sms_recipient_count'] = 'There are no valid phone numbers in the selected list.'
            #     return

        return attrs

    class Meta:
        model = Post
        fields = ('author', 'comments', 'content') # These fields will be available to the front end
