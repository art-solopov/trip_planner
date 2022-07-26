from django.urls import reverse_lazy

NAVIGATION = [
    (reverse_lazy('cities-list'), 'Cities')
]


def navigation(_request):
    return {'navigation': NAVIGATION}
