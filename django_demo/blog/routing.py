from django.urls import re_path
from . import consumers
#route the traffic to chat consumer

websocket_urlpatterns=[
    re_path(r'^ws/chat/$',consumers.ChatConsumer)
]

#路徑導到chat的時候且是用ws(和https很像 只是 是告訴瀏覽器現在要建立的是一個websocket的瀏覽器)的時候 就使用webocket