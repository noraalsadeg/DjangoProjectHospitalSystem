import io
from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request

from rest_framework import status

from .  import sections, Comment
from serializers import CommentSerializer

from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated



#requiring authentication for this view
@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])

def add_store(request : Request):

    #authenticated user info is stored in request.user
    user = request.user

    if not user.is_authenticated:
        return Response({"msg" : "Please Log In"})

    name = request.data["name"]
    desc = request.data["description"]
    rating = request.data["rating"]
    pub_date = request.data["pub_date"]

    new_store = sections(title=name, description=desc, rating=rating, pub_date=pub_date)
    new_store.save()

    res_data = {
        "msg" : "Created store Successfully"
    }

    return Response(res_data)


@api_view(["GET"])
def list_sections(request : Request):


    print(sections.objects.count()) #returns the total count of stores in the database, for testing only

    stores_with_high_rating_count = sections.objects.filter(rating__gte=4).count() #get count of stores greater thank 4
    print(stores_with_high_rating_count) #for testing only


    skip = int(request.query_params.get("skip", 0))
    get = int(request.query_params.get("get", 10))

    if "search" in request.query_params:
        search_phrase = request.query_params["search"]
        all_stores = sections.objects.filter(title__startswith=search_phrase)[skip:get]
    else:
        all_stores = sections.objects.all().order_by('-rating')[skip:get]

    all_sections_list = [{"id" : sections.id, "title" : sections.title, "rating" : sections.rating, "pub_date" : sections.pub_date} for store in all_stores]

    res_data = {
        "msg" : "A list of All stores",
        "stores" : all_sections_list
    }

    return Response(res_data, status=status.HTTP_200_OK)



@api_view(['PUT'])
def update_sections(request : Request, sections_id):

    name = request.data["name"]
    desc = request.data["description"]
    rating = request.data["rating"]

    sections = sections.objects.get(id=sections_id)

    sections.title = name
    sections.description = desc
    sections.rating = rating

    sections.save()

    return Response({"msg" : " store is updated  200!"})



@api_view(["DELETE"])
def delete_sections(request : Request, sections_id):

    try:
        sections = sections.objects.get(id=sections_id)
        sections.delete()
    except Exception as e:
        return Response({"msg" : "The store is not Found!"})

    return Response({"msg" : f"delete the following store {sections.title}"})



@api_view(['POST'])
def add_comment(request : Request):

    comment_serializer = CommentSerializer(data=request.data)

    if comment_serializer.is_valid():
        comment_serializer.save()
    else:
        return Response({"msg" : "couldn't create a comment", "errors" : comment_serializer.errors}, status=status.HTTP_403_FORBIDDEN)


    return Response({"msg" : "Comment Added Successfully!"}, status=status.HTTP_201_CREATED)



@api_view(['GET'])
def list_comments(request : Request):

    if "store_id" in request.query_params:
        comments = Comment.objects.filter(store=request.query_params["store_id"])
    else:
        comments = Comment.objects.all()

    comments_data = CommentSerializer(instance=comments, many=True).data

    return Response({"msg" : "list of all comments", "comments" : comments_data})


@api_view(['PUT'])
def update_comment(request : Request, comment_id):

    try:
        comment = Comment.objects.get(id=comment_id)
    except Exception as e:
        return Response({"msg" : "This comment is not found"}, status=status.HTTP_404_NOT_FOUND)

    comment_serializer = CommentSerializer(instance=comment, data=request.data)

    if comment_serializer.is_valid():
        comment_serializer.save()
    else:
        return Response({"msg" : "couldn't update", "errors" : comment_serializer.errors})

    return Response({"msg" : "Comment updated successfully"})
