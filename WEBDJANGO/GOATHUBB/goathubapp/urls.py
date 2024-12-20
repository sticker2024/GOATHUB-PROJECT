from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),  # Home page
    path('index/', views.index, name='index'),
    path('index1/', views.index1, name='index1'),

    path('adminHub/', views.admin_hub, name='adminHub'),
    path('add_vet/', views.add_vet, name='add_vet'),
    path('consult_a_vet/', views.consult_a_vet, name='consult_a_vet'),
    path('education/', views.education, name='education'),

    path('login/', views.login_view, name='login'),
    path('register/', views.register_farmer, name='register_farmer'),
    path('special_cases/', views.special_cases, name='special_cases'),
    path('vet_message/', views.vet_message, name='vet_message'),
    path('products/', views.products, name='products'),
    
    path('farmers/', views.farmer_list, name='farmer_list'),  # Farmer management routes
    path('farmers/edit/<int:farmer_id>/', views.farmer_edit, name='farmer_edit'),  # Edit route
    path('farmers/delete/<int:farmer_id>/', views.farmer_delete, name='farmer_delete'),  # Delete route
    path('farmer/<int:farmer_id>/', views.farmer_detail, name='farmer_detail'),  

    path('cooperative_farmers/', views.cooperative_farmers, name='cooperative_farmers'),  # New route for cooperative farmers

    path('consultations/', views.consultations, name='consultations'),

    path('veterinary_list/', views.veterinary_list, name='veterinary_list'),
    path('veterinary/edit/<int:id>/', views.edit_veterinary, name='edit_veterinary'),
    path('veterinary/delete/<int:id>/', views.delete_veterinary, name='delete_veterinary'),

    path('replies/', views.all_replies, name='all_replies'),  # New route for all replies
    path('reply_to_farmer/', views.reply_to_farmer, name='reply_to_farmer'),  # URL to handle replies
     

    path('logout/', views.logout, name='logout'),  # Logout route
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)