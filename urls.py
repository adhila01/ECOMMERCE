from django.urls import path
from .views import *

urlpatterns = [
    path('index/', index),
    path('register/', reg),
    path('userlogin/', userlogin),
    path('userprofile/', userprofile),
    path('usersingleview/', usersingleview),
    path('updateuserdetails/', updateuserdetails),
    path('productupload/',productupload),
    path('addtocart/<int:itemid>',addtocart),
    path('cartdisplay/',Cartdisplay),
    path('incdec/<int:itemid>',inc_dec),
    path('deletecart/<int:cartid>',deletecart),
    path('wishlist/<int:cartid>',wishli),
    path('wishlistdisplay/',wishlistdisplay),
    path('wislistdelete/',wishlistdelete),
    path('addaddress/',addaddress),
    path('delivery_details/',delivery_details),
    path('summary/',summary),
    path('create_order/',create_order),
    path('order_view/',order_view),
    path('order_cancel/<int:id>',order_cancel),
    path('logout/',logout),
    path('changepassword/',changepassword)



]