from django.shortcuts import render

def handle_not_found(request, exception):
    return render(request, 'portfolio/not-found.html', status=404)