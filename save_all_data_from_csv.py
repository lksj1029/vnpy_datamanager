from engine import ManagerEngine
from vnpy.trader.constant import Interval, Exchange
from vnpy.trader.engine import BaseEngine, MainEngine, EventEngine


me = ManagerEngine(MainEngine, EventEngine)
filepath: str = 'kdata_daily\\000001.csv'
me.import_data_from_csv(
    file_path=filepath,
    symbol='000001',
    exchange=Exchange.SSE,
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
    datetime_format='%Y-%m-%d'

)
