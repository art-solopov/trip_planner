from django.urls import reverse_lazy

NAVIGATION = [
    ('/', 'Cities')
]


def navigation(_request):
    return {'navigation': NAVIGATION}
