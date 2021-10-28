from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum

class Author(models.Model):
    author_user = models.OneToOneField(User, on_delete = models.CASCADE)
    author_rate = models.IntegerField(default=0)

    def update_rating(self):
        posts_rate = self.post_set.all().aggregate(postRate=Sum('post_rate'))
        p_rate = 0
        p_rate += posts_rate.get('postRate')

        comments_rate = self.author_user.comment_set.all().aggregate(commentRate=Sum('comment_rate'))
        c_rate = 0
        c_rate += comments_rate.get('commentRate')

        self.author_rate = p_rate * 3 + c_rate
        self.save()


class Category(models.Model):
    category_name = models.CharField(max_length=255, unique = True)


class Post(models.Model):
    post_author = models.ForeignKey(Author, on_delete = models.CASCADE)

    news = 'NW'
    article = 'AR'

    POST_TYPES = (
        (news, 'News'),
        (article, 'Article'),
    )

    post_type = models.CharField(max_length=2, choices=POST_TYPES, default=news)
    post_create_time = models.DateTimeField(auto_now_add=True)
    post_category = models.ManyToManyField(Category, through='PostCategory')
    post_name = models.CharField(max_length = 255)
    post_text = models.TextField(default = "None")
    post_rate = models.IntegerField(default=0)

    def like(self):
        self.post_rate += 1
        self.save()

    def dislike(self):
        if self.post_rate:
            self.post_rate -= 1
            self.save()

    def preview(self):
        return self.post_text[:125] + "..."


class PostCategory(models.Model):
    post_temp = models.ForeignKey(Post, on_delete=models.CASCADE)
    category_temp = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    comment_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField(default = "None")
    comment_creation_time = models.DateTimeField(auto_now_add=True)
    comment_rate = models.IntegerField(default = 0)


    def like(self):
        self.comment_rate += 1
        self.save()

    def dislike(self):
        if self.comment_rate:
            self.comment_rate -= 1
            self.save()


