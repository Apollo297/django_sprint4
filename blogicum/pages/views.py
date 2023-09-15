from django.shortcuts import render


def about(request):
    template = 'pages/about.html'
    return render(request, template)


def rules(request):
    template = 'pages/rules.html'
    return render(request, template)


def page_not_found(request, exception):
    """Обработка ошибки 404."""
    return render(request, 'pages/404.html', status=404)


def csrf_failure(request, reason=''):
    """Обработка ошибки 403."""
    return render(request, 'pages/403csrf.html', status=403)


def server_error(request):
    """Обработка ошибки 500."""
    return render(request, 'pages/500.html', status=500)
