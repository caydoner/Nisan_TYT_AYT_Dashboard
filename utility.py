import streamlit as st
import re
import sqlite3
from sqlite3 import Error
import pandas as pd
from st_aggrid import AgGrid, DataReturnMode, GridUpdateMode, GridOptionsBuilder
import streamlit_authenticator as stauth


def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


def create_dbconnection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    the_conn = None
    try:
        the_conn = sqlite3.connect(db_file, check_same_thread=False)
        return the_conn
    except Error as e:
        print(e)

    return the_conn


def create_table(the_conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param the_conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = the_conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def insert_row_from_teacher(the_conn, kayit):
    sql_for_insert_teacher_rec = """INSERT INTO teacher_table(sinav,tarih,ders,odev_veren,konu,kaynak,sayfa,sorular,soru_sayisi,cozulen_sorular,cozulen_soru_sayisi,kalan_sorular,kalan_soru_sayisi,degerlendirme,Aciklama)
       VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) """
    cur = the_conn.cursor()
    cur.execute(sql_for_insert_teacher_rec, kayit)
    the_conn.commit()


def delete_odev_from_teacher(conn, task):
    """
    update priority, begin_date, and end date of a task
    :param conn:
    :param task:
    :return: project id
    """
    sql = ''' DELETE FROM teacher_table
                 WHERE id=?'''
    cur = conn.cursor()
    cur.execute(sql, task)
    conn.commit()


def update_odev(conn, task):
    """
    update priority, begin_date, and end date of a task
    :param conn:
    :param task:
    :return: project id
    """
    sql = ''' UPDATE teacher_table
                 SET cozulen_sorular = ?, cozulen_soru_sayisi = ?, kalan_sorular=?, kalan_soru_sayisi=?, degerlendirme=?
                 WHERE id=? '''
    cur = conn.cursor()
    cur.execute(sql, task)
    conn.commit()


def konu_ekle(the_conn, kayit):
    sql_for_konu_ekle = """INSERT INTO konutable(sinav,ders,unite,konu) 
       VALUES(?,?,?,?) """
    cur = the_conn.cursor()
    cur.execute(sql_for_konu_ekle, kayit)
    the_conn.commit()


def konu_sil(conn, kayit):
    """
    update priority, begin_date, and end date of a task
    :param conn:
    :param task:
    :return: project id
    """
    sql = ''' DELETE FROM konutable
                 WHERE id=?'''
    cur = conn.cursor()
    cur.execute(sql, kayit)
    conn.commit()


def insert_user(the_conn, kayit):
    """Returns the user on a successful user creation, otherwise raises and error"""
    sql_for_user_ekle = """INSERT INTO users(key,name,password) 
       VALUES(?,?,?) """
    cur = the_conn.cursor()
    cur.execute(sql_for_user_ekle, kayit)
    the_conn.commit()


def soru_sayisi_hesapla(s):
    sorular = []
    patrn1 = r",\d+"
    patrn2 = r"\d+-\d+"
    p1_list = re.findall(pattern=patrn1, string=s)
    p2_list = re.findall(pattern=patrn2, string=s)

    if len(p1_list) > 0:
        for i in p1_list:
            sorular = sorular + [eval(i[1:])]
    if len(p2_list) > 0:
        for i in p2_list:
            t = i.split(sep='-')
            val = range(int(t[0]), int(t[1]) + 1)
            sorular = sorular + list(val)
    return [sorular, len(sorular)]


def degerlendir(soru_sayisi,cozulen_soru_sayisi):
    if cozulen_soru_sayisi == soru_sayisi:
        return 'Yapıldı'
    elif cozulen_soru_sayisi == "0":
        return 'Yapılmadı'
    else:
        return 'Eksik'



def calc_metrics(ders, kaynak, konu,sinav):
    df_teacher= pd.read_sql_query("SELECT * from teacher_table", the_conn)
    if ders == 'Tümü' and kaynak == 'Tümü' and konu == 'Tümü':
        m_tyt_soru_sayisi = df_teacher.loc[(df_teacher.odev_veren == "MUSTAFA TEKİN") & (df_teacher.sinav == sinav)].soru_sayisi.sum()
        m_tyt_cozulen_soru_sayisi = df_teacher.loc[(df_teacher.odev_veren == "MUSTAFA TEKİN") & (df_teacher.sinav == sinav)].cozulen_soru_sayisi.sum()
        m_tyt_kalan_soru_sayisi = df_teacher.loc[(df_teacher.odev_veren == "MUSTAFA TEKİN") & (df_teacher.sinav == sinav)].kalan_soru_sayisi.sum()
        o_tyt_soru_sayisi = df_teacher.loc[(df_teacher.odev_veren == "OKUL ÖĞRETMENİ") & (df_teacher.sinav == sinav)].soru_sayisi.sum()
        o_tyt_cozulen_soru_sayisi = df_teacher.loc[(df_teacher.odev_veren == "OKUL ÖĞRETMENİ") & (df_teacher.sinav == sinav)].cozulen_soru_sayisi.sum()
        o_tyt_kalan_soru_sayisi = df_teacher.loc[(df_teacher.odev_veren == "OKUL ÖĞRETMENİ") & (df_teacher.sinav == sinav)].kalan_soru_sayisi.sum()
        n_tyt_soru_sayisi = df_teacher.loc[(df_teacher.odev_veren == "ÖDEV HARİCİ ÇALIŞMA") & (df_teacher.sinav == sinav)].soru_sayisi.sum()
        n_tyt_cozulen_soru_sayisi = df_teacher.loc[(df_teacher.odev_veren == "ÖDEV HARİCİ ÇALIŞMA") & (df_teacher.sinav == sinav)].cozulen_soru_sayisi.sum()
        n_tyt_kalan_soru_sayisi = df_teacher.loc[(df_teacher.odev_veren == "ÖDEV HARİCİ ÇALIŞMA") & (df_teacher.sinav == sinav)].kalan_soru_sayisi.sum()
        t_tyt_soru_sayisi = df_teacher.loc[df_teacher.sinav == sinav].soru_sayisi.sum()
        t_tyt_cozulen_soru_sayisi = df_teacher.loc[df_teacher.sinav == sinav].cozulen_soru_sayisi.sum()
        t_tyt_kalan_soru_sayisi = df_teacher.loc[df_teacher.sinav == sinav].kalan_soru_sayisi.sum()
        return [m_tyt_soru_sayisi, m_tyt_cozulen_soru_sayisi, m_tyt_kalan_soru_sayisi, o_tyt_soru_sayisi,
                o_tyt_cozulen_soru_sayisi, o_tyt_kalan_soru_sayisi, n_tyt_soru_sayisi,
                n_tyt_cozulen_soru_sayisi, n_tyt_kalan_soru_sayisi, t_tyt_soru_sayisi, t_tyt_cozulen_soru_sayisi,
                t_tyt_kalan_soru_sayisi]
    elif ders != 'Tümü' and kaynak == 'Tümü' and konu == 'Tümü':
        m_tyt_soru_sayisi = df_teacher.loc[(df_teacher.ders == ders) & (df_teacher.odev_veren == "MUSTAFA TEKİN") & (df_teacher.sinav == sinav)].soru_sayisi.sum()
        m_tyt_cozulen_soru_sayisi = df_teacher.loc[(df_teacher.ders == ders) & (df_teacher.odev_veren == "MUSTAFA TEKİN") & (df_teacher.sinav == sinav)].cozulen_soru_sayisi.sum()
        m_tyt_kalan_soru_sayisi = df_teacher.loc[(df_teacher.ders == ders) & (df_teacher.odev_veren == "MUSTAFA TEKİN") & (df_teacher.sinav == sinav)].kalan_soru_sayisi.sum()
        o_tyt_soru_sayisi = df_teacher.loc[(df_teacher.ders == ders) & (df_teacher.odev_veren == "OKUL ÖĞRETMENİ") & (df_teacher.sinav == sinav)].soru_sayisi.sum()
        o_tyt_cozulen_soru_sayisi = df_teacher.loc[(df_teacher.ders == ders) & (df_teacher.odev_veren == "OKUL ÖĞRETMENİ") & (df_teacher.sinav == sinav)].cozulen_soru_sayisi.sum()
        o_tyt_kalan_soru_sayisi = df_teacher.loc[(df_teacher.ders == ders) & (df_teacher.odev_veren == "OKUL ÖĞRETMENİ") & (df_teacher.sinav == sinav)].kalan_soru_sayisi.sum()
        n_tyt_soru_sayisi = df_teacher.loc[(df_teacher.ders == ders) & (df_teacher.odev_veren == "ÖDEV HARİCİ ÇALIŞMA") & (df_teacher.sinav == sinav)].soru_sayisi.sum()
        n_tyt_cozulen_soru_sayisi = df_teacher.loc[(df_teacher.ders == ders) & (df_teacher.odev_veren == "ÖDEV HARİCİ ÇALIŞMA") & (df_teacher.sinav == sinav)].cozulen_soru_sayisi.sum()
        n_tyt_kalan_soru_sayisi = df_teacher.loc[(df_teacher.ders == ders) & (df_teacher.odev_veren == "ÖDEV HARİCİ ÇALIŞMA") & (df_teacher.sinav == sinav)].kalan_soru_sayisi.sum()
        t_tyt_soru_sayisi = df_teacher.loc[(df_teacher.ders == ders) & (df_teacher.sinav == sinav)].soru_sayisi.sum()
        t_tyt_cozulen_soru_sayisi = df_teacher.loc[(df_teacher.ders == ders) & (df_teacher.sinav == sinav)].cozulen_soru_sayisi.sum()
        t_tyt_kalan_soru_sayisi = df_teacher.loc[(df_teacher.ders == ders) & (df_teacher.sinav == sinav)].kalan_soru_sayisi.sum()
        return [m_tyt_soru_sayisi, m_tyt_cozulen_soru_sayisi, m_tyt_kalan_soru_sayisi, o_tyt_soru_sayisi,
                o_tyt_cozulen_soru_sayisi, o_tyt_kalan_soru_sayisi, n_tyt_soru_sayisi,
                n_tyt_cozulen_soru_sayisi, n_tyt_kalan_soru_sayisi, t_tyt_soru_sayisi, t_tyt_cozulen_soru_sayisi,
                t_tyt_kalan_soru_sayisi]
    elif ders != 'Tümü' and kaynak != 'Tümü' and konu == 'Tümü':
        m_tyt_soru_sayisi = df_teacher.loc[(df_teacher.ders == ders) & (df_teacher.kaynak == kaynak) & (df_teacher.odev_veren == "MUSTAFA TEKİN") & (df_teacher.sinav == sinav)].soru_sayisi.sum()
        m_tyt_cozulen_soru_sayisi = df_teacher.loc[(df_teacher.ders == ders) & (df_teacher.kaynak == kaynak) & (df_teacher.odev_veren == "MUSTAFA TEKİN") & (df_teacher.sinav == sinav)].cozulen_soru_sayisi.sum()
        m_tyt_kalan_soru_sayisi = df_teacher.loc[(df_teacher.ders == ders) & (df_teacher.kaynak == kaynak) & (df_teacher.odev_veren == "MUSTAFA TEKİN") & (df_teacher.sinav == sinav)].kalan_soru_sayisi.sum()
        o_tyt_soru_sayisi = df_teacher.loc[(df_teacher.ders == ders) & (df_teacher.kaynak == kaynak) & (df_teacher.odev_veren == "OKUL ÖĞRETMENİ") & (df_teacher.sinav == sinav)].soru_sayisi.sum()
        o_tyt_cozulen_soru_sayisi = df_teacher.loc[(df_teacher.ders == ders) & (df_teacher.kaynak == kaynak) & (df_teacher.odev_veren == "OKUL ÖĞRETMENİ") & (df_teacher.sinav == sinav)].cozulen_soru_sayisi.sum()
        o_tyt_kalan_soru_sayisi = df_teacher.loc[(df_teacher.ders == ders) & (df_teacher.kaynak == kaynak) & (df_teacher.odev_veren == "OKUL ÖĞRETMENİ") & (df_teacher.sinav == sinav)].kalan_soru_sayisi.sum()
        n_tyt_soru_sayisi = df_teacher.loc[(df_teacher.ders == ders) & (df_teacher.kaynak == kaynak) & (df_teacher.odev_veren == "ÖDEV HARİCİ ÇALIŞMA") & (df_teacher.sinav == sinav)].soru_sayisi.sum()
        n_tyt_cozulen_soru_sayisi = df_teacher.loc[(df_teacher.ders == ders) & (df_teacher.kaynak == kaynak) & (df_teacher.odev_veren == "ÖDEV HARİCİ ÇALIŞMA") & (df_teacher.sinav == sinav)].cozulen_soru_sayisi.sum()
        n_tyt_kalan_soru_sayisi = df_teacher.loc[(df_teacher.ders == ders) & (df_teacher.kaynak == kaynak) & (df_teacher.odev_veren == "ÖDEV HARİCİ ÇALIŞMA") & (df_teacher.sinav == sinav)].kalan_soru_sayisi.sum()
        t_tyt_soru_sayisi = df_teacher.loc[(df_teacher.ders == ders) & (df_teacher.kaynak == kaynak) & (df_teacher.sinav == sinav)].soru_sayisi.sum()
        t_tyt_cozulen_soru_sayisi = df_teacher.loc[(df_teacher.ders == ders) & (df_teacher.kaynak == kaynak) & (df_teacher.sinav == sinav)].cozulen_soru_sayisi.sum()
        t_tyt_kalan_soru_sayisi = df_teacher.loc[(df_teacher.ders == ders) & (df_teacher.kaynak == kaynak) & (df_teacher.sinav == sinav)].kalan_soru_sayisi.sum()
        return [m_tyt_soru_sayisi, m_tyt_cozulen_soru_sayisi, m_tyt_kalan_soru_sayisi, o_tyt_soru_sayisi,
                o_tyt_cozulen_soru_sayisi, o_tyt_kalan_soru_sayisi, n_tyt_soru_sayisi,
                n_tyt_cozulen_soru_sayisi, n_tyt_kalan_soru_sayisi, t_tyt_soru_sayisi, t_tyt_cozulen_soru_sayisi,
                t_tyt_kalan_soru_sayisi]
    elif ders != 'Tümü' and kaynak != 'Tümü' and konu != 'Tümü':
        m_tyt_soru_sayisi = df_teacher.loc[(df_teacher.ders == ders) & (df_teacher.kaynak == kaynak) & (df_teacher.konu == konu) & (df_teacher.odev_veren == "MUSTAFA TEKİN") & (df_teacher.sinav == sinav)].soru_sayisi.sum()
        m_tyt_cozulen_soru_sayisi = df_teacher.loc[(df_teacher.ders == ders) & (df_teacher.kaynak == kaynak) & (df_teacher.konu == konu) & (df_teacher.odev_veren == "MUSTAFA TEKİN") & (df_teacher.sinav == sinav)].cozulen_soru_sayisi.sum()
        m_tyt_kalan_soru_sayisi = df_teacher.loc[(df_teacher.ders == ders) & (df_teacher.kaynak == kaynak) & (df_teacher.konu == konu) & (df_teacher.odev_veren == "MUSTAFA TEKİN") & (df_teacher.sinav == sinav)].kalan_soru_sayisi.sum()
        o_tyt_soru_sayisi = df_teacher.loc[(df_teacher.ders == ders) & (df_teacher.kaynak == kaynak) & (df_teacher.konu == konu) & (df_teacher.odev_veren == "OKUL ÖĞRETMENİ") & (df_teacher.sinav == sinav)].soru_sayisi.sum()
        o_tyt_cozulen_soru_sayisi = df_teacher.loc[(df_teacher.ders == ders) & (df_teacher.kaynak == kaynak) & (df_teacher.konu == konu) & (df_teacher.odev_veren == "OKUL ÖĞRETMENİ") & (df_teacher.sinav == sinav)].cozulen_soru_sayisi.sum()
        o_tyt_kalan_soru_sayisi = df_teacher.loc[(df_teacher.ders == ders) & (df_teacher.kaynak == kaynak) & (df_teacher.konu == konu) & (df_teacher.odev_veren == "OKUL ÖĞRETMENİ") & (df_teacher.sinav == sinav)].kalan_soru_sayisi.sum()
        n_tyt_soru_sayisi = df_teacher.loc[(df_teacher.ders == ders) & (df_teacher.kaynak == kaynak) & (df_teacher.konu == konu) & (df_teacher.odev_veren == "ÖDEV HARİCİ ÇALIŞMA") & (df_teacher.sinav == sinav)].soru_sayisi.sum()
        n_tyt_cozulen_soru_sayisi = df_teacher.loc[(df_teacher.ders == ders) & (df_teacher.kaynak == kaynak) & (df_teacher.konu == konu) & (df_teacher.odev_veren == "ÖDEV HARİCİ ÇALIŞMA") & (df_teacher.sinav == sinav)].cozulen_soru_sayisi.sum()
        n_tyt_kalan_soru_sayisi = df_teacher.loc[(df_teacher.ders == ders) & (df_teacher.kaynak == kaynak) & (df_teacher.konu == konu) & (df_teacher.odev_veren == "ÖDEV HARİCİ ÇALIŞMA") & (df_teacher.sinav == sinav)].kalan_soru_sayisi.sum()
        t_tyt_soru_sayisi = df_teacher.loc[(df_teacher.ders == ders) & (df_teacher.kaynak == kaynak) & (df_teacher.konu == konu) & (df_teacher.sinav == sinav)].soru_sayisi.sum()
        t_tyt_cozulen_soru_sayisi = df_teacher.loc[(df_teacher.ders == ders) & (df_teacher.kaynak == kaynak) & (df_teacher.konu == konu) & (df_teacher.sinav == sinav)].cozulen_soru_sayisi.sum()
        t_tyt_kalan_soru_sayisi = df_teacher.loc[(df_teacher.ders == ders) & (df_teacher.kaynak == kaynak) & (df_teacher.konu == konu) & (df_teacher.sinav == sinav)].kalan_soru_sayisi.sum()
        return [m_tyt_soru_sayisi, m_tyt_cozulen_soru_sayisi, m_tyt_kalan_soru_sayisi, o_tyt_soru_sayisi,
                o_tyt_cozulen_soru_sayisi, o_tyt_kalan_soru_sayisi, n_tyt_soru_sayisi,
                n_tyt_cozulen_soru_sayisi, n_tyt_kalan_soru_sayisi, t_tyt_soru_sayisi, t_tyt_cozulen_soru_sayisi,
                t_tyt_kalan_soru_sayisi]
    elif ders == 'Tümü' and kaynak != 'Tümü' and konu == 'Tümü':
        m_tyt_soru_sayisi = df_teacher.loc[(df_teacher.kaynak == kaynak) & (df_teacher.odev_veren == "MUSTAFA TEKİN") & (df_teacher.sinav == sinav)].soru_sayisi.sum()
        m_tyt_cozulen_soru_sayisi = df_teacher.loc[(df_teacher.kaynak == kaynak) & (df_teacher.odev_veren == "MUSTAFA TEKİN") & (df_teacher.sinav == sinav)].cozulen_soru_sayisi.sum()
        m_tyt_kalan_soru_sayisi = df_teacher.loc[(df_teacher.kaynak == kaynak) & (df_teacher.odev_veren == "MUSTAFA TEKİN") & (df_teacher.sinav == sinav)].kalan_soru_sayisi.sum()
        o_tyt_soru_sayisi = df_teacher.loc[(df_teacher.kaynak == kaynak) & (df_teacher.odev_veren == "OKUL ÖĞRETMENİ") & (df_teacher.sinav == sinav)].soru_sayisi.sum()
        o_tyt_cozulen_soru_sayisi = df_teacher.loc[(df_teacher.kaynak == kaynak) & (df_teacher.odev_veren == "OKUL ÖĞRETMENİ") & (df_teacher.sinav == sinav)].cozulen_soru_sayisi.sum()
        o_tyt_kalan_soru_sayisi = df_teacher.loc[(df_teacher.kaynak == kaynak) & (df_teacher.odev_veren == "OKUL ÖĞRETMENİ") & (df_teacher.sinav == sinav)].kalan_soru_sayisi.sum()
        n_tyt_soru_sayisi = df_teacher.loc[(df_teacher.kaynak == kaynak) & (df_teacher.odev_veren == "ÖDEV HARİCİ ÇALIŞMA") & (df_teacher.sinav == sinav)].soru_sayisi.sum()
        n_tyt_cozulen_soru_sayisi = df_teacher.loc[(df_teacher.kaynak == kaynak) & (df_teacher.odev_veren == "ÖDEV HARİCİ ÇALIŞMA") & (df_teacher.sinav == sinav)].cozulen_soru_sayisi.sum()
        n_tyt_kalan_soru_sayisi = df_teacher.loc[(df_teacher.kaynak == kaynak) & (df_teacher.odev_veren == "ÖDEV HARİCİ ÇALIŞMA") & (df_teacher.sinav == sinav)].kalan_soru_sayisi.sum()
        t_tyt_soru_sayisi = df_teacher.loc[(df_teacher.kaynak == kaynak) & (df_teacher.sinav == sinav)].soru_sayisi.sum()
        t_tyt_cozulen_soru_sayisi = df_teacher.loc[(df_teacher.kaynak == kaynak) & (df_teacher.sinav == sinav)].cozulen_soru_sayisi.sum()
        t_tyt_kalan_soru_sayisi = df_teacher.loc[(df_teacher.kaynak == kaynak) & (df_teacher.sinav == sinav)].kalan_soru_sayisi.sum()
        return [m_tyt_soru_sayisi, m_tyt_cozulen_soru_sayisi, m_tyt_kalan_soru_sayisi, o_tyt_soru_sayisi,
                o_tyt_cozulen_soru_sayisi, o_tyt_kalan_soru_sayisi, n_tyt_soru_sayisi,
                n_tyt_cozulen_soru_sayisi, n_tyt_kalan_soru_sayisi, t_tyt_soru_sayisi, t_tyt_cozulen_soru_sayisi,
                t_tyt_kalan_soru_sayisi]
    elif (ders == 'Tümü' and kaynak == 'Tümü' and konu != 'Tümü') or (ders != 'Tümü' and kaynak == 'Tümü' and konu != 'Tümü'):
        m_tyt_soru_sayisi = df_teacher.loc[(df_teacher.konu == konu) & (df_teacher.odev_veren == "MUSTAFA TEKİN") & (df_teacher.sinav == sinav)].soru_sayisi.sum()
        m_tyt_cozulen_soru_sayisi = df_teacher.loc[(df_teacher.konu == konu) & (df_teacher.odev_veren == "MUSTAFA TEKİN") & (df_teacher.sinav == sinav)].cozulen_soru_sayisi.sum()
        m_tyt_kalan_soru_sayisi = df_teacher.loc[(df_teacher.konu == konu) & (df_teacher.odev_veren == "MUSTAFA TEKİN") & (df_teacher.sinav == sinav)].kalan_soru_sayisi.sum()
        o_tyt_soru_sayisi = df_teacher.loc[(df_teacher.konu == konu) & (df_teacher.odev_veren == "OKUL ÖĞRETMENİ") & (df_teacher.sinav == sinav)].soru_sayisi.sum()
        o_tyt_cozulen_soru_sayisi = df_teacher.loc[(df_teacher.konu == konu) & (df_teacher.odev_veren == "OKUL ÖĞRETMENİ") & (df_teacher.sinav == sinav)].cozulen_soru_sayisi.sum()
        o_tyt_kalan_soru_sayisi = df_teacher.loc[(df_teacher.konu == konu) & (df_teacher.odev_veren == "OKUL ÖĞRETMENİ") & (df_teacher.sinav == sinav)].kalan_soru_sayisi.sum()
        n_tyt_soru_sayisi = df_teacher.loc[(df_teacher.konu == konu) & (df_teacher.odev_veren == "ÖDEV HARİCİ ÇALIŞMA") & (df_teacher.sinav == sinav)].soru_sayisi.sum()
        n_tyt_cozulen_soru_sayisi = df_teacher.loc[(df_teacher.konu == konu) & (df_teacher.odev_veren == "ÖDEV HARİCİ ÇALIŞMA") & (df_teacher.sinav == sinav)].cozulen_soru_sayisi.sum()
        n_tyt_kalan_soru_sayisi = df_teacher.loc[(df_teacher.konu == konu) & (df_teacher.odev_veren == "ÖDEV HARİCİ ÇALIŞMA") & (df_teacher.sinav == sinav)].kalan_soru_sayisi.sum()
        t_tyt_soru_sayisi = df_teacher.loc[(df_teacher.konu == konu) & (df_teacher.sinav == sinav)].soru_sayisi.sum()
        t_tyt_cozulen_soru_sayisi = df_teacher.loc[(df_teacher.konu == konu) & (df_teacher.sinav == sinav)].cozulen_soru_sayisi.sum()
        t_tyt_kalan_soru_sayisi = df_teacher.loc[(df_teacher.konu == konu) & (df_teacher.sinav == sinav)].kalan_soru_sayisi.sum()
        return [m_tyt_soru_sayisi, m_tyt_cozulen_soru_sayisi, m_tyt_kalan_soru_sayisi, o_tyt_soru_sayisi,
                o_tyt_cozulen_soru_sayisi, o_tyt_kalan_soru_sayisi, n_tyt_soru_sayisi,
                n_tyt_cozulen_soru_sayisi, n_tyt_kalan_soru_sayisi, t_tyt_soru_sayisi, t_tyt_cozulen_soru_sayisi,
                t_tyt_kalan_soru_sayisi]
    elif (ders == 'Tümü' and kaynak != 'Tümü' and konu != 'Tümü'):
        m_tyt_soru_sayisi = df_teacher.loc[(df_teacher.kaynak == kaynak) & (df_teacher.konu == konu) & (df_teacher.odev_veren == "MUSTAFA TEKİN") & (df_teacher.sinav == sinav)].soru_sayisi.sum()
        m_tyt_cozulen_soru_sayisi = df_teacher.loc[(df_teacher.kaynak == kaynak) & (df_teacher.konu == konu) & (df_teacher.odev_veren == "MUSTAFA TEKİN") & (df_teacher.sinav == sinav)].cozulen_soru_sayisi.sum()
        m_tyt_kalan_soru_sayisi = df_teacher.loc[(df_teacher.kaynak == kaynak) & (df_teacher.konu == konu) & (df_teacher.odev_veren == "MUSTAFA TEKİN") & (df_teacher.sinav == sinav)].kalan_soru_sayisi.sum()
        o_tyt_soru_sayisi = df_teacher.loc[(df_teacher.kaynak == kaynak) & (df_teacher.konu == konu) & (df_teacher.odev_veren == "OKUL ÖĞRETMENİ") & (df_teacher.sinav == sinav)].soru_sayisi.sum()
        o_tyt_cozulen_soru_sayisi = df_teacher.loc[(df_teacher.kaynak == kaynak) & (df_teacher.konu == konu) & (df_teacher.odev_veren == "OKUL ÖĞRETMENİ") & (df_teacher.sinav == sinav)].cozulen_soru_sayisi.sum()
        o_tyt_kalan_soru_sayisi = df_teacher.loc[(df_teacher.kaynak == kaynak) & (df_teacher.konu == konu) & (df_teacher.odev_veren == "OKUL ÖĞRETMENİ") & (df_teacher.sinav == sinav)].kalan_soru_sayisi.sum()
        n_tyt_soru_sayisi = df_teacher.loc[(df_teacher.kaynak == kaynak) & (df_teacher.konu == konu) & (df_teacher.odev_veren == "ÖDEV HARİCİ ÇALIŞMA") & (df_teacher.sinav == sinav)].soru_sayisi.sum()
        n_tyt_cozulen_soru_sayisi = df_teacher.loc[(df_teacher.kaynak == kaynak) & (df_teacher.konu == konu) & (df_teacher.odev_veren == "ÖDEV HARİCİ ÇALIŞMA") & (df_teacher.sinav == sinav)].cozulen_soru_sayisi.sum()
        n_tyt_kalan_soru_sayisi = df_teacher.loc[(df_teacher.kaynak == kaynak) & (df_teacher.konu == konu) & (df_teacher.odev_veren == "ÖDEV HARİCİ ÇALIŞMA") & (df_teacher.sinav == sinav)].kalan_soru_sayisi.sum()
        t_tyt_soru_sayisi = df_teacher.loc[(df_teacher.kaynak == kaynak) & (df_teacher.konu == konu) & (df_teacher.sinav == sinav)].soru_sayisi.sum()
        t_tyt_cozulen_soru_sayisi = df_teacher.loc[(df_teacher.kaynak == kaynak) & (df_teacher.konu == konu) & (df_teacher.sinav == sinav)].cozulen_soru_sayisi.sum()
        t_tyt_kalan_soru_sayisi = df_teacher.loc[(df_teacher.kaynak == kaynak) & (df_teacher.konu == konu) & (df_teacher.sinav == sinav)].kalan_soru_sayisi.sum()
        return [m_tyt_soru_sayisi, m_tyt_cozulen_soru_sayisi, m_tyt_kalan_soru_sayisi, o_tyt_soru_sayisi,
                o_tyt_cozulen_soru_sayisi, o_tyt_kalan_soru_sayisi, n_tyt_soru_sayisi,
                n_tyt_cozulen_soru_sayisi, n_tyt_kalan_soru_sayisi, t_tyt_soru_sayisi, t_tyt_cozulen_soru_sayisi,
                t_tyt_kalan_soru_sayisi]
    else:
        print('oops')


# veritabanı oluştur ve tabloları olustur
database = r"Nisan_Data.db"
the_conn = create_dbconnection(database)
if the_conn is not None:
    sql_for_create_teacher_table = """ CREATE TABLE IF NOT EXISTS teacher_table(
                                        id integer PRIMARY KEY,
                                        sinav text NOT NULL,
                                        tarih text NOT NULL,
                                        ders text NOT NULL,
                                        odev_veren text NOT NULL,
                                        konu text NOT NULL,
                                        kaynak text NOT NULL,
                                        sayfa text NOT NULL,
                                        sorular text NOT NULL,
                                        soru_sayisi integer NOT NULL,
                                        cozulen_sorular text NULL,
                                        cozulen_soru_sayisi integer NULL,
                                        kalan_sorular text NULL,
                                        kalan_soru_sayisi integer NULL,
                                        degerlendirme text NULL,
                                        Aciklama text NULL
                                    ); """
    create_konu_table_sql = """ CREATE TABLE IF NOT EXISTS konutable(
                                            id integer PRIMARY KEY,
                                            sinav text NOT NULL,
                                            ders text NOT NULL,
                                            unite text NOT NULL,
                                            konu text NOT NULL
                                        ); """
    create_users_table_sql = """ CREATE TABLE IF NOT EXISTS users(
                                            id integer PRIMARY KEY,
                                            key text NOT NULL,
                                            name text NOT NULL,
                                            password text NOT NULL
                                        ); """

    create_table(the_conn, sql_for_create_teacher_table)
    create_table(the_conn, create_konu_table_sql)
    create_table(the_conn, create_users_table_sql)
    print('Tablolar başarılı')
else:
    print("Hata! veritabani baglantisi kurulamiyor.Tablolar Oluşturulamadı.")


df_teacher = pd.read_sql_query("SELECT * from teacher_table", the_conn)
df_konu = pd.read_sql_query("SELECT * from konutable", the_conn)

# --- USER AUTHENTICATION ---
# names = ["Mustafa Tekin", "Nisan Aydöner"]
# usernames = ["mtekin", "naydoner"]
# passwords = ['Mtekin123..', 'Naydoner123..']
# hashed_passwords = stauth.Hasher(passwords=passwords).generate()

# for (name, user, hash_password) in zip(names, usernames, hashed_passwords):
#     insert_user(the_conn=the_conn, kayit=(user, name, hash_password))

