from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User as auth_user
from django.shortcuts import render 
# Create your models here.
class User(models.Model):
    firstname= models.CharField(max_length=50)
    lastname= models.CharField(max_length=50)

def create_user_local():
    User.objects.create(firstname="g8g8g8",lastname="kuo")

class Articles_comment1(models.Model):
    user=models.ForeignKey(auth_user,on_delete=models.CASCADE)
    content=models.CharField(max_length=500,blank=False,null=False)
    last_update=models.DateField(auto_now=True)

def creat_articles_comments(content):
    user=auth_user.objects.get(username="root")
    content=content
    Articles_comment1.objects.create(user=user,content=content)#user從資料庫撈出來
    return

class Tag(models.Model):
    name=models.CharField(max_length=100,unique=True)#儲存文章的分類，unique=True同一個分類只能出現一次
    description=models.TextField(max_length=500)#幫tag加個註解
    def __str__(self):#self就代表是class本身
        return self.name # 如果想要呈現name的資料 就使用return的方式拿到 例如在create_artivle的form 
def create_tags(request):
    Tag.objects.create(name=request.POST["name"],description=request.POST['description'])
    return


class Articles1(models.Model):
    user=models.ForeignKey(auth_user,on_delete=models.CASCADE)
    title=models.CharField(max_length=500,default="",blank=False,null=False)
    contents=models.CharField(max_length=500,blank=False,null=False)
    last_update=models.DateField(auto_now=True)
    tags=models.ManyToManyField(#使用many to many filed 因為每個article可以屬於多個tag
        Tag,                                      #兩個必填資料表 1.所以對應的資料表
        related_name='article_related_tags'     #2.反向查找的資料表                 
)

def create_articles(request):
    a=Articles1.objects.create(user=request.user,title=request.POST['title'],contents=request.POST['content'])#從前端的Request中拿文章，create_article form 中有 content title
    query=dict(request.POST)#存成diction的形式
    for i in query['tags']:
        a.tags.add(Tag.objects.get(id=i))
    return
def get_articles_by_id(id):
    return Articles1.objects.filter(id=id).first()#可以去抓出特定id的文章，如果寫到first之前，他寫的會是一個陣列，需要用first()去抓出來會比較好處理，機奔上這整個陣列也只有一個文章  

def edit_articles_by_id(request,a_id):
    Articles1.objects.filter(id=a_id).update(title=request.POST["title"],contents=request.POST["content"])
    a= Articles1.objects.filter(id=a_id).get()
    a.tags.remove()#先移除所有的tag
    query=dict(request.POST)
    for i in query["tags"]:
        a.tags.add(Tag.objects.get(id=i))

def delete_articles_by_id(a_id):
     Articles1.objects.filter(id=a_id).delete()
     return


def get_article(a_num):
    #article=Articles.object.get(id=1)
    #user=article.user
    a_num=a_num
    user=Articles1.objects.all().select_related("user").get(id=a_num)
    return  user.contents

def get_articles():
    user=auth_user.objects.get(username="root")
    return   Articles1.objects.filter(user=user).all().order_by("-last_update")#因為使用了pagniator個函式所以 就必須要排序-代表時間由小到大

