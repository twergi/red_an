from django.contrib import admin
from .models import Section, SectionPost, SectionStaff, Comments, PostReview

admin.site.register(Section)
admin.site.register(SectionPost)
admin.site.register(SectionStaff)
admin.site.register(Comments)
admin.site.register(PostReview)
