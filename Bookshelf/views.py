from django.http import HttpResponse, Http404
from django.core.exceptions import PermissionDenied


def raise_my_404(request):
    raise Http404