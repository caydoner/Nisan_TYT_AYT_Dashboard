from utility import *
def app():
    # Yeni Ödev Verme Arayüzü
    st.subheader('YENİ ÖDEV VERME PANOSU')
    df_konu=pd.read_sql_query("SELECT * from konutable", the_conn)
    sinav=st.selectbox(label='Sınav',options=['TYT','AYT'],key='sinav')
    tarih=st.date_input(label='Odev Tarihi',value=None,key='tarih')
    ders=st.selectbox(label='Ders',options=df_konu.loc[(df_konu.sinav==sinav)].ders.unique().tolist(),key='ders')
    if st.session_state["username"]=='mtekin':
        odev_veren=st.text_input(label='Ödevi Veren',value="MUSTAFA TEKİN", key='unite',disabled=True)
    else:
        odev_veren = st.selectbox(label='Ödevi Veren', options=["MUSTAFA TEKİN", "OKUL ÖĞRETMENİ", "ÖDEV HARİCİ ÇALIŞMA"], key='unite')
    konu=st.selectbox(label='Konu',options=df_konu.loc[(df_konu.sinav==sinav)&(df_konu.ders==ders)].konu.unique().tolist(),key='konu')
    kaynak=st.selectbox(label='Ödevin Verildiği Kaynak Kitap:', options=['Apotemi','Acil','Orjinal','Bilgi Sarmalı','3-4-5'])
    sayfa=st.text_input(label='Ödev Sayfası:',key='sayfa')
    sorular=st.text_input(label='Çözülecek Sorular Örn.(1-5,8,10,12-18)',value="",key='sorular')
    soru_sayisi=st.text_input(label=f'Çözülecek Soru Sayısı',value=soru_sayisi_hesapla(sorular)[1],key='soru_sayisi',disabled=True)
    cozulen_sorular=st.text_input(label='Çözülen Sorular Örn.(1-5,10,12-17)',value="",key='cozulen_sorular',disabled=True)
    cozulen_soru_sayisi=st.text_input(label=f'Çözülen Soru Sayısı',value=soru_sayisi_hesapla(st.session_state.cozulen_sorular)[1],key='cozulen_soru_sayisi',disabled=True)
    kalan_sorular=st.text_input(label='Kalan Sorular Örn.(8,18)',value=sorted([i for i in soru_sayisi_hesapla(st.session_state.sorular)[0] if i not in soru_sayisi_hesapla(st.session_state.cozulen_sorular)[0]]),key='kalan_sorular',disabled=True)
    kalan_soru_sayisi=st.text_input(label='Kalan Soru Sayısı',value=len([i for i in soru_sayisi_hesapla(st.session_state.sorular)[0] if i not in soru_sayisi_hesapla(st.session_state.cozulen_sorular)[0]]),key='kalan_soru_sayisi',disabled=True)
    degerlendirme=st.selectbox(label='Ödev Yapıldı mı?',options=['Yapılmadı','Eksik','Yapıldı'],key='degerlendirme',disabled=True)
    aciklama=st.text_input(label='Görüşler:',value='',key='aciklama')
    teacher_rec_odev_ver=(sinav,tarih,ders,odev_veren,konu,kaynak,sayfa,sorular,soru_sayisi,cozulen_sorular,cozulen_soru_sayisi,kalan_sorular,kalan_soru_sayisi,degerlendirme,aciklama)
    teacher_submit_odev_ver = st.button('Ödev Ver')

    if teacher_submit_odev_ver:
        if the_conn is not None:
            insert_row_from_teacher(the_conn, teacher_rec_odev_ver)
            st.success('Ödev Verildi.')
        else:
            st.error("Hata! veritabani baglantisi kurulamiyor. Ödev Verilemedi.")

