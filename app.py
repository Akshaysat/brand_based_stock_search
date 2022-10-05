import json
import requests
import pandas as pd
import streamlit as st
import time

#set today's date and time
curr_time_dec = time.localtime(time.time())
date = time.strftime("%Y-%m-%d", curr_time_dec)

hide_table_row_index = """
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            </style>
            """

st.title("Search for stocks by famous brands")

brand_name = st.text_input("Enter the name of the brand:")

if st.button("Find Stock"):

    url = "https://ticker.finology.in/GetSearchData.ashx?q=" + brand_name

    payload={}
    headers = {
    'authority': 'ticker.finology.in',
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'en-US,en;q=0.7',
    'cookie': 'ASP.NET_SessionId=4lnkkwsro2rjje0bpkakbsgt; _fbp=fb.1.1664988675876.299203111',
    'referer': 'https://ticker.finology.in/',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sec-gpc': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest'
    }

    try:
        response = requests.request("GET", url, headers=headers, data=payload)
        data = json.loads(response.text)

        df = pd.DataFrame(data)
        df.rename(columns = {'compname':'Company Name','SYMBOL':'Symbol','brands':'Famous Brands'}, inplace = True)
        st.markdown(hide_table_row_index, unsafe_allow_html=True)
        st.table(df[['Company Name','Symbol']])
        
        #store data in database
        url_email = "https://3749e8lxlf.execute-api.ap-south-1.amazonaws.com/"
        payload_email = {"query_date" : date, "tool_name" : "tool-brand-based-stock-search", "Brand Name":brand_name, "status": "Success"}
        headers_email = {'Content-Type': 'text/plain'}
        response = requests.request("POST", url_email, headers=headers_email, data = json.dumps(payload_email))

    except:
        st.error("Sorry, we couldn't find that brand")
        
        #store data in database
        url_email = "https://3749e8lxlf.execute-api.ap-south-1.amazonaws.com/"
        payload_email = {"query_date" : date, "tool_name" : "tool-brand-based-stock-search", "Brand Name":brand_name, "status": "Failure"}
        headers_email = {'Content-Type': 'text/plain'}
        response = requests.request("POST", url_email, headers=headers_email, data = json.dumps(payload_email))


