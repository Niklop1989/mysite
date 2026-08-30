from django.shortcuts import render
from django.http import HttpResponse,HttpRequest
from timeit import default_timer
from django.contrib.auth.models import Group
from django.core.files.storage import FileSystemStorage
from .forms import UserBioForm,UploadFileForm

def process_get_view(request:HttpRequest) -> HttpResponse:
    a = request.GET.get("a","")

    b = request.GET.get("b","")
    result = a + b
    # http://127.0.0.1:8000/req/get/?name=Nik&a=6&b=6
    context = {
        "a":a,
        "b":b,
        "result":result
    }
    return render(request,"requestdataapp/request-query-params.html",context=context)


def user_form(request:HttpRequest):
    context = {
        'form':UserBioForm()
    }
    return render(request,"requestdataapp/user-bio-form.html",context=context)


def handl_file_upload(request:HttpRequest) ->HttpResponse:
    form = UploadFileForm()
    
    if request.method == 'POST':
        form = UploadFileForm(request.POST,request.FILES)
        if form.is_valid():
            # myfile = request.FILES['myfile']
            
            myfile = form.cleaned_data["file"]
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            file_size = fs.size(filename)
            if file_size > 1000000:
                fs.delete(filename)
                print(f'удалил файл {filename}')
                return render(request, 'requestdataapp/file-upload-error.html')

            else:
                print('saved file',filename)
            
    else:
        form = UploadFileForm()
    context = {
        "form":form
    }
    return render(request,'requestdataapp/file-upload.html',context=context)

