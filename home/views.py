from django.contrib.auth import logout, authenticate, login
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404

from home.forms import ContactForm, LoginForm
from home.models import PortfolioItem, BlogPost


def index(request):
    return render(request, "index.html", {
        'portfolioSnapshot': PortfolioItem.objects.all().order_by("-id")[:3]
    })


def portfolio(request):
    return render(request, "portfolio.html", {
        'portfolio_items': PortfolioItem.objects.all()
    })


def portfolio_item(request, item_id="0"):
    return render(request, "portfolio_item.html", {
        "item": get_object_or_404(PortfolioItem, id=int(item_id))
    })



def blog(request):
    return render(request, "blog.html", {
        'blog_items': BlogPost.objects.all()
    })


def blog_post(request, item_id="0"):
    return render(request, "blog_post.html", {
        "item": get_object_or_404(BlogPost, id=int(item_id))
    })


def contact(request):
    return render(request, "contact.html", {'form': ContactForm()})


def send_email(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            send_mail(subject=form.cleaned_data['reason'],
                      message=form.cleaned_data['message'] + "\n"
                              + form.cleaned_data['name'] + " at "
                              + form.cleaned_data['sender'],
                      from_email="contactForm@rickycatron.com",
                      recipient_list=['dev@rickycatron.com'],
                      fail_silently=False)
    return redirect("/")


def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        try:
            login(request, user)
            return redirect("/admin")
        except:
            return redirect("/")
    else:
        return render(request, "login.html", {
            'loginForm': LoginForm(),
        })


def logout_view(request):
    logout(request)
    return redirect("/")
