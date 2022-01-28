from django.db import models
import uuid
from django.core.exceptions import ValidationError
from django.conf import settings
from django.contrib.auth.models import Group

# Create your models here.
def filename_generator(instance, filename):
    return  uuid.uuid4().hex + filename

def document_fileextension_validator(value):
    import os
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.pdf', '.doc', '.docx']
    if not ext.lower() in valid_extensions:
        raise ValidationError(u'Unsupported file extension.')

class Post(models.Model):

    ANNOUNCEMENT = 'AN'
    RESULT = 'RS'
    QUESTION_BANK = 'QB'
    NOTES = 'NT'

    TYPE_CHOICES = (

    )

    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    file = models.FileField(upload_to=filename_generator, validators=[document_fileextension_validator], blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    tags = models.CharField(max_length=2, choices=TYPE_CHOICES, blank=True, null=True)
    groups = models.ManyToManyField(Group, on_delete=models.CASCADE, blank=True, null=True) # groups that can see this announcement

    def __str__(self):
        return self.title