import pandas as pd
import streamlit as st
from st_aggrid import AgGrid
from app import the_conn

def app():
    df_teacher= pd.read_sql_query("SELECT * from teacher_table", the_conn)
    st.header('İZLEME VE DEĞERLENDİRME PANOSU')
    tyt,ayt= st.columns(2)
    with tyt:
        st.title('TYT')
    with ayt:
        st.title('AYT')

    d1, d2, d3,d4,d5,d6 = st.columns([1, 1, 3,1,1,3])

    with d1:
        tytders = st.selectbox(label='DERS',options=["Tümü"]+df_teacher.loc[df_teacher.sinav == 'TYT'].ders.unique().tolist(),key='tytders')
    with d2:
        tytkaynak = st.selectbox(label='KAYNAK',
                                 options=["Tümü"]+df_teacher.loc[df_teacher.sinav == 'TYT'].kaynak.unique().tolist(),
                                 key='tytkaynak')
    with d3:
        tytkonu = st.selectbox(label='KONU',
                               options=["Tümü"]+df_teacher.loc[df_teacher.sinav == 'TYT'].konu.unique().tolist(),
                               key='tytkonu')
    with d4:
        aytders = st.selectbox(label='DERS',
                               options=["Tümü"]+df_teacher.loc[df_teacher.sinav == 'AYT'].ders.unique().tolist(),
                               key='aytders')
    with d5:
        aytkaynak = st.selectbox(label='KAYNAK',
                                 options=["Tümü"]+df_teacher.loc[df_teacher.sinav == 'AYT'].kaynak.unique().tolist(),
                                 key='aytkaynak')
    with d6:
        aytkonu = st.selectbox(label='KONU',
                               options=["Tümü"]+df_teacher.loc[df_teacher.sinav == 'AYT'].konu.unique().tolist(),
                               key='aytkonu')

    st.subheader('MUSTAFA TEKİN')
    m1, m2, m3,m4,m5,m6 = st.columns([2, 2, 4,2, 2, 4])
    with m1:
        tyt_mhoca_verilen_soru_sayisi = st.metric(label="Verilen Soru Sayısı", value=calc_metrics(tytders,tytkaynak,tytkonu,'TYT')[0], delta="1.2 °F")
    with m2:
        tyt_mhoca_cozulen_soru_sayisi = st.metric(label="Çözülen Soru Sayısı", value=calc_metrics(tytders,tytkaynak,tytkonu,'TYT')[1], delta="1.2 °F")
    with m3:
        tyt_mhoca_cozulemeyen_soru_sayisi = st.metric(label="Çözülemeyen Soru Sayısı", value=calc_metrics(tytders,tytkaynak,tytkonu,'TYT')[2], delta="1.2 °F")
    with m4:
        ayt_mhoca_verilen_soru_sayisi = st.metric(label="Verilen Soru Sayısı", value=calc_metrics(aytders,aytkaynak,aytkonu, 'AYT')[0], delta="1.2 °F")
    with m5:
        ayt_mhoca_cozulen_soru_sayisi = st.metric(label="Çözülen Soru Sayısı", value=calc_metrics(aytders,aytkaynak,aytkonu, 'AYT')[1], delta="1.2 °F")
    with m6:
        ayt_mhoca_cozulemeyen_soru_sayisi = st.metric(label="Çözülemeyen Soru Sayısı", value=calc_metrics(aytders,aytkaynak,aytkonu,'AYT')[2], delta="1.2 °F")

    st.subheader('OKUL')
    o1, o2, o3,o4,o5,o6 = st.columns([2, 2, 4,2, 2, 4])
    with o1:
        tyt_okul_verilen_soru_sayisi = st.metric(label="Verilen Soru Sayısı", value=calc_metrics(tytders,tytkaynak,tytkonu,'TYT')[3], delta="1.2 °F")
    with o2:
        tyt_okul_cozulen_soru_sayisi = st.metric(label="Çözülen Soru Sayısı", value=calc_metrics(tytders,tytkaynak,tytkonu,'TYT')[4], delta="1.2 °F")
    with o3:
        tyt_okul_cozulemeyen_soru_sayisi = st.metric(label="Çözülemeyen Soru Sayısı", value=calc_metrics(tytders,tytkaynak,tytkonu,'TYT')[5],
                                                     delta="1.2 °F")
    with o4:
        ayt_okul_verilen_soru_sayisi = st.metric(label="Verilen Soru Sayısı", value=calc_metrics(aytders,aytkaynak,aytkonu,'AYT')[3], delta="1.2 °F")
    with o5:
        ayt_okul_cozulen_soru_sayisi = st.metric(label="Çözülen Soru Sayısı", value=calc_metrics(aytders,aytkaynak,aytkonu,'AYT')[4], delta="1.2 °F")
    with o6:
        ayt_okul_cozulemeyen_soru_sayisi = st.metric(label="Çözülemeyen Soru Sayısı", value=calc_metrics(aytders,aytkaynak,aytkonu,'AYT')[5], delta="1.2 °F")

    st.subheader('ÖDEV HARİCİ')
    n1, n2, n3,n4,n5,n6 = st.columns([2, 2, 4,2, 2, 4])
    with n1:
        tyt_okul_verilen_soru_sayisi = st.metric(label="Verilen Soru Sayısı", value=calc_metrics(tytders,tytkaynak,tytkonu,'TYT')[6], delta="1.2 °F")
    with n2:
        tyt_okul_cozulen_soru_sayisi = st.metric(label="Çözülen Soru Sayısı", value=calc_metrics(tytders,tytkaynak,tytkonu,'TYT')[7], delta="1.2 °F")
    with n3:
        tyt_okul_cozulemeyen_soru_sayisi = st.metric(label="Çözülemeyen Soru Sayısı", value=calc_metrics(tytders,tytkaynak,tytkonu,'TYT')[8],
                                                     delta="1.2 °F")
    with n4:
        ayt_okul_verilen_soru_sayisi = st.metric(label="Verilen Soru Sayısı", value=calc_metrics(aytders,aytkaynak,aytkonu,'AYT')[6], delta="1.2 °F")
    with n5:
        ayt_okul_cozulen_soru_sayisi = st.metric(label="Çözülen Soru Sayısı", value=calc_metrics(aytders,aytkaynak,aytkonu,'AYT')[7], delta="1.2 °F")
    with n6:
        ayt_okul_cozulemeyen_soru_sayisi = st.metric(label="Çözülemeyen Soru Sayısı", value=calc_metrics(aytders,aytkaynak,aytkonu,'AYT')[8], delta="1.2 °F")

    st.subheader('TOPLAM')
    t1, t2, t3,t4,t5,t6 = st.columns([2, 2, 4,2, 2, 4])
    with t1:
        tyt_okul_verilen_soru_sayisi = st.metric(label="Verilen Soru Sayısı", value=calc_metrics(tytders,tytkaynak,tytkonu,'TYT')[9], delta="1.2 °F")
    with t2:
        tyt_okul_cozulen_soru_sayisi = st.metric(label="Çözülen Soru Sayısı", value=calc_metrics(tytders,tytkaynak,tytkonu,'TYT')[10], delta="1.2 °F")
    with t3:
        tyt_okul_cozulemeyen_soru_sayisi = st.metric(label="Çözülemeyen Soru Sayısı", value=calc_metrics(tytders,tytkaynak,tytkonu,'TYT')[11],
                                                     delta="1.2 °F")
    with t4:
        ayt_okul_verilen_soru_sayisi = st.metric(label="Verilen Soru Sayısı", value=calc_metrics(aytders,aytkaynak,aytkonu,'AYT')[9], delta="1.2 °F")
    with t5:
        ayt_okul_cozulen_soru_sayisi = st.metric(label="Çözülen Soru Sayısı", value=calc_metrics(aytders,aytkaynak,aytkonu,'AYT')[10], delta="1.2 °F")
    with t6:
        ayt_okul_cozulemeyen_soru_sayisi = st.metric(label="Çözülemeyen Soru Sayısı", value=calc_metrics(aytders,aytkaynak,aytkonu,'AYT')[11], delta="1.2 °F")

    st.subheader('VERİLEN ÖDEVLER VE ÖDEV HARİCİ ÇALIŞMALAR TABLOSU')
    df_teacher = pd.read_sql_query("SELECT * from teacher_table", the_conn)
    odevler = AgGrid(data=df_teacher)
