from django.contrib import admin
from .models import Section, SectionPost, SectionStaff, Comments

admin.site.register(Section)
admin.site.register(SectionPost)
admin.site.register(SectionStaff)
admin.site.register(Comments)
