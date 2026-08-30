from django.shortcuts import (render,redirect,reverse,get_object_or_404,)
from django.urls import reverse_lazy,reverse
from django.http import HttpResponse,HttpRequest,HttpResponseRedirect
from timeit import default_timer
from django.contrib.auth.models import Group,User
from django.views import View
from django.views.generic import (TemplateView,
                                  ListView,
                                  DetailView,
                                  CreateView,
                                  DeleteView,
                                  UpdateView,)
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin,
                                        UserPassesTestMixin)



from .models import Product,Order,ProductImage
from .forms import ProductForm,OrderForm,GroupForm

import logging
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from .serializers import ProductSerializer,OrderSerializer
from rest_framework.filters import SearchFilter,OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from csv import DictReader,DictWriter

from .common import save_csv_products

# для кеширования 
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page


log = logging.getLogger(__name__)

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [
        SearchFilter,
        DjangoFilterBackend,
        OrderingFilter,
    ]
    search_fields = ['name','description']
    filterset_fields = [
        "name",
        "description",
        "price",
        "discount",
        'archived',
    ]
    ordering_fields = [
        "name",
        "price",
        "discount",
    ]

    @method_decorator(cache_page(10 * 2))
    def list(self,*args, **kwargs):
        return super().list(*args,**kwargs)


    @action(methods=["get"], detail=False)
    def download_csv(self, request: Request):
        response = HttpResponse(content_type="text/csv")
        filename = "products-export.csv"
        response["Content-Disposition"] = f"attachment; filename={filename}"
        queryset = self.filter_queryset(self.get_queryset())
        fields = [
            "name",
            "description",
            "price",
            "discount",
        ]
        queryset = queryset.only(*fields)
        writer = DictWriter(response, fieldnames=fields)
        writer.writeheader()

        for product in queryset:
            writer.writerow({
                field: getattr(product, field)
                for field in fields
            })

        return response 
    @action(detail=False,methods=['post'],parser_classes=[MultiPartParser])
    def upload_csv(self,request:Request):
        products = save_csv_products(
            request.FILES['file'].file,
            encoding=request.encoding,
                          )
        serializer = self.get_serializer(products,many=True)
        return Response(serializer.data)


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [
        SearchFilter,
        DjangoFilterBackend,
        OrderingFilter,
    ]
    search_fields = ['delivery_address','promocode']
    filterset_fields = [
        "delivery_address",
        "promocode",
    ]
    ordering_fields = ['delivery_address','promocode']

class ShopIndexView(View):
    # @method_decorator(cache_page(10 * 2))
    def get(self,request:HttpRequest) ->HttpResponse:
            products = [
            ("Laptop",1999),
            ("Desctop",2999),
            ('Smatrphone',3999)
            ]
            context = {
                "time_running":default_timer,
                "products":products,
                "items":4
            }
            log.debug("Product for index shop",products)
            log.info('Info shop index')
            print('cacheCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC',context)
            return render(request,"shopapp/shop-index.html",context=context)

class GroupsListView(View):
    def get(self,request:HttpRequest) ->HttpResponse:
            context = {
                'form':GroupForm,
            'groupsss': Group.objects.prefetch_related('permissions').all()
            }
            return render(request,"shopapp/groups-list.html",context=context)

    def post(self,request:HttpRequest):
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect(request.path)
    


class ProductDetailViews(DetailView):
    template_name = 'shopapp/product-details.html'
    # model = Product
    queryset = Product.objects.prefetch_related('images')
    context_object_name = 'prod'

    

    #def get(self,request:HttpRequest, pk:int) ->HttpResponse:
    #    product = get_object_or_404(Product,pk=pk)
    #    context = {
    #        'product':product
    #    }

    #    return render(request,'shopapp/product-details.html',context=context)


class ProfuctListView(ListView):
    template_name = 'shopapp/products-list.html'
    # отображаются все продукты
    # model = Product
    context_object_name = 'products1'
    # не отображаются архивные продукты
    queryset = Product.objects.filter(archived=False)

    #def get_context_data(self, **kwargs):
    #    context = super().get_context_data(**kwargs)
    #    context['products1'] = Product.objects.all()
    #    return context


class ProductCreateView(UserPassesTestMixin,CreateView):
    # проверка может ли пользователь создавать заказ
    def test_func(self):
        #return self.request.user.groups.filter(name='secret-group').exists()
        return self.request.user.is_superuser
    model = Product
    fields = 'name','price','description','discount','prewiew'
    #form = ProductForm 
    # шаблон должен называться product_form.html
    success_url = reverse_lazy('shopapp:products_list_url')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        response = super().form_valid(form)
        return response


class ProductUpdateView(UpdateView):
    model = Product
    # fields = 'name','price','description','discount','prewiew'
    # template_name = ''
    form_class = ProductForm
    template_name_suffix = '_update_form'
    context_object_name = 'prod_det'
    # success_url = reverse_lazy('shopapp:products_list_url')

    def form_valid(self, form):
        response = super().form_valid(form)
        for image in form.files.getlist('images'):
            ProductImage.objects.create(
               product = self.object,
               image=image
            )
        return response


    # для того чтобы вернутся к продукту нужно сделать get_succsess_url
    def get_success_url(self):
        return reverse(
            'shopapp:product_details_url',
            kwargs={"pk":self.object.pk},
        )
class ProductDelateView(DeleteView):
    # для удаления
    model = Product
    success_url = reverse_lazy('shopapp:products_list_url')

    # для архивации добавим функцию
    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.archived = True
        self.object.save()
        return HttpResponseRedirect(success_url)

###############################################################################################
#!!!orders!!!!!!!orders!!!!!!orders!!!!!orders!!!!!!!orders!!!!!!!!!!!orders!!!!!!!!!!orders
##############################################################################

# LoginRequiredMixin просмотреть заказы можно только после login
class OrderListView(LoginRequiredMixin,ListView):
    queryset = (
       Order.objects.select_related("user")
        .prefetch_related('products')
    )
    context_object_name = 'orders'

# просмотр деталей заказа не всем пользователям
class OrderDetailtView(PermissionRequiredMixin,DetailView):
    permission_required = ['view_order'] # просмотр деталей заказа не всем пользователям
    queryset = (
       Order.objects.select_related("user")
        .prefetch_related('products')
    )
    # context_object_name = 'order_detail'

class OrderCreateView(CreateView):
        # шаблон должен называться order_form.html
    model = Order
    fields = 'delivery_address','promocode','user','products'
    success_url = reverse_lazy('shopapp:orders_list_url')

class OrderUpdateView(UpdateView):
    model = Order
    fields = 'delivery_address','promocode','user','products'  
    template_name_suffix = '_update_form'
    context_object_name = 'order_upd'
    # success_url = reverse_lazy('shopapp:products_list_url')

    # для того чтобы вернутся к продукту нужно сделать get_succsess_url
    def get_success_url(self):
        return reverse(
            'shopapp:order_details_url',
            kwargs={"pk":self.object.pk},
        ) 

class OrdertDelateView(DeleteView):
    # для удаления
    model = Order
    success_url = reverse_lazy('shopapp:orders_list_url')

   
###############################################################################################
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!11
##############################################################################
# Create your views here.
def shop_index(request:HttpRequest):
    products = [
        ("Laptop",1999),
         ("Desctop",2999),
         ('Smatrphone',3999)
    ]
    context = {
        "time_running":default_timer,
        "products":products
    }
    return render(request,"shopapp/shop-index.html",context=context)

def groups_list(request:HttpRequest):
    context = {
       'groupsss': Group.objects.prefetch_related('permissions').all()
    }
    return render(request,"shopapp/groups-list.html",context=context)

def products_list(request:HttpRequest):
    context = {
        "products1":Product.objects.all()
    }
    return render(request,'shopapp/products-list.html',context=context)


def create_product(request:HttpRequest) -> HttpResponse:
    if request.method == 'POST':
         form = ProductForm(request.POST) #валидность 
         if form.is_valid():
            # name = form.cleaned_data['name']
            # price = form.cleaned_data['price']
            # description = form.cleaned_data['description']
            
            # Product.objects.create(**form.cleaned_data) # **для распакрвки
            form.save()
            url = reverse('shopapp:products_list_url')
            return redirect(url)
    else:     
        form = ProductForm()
    context = {
        'form':form
    }
   
    return render(request,'shopapp/create-product.html',context=context)

def orders_list(request:HttpRequest):
    context = {
        'orders':Order.objects.select_related("user").prefetch_related('products').all()
    }
    return render(request,"shopapp/orders-list.html",context=context)

def create_order(request:HttpRequest) -> HttpResponse:
    if request.method == 'POST':
         form = OrderForm(request.POST) #валидность 
         if form.is_valid():
            # name = form.cleaned_data['name']
            # price = form.cleaned_data['price']
            # description = form.cleaned_data['description']
            
            # Product.objects.create(**form.cleaned_data) # **для распакрвки
            form.save()
            url = reverse('shopapp:orders_list_url')
            return redirect(url)
    else:     
        form = OrderForm()
    context = {
        'form':form
    }
   
    return render(request,'shopapp/create-order.html',context=context)
###############################################################################################
#                                JsonProductsData
##########################################################################

from django.http import JsonResponse
from django.core.cache import cache
class ProductDataExportView(View):

    def get(self, request:HttpRequest) -> HttpResponse:
        cache_key = "products_data_export"
        products_data = cache.get(cache_key)
        if products_data is None:
            products = Product.objects.order_by('pk').all()
            products_data = [
                {
                    "pk":product.pk,
                    'name':product.name,
                    'price':product.price,
                }
                for product in products
            ]
        cache.set(cache_key,products_data,10)
        return JsonResponse({'products':products_data})

class UserOrdersListView(ListView):
    from .models import Order
    model = Order
    template_name = 'shopapp/user_orders_list.html'
    context_object_name = 'user_orders'

    def get_queryset(self):
        from .models import Order
        user_id = self.kwargs['user_id']

        self.user = get_object_or_404(User, pk=user_id)

        return Order.objects.filter(user=self.user).order_by('-created_at')

    def get_context_data(self, *, object_list = ..., **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.user
        context['orders_count'] = self.object_list.count()
        return context