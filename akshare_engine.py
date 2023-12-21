import akshare as ak
import time
import numpy as np
import datetime as dt
import os
import pandas as pd

from tqdm import tqdm

class AkshareData:
    """通过akshare接口下载K线数据"""
    dirpath = "data"
    start = '20100101'

    def __init__(self):
        stockcode_sh = ak.stock_sh_a_spot_em()
        shStockList = stockcode_sh['代码']
        stockcode_sz = ak.stock_sz_a_spot_em()
        szStockList = stockcode_sz['代码']
        self.stockList = np.concatenate(
            (
                shStockList.apply(lambda x, prefix: prefix + x, prefix='sh.'),
                szStockList.apply(lambda x, prefix: prefix + x, prefix='sz.')
            )
        )


    def daily_kdatafeed(self, stockcode: str):
        """获取指定股票的日线数据"""
        end = dt.datetime.now().strftime('%Y%m%d')
        try:
            kdata = ak.stock_zh_a_hist(
                symbol=stockcode,
                period="daily",
                start_date=self.start,
                end_date=end
                )
        except Exception as e:
            print(e)
            return None
        if len(kdata) < 10:
            return None
        colums = [
            'datetime',
            'open',
            'close',
            'high',
            'low',
            'volume',
            'turnover',
            'amplitude',
            'pricelimit',
            'change',
            'turnoverratio'
            ]
        kdata.columns = colums
        kdata = kdata[colums]
        return kdata


    def daily_cyqdatafeed(self, stockcode: str):
        """获取指定股票的筹码分布数据"""
        cyqdata: pd.DataFrame = pd.DataFrame()
        try:
            cyqdata = ak.stock_cyq_em(
                symbol=stockcode,
                adjust=""
                )
        except Exception as e:
            print(e)
            return None
        if len(cyqdata) < 10:
            return None
        colums = [
            'datetime',
            'takeprofitratio',
            'averagecost',
            'ratio90low',
            'raio90high',
            'concentration90',
            'raio70low',
            'raio70high',
            'concentration70'
            ]
        cyqdata.columns = colums
        cyqdata = cyqdata[colums]
        return cyqdata

    def download_akshredata(self):
        """下载Akshare K线、筹码分布数据"""
        end = dt.datetime.now().strftime('%Y%m%d')
        for stock in tqdm(self.stockList, position=0, desc='下载K线、筹码分布数据'):
            """获取每只股票的K线数据和筹码分布"""
            stockcode = stock[3:]
            kdata: pd.DataFrame = self.daily_kdatafeed(stockcode)
            cyqdata: pd.DataFrame = self.daily_cyqdatafeed(stockcode)
            if kdata is None or cyqdata is None:
                continue
            if len(kdata) < 10 or len(cyqdata) < 10:
                continue
            cyqdata = cyqdata.round(
                {'takeprofitratio': 6}
            )
            data: pd.DataFrame = pd.merge(
                kdata,
                cyqdata, on='datetime'
                )
            filepath = self.dirpath + "/" + stock + ".csv"
            if os.path.exists(filepath):
                os.remove(filepath)
            data.to_csv(filepath, index=False)


if __name__ == '__main__':
    ad = AkshareData()
    ad.download_akshredata()
