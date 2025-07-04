from django.db import models

# Create your models here.
class WebsiteCategory(models.Model):
    id = models.AutoField(primary_key=True)
    category_name = models.TextField(blank=True, null=True)
    is_active = models.IntegerField(default=1)
    created_at = models.DateTimeField(blank=True, null=True)
    created_by = models.CharField(max_length=100, blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    updated_by = models.CharField(max_length=100, blank=True, null=True)
    class Meta:
        db_table = 'tbl_websiteCategoryMaster'

class WebsiteTemplate(models.Model):
    id = models.AutoField(primary_key=True)
    template_name = models.TextField(blank=True, null=True)
    
    # ForeignKey linking to WebsiteCategory
    category = models.ForeignKey(
        WebsiteCategory,
        on_delete=models.CASCADE,
        db_column='category_id',
        related_name='templates',
        blank=True,
        null=True
    )
    is_active = models.IntegerField(default=1)
    function_name = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    created_by = models.CharField(max_length=100, blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    updated_by = models.CharField(max_length=100, blank=True, null=True)
    
    class Meta:
        db_table = 'tbl_websiteTemplateMaster'
