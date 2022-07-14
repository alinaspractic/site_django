from django.contrib.auth import logout, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView

from bloginf.forms import AddPostForm, LoginUserForm
from bloginf.models import *
from bloginf.utils import DataMixin

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        #{'title': "Войти", 'url_name': 'login'},

]

class RegisterUser(DataMixin, CreateView):
    form_class = UserCreationForm
    template_name = 'bloginf/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'bloginf/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))


    def get_success_url(self):
        return reverse_lazy('home')

def logout_user(request):
    logout(request)
    return redirect('login')


class AddPage(CreateView):
    form_class = AddPostForm
    template_name = 'Post/addpage.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавить статью'
        context['menu'] = menu
        return context






#def addpage(request):
#     if request.method == 'POST':
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             #print(form.cleaned_data)
#             form.save()
#             return redirect('home')
#     else:
#         form = AddPostForm()

def contact(request):
    return HttpResponse("Обратная связь")


#def login(request):
    #return HttpResponse("Авторизация")


def get_objects_or_404(Post, pk):
    pass


class ShowPost(DataMixin, DetailView):
    model = Post
    template_name = 'blofinf/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['post']
        context['menu'] = menu
        return context



# def show_post(request, post_slug):
# #     post = get_objects_or_404(Post, pk=post_slug)
# #
# #     context = {
# #         'posts': post,
# #         'menu': menu,
# #         'title': post.title,
# #         'cat_selected': post.cat_id,
# #     }
# #     return render(request, 'bloginf/post.html', context=context)
# # #
class PostCategory(ListView):
    model = Post
    template_name = 'blofinf/post.html'
    context_object_name = 'post'
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = 'Категория - ' + str(context['post'][0].cat)
        context['cat_selected'] = context['post'][0].cat_id
        return context




# def show_category(request, cat_id):
#     posts = Post.objects.filter(cat_id=cat_id)
#     cats = Category.objects.all()
#     if len(posts) == 0:
#         raise Http404()
#     context = {
#         'posts': posts,
#         'cats': cats,
#         'menu': menu,
#         'title': 'Отображения по жанрам',
#         'cat_selected': cat_id,
#     # }
#     return render(request, 'bloginf/index.html', context=context)


class BlogHome(ListView):
    model = Post
    template_name = 'bloginf/index.html'
    context_object_name = 'posts'


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = 'Главная страница.Литература'
        context['cat_selected'] = 0
        return context

    def get_queryset(self):
        return Post.objects.filter(is_published=True)












#def index(request):  # HttpReguest
   #    posts = Post.objects.all()
    #cats = Category.objects.all()
    #if len(posts) == 0:
    #    raise Http404()
    #context = {
      # 'posts': posts,
       # 'cats': cats,
        #'menu': menu,
        #'title': 'Произведения',
        #'cat_selected': 0,
    #}
    # return render(request, 'bloginf/index.html', context=context)


def about(request):  # HttpReguest
    return render(request, 'bloginf/about.html', {'menu': menu, 'title': 'Литература'})


def categories(request, cat):
    print(request.GET)
    return HttpResponse(f"<h1> Статья по категориям<h1><p>{cat}</p>")


def archive(request, year):
    if int(year) > 2022:
        return redirect('home', permanent=True)

    return HttpResponse(f"<h1> Архив по годам<h1><p>{year}</p>")


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
