from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.views import generic

# Create your views here.
from .models import Book, Author, BookInstance, Genre


def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact="a").count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()
    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_books": num_books,
        "num_instances": num_instances,
        "num_instances_available": num_instances_available,
        "num_authors": num_authors,
        "num_visits": num_visits,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, "index.html", context=context)


class BookListView(generic.ListView):
    model = Book
    context_object_name = "book_list"
    queryset = Book.objects.all()
    template_name = "book_list.html"


class BookDetailView(generic.DetailView):
    model = Book
    template_name = "book_detail.html"


def book_detail_view(request, primary_key):
    # try:
    #     book = Book.objects.get(pk=primary_key)
    # except Book.DoesNotExist:
    #     raise Http404('Book does not exist')
    book = get_object_or_404(Book, pk=primary_key)
    return render(request, "catalog/book_detail.html", context={"book": book})


class AuthorDetailView(generic.DetailView):
    model = Author
    template_name = "author_detail.html"
