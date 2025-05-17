from django.http import HttpResponse


def hello(request):
    """Return a simple Hello, world! response."""
    return HttpResponse("Hello, world!\n")
