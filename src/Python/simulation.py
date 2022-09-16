"""
    pyupbit패키지를 활용한 코인 정보 가져오기 및 rsi, macd구하기
"""
# import pyupbit
import numpy
import os
import os.path
import pandas
import json
import math
import platform
from datetime import datetime, timedelta
import unittest
from multiprocessing import Process, Queue, Pool, set_start_method

# profile
enable_profile = True
enable_profile = False
from cProfile import Profile
import pstats
def profile(sort_args=['cumulative'], print_args=[10]):
    profiler = Profile()
    def decorator(fn):
        def inner(*args, **kwargs):
            result = None
            try:
                result = profiler.runcall(fn, *args, **kwargs)
            finally:
                stats = pstats.Stats(profiler)
                stats.strip_dirs().sort_stats(*sort_args).print_stats(*print_args)
            return result
        return inner
    return decorator

def profile_for_multuprocess(f):
    profiler = Profile()
    def inner(*args, **kwargs):
        result = None
        try:
            result = profiler.runcall(f, *args, **kwargs)
        finally:
            stats = pstats.Stats(profiler)
            stats.strip_dirs().sort_stats('cumulative').print_stats(10)
        return result
    return inner
    
# def profile_print():
#     if enable_profile == True:
#         stats = Stats(profiler)
#         stats.strip_dirs()
#         stats.sort_stats('cumulative')
#         stats.print_stats(30)

def get_config():
    """
        설정파일인 config.json파일을 읽어오는 함수.

        Args:
            None
        Returns: 
            int타입
            dictionary타입
    """
    dataList = {}
    #현재 경로 받아오기
    path = os.getcwd()
    if os.path.isfile(os.path.join(path,"config","config.json")):
        file  = open(os.path.join(path,"config","config.json"),"r",encoding="utf-8")
        jsonObject = json.load(file)
        dataList["coin"] = jsonObject.get("coin")
        dataList["bong"] = jsonObject.get("bong")
        dataList["count"] = jsonObject.get("count")
        dataList["macd_fast"] = jsonObject.get("macd_fast")
        dataList["rsi"] = jsonObject.get("rsi")
        dataList["fast_k"] = jsonObject.get("fast_k")
        dataList["slow_k"] = jsonObject.get("slow_k")
        dataList["slow_d"] = jsonObject.get("slow_k")
        dataList["macd_slow"] = jsonObject.get("macd_slow")
        dataList["macd_signal"] = jsonObject.get("macd_signal")
        dataList["bollinger_move_average"] = jsonObject.get("bollinger_move_average")
        dataList["bollinger_k"] = jsonObject.get("bollinger_k")
    else:
        print("[ERROR] 현재 경로 "+path+"에 config.json 이름으로 된 파일이 없습니다.")
        return -1 , None
    return 0 , dataList
def coin_list():
    """ 
        업비트에 상장되어있는 코인 리스트 조회해온다. 

        Args:
            None : 없음.
        Returns:
            dictionary타입

    """
    coinMap = {}
    coinList = pyupbit.get_tickers()
    for i in range(len(coinList)):
        coinMap[i] = coinList[i]
    return coinMap
def make_csv_file(dataMap,columnList):
    """ 
        데이터를 csv 형태로 저장한다. 

        Args:
            dataMap : dictionary타입.
            columnList : list타입.
        Returns:
            int 타입
            파일을 덮어쓸지에 대한 유무 판단시 입력을 잘못하면 1
            정상적으로 파일 쓰기사 실행되면 0
    """
    print("=====파일이 저장될 경로 : "+os.getcwd())
    path = os.getcwd()
    if os.path.isfile(os.path.join(path,"result.csv")):
        print("파일이 이미 있습니다. 덮어 쓰시겠습니까?(y/n)")
        exist = input()
        if "n" == exist.lower():
            print("파일 뒤에 이어써집니다.")
            file = open(os.path.join(path,"result.csv"),"a",encoding="utf-8",newline='')
        elif "y" == exist.lower():
            file = open(os.path.join(path,"result.csv"),"w",encoding="utf-8", newline='')
            file.write("{a},{b},{c},{d},{e},{f}".format(a="date",b=columnList[0],c=columnList[1],d=columnList[2],e=columnList[3],f=columnList[4]))
        else:
            print("잘못 입력 하셨습니다.")
            return 1
    else:
        file = open(os.path.join(path,"result.csv"),"w",encoding="utf-8", newline='')
        file.write("{a},{b},{c},{d},{e},{f}".format(a="date",b=columnList[0],c=columnList[1],d=columnList[2],e=columnList[3],f=columnList[4]))
    for key in dataMap.keys():
        data = dataMap[key]
        dataFormat = ",{a},{b},{c},{d},{e},{f}".format(a=key,b=data[columnList[0]],c=data[columnList[1]],d=data[columnList[2]],e=data[columnList[3]],f=data[columnList[4]])
        file.write(dataFormat)
    if "Windows" in platform.system():
        file.write("\r\n")
    else:
        file.write("\n")
    file.close()
    return 0
def make_csv_file_no_alert(data_frame):
    """ 
        데이터를 csv 형태로 저장한다. 파일 덮어쓸 것인지 물어보지 않는다 무조건 덮어쓴다.    
        Args:
            data_frame : DataFrame타입.
        Returns:
            int 타입
            정상적으로 파일 쓰기가 실행되면 0
    """
    print("=====파일이 저장될 경로 : "+os.getcwd())
    path = os.getcwd()
    if os.path.isfile(os.path.join(path,"result.csv")):
        file = open(os.path.join(path,"result.csv"),"a",encoding="utf-8",newline='')
    else:
        file = open(os.path.join(path,"result.csv"),"w",encoding="utf-8", newline='')
    # file.write("{a},{b},{c},{d},{e},{f}".format(a="date",b=columnList[0],c=columnList[1],d=columnList[2],e=columnList[3],f=columnList[4]))
    format = "date,open,high,low,close,volume,value,"
    file.write(format)
    if "Windows" in platform.system():
        file.write("\r\n")
    else:
        file.write("\n")

    for i in range(len(data_frame)):
        file.write(str(data_frame.index[i])+",")
        for key,value in data_frame.iloc[i].items():
            file.write(str(value)+",")
        if "Windows" in platform.system():
            file.write("\r\n")
        else:
            file.write("\n")
    file.close()
    return 0
def make_csv_data_indicator(coin_data,sheet_name):
    """ 
        데이터를 csv 형태로 저장한다. 파일 덮어쓸 것인지 물어보지 않는다 무조건 덮어쓴다.    
        Args:
            coin_data : 코인정보를 담고있는 DataFrame
            macd : macd정보를 담고있는 DataFrame
            macd_signal : macd signal 정보를 담고있는 DataFrame
            rsi : DataFrame
            fast_k : DataFrame
            slow_k : DataFrame
            slow_d : DataFrame
            bollinger : DataFrame
            bollinger_lbb : DataFrame
            bollinger_ubb : DataFrame

        Returns:
            int 타입
            정상적으로 파일 쓰기가 실행되면 0
    """
    path = os.getcwd()
    if os.path.isfile(os.path.join(path,"result.xlsx")):
        file = pandas.ExcelWriter(os.path.join(path,"result.xlsx"),date_format="YYYY-MM-DD",datetime_format="YYYY-MM-DD HH:MM:SS", mode='a')
    else:
        file = pandas.ExcelWriter(os.path.join(path,"result.xlsx"),date_format="YYYY-MM-DD",datetime_format="YYYY-MM-DD HH:MM:SS", mode='w')
    coin_data.to_excel(file, sheet_name=sheet_name)
    file.save()
    file.close()
    return 0
def make_csv_indicator(id,dataMap):
    """ 
        데이터를 csv 형태로 저장한다. 파일 덮어쓸 것인지 물어보지 않는다 무조건 덮어쓴다.    
        Args:
            dataMap : dictionary type. key : date, value : indicator
            id : 식별자
        Returns:
            int 타입
            정상적으로 파일 쓰기가 실행되면 0
    """
    path = os.getcwd()
    if os.path.isfile(os.path.join(path,"result.csv")):
        file = open(os.path.join(path,"result.csv"),"a",encoding="utf-8",newline='')
    else:
        file = open(os.path.join(path,"result.csv"),"w",encoding="utf-8", newline='')
    file.write("{a},".format(a=id))
    if isinstance(dataMap, float):
        file.write("{a},".format(a=dataMap))
    else:
        for key in dataMap.keys():
            data = dataMap[key]
            dataFormat = "{b},{c},".format(b=key,c=data)
            file.write(dataFormat)
    print(platform.system())
    if "Windows" in platform.system():
        file.write("\r\n")
    else:
        file.write("\n")
    file.close()
    return 0
class Util():
    """
        지표 구하는데 필요한 기타 함수들.
    """
    candle_types = {
    "delim_1m"  : 1,
    "delim_5m"  : 5,
    "delim_15m" : 15,
    "delim_30m" : 30,
    "delim_1h"  : 60,
    "delim_2h"  : 60 * 2,
    "delim_3h"  : 60 * 3,
    "delim_4h"  : 60 * 4,
    "delim_6h"  : 60 * 6,
    "delim_12h" : 60 * 12,
    "delim_1d"  : 60 * 24,
    }
    def convert_dataframe_from_1m(self, df:pandas.DataFrame, delimiter:str):
        assert(delimiter in self.candle_types.keys())
        result_df = pandas.DataFrame()
        length = len(df)
        dic = {}
        for i in range(length):
            if df[delimiter][i] == 1:
                dic[df["datetime"][i]] = [df["close"][i]]
        result_df = result_df.from_dict(dic, orient="index", columns=["close"])
        return result_df
    def basic(self):
        df = pandas.read_csv("../sample_raw_data_2years2month.csv")
        df['datetime'] = df['datetime'].map(pandas.Timestamp)
        df.index = df['datetime'].values

        df['delim_1m'] = numpy.select(
                [(df['datetime'] - datetime(2000, 1, 1, 0, 0, 0))
                    .dt.total_seconds().astype(int) % (60 * 1) == 0, ],
                [1], 0)
        df['delim_5m'] = numpy.select(
                [(df['datetime'] - datetime(2000, 1, 1, 0, 0, 0))
                    .dt.total_seconds().astype(int) % (60 * 5) == 0, ],
                [1], 0)
        df['delim_15m'] = numpy.select(
                [(df['datetime'] - datetime(2000, 1, 1, 0, 0, 0))
                    .dt.total_seconds().astype(int) % (60 * 15) == 0, ],
                [1], 0)
        df['delim_30m'] = numpy.select(
                [(df['datetime'] - datetime(2000, 1, 1, 0, 0, 0))
                    .dt.total_seconds().astype(int) % (60 * 30) == 0, ],
                [1], 0)
        df['delim_1h'] = numpy.select(
                [(df['datetime'] - datetime(2000, 1, 1, 0, 0, 0))
                    .dt.total_seconds().astype(int) % (60 * 60 * 1) == 0, ],
                [1], 0)
        df['delim_1d'] = numpy.select(
                [(df['datetime'] - datetime(2000, 1, 1, 9, 0, 0))
                    .dt.total_seconds().astype(int) % (60 * 60 * 24) == 0, ],
                [1], 0)

        pandas.set_option('display.max_rows', None)
        pandas.set_option('display.max_columns', None)
        pandas.set_option('display.width', None)
        return df
class search_coin():
    """ 
        코인의 정보를 가지고 오는 클래스.
    """
    def get_coin_info(self):
        """ 
            업비트에서 일봉,주봉,월봉 등 총 11가지의 차트를 얻어올 수 있다. 

            Returns:
                딕셔너리 타입 , pandas패키지의 dataframe타입
        """
        selectList = {} 
        coinMap = {}
        """ 코인 리스트 얻어오기 """
        coinMap = coin_list()
        print(coinMap)
        print("\nPlease choose coin>>>>")
        inputCoin = input()
        if int(inputCoin) in coinMap :
            print(coinMap[int(inputCoin)])
            selectList["stock"] = coinMap[int(inputCoin)]
        else:
            print("[ERROR] There is no coin")
            return
        print("1. 일봉\n2. 주봉\n3. 월봉\n4. 1분봉\n5. 3분봉\n6. 5분봉\n7. 10분봉\n8. 15분봉\n9. 30분봉\n10. 60분봉\n11. 240분봉\n")
        optionMap = {"1":"day","2":"week","3":"month","4":"minute1","5":"minute3","6":"minute5","7":"minute10","8":"minute15","9":"minute30","10":"minute60","11":"minute240"}
        selectNum = input()
        if optionMap[selectNum]:
            selectList["bong"] = optionMap[selectNum]
            print(optionMap[selectNum])
        else:
            print("[ERROR] Wrong Input")
            return
        print("몇개를 출력할 것인가?\n")
        selectNum = input()
        selectList["count"] = int(selectNum)
        dataFrame = pyupbit.get_ohlcv(selectList["coin"], interval=selectList["bong"], count=selectList["count"])
        print(dataFrame.columns.tolist())
        columnList = dataFrame.columns.tolist()
        dataMap = {}
        for i in range(len(dataFrame)):
            data = dataFrame.iloc[i]
            key = dataFrame.index[i]
            dataMap[key] = {}
            dataMap[key][columnList[0]] = "%.3f"%data[0]
            dataMap[key][columnList[1]] = "%.3f"%data[1]
            dataMap[key][columnList[2]] = "%.3f"%data[2]
            dataMap[key][columnList[3]] = "%.3f"%data[3]
            dataMap[key][columnList[4]] = "%.3f"%data[4]
            dataMap[key][columnList[5]] = "%.3f"%data[5]
        # for key in dataMap.keys():
        #     print(dataMap[key])
        print("파일을 저장할까요?(y/n)")
        inputCoin = input()
        if "y" == inputCoin.lower():
            retCode = make_csv_file(dataMap,columnList)
            if retCode == 1:
                print("[ERROR] file overwrite error")
            else:
                print("[INFO] file write Success")
        elif "n" == inputCoin.lower():
            print("[INFO] NO Save File")
        else:
            print("[ERROR] Wrong Input")
        dataMap["option"] = selectList
        return dataMap, dataFrame

    def get_coin_data(self,coin:str="KRW-BTC",candle_type:str="minute1",candle_count:int=200,date_time:datetime=datetime.now()):
        """ 
            업비트에서 종목에 대한 주가 정보를 얻어오는 함수.
            Args:
                string   : 코인 종류
    		    string   : minute1,day,week,month...
    		    int      : 봉 개수
                datetime : 시간
            Returns:
                dictoinary
                dataFrame type
        """
#        retCode, dataList = get_config()
#        if retCode == -1 or dataList is None:
#            return
#        for key in dataList.keys():
#            print(dataList[key])
#        print("coin : {a}, bong : {b}, count : {c}".format(a=dataList["coin"],b=dataList["bong"],c=dataList["count"]))
        # optionMap = {1:"day",2:"week",3:"month",4:"minute1",5:"minute3",6:"minute5",7:"minute10",8:"minute15",9:"minute30",10:"minute60",11:"minute240"}
        dataFrame = pyupbit.get_ohlcv(coin, interval=candle_type, count=candle_count, to = date_time)
        columnList = dataFrame.columns.tolist()
        dataMap = {}
        for i in range(len(dataFrame)):
            data = dataFrame.iloc[i].tolist()
            key = dataFrame.index[i]
            dataMap[key] = {}
            dataMap[key][columnList[0]] = float(data[0])
            dataMap[key][columnList[1]] = float(data[1])
            dataMap[key][columnList[2]] = float(data[2])
            dataMap[key][columnList[3]] = float(data[3])
            dataMap[key][columnList[4]] = float(data[4])
            dataMap[key][columnList[5]] = float(data[5])

        return dataMap, dataFrame
        
class Macd():
    def search_macd(self):
        """ 
            이동 평균선 구하는 함수
            
            Args:
                None
            Returns:
                float64
        """
        dataMap = {}
        dataMap, dataFrame = search_coin().get_coin_info()
        # bong = dataMap["option"]["bong"]
        count = dataMap["option"]["count"]
        macd = dataFrame['close'].rolling(window=count, min_periods=1).mean().iloc[-1]
        # print(str(count)+"개 "+bong+" macd : "+str(macd))
        return macd
    def get_macd_value(self, data_frame, macd_slow:int=26):
        """
            이동 평균선값을 구하는 함수
            Args:
                Pandas dataFrame : coin data
                macd_slow : macd 지수
            Returns:
                dataFrame : macd 지표
                dictionary : macd 지표 dictionary
        """ 
        macd_data = {}
        macd = data_frame["close"].ewm(span = macd_slow, min_periods = macd_slow - 1).mean()
        for i in range(len(macd)):
            data = macd.iloc[i]
            key = macd.index[i]
            if math.isnan(data):
                macd_data[key] = None
            else:
                macd_data[key] = float(data)
        return macd, macd_data

    def get_macd(self,dataFrame,macd_fast:int=12,macd_slow:int=26):
        """ 
            이동 평균선 구하는 함수

            Args:
                Pandas dataFrame
            Returns:
                dataFrame : macd지표
				dictionary : macd지표를 dictionary로 변환
        """
        macdData = {}
#        ret , configData = get_config()
#        if ret != 0:
#            return None
#        macdFast = int(configData["macd_fast"])
#        macdSlow = int(configData["macd_slow"])
                
        emaFast = dataFrame["close"].ewm( span = macd_fast, min_periods = macd_fast - 1).mean()
        emaSlow = dataFrame["close"].ewm( span = macd_slow, min_periods = macd_slow - 1).mean()
        macd = emaFast - emaSlow
        for i in range(len(macd)):
            data = macd.iloc[i]
            key = macd.index[i]
            if math.isnan(data):
                macdData[key] = None
            else:
                macdData[key] = float(data)

        return macd,macdData
    def get_macd_signal(self,macd, macd_signal:int=9):
        """
            MACD Signal을 구하는 함수

            Args:
            	Pandas DataFrame 타입
			Returns:
				DataFrame
				dictionary
        """
        macdSignal = {}
#        ret, configData = get_config()
#        if ret != 0:
#            return None
#        macdSignalCount = int(configData["macd_signal"])   
        signal = macd.ewm( span = macd_signal, min_periods = macd_signal-1).mean()
        for i in range(len(signal)):
            data = signal.iloc[i]
            key = signal.index[i]
            if math.isnan(data):
                macdSignal[key] = None
            else:
                macdSignal[key] = float(data)
        return signal,macdSignal

class Rsi():
    def search_rsi(self):
        """ 
            투자지표 구하는 함수  
            return pandas패키지 타입.
        """
        dataMap = {}
        dataMap, dataFrame = search_coin().get_coin_info()
        delta = dataFrame['close'].diff()
        # period = dataMap["option"]["count"]
        up, down = delta.copy(), delta.copy()
        up[up < 0] = 0
        down[down > 0] = 0
        _gain = up.ewm(com=(14 - 1), min_periods=14).mean()
        _loss = down.abs().ewm(com=(14 - 1), min_periods=14).mean()
        rs = _gain / _loss
        result = pandas.Series(100 - (100/(1 + rs)), name="RSI")
        return result
    
    def search_rsi_infinite(self,dataFrame,rsi):
        delta = dataFrame['close'].diff()
        count = int(rsi)
        up, down = delta.copy(), delta.copy()
        up[up < 0] = 0
        down[down > 0] = 0
        _gain = up.ewm(com=(count - 1), min_periods=count).mean()
        _loss = down.abs().ewm(com=(count - 1), min_periods=count).mean()
        rs = _gain / _loss
        result = pandas.Series(100 - (100/(1 + rs)), name="RSI")
        return 0, result

class Stochastic():
    """
        Stochastic지표를 구하는 클래스.
        Fast_K, Slow_d, Slow_k를 구할 수 있다.
        최종적으로는 Slow_d, Slow_k가 필요하다.
    """
    def fast_k(self,dataFrame,fast_k:int=14):
        """
            Fast_k지표를 구하는 함수.

            Args:
                [각 봉 정보를 담고 있는] dataFrame
                
            
            Returns:
                dataFrame : fast_k지표값
                dictionary : fast_k지표값을 eky,value로 변환한 dictomary type
        """
        indicatorFastK = {}
        low = dataFrame["low"].rolling(window=fast_k).min()
        close = dataFrame["close"]
        high = dataFrame["high"].rolling(window=fast_k).max()
        stochastic_fast = ((close - low ) / (high - low)) * 100
        for i in range(len(stochastic_fast)):
            data = stochastic_fast.iloc[i]
            key = stochastic_fast.index[i]
            if math.isnan(data):
                indicatorFastK[key] = None
            else:
                indicatorFastK[key] = float(data)
        return stochastic_fast, indicatorFastK
    def slow_k(self, stochastic_fast, slow_k:int=5):
        """
            fast_k 구한 값으로 Slow_k를 구한다.

            Args:
                dictionary 
                key : date
                value : fast_k
            
            Returns:
                dataFrame : slow_k지표값
                dictionary : slow_k지표값을 key,value로 변환한 dictomary type
        """
        stochastic_slow = ""
        indicatorSlowK = {}
        stochastic_slow = stochastic_fast.ewm(span=slow_k).mean()
        for i in range(len(stochastic_slow)):
            data = stochastic_slow.iloc[i]
            key = stochastic_slow.index[i]
            if math.isnan(data):
                indicatorSlowK[key] = None
            else:
                indicatorSlowK[key] = float(data)
        return stochastic_slow, indicatorSlowK

    def slow_d(self, stochastic_slow, slow_d:int=3):
        """
            slow_k 구한 값으로 slow_d를 구한다.

            Args:
                dictionary
                key : date,
                value : slow_k
            
            Returns:
                dataFrame : slow_d지표값
                dictionary : slow_d지표값을 key,value로 변환한 dictomary type
        """
        stochastic_slow_d = ""
        indicatorSlowD = {}
        stochastic_slow_d = stochastic_slow.ewm(span=slow_d).mean()
        for i in range(len(stochastic_slow_d)):
            data = stochastic_slow_d.iloc[i]
            key = stochastic_slow_d.index[i]
            if math.isnan(data):
                indicatorSlowD[key] = None
            else:
                indicatorSlowD[key] = float(data)
        return stochastic_slow_d,indicatorSlowD
class BollingerBand():
    """
        볼린저 밴드 지표를 구하는 클래스
    """
    def get_bollinger_band(self,data_frame,move_average:int=20):
        """
            볼린저 밴드 지표를 구하는 함수

            Args:
                @ dataFrame : Pandas DataFrame type  coin 주가 정보가 들어있는 데이터
                int         : 지수값
            Returns:
                Pandas DataFrame type : 볼린저 밴드 지표
                dictionary type : 볼린저 밴드 지표를 dictionary로 변환한 데이터
        """
        indicator_bollinger = {}
        bollinger_band = data_frame["close"].rolling(window=move_average).mean()
        for i in range(len(bollinger_band)):
            data = bollinger_band.iloc[i]
            key = bollinger_band.index[i]
            if math.isnan(data):
                indicator_bollinger[key] = None
            else:
                indicator_bollinger[key] = float(data)
        return bollinger_band, indicator_bollinger
    def get_bollinger_ubb_lbb(self,data_frame,bollinger_band,move_average:int=20,bollinger_k:int=2):
        """
            볼린저 밴드 지표중 상한선, 하한선을 구하는 함수

            Args:
                Pandas DataFrame type : coin 주가 정보가 들어있는 데이터
                Pandas DataFrame type : bollinger band data
            Returns:
                Pandas DataFrame type : 볼린저 밴드 상한선 지표
                Pandas DataFrame type : 볼린저 밴드 하한선 지표
                dictionary type : 볼린저 밴드 상한선 지표를 dictionary로 변환한 데이터
                dictionary type : 볼린저 밴드 하한선 지표를 dictionary로 변환한 데이터
        """
        bollinger_ubb = {}
        bollinger_lbb = {}
        std = data_frame["close"].rolling(window=move_average).std()
        ubb = bollinger_band + (bollinger_k * std)
        lbb = bollinger_band - (bollinger_k * std)
        for i in range(len(lbb)):
            ubbData = ubb.iloc[i]
            lbbData = lbb.iloc[i]
            ubbKey = ubb.index[i]
            lbbKey = lbb.index[i]

            if math.isnan(ubbData):
                bollinger_ubb[ubbKey] = None
            else:
                bollinger_ubb[ubbKey] = float(ubbData)
             
            if math.isnan(ubbData):
               bollinger_lbb[lbbKey] = None
            else:
               bollinger_lbb[lbbKey] = float(lbbData)
        return ubb,lbb,bollinger_ubb,bollinger_lbb
class TestMacd(unittest.TestCase):
    def __init__(self):
        self.util = None
        self.df = None
    
    def prepare(self):
        self.util = Util()
        self.df = self.util.basic() 

    # @profile()
    def TestMacd_get_macdsignal(self, df:pandas.DataFrame):
        macd = Macd()
        macd_df, macd_dict = macd.get_macd(df)
        signal_df, signal_dict = macd.get_macd_signal(macd_df)
        return signal_df, signal_dict

    def test_multiprocess(self):
        self.prepare()
        count = len(self.df)
        df_5m = self.util.convert_dataframe_from_1m(self.df, "delim_5m")
        df_15m = self.util.convert_dataframe_from_1m(self.df, "delim_15m")
        df_30m = self.util.convert_dataframe_from_1m(self.df, "delim_30m")
        df_1h = self.util.convert_dataframe_from_1m(self.df, "delim_1h")
        df_1d = self.util.convert_dataframe_from_1m(self.df, "delim_1d")
        result_queue = Queue()
        th1 = Process(target=self.TestMacd_get_macdsignal,args=(self.df,))
        th2 = Process(target=self.TestMacd_get_macdsignal,args=(df_5m,))
        th3 = Process(target=self.TestMacd_get_macdsignal,args=(df_15m,))
        th4 = Process(target=self.TestMacd_get_macdsignal,args=(df_30m,))
        th5 = Process(target=self.TestMacd_get_macdsignal,args=(df_1h,))
        th6 = Process(target=self.TestMacd_get_macdsignal,args=(df_1d,))

        start = datetime.now()
        th1.start()
        th2.start()
        th3.start()
        th4.start()
        th5.start()
        th6.start()
        th1.join()
        th2.join()
        th3.join()
        th4.join()
        th5.join()
        th6.join()


        end = datetime.now()
        diff = (end - start).total_seconds()
        speed = count / diff
        print("[ macd signal ] python multi")
        print(f"elapsed time : {diff: 12.2f} s")
        print(f"speed        : {speed: 12.2f}")
        print()
        print()

    def test_example(self):
        self.prepare()
        count = len(self.df)

        df_5m = self.util.convert_dataframe_from_1m(self.df, "delim_5m")
        df_15m = self.util.convert_dataframe_from_1m(self.df, "delim_15m")
        df_30m = self.util.convert_dataframe_from_1m(self.df, "delim_30m")
        df_1h = self.util.convert_dataframe_from_1m(self.df, "delim_1h")
        df_1d = self.util.convert_dataframe_from_1m(self.df, "delim_1d")
        
        start = datetime.now()
        #1m
        self.TestMacd_get_macdsignal(self.df)
        #5m
        self.TestMacd_get_macdsignal(df_5m)
        #15m
        self.TestMacd_get_macdsignal(df_15m)
        #30m
        self.TestMacd_get_macdsignal(df_30m)
        #1h
        self.TestMacd_get_macdsignal(df_1h)
        #1d
        self.TestMacd_get_macdsignal(df_1d)

        end = datetime.now()
        diff = (end - start).total_seconds()
        speed = count / diff
        print("[ macd signal ] python")
        print(f"elapsed time : {diff: 12.2f} s")
        print(f"speed        : {speed: 12.2f}")
        print()
        print()

if __name__ == "__main__":
    test = TestMacd()
    test.prepare()
    test.test_multiprocess()
