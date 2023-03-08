from django.urls import path
from . import views

urlpatterns=[

    path("",views.index, name="index"),
    path("articles/<int:a_id>",views.show_article, name="articles"),
    path("articles/edit/<int:a_id>",views.edit_article, name="edit_article"),
    path("articles/delete/<int:a_id>",views.delete_article, name="delete_article"),
    path("author",views.author, name="author"),
    path("comments",views.comments, name="comments"),
    path("articles/create",views.create_article, name="create_article"),
    path("create_article",views.create_article, name="create_article"),
    path("upload_file",views.upload_file, name="upload_file"),
    path("download_file",views.download_file, name="download_file"),
    path("user_login",views.user_login, name="user_login"),
    path("user_logout",views.user_logout, name="user_logout"),
    # path("cookies",views.cookies, name="cookies"),
    # path("get_cookies",views.get_cookies, name="get_cookies"),
    # path("set_session",views.set_session, name="set_session"),
    # path("get_session",views.get_session, name="get_session"),
    path("write_article",views.write_article, name="write_article"),
    path("login",views.login, name="login"),
    path("articles/tag",views.tag, name="tag"),
    path("articles/tag/create_tag",views.create_tag, name="create_tag"),
    path('<str:room_name>/',views.chat, name="chat"),
    # path("article_show",views.article_show, name="article_show")

]