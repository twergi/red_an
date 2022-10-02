from rest_framework.response import Response
from .serializers import PostSerializer, SectionSerializer, SectionStaffSerializer
from ribbon.models import SectionPost, Section, PostReview
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated


@api_view(['GET'])
def getRoutes(request):
    routes = [
        {'GET': '/api/sections'},
        {'GET': '/api/sections/id'},
        {'GET': '/api/sections/id/posts'},
        {'GET': '/api/sections/id/posts/id'},
        {'POST': '/api/sections/id/posts/id/vote'},
    ]
    return Response(routes)


@api_view(['GET'])
def getSections(request):
    sections = Section.objects.all()
    serializer = SectionSerializer(sections, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getSection(request, section_id):
    section = Section.objects.get(id=section_id)
    context = {
        'id': section_id,
        'title': section.title,
        'short_description': section.short_description,
        'description': section.description,
        'owner': section.owner.user_id,
        'date_created': section.date_created,
    }
    serializer = SectionStaffSerializer(context, many=False)
    return Response(serializer.data)


@api_view(['GET'])
def getPosts(request, section_id):
    posts = SectionPost.objects.filter(section_id=section_id)
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getPost(request, post_id, section_id):
    post = SectionPost.objects.get(id=post_id)
    serializer = PostSerializer(post, many=False)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def postVote(request, post_id):
    post = SectionPost.objects.get(id=post_id)
    user = request.user
    data = request.data

    review, created = PostReview.objects.get_or_create(
        owner=user,
        post=post,
    )

    review.value = data['value']
    review.save()
    post.updateRating()

    serializer = PostSerializer(post, many=False)
    return Response(serializer.data)
