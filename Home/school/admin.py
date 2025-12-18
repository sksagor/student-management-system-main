from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Notification)



# The text in the upper left of every page (header)
admin.site.site_header = "Student Management System MGT Admin"

# The text at the top of the dashboard (index page)
admin.site.index_title = "Welcome to the Student Management System Dashboard"

# The text in the browser tab title
admin.site.site_title = "Admin Portal"