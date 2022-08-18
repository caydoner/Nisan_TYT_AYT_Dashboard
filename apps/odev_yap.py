from utility import *
def app():
    # Ödev Yapma Arayüzü
    st.subheader('YAPILMAYAN VE EKSİK ÖDEVLER LİSTESİ')
    df= pd.read_sql_query("SELECT * from teacher_table", the_conn)
    odevler = AgGrid(data=df)

    if df.shape[0]>0:
        st.write('Lütfen Yapılacak Ödev ID Numarasını Seçiniz. ')
        id=st.selectbox(label='ID',options=df.loc[df.degerlendirme!='Yapıldı'].id.unique().tolist(),key='id')
        tarih=st.text_input(label='Odev Tarihi',value=df.loc[df.id==id].tarih.values[0],key='tarih',disabled=True)
        ders=st.text_input(label='Ders',value=df.loc[df.id==id].ders.values[0],key='ders',disabled=True)
        odev_veren=st.text_input(label='Unite',value=df.loc[df.id==id].odev_veren.values[0],key='odev_veren',disabled=True)
        konu=st.text_input(label='Konu',value=df.loc[df.id==id].konu.values[0],key='konu',disabled=True)
        kaynak=st.text_input(label='Ödevin Verildiği Kaynak Kitap:', value=df.loc[df.id==id].kaynak.values[0],key='kaynak',disabled=True)
        sayfa=st.text_input(label='Ödev Sayfası:',value=df.loc[df.id==id].sayfa.values[0],key='sayfa',disabled=True)
        sorular=st.text_input(label='Çözülecek Sorular Örn.(1-5,8,10,12-18)',value=df.loc[df.id==id].sorular.values[0],key='sorular',disabled=True)
        soru_sayisi = st.text_input(label=f'Çözülecek Soru Sayısı', value=soru_sayisi_hesapla(sorular)[1], key='soru_sayisi', disabled=True)
        cozulen_sorular=st.text_input(label='Çözülen Sorular Örn.(1-5,10,12-15)',value=df.loc[df.id==id].cozulen_sorular.values[0],key='cozulen_sorular')
        cozulen_soru_sayisi = st.text_input(label=f'Çözülen Soru Sayısı',  value=soru_sayisi_hesapla(cozulen_sorular)[1], key='cozulen_soru_sayisi', disabled=True)
        kalan_sorular = st.text_input(label='Kalan Sorular Örn.(8,18)', value=sorted(list(set([i for i in soru_sayisi_hesapla(sorular)[0] if i not in soru_sayisi_hesapla(cozulen_sorular)[0]]))), key='kalan_sorular', disabled=True)
        kalan_soru_sayisi = st.text_input(label='Kalan Soru Sayısı', value=str(int(soru_sayisi)-int(cozulen_soru_sayisi)),key='kalan_soru_sayisi', disabled=True)

        student_rec_odev_yap=(cozulen_sorular,cozulen_soru_sayisi,kalan_sorular,kalan_soru_sayisi,id)
        student_submit = st.button('Kaydet')
        if student_submit:
            if the_conn is not None:
                update_odev(the_conn, student_rec_odev_yap)
                st.success('Kaydedildi.')
            else:
                st.error("Hata! veritabani baglantisi kurulamiyor. Kaydedilemedi.")
