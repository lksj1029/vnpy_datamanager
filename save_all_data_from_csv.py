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
        symbol: str = file.split('.')[1]
        if 'sh' in file:
            exchange: Exchange = Exchange.SSE
        else:
            exchange: Exchange = Exchange.SZSE
        me.import_data_from_csv(
            file_path=filepath,
            symbol=symbol,
            exchange=exchange,
            interval=Interval.DAILY,
            tz_name='Asia/Shanghai',
            datetime_head='datetime',
            open_head='open',
            high_head='high',
            low_head='low',
            close_head='close',
            volume_head='volume',
            turnover_head='turnover',
            open_interest_head='',
            amplitude_head='amplitude',
            takeprofitratio_head='takeprofitratio',
            datetime_format='%Y-%m-%d'
        )
