import pandas as pd
import requests
from bs4 import BeautifulSoup
from typing import List, Dict
import re
import numpy as np
from datetime import datetime




# functions
def handle_index_error(data: List, index: int):
    if len(data) <= index:
        return np.NaN
    else:
        return data[index]


def fetch_earthquake_data(link: str, parser="html.parser"):
    """
    Fetch parsed HTML for given link
    :param link: website address
    :return: parsed HTML
    """
    # use fake User-Agent to deal 403 Forbidden
    headers: Dict[str, str] = {
        'User-Agent':
            'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'
    }
    # get page content in HTML form
    page_content = requests.get(link, headers=headers).content
    soup_obj = BeautifulSoup(page_content, parser)
    # get table data
    data = soup_obj.find("pre").text[586:]
    return data


def text_cleanup(text: str)->pd.DataFrame:
    """
    Clean up fetched data to be able put in df format
    :param text: fetched data
    :return: formatted df
    """
    text_df: List[str] = []
    # convert to list by \n
    lines: List[str] = text.split("\n")
    for line in lines:
        # replace single space with underscore
        line = re.sub(r'(?<=\S)\s(?=\S)', '_', line)
        # replace multiple space with single space
        fixed_line = " ".join(line.split())
        fixed_line = fixed_line.split()
        text_df.append({
            "Tarih - Saat": handle_index_error(data=fixed_line, index=0),
            "Enlem(N)": handle_index_error(data=fixed_line, index=1),
            "Boylam(E)": handle_index_error(data=fixed_line, index=2),
            "Derinlik(km)": handle_index_error(data=fixed_line, index=3),
            "MD": handle_index_error(data=fixed_line, index=4),
            "ML": handle_index_error(data=fixed_line, index=5),
            "MW": handle_index_error(data=fixed_line, index=6),
            "Lokasyon": handle_index_error(data=fixed_line, index=7),
            "Çözüm Niteliği": handle_index_error(data=fixed_line, index=8),
            "Son Durum": handle_index_error(data=fixed_line, index=9),
        })
    text_df = pd.DataFrame(text_df)
    text_df['Tarih - Saat'] = pd.to_datetime(text_df['Tarih - Saat'], format='%Y.%m.%d_%H:%M:%S')
    text_df['date'] = text_df['Tarih - Saat'].dt.strftime('%d.%m.%Y')
    text_df['time'] = text_df['Tarih - Saat'].dt.strftime('%H:%M:%S')
    text_df.rename(columns={'Tarih - Saat': 'Tarih-Saat', 'Enlem(N)': 'Enlem', 'Boylam(E)': 'Boylam', 'Derinlik(km)':'Derinlik'}, inplace=True)
    text_df.drop(columns=['Tarih-Saat','Çözüm Niteliği'], inplace=True)
    
    

    text_df['sehir'] = text_df['Lokasyon'].str.extract('\((.*?)\)', expand=True)
    text_df['Lokasyon'] = (text_df['Lokasyon'].str.replace('\(.*\)', '')).str[:-1]
        # drop if all columns is NaN
    text_df.dropna(subset=[
       
        "Enlem", "Boylam", "Derinlik", "MD", "ML",
        "MW", "Lokasyon", "Lokasyon", "Son Durum"
    ],
                   how='all',
                   inplace=True)
    return text_df.to_json(orient='records')

if __name__ == '__main__':
    print("Directly processed")