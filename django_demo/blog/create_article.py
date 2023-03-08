from django import forms
from .models import Tag,Articles1

class create_article_form(forms.Form):
    title=forms.CharField(required=True,widget=forms.TextInput(attrs={'class':"form-control"}))#(attrs={'class':"form-control"} 給html 的class or id
    content=forms.CharField(required=True,widget=forms.Textarea(attrs={'class':"form-control"}))#textarea會有比較好的使用者體驗的input區域
    tags=forms.ModelMultipleChoiceField(queryset=Tag.objects.all()#抓出所有的tag 這個tag的choicefield
    ,widget=forms.SelectMultiple(attrs={'class':"selectpicker"}))#幫文章做分類，Multiplechoice 每個文章可以屬於多種類別

class edit_article_form(forms.Form):#django的class 通常只傳入form.form得到request所以要進行擴充
    def __init__(self,id): #重寫pythion class 新增 id 這個參數 class 中 init的程式會先被執行過再執行下面的 
        super(edit_article_form,self).__init__()
        self.fields["title"].initial= Articles1.objects.filter(id=id)[0].title#設定初始值  從資料庫鐘用id撈出資料也可以使用.first()
        self.fields["content"].initial= Articles1.objects.filter(id=id)[0].contents
        self.fields["tags"].initial= Articles1.objects.filter(id=id)[0].tags.all()
    title=forms.CharField(required=True,widget=forms.TextInput(attrs={'class':"form-control"}))#(attrs={'class':"form-control"} 給html 的class or id
    content=forms.CharField(required=True,widget=forms.Textarea(attrs={'class':"form-control"}))#textarea會有比較好的使用者體驗的input區域
    tags=forms.ModelMultipleChoiceField(queryset=Tag.objects.all()#抓出所有的tag 這個tag的choicefield
    ,widget=forms.SelectMultiple(attrs={'class':"selectpicker"}))#幫文章做分類，Multiplechoice 每個文章可以屬於多種類別