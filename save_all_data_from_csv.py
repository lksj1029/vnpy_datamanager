import os
from tqdm import tqdm

from engine import ManagerEngine
from akshare_engine import AkshareData
from vnpy.trader.constant import Interval, Exchange
from vnpy.trader.engine import MainEngine, EventEngine


"""获取日K线数据并且写入VNPY数据库"""
if __name__ == '__main__':
    filedir: str = 'data'
    filenames: str = os.listdir(filedir)
    me = ManagerEngine(MainEngine, EventEngine)
    for file in tqdm(filenames, position=0, desc='导入K线数据'):
        filepath: str = filedir + '\\' + file
        symbol: str = file.split('.')[0]
        if 'SH' in file:
            exchange: Exchange = Exchange.SSE
        elif 'SZ' in file:
            exchange: Exchange = Exchange.SZSE
        else:
            continue
        me.import_data_from_csv(
            file_path=filepath,
            symbol=symbol,
            exchange=exchange,
            interval=Interval.DAILY,
            tz_name='Asia/Shanghai',
            datetime_head='trade_date',
            open_head='open',
            high_head='high',
            low_head='low',
            close_head='close',
            volume_head='vol',
            amount_head='amount',
            pct_chg_head='pct_chg',
            his_low_head='his_low',
            his_high_head='his_high',
            cost_5pct_head='cost_5pct',
            cost_15pct_head='cost_15pct',
            cost_50pct_head='cost_50pct',
            cost_85pct_head='cost_85pct',
            cost_95pct_head='cost_95pct',
            weight_avg_head='weight_avg',
            winner_rate_head='winner_rate',
            open_interest_head='',
            datetime_format='%Y%m%d'
        )
