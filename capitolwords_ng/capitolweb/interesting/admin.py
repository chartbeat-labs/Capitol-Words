from django.contrib import admin
from interesting.models import *
# Register your models here.
admin.site.register(NamedEntity)
admin.site.register(SearchTerm)
admin.site.register(InterestingSearch)
admin.site.register(FoundResult)
