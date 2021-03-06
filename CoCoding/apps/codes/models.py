from django.db import models

# Create your models here.
from django_extensions.db.models import TimeStampedModel


class Code(TimeStampedModel):
    QUEUED, ONGOING, COMPLETED, FAILED = 0, 10, 20, 30
    STATUS_CHOICES = (
        (QUEUED, '대기중'),
        (ONGOING, '실행중'),
        (COMPLETED, '완료'),
        (FAILED, '실패'),
    )
    C, JAVA, PYTHON = 'c', 'java', 'python'
    LANGUAGE_CHOICES = (
        (C, 'C'),
        (JAVA, 'Java'),
        (PYTHON, 'Python'),
    )
    std_in = models.TextField(blank=True)
    std_out = models.TextField(null=True, blank=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=QUEUED)
    code = models.TextField()
    language = models.CharField(choices=LANGUAGE_CHOICES, default=C, max_length=10)
    author = models.ForeignKey('users.User', on_delete=models.CASCADE)

    def __str__(self):
        return '{}s code#{}'.format(self.author, self.id)
