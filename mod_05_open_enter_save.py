from mod_01_enter_open import enter_url
from mod_02_scrap import news_scrap_full
from mod_01_os import open_csv
from mod_01_enter_open import urls_to_list
import pandas as pd


def open_enter_save():
    df = open_csv("/Users/tazgal/DIGITAL_HUMANITITES/ΨΑΕ_πτυχιακή_όλα/news_data_01.csv")
    url = enter_url()
    line = news_scrap_full(url)
    df.loc[len(df)] = line 
    print(df.tail())
    df.to_csv("/Users/tazgal/DIGITAL_HUMANITITES/ΨΑΕ_πτυχιακή_όλα/news_data_01.csv", index = False)

def open_enter_save_url(url):
    df = open_csv("/Users/tazgal/DIGITAL_HUMANITITES/ΨΑΕ_πτυχιακή_όλα/news_data_01.csv")
    line = news_scrap_full(url)
    df.loc[len(df)] = line 
    print(df.tail())
    df.to_csv("/Users/tazgal/DIGITAL_HUMANITITES/ΨΑΕ_πτυχιακή_όλα/news_data_01.csv", index = False)


def open_enter_save_multiple_urls(text):
    list_urls = urls_to_list(text)
    for l in list_urls:
        url = l
        open_enter_save_url(url)

def open_enter_save_list_urls(list):
    for l in list:
        url = l
        open_enter_save_url(url)