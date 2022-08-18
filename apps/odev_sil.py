import pandas as pd
import streamlit as st
from st_aggrid import AgGrid
from app import the_conn
def app():
    # Ödev Silme Arayüzü
    st.subheader('VERİLEN ÖDEVİ SİLME PANOSU')
    df_teacher = pd.read_sql_query("SELECT * from teacher_table", the_conn)
    response=AgGrid(data=df_teacher)
    delete_form = st.form(key='delete-form')
    delete_id=delete_form.number_input(label='Silinecek Kayıt ID numarası',min_value=1)
    teacher_delete=delete_form.form_submit_button(label='Ödev Sil')
    if teacher_delete:
        if the_conn is not None:
            cur=the_conn.cursor()
            cur.execute("DELETE FROM teacher_table WHERE id=?",[delete_id])
            the_conn.commit()
            st.success('Ödev Silindi')
        else:
            st.error("Hata! veritabani baglantisi kurulamiyor. Ödev Silinemedi.")

