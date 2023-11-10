from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework import serializers
from django.contrib.auth.models import User
from digestapi.models import Book, Review
from .categories import CategorySerializer


class BookReviewUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name']


class BookReviewSerializer(serializers.ModelSerializer):

    user = BookReviewUserSerializer(many=False)

    class Meta:
        model = Review
        fields = ['id', 'user', 'date', 'rating', 'comments']


class BookSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True)
    reviews = BookReviewSerializer(many=True)
    # Declare that an ad-hoc property should be included in JSON
    is_owner = serializers.SerializerMethodField()

    # Function containing instructions for ad-hoc property
    def get_is_owner(self, obj):
        # Check if the authenticated user is the owner
        return self.context['request'].user == obj.user

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'isbn_number',
                  'cover_image', 'is_owner', 'categories', 'reviews']


class BookViewSet(viewsets.ViewSet):

    def list(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(
            books,
            many=True,
            context={'request': request}  # Allow serializer to access request
        )
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            book = Book.objects.get(pk=pk)
            serializer = BookSerializer(book, context={'request': request})
            return Response(serializer.data)

        except Book.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        # Get the data from the client's JSON payload
        title = request.data.get('title')
        author = request.data.get('author')
        isbn_number = request.data.get('isbn_number')
        cover_image = request.data.get('cover_image')

        # Create a book database row first, so you have a
        # primary key to work with
        book = Book.objects.create(
            user=request.user,
            title=title,
            author=author,
            cover_image=cover_image,
            isbn_number=isbn_number)

        # Get the list of [3, 5] from the request payload
        category_ids = request.data.get('categories', [])
        # Assign categories 3 and 5 to the new book 12 with one line of code
        book.categories.set(category_ids)

        serializer = BookSerializer(book, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        try:

            book = Book.objects.get(pk=pk)

            # Is the authenticated user allowed to edit this book?
            self.check_object_permissions(request, book)

            serializer = BookSerializer(data=request.data)
            if serializer.is_valid():
                book.title = serializer.validated_data['title']
                book.author = serializer.validated_data['author']
                book.isbn_number = serializer.validated_data['isbn_number']
                book.cover_image = serializer.validated_data['cover_image']
                book.save()

                category_ids = request.data.get('categories', [])
                book.categories.set(category_ids)

                serializer = BookSerializer(book, context={'request': request})
                return Response(None, status.HTTP_204_NO_CONTENT)

            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        except Book.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        try:
            book = Book.objects.get(pk=pk)
            self.check_object_permissions(request, book)
            book.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        except Book.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
