from django.contrib import admin
from .models import Day

class DayAdmin(admin.ModelAdmin):
    list_display = ('title', 'date')  # 管理画面で表示する項目

admin.site.register(Day, DayAdmin)
