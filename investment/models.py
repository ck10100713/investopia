from django.db import models
from django.contrib import admin

# Create your models here.
class StockData(models.Model):
    Ticker = models.CharField(max_length=10)
    Date = models.DateField()
    Open = models.FloatField()
    High = models.FloatField()
    Low = models.FloatField()
    Close = models.FloatField()
    Volume = models.IntegerField()

    def __str__(self):
        return self.Ticker


class TickerFilter(admin.SimpleListFilter):
    title = 'Ticker'  # 过滤器的标题
    parameter_name = 'ticker'  # URL 参数名

    def lookups(self, request, model_admin):
        # 返回一个元组的列表，每个元组包含两个值：过滤器选项的显示名称和相应的值
        return StockData.objects.values_list('Ticker', 'Ticker').distinct()

    def queryset(self, request, queryset):
        # 根据过滤器选项的值过滤查询集
        value = self.value()
        if value:
            return queryset.filter(Ticker=value)

class StockDataAdmin(admin.ModelAdmin):
    list_display = ('Ticker', 'Date', 'Open', 'High', 'Low', 'Close', 'Volume')
    list_filter = (TickerFilter, 'Date')