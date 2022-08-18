from utility import *
def app():
    # KONU Silme Arayüzü
    st.subheader('KONU SİLME PANOSU')
    df_konu=pd.read_sql_query("SELECT * from konutable", the_conn)
    id=st.selectbox(label='id',options=df_konu.id.unique().tolist())
    sinav=st.text_input(label='Sınav',value=df_konu.loc[df_konu.id==id].sinav.values[0],disabled=True)
    ders=st.text_input(label='ders',value=df_konu.loc[df_konu.id==id].ders.values[0],disabled=True)
    unite=st.text_input(label='unite',value=df_konu.loc[df_konu.id==id].unite.values[0],disabled=True)
    konu=st.text_input(label='konu',value=df_konu.loc[df_konu.id==id].konu.values[0],disabled=True)
    konu_sil =  st.button('Konu Sil')
    if konu_sil:
        if the_conn is not None:
            cur = the_conn.cursor()
            cur.execute("DELETE FROM konutable WHERE id=?", [id])
            the_conn.commit()
            st.success('Konu Silindi!')

        else:
            st.error("Hata! veritabani baglantisi kurulamiyor. Konu Eklenemedi.")
    st.dataframe(df_konu)


