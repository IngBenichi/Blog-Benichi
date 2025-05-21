from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Count
from django.utils.text import slugify
from django.contrib.postgres.search import SearchVector
from unidecode import unidecode
from taggit.models import Tag
from django.contrib.auth.models import User

from .models import Post, Comment
from .forms import EmailPostForm, CommentForm, SearchForm, CustomLoginForm, CustomRegisterForm
from django.contrib.auth.models import Group

import logging
from django.http import HttpResponse

from rest_framework import routers, viewsets, mixins
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer, TagSerializer, AuthorSerializer
from rest_framework.decorators import action
from rest_framework.response import Response

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.published.all()
    serializer_class = PostSerializer
    pagination_class = None  # Desactiva la paginación para que devuelva un array

    @action(detail=False, methods=['get'], url_path='latest')
    def latest(self, request):
        limit = int(request.query_params.get('limit', 5))
        latest_posts = self.get_queryset().order_by('-publish')[:limit]
        serializer = self.get_serializer(latest_posts, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='featured')
    def featured(self, request):
        featured_posts = self.get_queryset().filter(featured=True)
        serializer = self.get_serializer(featured_posts, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='popular')
    def popular(self, request):
        limit = int(request.query_params.get('limit', 5))
        popular_posts = self.get_queryset().order_by('-likesCount')[:limit]  # Ajusta si tienes otro campo
        serializer = self.get_serializer(popular_posts, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='stats/most-commented')
    def most_commented(self, request):
        limit = int(request.query_params.get('limit', 5))
        posts = self.get_queryset().annotate(num_comments=Count('comments')).order_by('-num_comments')[:limit]
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='stats/popular-tags')
    def popular_tags(self, request):
        limit = int(request.query_params.get('limit', 10))
        tags = Tag.objects.annotate(num_posts=Count('posts')).order_by('-num_posts')[:limit]
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='stats/trending')
    def trending(self, request):
        limit = int(request.query_params.get('limit', 5))
        from django.utils import timezone
        from datetime import timedelta
        week_ago = timezone.now() - timedelta(days=7)
        posts = self.get_queryset().filter(publish__gte=week_ago).annotate(num_likes=Count('likes')).order_by('-num_likes')[:limit]
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='stats')
    def general_stats(self, request):
        from .models import Category, Comment
        return Response({
            'postsCount': Post.published.count(),
            'usersCount': User.objects.count(),
            'commentsCount': Comment.objects.count(),
            'categoriesCount': Category.objects.count(),
        })

    @action(detail=True, methods=['post', 'delete'], url_path='like')
    def like(self, request, pk=None):
        post = self.get_object()
        user = request.user
        if request.method == 'POST':
            post.likes.add(user)
        else:
            post.likes.remove(user)
        return Response({
            'likesCount': post.likes.count(),
            'isLiked': post.likes.filter(id=user.id).exists()
        })

    @action(detail=True, methods=['post', 'delete'], url_path='save')
    def save(self, request, pk=None):
        post = self.get_object()
        user = request.user
        if request.method == 'POST':
            post.saved_by.add(user)
        else:
            post.saved_by.remove(user)
        return Response({
            'isSaved': post.saved_by.filter(id=user.id).exists()
        })

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response({"data": serializer.data})

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class UserViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = AuthorSerializer

    # Endpoint personalizado para obtener el perfil de usuario por id
    @action(detail=True, methods=['get'])
    def profile(self, request, pk=None):
        user = self.get_object()
        serializer = self.get_serializer(user)
        return Response(serializer.data)

# API router
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'comments', CommentViewSet)
# Registrar el viewset en el router
router.register(r'users', UserViewSet)

logger = logging.getLogger('django.request')

def prueba_logging(request):
    logger.info(f"Se recibió una petición: {request.method} {request.path}")
    return HttpResponse("Log generado correctamente")

def home(request):
    return render(request, 'home.html')

@login_required(login_url='blog:login')
def post_list(request, tag_slug=None):
    post_list = Post.published.all()
    tag = None  

    if tag_slug:
        normalized_slug = slugify(unidecode(tag_slug))
        tag = get_object_or_404(Tag, slug=normalized_slug)
        post_list = post_list.filter(tags__in=[tag])

    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page', 1)
    posts = paginator.get_page(page_number)

    return render(request, 'blog/post/list.html', {
        'page': page_number,
        'posts': posts,
        'tag': tag
    })

@login_required(login_url='blog:login')
def posts_detail(request, year, month, day, post):
    post = get_object_or_404(
        Post,
        status=Post.Status.PUBLISHED,
        slug=post,
        publish__year=year,
        publish__month=month,
        publish__day=day)
    comments = post.comments.filter(active=True)
    form = CommentForm()
    post_tags_ids= post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)   
                                  
    similar_posts = similar_posts.annotate(same_tags=Count('tags'))\
                                 .order_by('-same_tags','-publish')[:4]
    
    return render(request, 'blog/post/detail.html',
                  {'post': post,
                   'comments': comments,
                   'form': form,
                   'similar_posts': similar_posts,})

@require_POST
@login_required(login_url='blog:login')
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    form = CommentForm(request.POST)
    comment = None
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        # Asigna automáticamente el nombre y correo del usuario logueado
        comment.name = request.user.get_full_name() or request.user.username
        comment.email = request.user.email
        comment.save()
        from django.urls import reverse
        from django.http import HttpResponseRedirect
        return HttpResponseRedirect(reverse('blog:post_detail', args=[post.publish.year, post.publish.month, post.publish.day, post.slug]))
    return render(request, 'blog/post/detail.html', {
        'post': post,
        'form': form,
        'comment': comment
    })

@login_required(login_url='blog:login')
def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} te recomienda este post: {post.title}"
            message = f"Lee mi post {post.title} en {post_url}\n\n"  \
                      f"{cd['name']} comenta: {cd['comments']}"
            
            send_mail(subject, message, 'djangobenichi@gmail.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent})

class CustomLoginView(LoginView):
    template_name = "registration/login.html"
    authentication_form = AuthenticationForm
    redirect_authenticated_user = True

def register_view(request):
    if request.method == "POST":
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            group, created = Group.objects.get_or_create(name='Users')
            user.groups.add(group)
            
            login(request, user)
            return redirect("blog:post_list")
    else:
        form = CustomRegisterForm()
    return render(request, "registration/register.html", {"form": form})

def post_search(request):
    form = SearchForm()
    query = None
    results = []
    
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Post.published.annotate(
                search=SearchVector('title', 'body'),
            ).filter(search=query)

    return render(request, 'blog/post/search.html', {
        'form': form,
        'query': query,
        'results': results
    })

@login_required(login_url='blog:login')
def user_profile(request):
    user = request.user
    return render(request, 'blog/profile.html', {
        'user': user
    })
