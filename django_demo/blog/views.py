from django.shortcuts import render
from .form import django_form
from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseNotFound,JsonResponse,HttpResponseRedirect
from django.views.decorators.http import require_http_methods
from .models import creat_articles_comments,create_user_local,get_article,create_articles,get_articles,create_tags,get_articles_by_id,edit_articles_by_id,delete_articles_by_id
from .upload import UplaodFileForm
from .login import login_form
import os
from django.contrib.auth import authenticate,login as auth_login,logout
from django.views.decorators.cache import cache_page
from django.core.cache import cache
import logging
from django.core.paginator import Paginator
from .create_article import create_article_form,edit_article_form
from .create_tag import create_tag_form 
from django.contrib.auth.decorators import login_required
logger=logging.getLogger('django')

# # def set_session(request):
#     request.session['pref']="c++" #在request 的 session把key包進去，後面為值
#     Response= HttpResponse("Session set!")
#     return Response

# # def get_session(request):
#     response=HttpResponse("Session srt!"+str(request.session["pref"]))
#     return response

# # def cookies(request):#回應給用戶端瀏覽器的時候，塞入一個cookie，收到至後會再瀏覽器塞入一個cookie
#     response=HttpResponse("Cookie set")
#     response.set_cookie("pref","PTYHON")
#     return response
# # def get_cookies(request):
    # if "pref" in request.COOKIES:
    #     print("prief:",request.COOKIES["pref"])

#chat
# @login_required#沒有login是沒罷法進去的喔
def chat(request,room_name):
    return render(request,"room.html",{
        'room_name': room_name
    })

def index(request):
    article=get_articles()
    context={
        "articles":article
    }
    return render(request,"index.html",context) #可以直接render html code 或是利用status= xxx 來報html code

def write_article(request):
    form=create_article_form
    context={
        "form":form,
    }
    return render(request,"create_article.html",context)
def login(request):
    if not request.user.is_authenticated:
        return render(request,"login.html")
    else:
        return redirect("index")

def user_login(request):
    user=authenticate(request,username=request.POST['username'],password=request.POST['password'])#authenticate自帶USERNAME 以及PASSWORD參數
    if user is not None:
        auth_login(request,user)
        #login(request,user) #實作COOKIE LOGIN 瀏覽器開著可以保持一段時間的登入
        return redirect("index")
    else:
        return render(request,"login.html")

def show_article(request,a_id):
    
    context={"article":get_articles_by_id(a_id)}
    return render(request,"show_article.html",context)

def edit_article(request,a_id):
    if request.method=="POST":
        edit_articles_by_id(request,a_id)
        return redirect("index")
    else:
        form =edit_article_form(a_id)
        context={
            "form":form,
            "id":a_id
        }
        return render(request,"edit_article.html",context) 

def delete_article(request,a_id):
    delete_articles_by_id(a_id)
    return redirect("index")
        


#@require_http_methods(['GET'])#裝飾子功能 限定獲得方式
def comments(request): #從article 填完comment會轉來這
    #save comment
    content=request.POST.get("content")
    creat_articles_comments(content)#傳到model去做儲存
    return HttpResponse("comments updated!")
    #return JsonResponse({"one":"a","two":"b"})
def articles(request,a_num):
    a_num=a_num
    article=get_articles(a_num)
    if request.user.is_authenticated:
        context={"articles":article,"user":request.user.username}
    else:
       context={"articles":article,"user":""} 
    
    return render(request,"article.html",context)
def create_article(request):
    if request.method=="POST":
        # content=request.POST.get("contents")
        # creat_articles(content)
        create_articles(request)
        return redirect("index")
    else:
        form=create_article_form
        context={"form":form}
        return render(request,"create_article.html",context)

def create(request):
    create_user_local()
    return HttpResponse("User created")


def author(request):
    if request.user.is_authenticated:
        article= cache.get("root")#當使用者瀏覽author頁面時，秀出資料庫文章的內容
        if not article:
            article=get_articles()
            cache.set("root",article,30)
        paginator =Paginator(article,2)
        article=paginator.get_page(request.GET['page'])#自動帶入page的功能，典籍page就可知道式第幾頁德article
        name=request.user
        sidebar_name=["home","articles","authors"]
        path_url=["/blog","/blog/atricles","/blog/author"]
        context={
        "name":name,
        "sidebar":sidebar_name,
        "path":path_url,
        "articles":article
        }
    else:
        return HttpResponseRedirect('/blog/')
    return render(request,"author.html",context)#要記得從django shortcuts import render

def tag(request):
    form=create_tag_form
    context={
        "form":form,
    }
    return render(request,"create_tag.html",context)
def create_tag(request):
    if request.method=="POST":
        create_tags(request)
        return redirect("index")
    else:
        form=create_tag_form
        context={
        "form":form,}
        return render(request,"create_tag.html",context)



def upload_file(request):
    if request.method=="POST":
        form=UplaodFileForm(request.POST,request.FILES)#表示用post的方式處理表單，同時把船上去的檔案的表單也給form
        if form.is_valid():#如果這個form的請求是合法的話
            print("form valid")
            with open("/Users/as222/for_django_upload_file/upload.text","wb+") as destination: #開啟伺服器存放檔案的位置以及開啟檔案的權限(file I/O)wb+ 紀錄在mysql的方式是將膽岸路經存入mysql而非檔案
                for chunk in request.FILES['file']:
                    destination.write(chunk)#將上傳的檔案已chunk的方式慢慢的一步一步存放到destination中 aka 我們的檔案路徑
                return HttpResponse('File updated')
        else:
            print('form invalid')
    else:
        form=UplaodFileForm()
        return render(request, "upload.html",{"form":form})    

def download_file(request):
    file_path=os.path.join("/Users/as222/for_django_upload_file/upload.text") #使用os套件抓出剛剛上傳檔案的路徑存乘file_patj
    response=HttpResponse(open(file_path,"rb"),content_type="applicztion/zip")
    response["Content-Disposition"]='attachment;filename="{}"'.format("download")#應應http的要求乳果response是一個檔案的畫要使用response["Content-Disposition"]因應要求
    return response

# def user_login(request):
#     user=authenticate(request,username=request.POST['username'],password=request.POST['password'])#authenticate自帶USERNAME 以及PASSWORD參數
#     if user is not None:
#         form=django_form()
#         if request.user.is_authenticated:
#             context={"form":form,"username":request.user.username}
#         #login(request,user) #實作COOKIE LOGIN 瀏覽器開著可以保持一段時間的登入
#         return render(request,"create_article.html", context)
#     else:
#         return render(request,"login.html")


def user_logout(request):
    logout(request)
    return HttpResponseRedirect("/blog")


    #使用os.path.join的原因
    #在網頁前端顯示處檔案位置很危險找李來說應該寫成file_path=os.path.join("/Users/as222/for_django_upload_file/",request.POST...)
                                                                     #("/Users/as222/for_django_upload_file/","../../manage.py".strip(../).strip(./).strip(/))
# def article_show(request,a_num,article):
#     article_id=a_num
#     writings=article
#     context={
#          "article":writings,
#          "no.":article_id
#      }
#     return render(request,"show_article.html",context)
