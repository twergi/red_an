from rest_framework import serializers
from ribbon.models import Section, SectionPost, SectionStaff


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = SectionPost
        fields = '__all__'


class SectionSerializer(serializers.ModelSerializer):
    staff = ''

    class Meta:
        model = Section
        fields = [
            'id',
            'title',
            'short_description',
            'description',
            'date_created'
        ]


class SectionStaffSerializer(serializers.ModelSerializer):
    section = SectionSerializer(many=False)

    class Meta:
        model = SectionStaff
        fields = [
            'section',
            'owner',
            'moderators',
        ]

# class SectionAndStaffSerializer
