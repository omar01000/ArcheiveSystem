from django.db import models

# الجهات الداخلية
class InternalEntity(models.Model):
    name = models.CharField(max_length=1000)

    def __str__(self):
        return self.name

class InternalDepartment(models.Model):
    name = models.CharField(max_length=1000)
    internal_entity = models.ForeignKey(InternalEntity, on_delete=models.CASCADE, related_name='faculties')
  

    def __str__(self):
        return self.name

# الجهات الخارجية
class ExternalEntity(models.Model):
    name = models.CharField(max_length=1000)

    def __str__(self):
        return self.name

class ExternalDepartment(models.Model):
    name = models.CharField(max_length=1000)
    external_entity = models.ForeignKey(ExternalEntity, on_delete=models.CASCADE, related_name='departments')

    def __str__(self):
        return self.name

# الملفات المرفوعة
class Document(models.Model):
    
    
    
    INTERNAL = 'internal'
    EXTERNAL = 'external'
    ENTITY_TYPE_CHOICES = [
        (INTERNAL, 'Internal'),
        (EXTERNAL, 'External'),
    ]


    title = models.CharField(max_length=100)
    document_number = models.CharField(max_length=100,unique=True)
    notes= models.TextField(null=True,blank=True)
    entity_type = models.CharField(max_length=1222, choices=ENTITY_TYPE_CHOICES)
    internal_entity = models.ForeignKey(InternalEntity, on_delete=models.CASCADE, null=True, blank=True)
    internal_department = models.ForeignKey(InternalDepartment, on_delete=models.CASCADE, null=True, blank=True)
    external_entity = models.ForeignKey(ExternalEntity, on_delete=models.CASCADE, null=True, blank=True)
    external_department = models.ForeignKey(ExternalDepartment, on_delete=models.CASCADE, null=True, blank=True)
    document_type = models.CharField(max_length=1000, choices=[('incoming', 'Incoming'), ('outgoing', 'Outgoing')])
    file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Document {self.id}"