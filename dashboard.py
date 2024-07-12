import streamlit as st, pandas as pd, numpy as np, yfinance as yf
import plotly.express as px

st.title('Stock Dashboard')
ticker = st.sidebar.text_input('Ticker')
start_date = st.sidebar.date_input('Start Date')
end_date = st.sidebar.date_input('End Date')

if ticker:

    print("Ticker is found")

    # download ticker stock data from yahoo finance for the date range specified
    data = yf.download(ticker, start=start_date, end=end_date)

    # plot stock data using plotly

    fig = px.line(data, x = data.index, y = data['Adj Close'], title = ticker)
    # fig = px.line(data, title = ticker)
    st.plotly_chart(fig)

    # create 3 tabs: Pricing Data, Fundamental Data, and Top 10 News

    pricing_data, fundamental_data, news = st.tabs(["Pricing Data", "Fundamental Data", "Top 10 News"])


    ################################################################
    ### Pricing Tab

    with pricing_data:
        st.header('Price Movements')
        
        # get daily change 

        data2 = data
        data2['% Change'] = data['Adj Close'] / data['Adj Close'].shift(1) -1
        data2.dropna(inplace= True)  # drop row that has NA value (1st row as there is no data for the day before it)
        st.write(data2)

        # Annual return

        annual_return = data2['% Change'].mean()*252*100
        st.write('Annual Return: ', annual_return, "%")
        stdev = np.std(data2['% Change'])*np.sqrt(252)
        st.write('Standard Deviation: ', stdev*100, "%")


    ################################################################
    ### alpha vantage api to show fundamental data tab

    from alpha_vantage.fundamentaldata import FundamentalData

    with fundamental_data:

        # generat alpha vantage key

        key = '4OPXPEKDVIHWNE1F'

        # get fundamental data from alpha vantage in pandas format

        fd = FundamentalData(key, output_format = 'pandas')

        # get balance sheet annual return

        st.subheader('Balance Sheet')
        balance_sheet = fd.get_balance_sheet_annual(ticker)[0]
        bs = balance_sheet.T[2:]
        bs.columns = list(balance_sheet.T.iloc[0])
        st.write(bs)

        # get income statement annual return

        st.subheader('Income Statement')
        income_statement = fd.get_income_statement_annual(ticker)[0]
        is1 = income_statement.T[2:]
        is1.columns = list(income_statement.T.iloc[0])
        st.write(is1)

        # get cash flow statement annual return
        st.subheader('Cash Flow Statement')
        cash_flow = fd.get_cash_flow_annual(ticker)[0]
        cf = cash_flow.T[2:]
        cf.columns = list(cash_flow.T.iloc[0])
        st.write(cf)


    ################################################################
    ### stocknews to retrieve the latest 10 stock news 

    from stocknews import StockNews

    with news:
        st.header(f'News of {ticker}')
        sn = StockNews(ticker, save_news=False)
        df_news = sn.read_rss()
        for i in range(10):
            st.subheader(f'{i+1})', df_news['title'][i])
            st.write(df_news['published'][i])
            st.write()
            st.write(df_news['summary'][i])
            title_sentiment = df_news['sentiment_title'][i]
            st.write(f'Title Sentiment {title_sentiment}')
            news_sentiment = df_news['sentiment_summary'][i]
            st.write(f'News Sentiment {news_sentiment}')