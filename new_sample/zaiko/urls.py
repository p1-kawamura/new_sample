from django.urls import path
from django.contrib.auth import views as auth_views
from .views import index,shouhin_all,csv_imp,csv_imp_page,dele,hinban_enter_ajax,hinban_click_ajax,color_size_click_ajax,\
                    kakou_click_ajax,swatch_click_ajax,keep_kaijo_ajax,check_addlist_ajax,irai_del_ajax,irai_num_copy,\
                    hinban_click_ajax2,color_size_click_ajax2,toriyose_add_ajax,last_kakunin,\
                    haisou_cus_success,haisou_tempo_success,haisou_keep_success,irai_success,irai_rireki,irai_shusei_ajax,irai_shusei_index,irai_shusei,\
                    rireki_kakunin,page_prev,page_first,page_next,page_last,rireki_kensaku,rireki_kensaku_all,cancel_ajax,keep_hassou,\
                    csv_make,csv_download,unsou_page,unsou_csv_imp,all_delete,eigyou_csv_download


app_name="zaiko"
urlpatterns = [
    path('', index, name="index"),
    path('login/', auth_views.LoginView.as_view(template_name='zaiko/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('shouhin_all/', shouhin_all, name="shouhin_all"), 
    path('irai_success/', irai_success, name="irai_success"), 
    path('irai_rireki/', irai_rireki, name="irai_rireki"), 
    path('irai_shusei_ajax/', irai_shusei_ajax, name="irai_shusei_ajax"), 
    path('irai_shusei_index/', irai_shusei_index, name="irai_shusei_index"), 
    path('irai_shusei/', irai_shusei, name="irai_shusei"), 
    path('rireki_kensaku/', rireki_kensaku, name="rireki_kensaku"),
    path('rireki_kensaku_all/', rireki_kensaku_all, name="rireki_kensaku_all"), 
    path('page_prev/', page_prev, name="page_prev"), 
    path('page_first/', page_first, name="page_first"),
    path('page_next/', page_next, name="page_next"), 
    path('page_last/', page_last, name="page_last"), 
    path('csv_imp_page/', csv_imp_page, name="csv_imp_page"), 
    path('csv_imp/', csv_imp, name="csv_imp"),
    path('dele/', dele, name="dele"), 
    path('hinban_enter_ajax/', hinban_enter_ajax, name="hinban_enter_ajax"),
    path('hinban_click_ajax/', hinban_click_ajax, name="hinban_click_ajax"),
    path('color_size_click_ajax/', color_size_click_ajax, name="color_size_click_ajax"),
    path('kakou_click_ajax/', kakou_click_ajax, name="kakou_click_ajax"),
    path('swatch_click_ajax/', swatch_click_ajax, name="swatch_click_ajax"),
    path('keep_kaijo_ajax/', keep_kaijo_ajax, name="keep_kaijo_ajax"),
    path('check_addlist_ajax/', check_addlist_ajax, name="check_addlist_ajax"),
    path('irai_del_ajax/', irai_del_ajax, name="irai_del_ajax"),
    path('irai_num_copy/', irai_num_copy, name="irai_num_copy"),
    path('hinban_click_ajax2/', hinban_click_ajax2, name="hinban_click_ajax2"),
    path('color_size_click_ajax2/', color_size_click_ajax2, name="color_size_click_ajax2"),
    path('toriyose_add_ajax/', toriyose_add_ajax, name="toriyose_add_ajax"),
    path('last_kakunin/', last_kakunin, name="last_kakunin"),
    path('haisou_cus_success/', haisou_cus_success, name="haisou_cus_success"),
    path('haisou_tempo_success/', haisou_tempo_success, name="haisou_tempo_success"),
    path('haisou_keep_success/', haisou_keep_success, name="haisou_keep_success"),
    path('rireki_kakunin/<int:pk>', rireki_kakunin, name="rireki_kakunin"),
    path('cancel_ajax/', cancel_ajax, name="cancel_ajax"),
    path('keep_hassou/', keep_hassou, name="keep_hassou"),
    path('csv_make/', csv_make, name="csv_make"),
    path('csv_download/', csv_download, name="csv_download"),
    path('unsou_page/', unsou_page, name="unsou_page"),
    path('unsou_csv_imp/', unsou_csv_imp, name="unsou_csv_imp"),
    path('all_delete/', all_delete, name="all_delete"),
    path('eigyou_csv_download/', eigyou_csv_download, name="eigyou_csv_download")
]