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

class WebsiteWorkflow(models.Model):
    id = models.AutoField(primary_key=True)

    template = models.ForeignKey(
        WebsiteTemplate,
        on_delete=models.CASCADE,
        db_column='template_id',
        related_name='workflows'
    )
    category = models.ForeignKey(
        WebsiteCategory,
        on_delete=models.CASCADE,
        db_column='category_id',
        related_name='workflows'
    )
    client_id = models.IntegerField(blank=True, null=True)  # ForeignKey optional

    template = models.ForeignKey(
        WebsiteTemplate,
        on_delete=models.CASCADE,
        db_column='template_id',
        related_name='templates',
        blank=True,
        null=True
    )
    
    # New branding fields
    website_name = models.CharField(max_length=2555, blank=True, null=True)
    logo = models.ImageField(blank=True, null=True)
    favicon = models.ImageField(blank=True, null=True)
    second_logo = models.ImageField(blank=True, null=True)

    primary_color = models.CharField(max_length=71, blank=True, null=True)
    secondary_color = models.CharField(max_length=71, blank=True, null=True)

    # Social Media URLs
    facebook_url = models.URLField(blank=True, null=True)
    instagram_url = models.URLField(blank=True, null=True)
    youtube_url = models.URLField(blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)
    
    address = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    email_address = models.EmailField(blank=True, null=True)
    
    is_active = models.IntegerField(default=1)
    enable_accessibility = models.IntegerField(default=0)
    show_second_logo  = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=1000, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        db_table = 'tbl_websiteWorkflow'

class Page(models.Model):
    id = models.AutoField(primary_key=True)

    website = models.ForeignKey(
        WebsiteWorkflow,
        on_delete=models.CASCADE,
        db_column='website_id',
        related_name='pages'
    )
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    template_path = models.CharField(max_length=555, null=True, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.IntegerField(default=1)

    created_by = models.CharField(max_length=255, null=True, blank=True)
    updated_by = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        db_table = 'tbl_page'

class Section(models.Model):
    id = models.AutoField(primary_key=True)

    page = models.ForeignKey(
        Page,
        on_delete=models.CASCADE,
        db_column='page_id',
        related_name='sections'
    )
    section_type = models.ForeignKey(
        'SectionType',
        on_delete=models.CASCADE,
        db_column='section_type_id'
    )
    title = models.CharField(max_length=255, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.IntegerField(default=1)

    created_by = models.CharField(max_length=255, null=True, blank=True)
    updated_by = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        db_table = 'tbl_section'

class ContentBlock(models.Model):
    id = models.AutoField(primary_key=True)

    section = models.ForeignKey(
        'Section',
        on_delete=models.CASCADE,
        db_column='section_id',
        related_name='blocks'
    )

    title = models.CharField(max_length=255, blank=True, null=True)  # 🆕 New Title field

    block_type = models.CharField(max_length=50, choices=[
        ('text', 'Text'),
        ('file', 'File'),
        ('html', 'HTML'),
        ('video', 'Video'),
        ('button', 'Button'),
    ])

    description = models.TextField(blank=True)  # ✏️ Renamed from content → description
    media_file = models.FileField(blank=True, null=True)

    pdf_file = models.FileField(blank=True, null=True)
    url = models.TextField(blank=True, null=True)

    order = models.PositiveIntegerField(default=0)
    is_active = models.IntegerField(default=1)

    created_by = models.CharField(max_length=255, null=True, blank=True)
    updated_by = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        db_table = 'tbl_content_block'

class SectionType(models.Model):
    id = models.AutoField(primary_key=True)

    name = models.CharField(max_length=100)
    identifier = models.SlugField(unique=True)
    description = models.TextField(blank=True)

    created_by = models.CharField(max_length=255, null=True, blank=True)
    updated_by = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        db_table = 'tbl_section_type'

class ContactMessage(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_by = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    class Meta:
        db_table = 'tbl_contact_message'

class Client(models.Model):
    id = models.AutoField(primary_key=True)
    
    name = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255, blank=True, null=True)
    
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    domain_name = models.CharField(max_length=255, blank=True, null=True, unique=True)

    is_active = models.IntegerField(default=1) 

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=255, blank=True, null=True)  # CharField is better than TextField for short names

    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'tbl_client'