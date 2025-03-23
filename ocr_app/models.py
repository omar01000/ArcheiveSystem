from django.db import models

class Document(models.Model):
    file = models.FileField(upload_to='documents/')
    extracted_text = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Document {self.id}"

    def get_file_url(self):
        """Returns the full URL of the document file."""
        return self.file.url  # Django automatically resolves MEDIA_URL


