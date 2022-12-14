from rest_framework import serializers
from ribbon.models import Section, SectionPost, Comment


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = SectionPost
        fields = [
            'id',
            'title',
            'rating',
            'section_id',
            'date_published'
        ]


class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = [
            'id',
            'title',
            'date_created'
        ]


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField()


class SectionStaffSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    title = serializers.CharField()
    short_description = serializers.CharField()
    description = serializers.CharField()
    owner = UserSerializer(many=False)
    date_created = serializers.DateTimeField()


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            'id',
            'profile_id',
            'section_post_id',
            'rating',
        ]
