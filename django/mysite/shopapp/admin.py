from io import TextIOWrapper
from csv import DictReader


from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import path
from .models import Product,Order,ProductImage
from .admin_mixins import ExportAsCSVMixin
from .forms import CSVImportForm


class OrderInline(admin.TabularInline):
    model = Product.orders.through

@admin.action(description='Archivrd products')
def mark_archived(modeladmin: admin.ModelAdmin,request:HttpRequest,queryset:QuerySet):
    queryset.update(archived=True)

@admin.action(description='Unarchivrd products')
def mark_unarchived(modeladmin: admin.ModelAdmin,request:HttpRequest,queryset:QuerySet):
    queryset.update(archived=False)



class ProductInline(admin.TabularInline): #StackedInline
    model = Order.products.through
class ProductInlineImages(admin.StackedInline):
    model = ProductImage


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin,ExportAsCSVMixin):

    change_list_template = "shopapp/products_changelist.html"

    actions = [
        mark_archived,
        mark_unarchived,
        "export_csv"
    ]
    inlines = [
        OrderInline,
        ProductInlineImages,
    ]
    #list_display = "pk",'name','price','discount','description'
    list_display = "pk",'name','price','discount','description_short','archived'
    list_display_links = 'pk','name'
    ordering = ['name','price']
    search_fields = 'name','description'
    fieldsets = [
        ('none',{
            'fields':('name','description'),
        }),
        ('Price options',{
            'fields':('price','discount'),
            'classes':('collapse','wide'),
        }),
        ('Images',{
            'fields':('prewiew',),
        }),
        ('Extra options',{
            'fields':('archived',),
            'classes':('collapse',),
            'description':'Extra options, field "archived" is soft delete',
        })
    ]

    def import_csv(self,request:HttpRequest) -> HttpResponse:
        from .common import save_csv_products
        if request.method == "GET":
            form = CSVImportForm()
            context = {
                'form':form,
            }
            return render(request, 'admin/csv_form.html', context)
        form = CSVImportForm(request.POST,request.FILES)
        if not form.is_valid():
            context = {
                'form':form,
            }
            return render(request, 'admin/csv_form.html', context,status=400)
        save_csv_products(
            form.files['csv_file'].file,
            encoding=request.encoding,
        )            
        self.message_user(request,'create csv file')
        return redirect("..")
            

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [
            path(
                "import-products-csv/",
                self.import_csv,
                name="import_products_csv",
            ),
        ]
        return new_urls + urls



# admin.site.register(Product,ProductAdmin)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = 'delivery_address','promocode','created_at','user_verbose'
    inlines = [
        ProductInline
    ]
    def get_queryset(self, request):
        return Order.objects.select_related('user').prefetch_related('products')
    
    def user_verbose(self, obj:Order) -> str:
        return obj.user.first_name,obj.user.last_name or obj.user.username