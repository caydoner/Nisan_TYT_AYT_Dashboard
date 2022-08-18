from multiapp import MultiApp
from apps import yeni_odev_ver,odev_sil,odev_yap,izleme,odev_harici_calisma,yeni_konu_ekle,konu_silme
import yaml
from streamlit_authenticator import Authenticate
from yaml import SafeLoader
from utility import *
st.set_page_config(
    page_title="Nisan's TYT and AYT Dashboard",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded")
local_css('style.css')


# --- USER AUTHENTICATION ---
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status == False:
    st.error("Kullanıcı Adı/Şifre Yanlış!")

if authentication_status == None:
    st.warning("Lütfen Kullanıcı Adı ve Şifre Giriniz.")

if authentication_status:
    if username=='naydoner':

        app = MultiApp()

        # Add all your application here
        app.add_app("ÖDEV İZLEME VE DEĞERLENDİRME", izleme.app)
        #app.add_app("YENİ ÖDEV VER", yeni_odev_ver.app)
        app.add_app("ÖDEV YAP", odev_yap.app)
        #app.add_app("ÖDEV SİL", odev_sil.app)
        app.add_app("KONU EKLE",yeni_konu_ekle.app)
        app.add_app("KONU SİL", konu_silme.app)
        app.add_app("ÖDEV HARİCİ ÇALIŞMA",odev_harici_calisma.app)
        # The main app
        app.run()
    else:
        app = MultiApp()
        # Add all your application here
        app.add_app("İzleme ve Değerlendirme", izleme.app)
        app.add_app("Yeni Ödev Ver", yeni_odev_ver.app)
        app.add_app("Ödev Yap", odev_yap.app)
        app.add_app("Ödev Sil", odev_sil.app)
        app.add_app("Yeni Konu Ekle", yeni_konu_ekle.app)
        app.add_app("Konu Sil", konu_silme.app)
        # The main app
        app.run()