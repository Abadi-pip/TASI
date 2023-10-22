import numpy as np
import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
import datetime as dt
import plotly.express as px
import yfinance as yf
import time
import More, Information

# ====== PAGE VAR & CONFIG ==========
page_title = "Stock Analysis Selector"
Page_icon = '📈'
layout = 'centered'
initial_sidebar_state= "auto"
# ====== PAGE CONFIG CODE ===========

st.set_page_config(layout = layout ,initial_sidebar_state = initial_sidebar_state, page_title = page_title ,  page_icon= Page_icon)
st.image("logo.png")
st.title(page_title+" "+Page_icon)
#======= DATE & TIME HEADER =========
date = dt.datetime.now().strftime('TODAY\'S DATE : [%d-%m-%y]   TIME :[ %H:%M]')
st.write(date)

"---"
#========================= DICTIONARY OF STOCK & TICKERS ================================
stock_names = {
            
            'المؤشر العام':'^TASI.SR',
            'ســـــابك':'2020.SR',
            'دار الاركان':'4300.SR',
            'سييرا القابضة':'1810.SR',
            'الاتصالات':'7010.SR',
            'الراجحي':'1120.SR',
            'شركة المراعي':'2280.SR',
            'البنك العربي الوطني':'1180.SR',
            'اللجين':'2170.SR',
            'البنك السعودي الاول':'1060.SR'
               }

# ======================== VARIABLE TO ADD DROPDOWN =====================================
my_stock = {key:val for (key, val) in stock_names.items()}

# ========================= CODES FOR WIDJETS ===========================================
drop = st.selectbox('أختر السهم', my_stock )
start = st.date_input('بداية المدة : اختر التاريخ', value = pd.to_datetime('2023-08-31')) #THIS STARŢ DATE AS DEFAULT COULD BE CHANGED
end = st.date_input('نهاية المدة : اختر التاريخ', value = pd.to_datetime('today'))
#========================== CODING TO APP ===============================================


if len(drop) >0:
    #========= LOADING BAR =======================
    txt = "...انتظر قليـــلا"
    my_bar = st.progress(0 , text = txt)
    #========== FOR LOOP---LOADING BAR ===========
    for pr in range(100):
        tm = time.sleep(0.01)
        my_bar.progress(pr + 1 , text = txt)
    time.sleep(1)
    my_bar.empty()
    #=======  OPERATION CODE =====================
    y =yf.download(my_stock[f'{drop}'],start,end)
    if st.checkbox(f' اظهر البيانات لـ: {drop}'):                   #=== CHECK BOX TO SHOW THE DATA =====
        with st.form(f'Data {drop}'):                             
            st.table(y.drop(['Adj Close', 'Volume'], axis=1))
            if st.form_submit_button("Export to Excel"):
                y.to_excel(f"C:\\Users\\Abdullah\\Desktop\\Tasi Data\\TasiStock-{drop}.xlsx")
                st.success(" تم تصدير البيانات تم بنجاح✅ انظر سطح المكتب")
    #======  CLOSING PRICE OUTPUT ===============
    R =  y['Close'].iloc[-1]
    R = round(R, 2)
    col1, col2 = st.columns(2)
    with col1: 
        st.info(f'{R}')
    with col2: 
        st.info(f'آخر سعر اغلاق لـ {drop}')
    #======  PLOTING THE CHART ==================
    plot_chart = y.drop(['Adj Close', 'Volume'], axis=1)
    st.subheader(f'  الرسم البياني لــ: {drop}' )
    st.write(px.line(plot_chart)) #===== PLOTING THE CHART =========== WIDTH RECONFIGURED TO SUITS MOBILE AAPS
    
def run():
    app = option_menu(
        menu_title= f"المعلومات الاضافية لـ: {drop}",
        options = [ 'التوزيعات النقدية' , 'معلومات الشركة'],
        icons=['bar-chart', 'bar-chart-fill'],
        menu_icon= None,
        default_index=0,
        orientation='horizontal'
        
    )

    if app== 'التوزيعات النقدية':
        
        Information.app()
        if drop != 'المؤشر العام' :
            ticker = yf.Ticker(my_stock[f'{drop}'])
            Dividends = ticker.dividends 
            st.table(ticker.dividends)
            st.write(px.bar(Dividends, title=f'الرسم البياني للـتوزيعات النقدية لـ: {drop}'))
        elif drop == 'المؤشر العام' :
            st.info("اختر الشركة من القائمة الاسهم")

    if app== 'معلومات الشركة' :

        More.app()
        ticker = yf.Ticker(my_stock[f'{drop}'])
        if drop != 'المؤشر العام' :
            st.write(ticker.info)
        elif drop == 'المؤشر العام' :
            st.info("اختر الشركة من القائمة الاسهم")
run()

#App deployed with streamlit you can run link:
# https://abadi-pip-tasi-main-xq5hyj.streamlit.app/

# [theme]
# base="dark"
# backgroundColor="#7e95b7"
# secondaryBackgroundColor="#555d81"
