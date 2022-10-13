from django.contrib import admin
from .models import Section, SectionPost, Comment, PostReview
from .forms import SectionCreateFormAdmin

admin.site.register(Section, SectionCreateFormAdmin)
admin.site.register(SectionPost)
admin.site.register(Comment)
admin.site.register(PostReview)
