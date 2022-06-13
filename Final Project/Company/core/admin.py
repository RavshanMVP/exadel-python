from django.contrib import admin
from core.models import User, Role, Request, RequestStatus, Review, Service, Category, Notification, Response


class CustomUserAdmin(admin.ModelAdmin):
    model = User
    list_display = ('id', 'fullname', 'email', 'role')
    list_filter = ('fullname', 'email')
    search_fields = ('id', 'fullname', 'email', 'city', 'country')
    ordering = ('id', )


class ServiceAdmin(admin.ModelAdmin, admin.AdminSite):
    model = Service
    list_display = ('name', 'category', 'cost', 'company',)
    list_filter = ('category', 'name', 'cost', 'company',)
    ordering = ('cost',)
    search_fields = ('category__category', 'cost', 'company__fullname',)


class RequestAdmin(admin.ModelAdmin):
    model = Request
    list_display = ('id', 'created_at', 'address', 'status', 'user')
    list_filter = ('status__status', 'minutes')
    ordering = ('created_at', 'status__status')
    search_fields = ('status__status', 'id', 'area', 'minutes')


class ReviewAdmin(admin.ModelAdmin):
    model = Review
    list_display = ('id', 'created_at', 'rating', 'service', 'user')
    list_filter = ('created_at', 'rating')
    ordering = ('created_at', 'rating')
    search_fields = ('id', 'created_at', 'rating', 'service', 'user')


class ResponseAdmin(admin.ModelAdmin):
    model = Response
    list_display = ('id', 'service', 'request', 'is_accepted', 'is_completed')
    list_filter = ('service', 'request',)
    ordering = ('is_accepted', 'is_completed', 'id')
    search_fields = ('id', 'service', 'request', 'is_accepted', 'is_completed')


class NotificationAdmin(admin.ModelAdmin):
    model = Notification
    list_display = ('id', 'sender', 'recipient', 'subject',)
    list_filter = ('sender', 'recipient', 'subject',)
    ordering = ('sender', 'recipient', 'subject',)
    search_fields = ('sender', 'recipient', 'subject',)


admin.site.register(User, CustomUserAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Role)
admin.site.register(Request, RequestAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(RequestStatus)
admin.site.register(Category)
admin.site.register(Notification, NotificationAdmin)
admin.site.register(Response, ResponseAdmin)
