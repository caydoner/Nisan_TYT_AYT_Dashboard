from main import *
def app():
    # KONU Ekleme ARAYÜZÜ
    st.subheader('YENİ KONU EKLEME PANOSU')
    df_konu=pd.read_sql_query("SELECT * from konutable", the_conn)
    konu_form = st.form(key='konu-form')
    sinav=konu_form.selectbox(label='Sınav',options=['TYT','AYT'])
    ders=konu_form.selectbox(label='Ders',options=['Matematik','Türkçe','Geometri','Fizik','Kimya','Biyoloji','Coğrafya','Tarih','Felsefe','Din'],key='ders')
    unite=konu_form.text_input(label='Unite Adı',value='',key='unite_adi')
    konu=konu_form.text_input(label='Konu Adı',value='',key='konu_adi')
    konu_rec=(sinav,ders,unite,konu)
    konu_submit = konu_form.form_submit_button('Konu Ekle')

    if konu_submit:
        if the_conn is not None:
            konu_ekle(the_conn, konu_rec)
            st.success('Konu Eklendi!')
        else:
            st.error("Hata! veritabani baglantisi kurulamiyor. Konu Eklenemedi.")

    st.dataframe(df_konu)
