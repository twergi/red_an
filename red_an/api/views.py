from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import PostSerializer, SectionSerializer, SectionStaffSerializer
from ribbon.models import SectionPost, Section


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
def getSection(request, section_id):
    section = Section.objects.get(id=section_id)
    serializer = SectionSerializer(section, many=False)
    return Response(serializer.data)


@api_view(['GET'])
def getPosts(request, section_id):
    posts = SectionPost.objects.filter(section_id=section_id)
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getPost(request, post_id, section_id):
    post = SectionPost.objects.get(id=post_id)
    serializer = PostSerializer(post, many=False)
    return Response(serializer.data)
