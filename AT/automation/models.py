from django.db import models

class Document(models.Model):
    document=models.FileField(upload_to='uploads/')
    create_at=models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=('-create_at',)