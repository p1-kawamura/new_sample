from django.urls import path
from .views import index,shouhin_all,csv_imp,csv_imp_page,dele,hinban_enter_ajax,hinban_click_ajax,color_size_click_ajax,\
                    kakou_click_ajax,swatch_click_ajax,keep_kaijo_ajax,check_addlist_ajax,irai_del_ajax,\
                    kokyaku_index,kokyaku_api,hinban_click_ajax2,color_size_click_ajax2,toriyose_add_ajax,\
                    last_kakunin,haisou_cus_success,haisou_tempo_success,haisou_keep_success,irai_success,irai_rireki,\
                    rireki_btn,rireki_kakunin


app_name="zaiko"
urlpatterns = [
    path('', index, name="index"),
    path('shouhin_all/', shouhin_all, name="shouhin_all"), 
    path('irai_success/', irai_success, name="irai_success"), 
    path('irai_rireki/', irai_rireki, name="irai_rireki"), 
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
    path('hinban_click_ajax2/', hinban_click_ajax2, name="hinban_click_ajax2"),
    path('color_size_click_ajax2/', color_size_click_ajax2, name="color_size_click_ajax2"),
    path('toriyose_add_ajax/', toriyose_add_ajax, name="toriyose_add_ajax"),
    path('last_kakunin/', last_kakunin, name="last_kakunin"),
    path('haisou_cus_success/', haisou_cus_success, name="haisou_cus_success"),
    path('haisou_tempo_success/', haisou_tempo_success, name="haisou_tempo_success"),
    path('haisou_keep_success/', haisou_keep_success, name="haisou_keep_success"),
    path('rireki_btn/', rireki_btn, name="rireki_btn"),
    path('rireki_kakunin/', rireki_kakunin, name="rireki_kakunin"),
    path('kokyaku_index/', kokyaku_index, name="kokyaku_index"), #顧客APIテスト
    path('kokyaku_api/', kokyaku_api, name="kokyaku_api"), #顧客APIテスト
]