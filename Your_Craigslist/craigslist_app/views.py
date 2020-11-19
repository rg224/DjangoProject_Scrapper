from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, template_name='base.html')

def new_search(request):

    if request.method == "POST":
        searched = request.POST.get("search")

    stuff_to_search = {'search':searched}

    return render(request, 'craigslist_app/new_search.html', stuff_to_search)