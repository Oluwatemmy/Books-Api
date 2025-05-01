from .models import Book
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, DestroyAPIView
from .serializers import BookSerializer
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

# Create your views here.
class CreateBookView(CreateAPIView):
    """
    A view that handles the creation of a new book entry.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class ListAllBookView(ListAPIView):
    """
    A view that handles the listing of all book entries.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class ListABookView(ListAPIView):
    """
    A view that handles the listing of a single book entry.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get(self, request, pk):
        try:
            book = Book.objects.get(pk=pk)
            serializer = self.serializer_class(book)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Book.DoesNotExist:
            return Response(
                {"error": "Book not found."},  # Corrected error message
                status=status.HTTP_404_NOT_FOUND
            )
        
class DeleteBookView(DestroyAPIView):
    """
    A view that handles the deletion of a book entry.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def delete(self, request, pk):
        try:
            book = Book.objects.get(pk=pk)
            book.delete()
            return Response({"message": "Book deleted."}, status=status.HTTP_200_OK)
        except Book.DoesNotExist:
            return Response(
                {"error": "Book not found."}, status=status.HTTP_404_NOT_FOUND
            )
        
class UpdateBookView(UpdateAPIView):
    """
    A view that handles the updating of a book entry.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def put(self, request, pk):
        try:
            book = get_object_or_404(Book, pk=pk)
        except Book.DoesNotExist:
            return Response({"error": "Book not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(book, data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                    {
                        "message": "Book updated successfully",
                        "data": serializer.data,
                    },
                    status=status.HTTP_200_OK,
                )
        return Response(
            {"message": "Product update failed", "data": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )
        
