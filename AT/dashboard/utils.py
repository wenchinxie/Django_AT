from pandas.tseries.offsets import BDay
import pandas as pd
import pandas_datareader as pdr
import sqlite3
from dateutil import parser
import datetime
from sqlalchemy import create_engine,engine,Table,text

def get_mysql_conn() -> engine.base.Connection:

    address = "mysql+pymysql://root:test@localhost:3306/django"
    engine = create_engine(address)
    connect = engine.connect()
    return connect

class update_data:
    def __init__(self,data):

        if data=="Currencies":
            self.symbol_list=['DX-Y.NYB']
            self.symbol_name=['美元指數']

        self.conn = get_mysql_conn()
        self.data=data
        self.chartdiv=''

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self,value):
        '''
        If the database has not been updated, then execute update and return renewed data
        '''

        for row in self.conn.execute(text(f'SELECT * FROM {value} ORDER BY Date DESC LIMIT 1;')):
            recent_date = parser.parse(str(row['Date']))

        lastest_bday=datetime.datetime.today()-BDay(1)
        if recent_date.date()!= lastest_bday.date() :
            renew_data=self.update(recent_date)
            renew_data.to_sql(value,self.conn, if_exists='append',index=False)

        df = pd.read_sql(f'SELECT Date,Material_name,Price FROM {value}', self.conn, parse_dates='Date')
        df_table = self.table_calculation(df)
        self.conn.execute(f"Replace INTO {value}_table (Product, Date , Price, Day, Week, Month, Quarter,Year) VALUES (%s,%s,%s,%s,%s,%s,%s,%s) ",
                          tuple(df_table.iloc[0, :].values))

    def update(self,start_time):
        '''
        Only support the pandas datareader, use scrapy to fetch other data instead of datareader
        '''
        renew_data=pd.DataFrame()
        for i,symbol in enumerate(self.symbol_list):
            downloaded = pdr.DataReader(symbol, 'yahoo', start=start_time)
            downloaded=downloaded.reset_index()
            downloaded['Material_name']=self.symbol_name[i]
            downloaded['Price']=downloaded['Close']
            downloaded=downloaded[['Date','Material_name','Price']]
            downloaded['Date']=downloaded['Date'].dt.strftime('%Y-%m-%d')
            renew_data=pd.concat([renew_data,downloaded])

        return renew_data

    def table_calculation(self,df):
        '''
        Return the table data
        '''
        data = df.reset_index().drop_duplicates(subset='Date').set_index('Date')
        data=data.resample('D').ffill().sort_values('Date', ascending=False).reset_index().drop('index', axis=1)

        colname = ['Day', 'Week', 'Month', 'Quarter', 'Year']
        period = [1, 1,1, 3, 12]

        for i, n in enumerate(colname):
            if n == 'Day':
                price_b = data[data['Date'] == (data['Date'][0] - pd.DateOffset(days=1))]['Price'].values[0]
            elif n == 'Week':
                price_b = data[data['Date'] == (data['Date'][0] - pd.DateOffset(weeks=1))]['Price'].values[0]
            else:
                price_b = data[data['Date'] == (data['Date'][0] - pd.DateOffset(months=period[i]))]['Price'].values[0]

            data[n] = ''
            data[n][0] = str(round((data['Price'][0] / price_b - 1) * 100, 2)) + "%"

        data = data.head(1)
        data = data[['Material_name', 'Date', 'Price', 'Day', 'Week', 'Month', 'Quarter', 'Year']]
        data['Date']=data['Date'].astype(str)

        return data
