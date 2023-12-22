import numpy as np
import datetime as dt
import os
import pandas as pd
import tushare as ts

from tqdm import tqdm

class TushareData:
    """通过tushare接口下载K线、筹码数据"""
    dirpath = "data"
    start = '20100101'

    def __init__(self):
        ts.set_token(
            '7eb4bc05a48bb2704d76c1b79c501053b58ad1b190b505faa9009d5c'
            )
        self.pro = ts.pro_api()
        stocklist = self.pro.stock_basic(exchange='',
                                         list_status='L',
                                         fields='ts_code')
        self.stocklist = stocklist['ts_code'].values


    def daily_kdatafeed(self, stockcode: str, freq: str='D'):
        """获取指定股票的日线数据"""
        end = dt.datetime.now().strftime('%Y%m%d')
        try:
            kdata: pd.DataFrame = ts.pro_bar(
                ts_code=stockcode,
                start_date=self.start,
                end_date=end)
        except Exception as e:
            print(e)
            return None
        if len(kdata) < 10:
            return None
        return kdata.drop('ts_code', axis=1)


    def daily_cyqdatafeed(self, stockcode: str):
        """获取指定股票的筹码分布数据"""
        end = dt.datetime.now().strftime('%Y%m%d')
        try:
            cyqdata: pd.DataFrame = self.pro.cyq_perf(
                ts_code=stockcode,
                start_date=self.start,
                end_date=end)
        except Exception as e:
            print(e)
            return None
        if len(cyqdata) < 10:
            return None
        return cyqdata.drop('ts_code', axis=1)

    def download_tushredata(self):
        """下载Akshare K线、筹码分布数据"""
        end = dt.datetime.now().strftime('%Y%m%d')
        for stockcode in tqdm(self.stocklist, position=0, desc='下载K线、筹码分布数据'):
            """获取每只股票的K线数据和筹码分布"""
            stock = stockcode[:5]
            kdata: pd.DataFrame = self.daily_kdatafeed(stockcode)
            cyqdata: pd.DataFrame = self.daily_cyqdatafeed(stockcode)
            if kdata is None or cyqdata is None:
                continue
            if len(kdata) < 10 or len(cyqdata) < 10:
                continue
            cyqdata = cyqdata.round(2)
            data: pd.DataFrame = pd.merge(
                kdata,
                cyqdata, on='trade_date'
                )
            filepath = self.dirpath + "/" + stockcode + ".csv"
            if os.path.exists(filepath):
                os.remove(filepath)
            data.to_csv(filepath, index=False)


if __name__ == '__main__':
    td = TushareData()
    td.download_tushredata()