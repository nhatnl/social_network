from django.db.models import fields
from rest_framework import serializers

from .models import Comments

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ['user','parent_id', 'post_id', 'content', 'create_at', 'update_at']
    def validate_user(self, obj):
        if obj != self.context.get('request').user:
            raise serializers.ValidationError(detail='Not assign for current user')
        return obj
    def validate_post_id(self, obj):

        if obj.id != self.context.get('view').kwargs[self.context.get('view').lookup_url_kwarg_post_pk]:
            raise serializers.ValidationError(detail='Not assign for current post')
        return obj

    