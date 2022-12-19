from pandas.tseries.offsets import BDay
import yfinance as yf
import pandas as pd
from pandas_datareader import data as pdr
from dateutil import parser
import datetime
from sqlalchemy import create_engine,engine,Table,text
import numpy as np

class update_data:
    def __init__(self,data_type):

        if data_type=="Currencies":
            self.symbol_list=['DX-Y.NYB']
            self.symbol_name=['美元指數']
        self.data_type=data_type
        self.conn = self.get_mysql_conn()
        self.data=None
        self.chartdiv=''

    @property
    def data(self):
        """
        Get the data stored in the DataStore object.
        """
        return self.__data

    @data.setter
    def data(self,_):
        """
        Update the data stored in the DataStore object, if the database has not been updated.
        """
        self.update_data_if_needed()
        df = pd.read_sql(f"SELECT Date,Material_name,Price FROM {self.data_type}", self.conn, parse_dates='Date')

        # Calculate the table data
        df_table = self.table_calculation(df)

        # Update the data in the table
        values = tuple(df_table.iloc[0, :].values)
        self.conn.execute(
            f"REPLACE INTO {self.data_type}_table (Product, Date , Price, Day, Week, Month, Quarter,Year) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
            values)

        # Update the __data attribute with the updated data
        self.__data = df

    def update_data_if_needed(self):
        """Update the data in the database if it is out of date."""
        try:
            #If the database has no data
            cursor = self.conn.execute(text(f"SELECT * FROM {self.data_type} ORDER BY Date DESC LIMIT 1;"))
            row = cursor.fetchone()
            recent_date = parser.parse(str(row['Date']))
        except:
            # Then make a fake data
            recent_date=  datetime.datetime(2021, 1, 1, 0, 0)

        lastest_bday = datetime.datetime.today() - BDay(1)
        if recent_date.date() != lastest_bday.date():
            renew_data = self.fetch_updated_data(recent_date)
            renew_data.to_sql(self.data_type, self.conn, if_exists='append', index=False)

    def fetch_updated_data(self,start_time):
        '''
        Update the data in the database if it is out of date.
        Only support the pandas datareader, use scrapy to fetch other data instead of datareader
        '''
        renew_data=pd.DataFrame()
        yf.pdr_override()
        print(start_time)
        for i,symbol in enumerate(self.symbol_list):
            downloaded = pdr.get_data_yahoo(symbol, start=start_time)
            downloaded=downloaded.reset_index()
            downloaded['Material_name']=self.symbol_name[i]
            downloaded['Price']=downloaded['Close']
            downloaded=downloaded[['Date','Material_name','Price']]
            downloaded['Date']=downloaded['Date'].dt.strftime('%Y-%m-%d')
            renew_data=pd.concat([renew_data,downloaded])

        return renew_data

    def table_calculation(self,df):
        """
        Return the table data.

        Parameters:
        - df: a Pandas DataFrame containing the data to be processed.

        Returns:
        - a Pandas DataFrame containing the processed data.
        """

        # Reset the index and drop duplicates
        data = df.reset_index().drop_duplicates(subset='Date').set_index('Date')

        # Resample the data to daily intervals and forward-fill missing values
        data=data.resample('D').ffill().sort_values('Date', ascending=False).reset_index().drop('index', axis=1)

        # Define the period mapping
        period_mapping = {'Day': {'days':1}, 'Week': {'weeks':1}, 'Month': {'months':1}, 'Quarter': {'months':3}, 'Year': {'months':12}}

        # Initialize the new columns with NaN values
        for col in period_mapping.keys():
            data[col] = np.nan

        def calc_percent_change(period):
            """
            Calculate the percentage change between the latest date and the previous date in the specified period.

            Parameters:
            - period: a string specifying the period ("Day", "Week", "Month", "Quarter", or "Year").

            Returns:
            - a string representation of the percentage change.
            """
            price_prev = data[data['Date'] == (data['Date'][0] - pd.DateOffset(**period_mapping[period]))]['Price'].values[0]
            change = (data['Price'][0] / price_prev - 1) * 100
            return f"{round(change, 2)}%"

        # Calculate the percentage change for each period
        for period in period_mapping.keys():
            data[period][0]= calc_percent_change(period)

        data = data.head(1)
        data = data[['Material_name', 'Date', 'Price', 'Day', 'Week', 'Month', 'Quarter', 'Year']]
        data['Date']=data['Date'].astype(str)

        return data

    def get_mysql_conn(self) -> engine.base.Connection:

        user='root'
        password='test'
        host='localhost'
        ports='3306'
        db='django'

        address = f"mysql+pymysql://{user}:{password}@{host}:{ports}/{db}"
        engine = create_engine(address)
        connect = engine.connect()
        return connect