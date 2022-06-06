from django.contrib import admin
from core.models import User, Role, Request, RequestStatus, Review, Service, Category, Notification, Response

admin.site.register(User)
admin.site.register(Role)
admin.site.register(Request)
admin.site.register(Review)
admin.site.register(RequestStatus)
admin.site.register(Service)
admin.site.register(Category)
admin.site.register(Notification)
admin.site.register(Response)
