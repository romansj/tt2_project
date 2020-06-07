from django.core.mail import get_connection, send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render

# from catalog.models import Book, Author, BookInstance, Genre
from .forms import ContactForm


# Create your views here.


def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    # num_books = Book.objects.all().count()
    num_books = 5
    # num_instances = BookInstance.objects.all().count()
    num_instances = 10

    # Available books (status = 'a')
    # num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_instances_available = 5

    # The 'all()' is implied by default.
    # num_authors = Author.objects.count()
    num_authors = 3

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'amachef/index.html', context=context)


def contact(request):
    submitted = False

    if request.method == 'POST':
        form = ContactForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            # assert False

            con = get_connection('django.core.mail.backends.console.EmailBackend')

            send_mail(

                cd['subject'],

                cd['message'],

                cd.get('email'), ['amachefdf@gmail.com'],

                connection=con
            )

        return HttpResponseRedirect('/amachef/contact/?submitted=True')
    else:

        form = ContactForm()

        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'amachef/contact.html', {'form': form, 'submitted': submitted})


def settings(request):
    return render(request, 'amachef/settings.html')
