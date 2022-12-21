from django.db import models
from django.conf import settings
from datetime import datetime, timedelta


class Military(models.Model):
    CHOICES = [
        ("F", "자유"),
        ("N", "소식"),
        ("C", "정보"),
        ("A", "공지"),
    ]
    category = models.CharField(max_length=2, choices=CHOICES)
    title = models.CharField(max_length=32, verbose_name="제목")
    content = models.TextField(verbose_name="내용")
    writer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="작성자")
    date = models.DateTimeField(auto_now_add=True, verbose_name="작성일")
    view = models.PositiveIntegerField(default=0, verbose_name="조회수")
    like = models.PositiveIntegerField(default=0, verbose_name="추천수")
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='LU')
    score = models.PositiveIntegerField(default=0, verbose_name="점수")

    @property
    def date_str(self):
        if self.date.strftime("%Y%m%d") == datetime.now().strftime("%Y%m%d"):
            return self.date.strftime("%H:%M")
        else:
            return self.date.strftime("%m-%d")

    @property
    def new(self):
        if datetime.now() - timedelta(hours=3) < self.date:
            return True
        else:
            return False

    @property
    def view_count(self):
        self.view += 1
        self.score += 1
        self.save()

    def __str__(self):
        return self.title

    class Meta:
        db_table = "Military"
        verbose_name = "밀리터리"
        verbose_name_plural = "밀리터리"
        ordering = ["-date"]


class Comment(models.Model):
    board = models.ForeignKey(
        Military, null=True, blank=True, on_delete=models.CASCADE, verbose_name="게시글"
    )
    writer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="작성자")
    content = models.CharField(max_length=1024, verbose_name="내용")
    date = models.DateTimeField(auto_now_add=True, verbose_name="작성일")
    parents = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="recomment",
        null=True,
        verbose_name="작성자",
    )

    @property
    def date_str(self):
        if self.date.strftime("%Y%m%d") == datetime.now().strftime("%Y%m%d"):
            return self.date.strftime("%H:%M")
        else:
            return self.date.strftime("%m-%d")

    class Meta:
        db_table = "Comment"
        verbose_name = "댓글"
        verbose_name_plural = "댓글"


class Image(models.Model):
    image = models.ImageField(null=True, blank=True, upload_to="%Y-%m-%d/")
