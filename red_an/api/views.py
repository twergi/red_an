from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import PostSerializer, SectionSerializer, SectionStaffSerializer, CommentSerializer
from ribbon.models import SectionPost, Section, PostReview, Comment, CommentReview
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
import json


@api_view(['GET'])
def getRoutes(request):
    routes = [
        {'GET': '/api/sections'},
        {'GET': '/api/sections/id'},
        {'GET': '/api/sections/id/posts'},
        {'GET': '/api/sections/id/posts/id'},
        {'POST': '/api/sections/id/posts/id/vote'},
        {'POST': '/api/sections/id/posts/id/comments/id/vote'},
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
def postVote(request, section_id, post_id):
    post = SectionPost.objects.get(id=post_id)
    user = request.user
    data = request.data

    vote_rating = {'up': 1, 'down': -1}

    review, created = PostReview.objects.get_or_create(
        owner=user,
        post=post,
    )

    if created is False:
        if data['value'] == review.value:
            review.delete()
            delta_rating = -vote_rating[data['value']]
        else:
            review.value = data['value']
            review.save()

            delta_rating = 2 * vote_rating[data['value']]

    else:
        review.value = data['value']
        review.save()

        delta_rating = vote_rating[data['value']]

    post.rating += delta_rating
    user.profile.rating += delta_rating
    post.save()
    user.profile.save()
    serializer = PostSerializer(post, many=False)
    print(serializer.data)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def commentVote(request, section_id, post_id, comment_id):
    comment = Comment.objects.get(id=comment_id)
    user = request.user
    data = request.data

    vote_rating = {'up': 1, 'down': -1}

    review, created = CommentReview.objects.get_or_create(
        owner=user,
        comment=comment,
    )

    if created is False:
        if data['value'] == review.value:
            review.delete()
            delta_rating = -vote_rating[data['value']]
        else:
            review.value = data['value']
            review.save()

            delta_rating = 2 * vote_rating[data['value']]

    else:
        review.value = data['value']
        review.save()

        delta_rating = vote_rating[data['value']]

    comment.rating += delta_rating
    comment.profile_id.rating += delta_rating
    comment.profile_id.save()
    comment.save()
    serializer = CommentSerializer(comment, many=False)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getVotedPosts(request, username):
    user = User.objects.get(username=username)
    reviews = PostReview.objects.filter(owner=user)
    voted_posts = {}
    for review in reviews:
        voted_posts[str(review.post.id)] = review.value

    data = json.dumps(voted_posts)
    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getVotedComments(request, username, post_id):
    user = User.objects.get(username=username)
    reviews = CommentReview.objects.filter(comment__section_post_id=post_id).filter(owner=user)

    voted_comments = {}
    for review in reviews:
        voted_comments[str(review.comment.id)] = review.value

    data = json.dumps(voted_comments)
    return Response(data)
