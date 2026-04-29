from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .forms import EmailLoginForm

urlpatterns = [
    path('', views.home, name='home'),
    path('catalog/', views.catalog_list, name='catalog_list'),
    path('catalog/<slug:slug>/', views.catalog_detail, name='catalog_detail'),
    path('catalog/<slug:slug>/oferta/', views.lead_offer, name='lead_offer'),
    path('comunitate/', views.comunitate, name='comunitate'),
    path('despre/', views.about_page, name='about'),
    path('contact/', views.contact_page, name='contact_page'),
    path('termeni/', views.terms_page, name='terms'),
    path('confidentialitate/', views.privacy_page, name='privacy'),
    path('sitemap.xml', views.sitemap_xml, name='sitemap'),
    path('robots.txt', views.robots_txt, name='robots_txt'),
    path('health/', views.health_check, name='health_check'),

    path('register/', views.register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(
        template_name='catalog/login.html',
        authentication_form=EmailLoginForm,
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.profile_edit_view, name='profile_edit'),

    path('forum/', views.forum_index, name='forum_index'),
    path('forum/categorie/<slug:slug>/', views.forum_category, name='forum_category'),
    path('forum/topic/nou/', views.topic_new, name='topic_new'),
    path('forum/topic/<slug:slug>/', views.topic_detail, name='topic_detail'),
    path('forum/topic/<slug:slug>/raspunde/', views.topic_reply, name='topic_reply'),
    path('forum/raporteaza/topic/<int:pk>/', views.report_topic, name='report_topic'),
    path('forum/raporteaza/reply/<int:pk>/', views.report_reply, name='report_reply'),
    path('forum/reguli/', views.forum_rules, name='forum_rules'),

    path('membri/', views.member_directory, name='member_directory'),
    path('membri/<str:username>/', views.member_public_profile, name='member_public_profile'),
]
