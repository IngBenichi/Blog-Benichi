from rest_framework import serializers
from .models import Post, Comment, Category, Tag
from django.contrib.auth.models import User

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']

class AuthorSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()  # Ajusta según tu modelo de perfil

    class Meta:
        model = User
        fields = ['id', 'name', 'username', 'avatar']

    def get_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip() or obj.username

    def get_avatar(self, obj):
        # Ajusta esto según tu modelo de perfil/avatar
        return getattr(obj, 'profile', None) and getattr(obj.profile, 'avatar', None) and obj.profile.avatar.url or ""

class PostSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    publishedAt = serializers.DateTimeField(source='publish')
    excerpt = serializers.CharField()
    content = serializers.CharField(source='body')
    featuredImage = serializers.ImageField(source='image', allow_null=True)
    readTime = serializers.SerializerMethodField()
    likesCount = serializers.SerializerMethodField()
    commentsCount = serializers.SerializerMethodField()
    isLiked = serializers.SerializerMethodField()
    isSaved = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'slug', 'excerpt', 'content', 'featuredImage', 'category',
            'tags', 'author', 'publishedAt', 'readTime', 'likesCount', 'commentsCount',
            'isLiked', 'isSaved'
        ]

    def get_readTime(self, obj):
        words = len(obj.body.split())
        return max(1, words // 200)

    def get_likesCount(self, obj):
        return obj.likes.count() if hasattr(obj, 'likes') else 0

    def get_commentsCount(self, obj):
        return obj.comments.count()

    def get_isLiked(self, obj):
        user = self.context.get('request').user
        return obj.likes.filter(id=user.id).exists() if user.is_authenticated and hasattr(obj, 'likes') else False

    def get_isSaved(self, obj):
        user = self.context.get('request').user
        return obj.saved_by.filter(id=user.id).exists() if user.is_authenticated and hasattr(obj, 'saved_by') else False
    
class CommentSerializer(serializers.ModelSerializer):
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())
    author = AuthorSerializer(read_only=True)  # Removed incorrect source='name'
    createdAt = serializers.DateTimeField(source='created')
    updatedAt = serializers.DateTimeField(source='updated')

    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'body', 'createdAt', 'updatedAt']

    def create(self, validated_data):
        post = validated_data.pop('post')
        comment = Comment.objects.create(post=post, **validated_data)
        return comment
    
class UserProfileSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()
    bio = serializers.CharField(source='profile.bio', default="", read_only=True)
    location = serializers.CharField(source='profile.location', default="", read_only=True)
    joined_at = serializers.DateTimeField(source='date_joined', format="%Y-%m-%d")
    social = serializers.SerializerMethodField()
    posts_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    email = serializers.EmailField(read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'full_name', 'username', 'email', 'avatar', 'bio', 'location', 'joined_at',
            'social', 'posts_count', 'comments_count'
        ]

    def get_full_name(self, obj):
        return obj.get_full_name() or obj.username

    def get_avatar(self, obj):
        return getattr(obj, 'profile', None) and getattr(obj.profile, 'avatar', None) and obj.profile.avatar.url or ""

    def get_social(self, obj):
        profile = getattr(obj, 'profile', None)
        if not profile:
            return {}
        return {
            'twitter': getattr(profile, 'twitter', ''),
            'github': getattr(profile, 'github', ''),
            'linkedin': getattr(profile, 'linkedin', ''),
        }

    def get_posts_count(self, obj):
        return obj.blog_posts.count() if hasattr(obj, 'blog_posts') else 0

    def get_comments_count(self, obj):
        return obj.comment_set.count() if hasattr(obj, 'comment_set') else 0