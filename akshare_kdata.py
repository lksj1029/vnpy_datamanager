import akshare as ak
from tqdm import tqdm
import numpy as np
import datetime as dt
import os


class akshare_kdata:
    dirpath = "kdata_daily"

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

    def daily_kdatafeed(self):
        start = '20100101'
        end = dt.datetime.now().strftime('%Y%m%d')
        for stock in tqdm(self.stockList, position=0, desc='下载日K线'):
            stockcode = stock[3:]
            kdata = ak.stock_zh_a_hist(
               symbol=stockcode,
               period="daily",
               start_date=start,
               end_date=end
               )
            if len(kdata) < 10:
                continue
            filepath = self.dirpath + "/" + stockcode + ".csv"
            if os.path.exists(filepath):
                os.remove(filepath)
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
            kdata[colums].to_csv(filepath, index=False)


if __name__ == '__main__':
    aks = akshare_kdata()
    aks.daily_kdatafeed()
