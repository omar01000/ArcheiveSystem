from django.db import models
# Create your models here.
class Document(models.Model):
    file = models.FileField(upload_to='documents/')
    extracted_text = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def str(self):
        return f"Document {self.id}"


