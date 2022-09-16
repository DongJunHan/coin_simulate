import ctypes
import platform
import pandas
import numpy
from datetime import datetime



class Calulator:

    def __init__(self, library: str):
        self.load_library(library)

    def load_library(self, library:str):
        c_lib = None
        print(platform.system())
        if "Windows" == platform.system():
            c_lib = ctypes.windll.LoadLibrary(library)
        elif "Linux" == platform.system():
            c_lib = ctypes.cdll.LoadLibrary(library)
        elif "Darwin" == platform.system():
            c_lib = ctypes.cdll.LoadLibrary(library)
        else:
            assert(True)
            raise OSError()
        self.c_lib = c_lib


    def get_basic_candles(self,
            open_df,
            high_df,
            low_df,
            close_df,
            volume_df,
            delim_df,
            count,
        ):

        c_lib = self.c_lib

        get_basic_candles = c_lib.get_basic_candles
        get_basic_candles.argtypes = (
                ctypes.POINTER(ctypes.c_double),
                ctypes.POINTER(ctypes.c_double),
                ctypes.POINTER(ctypes.c_double),
                ctypes.POINTER(ctypes.c_double),
                ctypes.POINTER(ctypes.c_double),
                ctypes.POINTER(ctypes.c_int),
                ctypes.c_int64,
                ctypes.POINTER(ctypes.c_double),
                ctypes.POINTER(ctypes.c_double),
                ctypes.POINTER(ctypes.c_double),
                ctypes.POINTER(ctypes.c_double),
                ctypes.POINTER(ctypes.c_double),
        )

        open_c_array = (ctypes.c_double * count)(*open_df)
        high_c_array = (ctypes.c_double * count)(*high_df)
        low_c_array = (ctypes.c_double * count)(*low_df)
        close_c_array = (ctypes.c_double * count)(*close_df)
        volume_c_array = (ctypes.c_double * count)(*volume_df)

        ret_open_c_array = (ctypes.c_double * count)()
        ret_high_c_array = (ctypes.c_double * count)()
        ret_low_c_array = (ctypes.c_double * count)()
        ret_close_c_array = (ctypes.c_double * count)()
        ret_volume_c_array = (ctypes.c_double * count)()

        delim_c_array = (ctypes.c_int * count)(*delim_df)

        count_c = ctypes.c_int64(count)

        get_basic_candles(
                open_c_array,
                high_c_array,
                low_c_array,
                close_c_array,
                volume_c_array,
                delim_c_array,
                count_c,
                ret_open_c_array,
                ret_high_c_array,
                ret_low_c_array,
                ret_close_c_array,
                ret_volume_c_array,
        )

        ret_open_list = list(ret_open_c_array[:count])
        ret_high_list = list(ret_high_c_array[:count])
        ret_low_list = list(ret_low_c_array[:count])
        ret_close_list = list(ret_close_c_array[:count])
        ret_volume_list = list(ret_volume_c_array[:count])

        return (
                ret_open_list,
                ret_high_list,
                ret_low_list,
                ret_close_list,
                ret_volume_list,
        )

    def get_basic_candles_realtime(self,
            open_df,
            high_df,
            low_df,
            close_df,
            volume_df,
            delim_df,
            count,
        ):

        c_lib = self.c_lib

        get_basic_candles_realtime = c_lib.get_basic_candles_realtime
        get_basic_candles_realtime.argtypes = (
                ctypes.POINTER(ctypes.c_double),
                ctypes.POINTER(ctypes.c_double),
                ctypes.POINTER(ctypes.c_double),
                ctypes.POINTER(ctypes.c_double),
                ctypes.POINTER(ctypes.c_double),
                ctypes.POINTER(ctypes.c_int),
                ctypes.c_int64,
                ctypes.POINTER(ctypes.c_double),
                ctypes.POINTER(ctypes.c_double),
                ctypes.POINTER(ctypes.c_double),
                ctypes.POINTER(ctypes.c_double),
                ctypes.POINTER(ctypes.c_double),
        )

        open_c_array = (ctypes.c_double * count)(*open_df)
        high_c_array = (ctypes.c_double * count)(*high_df)
        low_c_array = (ctypes.c_double * count)(*low_df)
        close_c_array = (ctypes.c_double * count)(*close_df)
        volume_c_array = (ctypes.c_double * count)(*volume_df)

        ret_open_c_array = (ctypes.c_double * count)()
        ret_high_c_array = (ctypes.c_double * count)()
        ret_low_c_array = (ctypes.c_double * count)()
        ret_close_c_array = (ctypes.c_double * count)()
        ret_volume_c_array = (ctypes.c_double * count)()

        delim_c_array = (ctypes.c_int * count)(*delim_df)

        count_c = ctypes.c_int64(count)

        get_basic_candles_realtime(
                open_c_array,
                high_c_array,
                low_c_array,
                close_c_array,
                volume_c_array,
                delim_c_array,
                count_c,
                ret_open_c_array,
                ret_high_c_array,
                ret_low_c_array,
                ret_close_c_array,
                ret_volume_c_array,
        )

        ret_open_list = list(ret_open_c_array[:count])
        ret_high_list = list(ret_high_c_array[:count])
        ret_low_list = list(ret_low_c_array[:count])
        ret_close_list = list(ret_close_c_array[:count])
        ret_volume_list = list(ret_volume_c_array[:count])

        return (
                ret_open_list,
                ret_high_list,
                ret_low_list,
                ret_close_list,
                ret_volume_list,
        )


    def get_ema_adjust(self,
            data_df,
            delim_df,
            count,
            indicator,
        ):

        c_lib = self.c_lib

        get_ema_adjust = c_lib.get_ema_adjust
        get_ema_adjust.argtypes = (
                ctypes.POINTER(ctypes.c_double),
                ctypes.POINTER(ctypes.c_int),
                ctypes.c_int64,
                ctypes.c_int,
                ctypes.POINTER(ctypes.c_double),
        )

        data_c_array = (ctypes.c_double * count)(*data_df)
        ret_ema_c_array = (ctypes.c_double * count)()
        delim_c_array = (ctypes.c_int * count)(*delim_df)

        count_c = ctypes.c_int64(count)
        indicator_c = ctypes.c_int(indicator)

        get_ema_adjust(
                data_c_array,
                delim_c_array,
                count_c,
                indicator_c,
                ret_ema_c_array,
        )

        ret_ema_list = list(ret_ema_c_array[:count])

        return ret_ema_list



    def get_ema_adjust_realtime(self,
            data_df,
            realtime_data_df,
            delim_df,
            count,
            indicator,
        ):

        c_lib = self.c_lib

        get_ema_adjust_realtime = c_lib.get_ema_adjust_realtime
        get_ema_adjust_realtime.argtypes = (
                ctypes.POINTER(ctypes.c_double),
                ctypes.POINTER(ctypes.c_double),
                ctypes.POINTER(ctypes.c_int),
                ctypes.c_int64,
                ctypes.c_int,
                ctypes.POINTER(ctypes.c_double),
        )

        data_c_array = (ctypes.c_double * count)(*data_df)
        realtime_data_c_array = (ctypes.c_double * count)(*realtime_data_df)
        ret_ema_c_array = (ctypes.c_double * count)()
        delim_c_array = (ctypes.c_int * count)(*delim_df)

        count_c = ctypes.c_int64(count)
        indicator_c = ctypes.c_int(indicator)

        get_ema_adjust_realtime(
                data_c_array,
                realtime_data_c_array,
                delim_c_array,
                count_c,
                indicator_c,
                ret_ema_c_array,
        )

        ret_ema_list = list(ret_ema_c_array[:count])

        return ret_ema_list

    def get_macd(self,
            data_df,
            delim_df,
            count,
            macd_fast,
            macd_slow,
        ):

        c_lib = self.c_lib

        get_macd = c_lib.get_macd
        get_macd.argtypes = (
                ctypes.POINTER(ctypes.c_double),
                ctypes.POINTER(ctypes.c_int),
                ctypes.c_int64,
                ctypes.c_int,
                ctypes.c_int,
                ctypes.POINTER(ctypes.c_double),
        )

        data_c_array = (ctypes.c_double * count)(*data_df)
        ret_macd_c_array = (ctypes.c_double * count)()
        delim_c_array = (ctypes.c_int * count)(*delim_df)

        count_c = ctypes.c_int64(count)

        macd_fast_c = ctypes.c_int(macd_fast)
        macd_slow_c = ctypes.c_int(macd_slow)

        get_macd(
                data_c_array,
                delim_c_array,
                count_c,
                macd_fast_c,
                macd_slow_c,
                ret_macd_c_array,
        )

        ret_macd_list = list(ret_macd_c_array[:count])

        return ret_macd_list


    def get_macd_realtime(self,
            data_df,
            realtime_data_df,
            delim_df,
            count,
            macd_fast,
            macd_slow,
        ):

        c_lib = self.c_lib

        get_macd_realtime = c_lib.get_macd_realtime
        get_macd_realtime.argtypes = (
                ctypes.POINTER(ctypes.c_double),
                ctypes.POINTER(ctypes.c_double),
                ctypes.POINTER(ctypes.c_int),
                ctypes.c_int64,
                ctypes.c_int,
                ctypes.c_int,
                ctypes.POINTER(ctypes.c_double),
        )

        data_c_array = (ctypes.c_double * count)(*data_df)
        realtime_data_c_array = (ctypes.c_double * count)(*realtime_data_df)
        ret_macd_c_array = (ctypes.c_double * count)()
        delim_c_array = (ctypes.c_int * count)(*delim_df)

        count_c = ctypes.c_int64(count)

        macd_fast_c = ctypes.c_int(macd_fast)
        macd_slow_c = ctypes.c_int(macd_slow)

        get_macd_realtime(
                data_c_array,
                realtime_data_c_array,
                delim_c_array,
                count_c,
                macd_fast_c,
                macd_slow_c,
                ret_macd_c_array,
        )

        ret_macd_list = list(ret_macd_c_array[:count])

        return ret_macd_list



    def get_macd_signal(self,
            data_df,
            delim_df,
            count,
            macd_fast,
            macd_slow,
            signal,
            ):

        c_lib = self.c_lib

        get_macd_signal = c_lib.get_macd_signal
        get_macd_signal.argtypes = (
                ctypes.POINTER(ctypes.c_double),
                ctypes.POINTER(ctypes.c_int),
                ctypes.c_int64,
                ctypes.c_int,
                ctypes.c_int,
                ctypes.c_int,
                ctypes.POINTER(ctypes.c_double),
        )

        data_c_array = (ctypes.c_double * count)(*data_df)
        ret_macd_signal_c_array = (ctypes.c_double * count)()
        delim_c_array = (ctypes.c_int * count)(*delim_df)

        count_c = ctypes.c_int64(count)

        macd_fast_c = ctypes.c_int(macd_fast)
        macd_slow_c = ctypes.c_int(macd_slow)
        macd_signal_c = ctypes.c_int(signal)

        get_macd_signal(
                data_c_array,
                delim_c_array,
                count_c,
                macd_fast_c,
                macd_slow_c,
                macd_signal_c,
                ret_macd_signal_c_array,
        )

        ret_macd_signal_list = list(ret_macd_signal_c_array[:count])

        return ret_macd_signal_list


    def get_macd_signal_realtime(self,
            data_df,
            realtime_data_df,
            delim_df,
            count,
            macd_fast,
            macd_slow,
            signal,
            ):

        c_lib = self.c_lib

        get_macd_signal_realtime = c_lib.get_macd_signal_realtime
        get_macd_signal_realtime.argtypes = (
                ctypes.POINTER(ctypes.c_double),
                ctypes.POINTER(ctypes.c_double),
                ctypes.POINTER(ctypes.c_int),
                ctypes.c_int64,
                ctypes.c_int,
                ctypes.c_int,
                ctypes.c_int,
                ctypes.POINTER(ctypes.c_double),
        )

        data_c_array = (ctypes.c_double * count)(*data_df)
        realtime_data_c_array = (ctypes.c_double * count)(*realtime_data_df)
        ret_macd_signal_c_array = (ctypes.c_double * count)()
        delim_c_array = (ctypes.c_int * count)(*delim_df)

        count_c = ctypes.c_int64(count)

        macd_fast_c = ctypes.c_int(macd_fast)
        macd_slow_c = ctypes.c_int(macd_slow)
        macd_signal_c = ctypes.c_int(signal)

        get_macd_signal_realtime(
                data_c_array,
                realtime_data_c_array,
                delim_c_array,
                count_c,
                macd_fast_c,
                macd_slow_c,
                macd_signal_c,
                ret_macd_signal_c_array,
        )

        ret_macd_signal_list = list(ret_macd_signal_c_array[:count])

        return ret_macd_signal_list


    def get_macd_oscillator(self,
            data_df,
            delim_df,
            count,
            macd_fast,
            macd_slow,
            signal,
            ):

        c_lib = self.c_lib

        get_macd_oscillator = c_lib.get_macd_oscillator
        get_macd_oscillator.argtypes = (
                ctypes.POINTER(ctypes.c_double),
                ctypes.POINTER(ctypes.c_int),
                ctypes.c_int64,
                ctypes.c_int,
                ctypes.c_int,
                ctypes.c_int,
                ctypes.POINTER(ctypes.c_double),
        )

        data_c_array = (ctypes.c_double * count)(*data_df)
        ret_macd_osc_c_array = (ctypes.c_double * count)()
        delim_c_array = (ctypes.c_int * count)(*delim_df)

        count_c = ctypes.c_int64(count)

        macd_fast_c = ctypes.c_int(macd_fast)
        macd_slow_c = ctypes.c_int(macd_slow)
        macd_signal_c = ctypes.c_int(signal)

        get_macd_oscillator(
                data_c_array,
                delim_c_array,
                count_c,
                macd_fast_c,
                macd_slow_c,
                macd_signal_c,
                ret_macd_osc_c_array,
        )

        ret_macd_osc_list = list(ret_macd_osc_c_array[:count])

        return ret_macd_osc_list



    def get_macd_oscillator_realtime(self,
            data_df,
            realtime_data_df,
            delim_df,
            count,
            macd_fast,
            macd_slow,
            signal,
            ):

        c_lib = self.c_lib

        get_macd_oscillator_realtime = c_lib.get_macd_oscillator_realtime
        get_macd_oscillator_realtime.argtypes = (
                ctypes.POINTER(ctypes.c_double),
                ctypes.POINTER(ctypes.c_double),
                ctypes.POINTER(ctypes.c_int),
                ctypes.c_int64,
                ctypes.c_int,
                ctypes.c_int,
                ctypes.c_int,
                ctypes.POINTER(ctypes.c_double),
        )

        data_c_array = (ctypes.c_double * count)(*data_df)
        realtime_data_c_array = (ctypes.c_double * count)(*realtime_data_df)
        ret_macd_osc_c_array = (ctypes.c_double * count)()
        delim_c_array = (ctypes.c_int * count)(*delim_df)

        count_c = ctypes.c_int64(count)

        macd_fast_c = ctypes.c_int(macd_fast)
        macd_slow_c = ctypes.c_int(macd_slow)
        macd_signal_c = ctypes.c_int(signal)

        get_macd_oscillator_realtime(
                data_c_array,
                realtime_data_c_array,
                delim_c_array,
                count_c,
                macd_fast_c,
                macd_slow_c,
                macd_signal_c,
                ret_macd_osc_c_array,
        )

        ret_macd_osc_list = list(ret_macd_osc_c_array[:count])

        return ret_macd_osc_list
# profile
import unittest
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
class TestMacd():
    # @profile()
    def TestMacd_get_macdsignal(self, cal: Calulator, df: pandas.DataFrame, result_column: str, close: str, delim: str, count: int, fast : int, slow: int, signal: int):
        df[result_column] = cal.get_macd_signal(
                df[close],
                df[delim],
                count, fast, slow, signal)
        return df
    def test_example(self):
        global_start = datetime.now()

        df = pandas.read_csv('../sample_raw_data_2years2month.csv')
        df['datetime'] = df['datetime'].map(pandas.Timestamp)
        df.index = df['datetime'].values
        count = len(df)

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





        cal = Calulator("./libcalculator.so")

        (
                df["open_1m"],
                df["high_1m"],
                df["low_1m"],
                df["close_1m"],
                df["volume_1m"]
        ) = cal.get_basic_candles(
                df['open'],
                df['high'],
                df['low'],
                df['close'],
                df['volume'],
                df['delim_1m'],
                count,
        )
        (
                df["open_1m_r"],
                df["high_1m_r"],
                df["low_1m_r"],
                df["close_1m_r"],
                df["volume_1m_r"]
        ) = cal.get_basic_candles_realtime(
                df['open'],
                df['high'],
                df['low'],
                df['close'],
                df['volume'],
                df['delim_1m'],
                count,
        )

        (
                df["open_5m"],
                df["high_5m"],
                df["low_5m"],
                df["close_5m"],
                df["volume_5m"]
        ) = cal.get_basic_candles(
                df['open'],
                df['high'],
                df['low'],
                df['close'],
                df['volume'],
                df['delim_5m'],
                count,
        )
        (
                df["open_5m_r"],
                df["high_5m_r"],
                df["low_5m_r"],
                df["close_5m_r"],
                df["volume_5m_r"]
        ) = cal.get_basic_candles_realtime(
                df['open'],
                df['high'],
                df['low'],
                df['close'],
                df['volume'],
                df['delim_5m'],
                count,
        )

        (
                df["open_15m"],
                df["high_15m"],
                df["low_15m"],
                df["close_15m"],
                df["volume_15m"]
        ) = cal.get_basic_candles(
                df['open'],
                df['high'],
                df['low'],
                df['close'],
                df['volume'],
                df['delim_15m'],
                count,
        )

        (
                df["open_15m_r"],
                df["high_15m_r"],
                df["low_15m_r"],
                df["close_15m_r"],
                df["volume_15m_r"]
        ) = cal.get_basic_candles_realtime(
                df['open'],
                df['high'],
                df['low'],
                df['close'],
                df['volume'],
                df['delim_15m'],
                count,
        )

        (
                df["open_30m"],
                df["high_30m"],
                df["low_30m"],
                df["close_30m"],
                df["volume_30m"]
        ) = cal.get_basic_candles(
                df['open'],
                df['high'],
                df['low'],
                df['close'],
                df['volume'],
                df['delim_30m'],
                count,
        )
        (
                df["open_30m_r"],
                df["high_30m_r"],
                df["low_30m_r"],
                df["close_30m_r"],
                df["volume_30m_r"]
        ) = cal.get_basic_candles_realtime(
                df['open'],
                df['high'],
                df['low'],
                df['close'],
                df['volume'],
                df['delim_30m'],
                count,
        )

        (
                df["open_1h"],
                df["high_1h"],
                df["low_1h"],
                df["close_1h"],
                df["volume_1h"]
        ) = cal.get_basic_candles(
                df['open'],
                df['high'],
                df['low'],
                df['close'],
                df['volume'],
                df['delim_1h'],
                count,
        )
        (
                df["open_1h_r"],
                df["high_1h_r"],
                df["low_1h_r"],
                df["close_1h_r"],
                df["volume_1h_r"]
        ) = cal.get_basic_candles_realtime(
                df['open'],
                df['high'],
                df['low'],
                df['close'],
                df['volume'],
                df['delim_1h'],
                count,
        )

        (
                df["open_1d"],
                df["high_1d"],
                df["low_1d"],
                df["close_1d"],
                df["volume_1d"]
        ) = cal.get_basic_candles(
                df['open'],
                df['high'],
                df['low'],
                df['close'],
                df['volume'],
                df['delim_1d'],
                count,
        )
        (
                df["open_1d_r"],
                df["high_1d_r"],
                df["low_1d_r"],
                df["close_1d_r"],
                df["volume_1d_r"]
        ) = cal.get_basic_candles_realtime(
                df['open'],
                df['high'],
                df['low'],
                df['close'],
                df['volume'],
                df['delim_1d'],
                count,
        )


        start = datetime.now()

        fast   =  7
        slow   = 80
        signal =  7
        df['macd_signal_1m'] = cal.get_macd_signal(
                df['close_1m'],
                df['delim_1m'],
                count, fast, slow, signal)
        # df['macd_signal_1m_r'] = cal.get_macd_signal_realtime(
        #         df['close_1m'],
        #         df['close_1m_r'],
        #         df['delim_1m'],
        #         count, fast, slow, signal)

        df['macd_signal_5m'] = cal.get_macd_signal(
                df['close_5m'],
                df['delim_5m'],
                count, fast, slow, signal)
        # df['macd_signal_5m_r'] = cal.get_macd_signal_realtime(
        #         df['close_5m'],
        #         df['close_5m_r'],
        #         df['delim_5m'],
        #         count, fast, slow, signal)

        df['macd_signal_15m'] = cal.get_macd_signal(
                df['close_15m'],
                df['delim_15m'],
                count, fast, slow, signal)
        # df['macd_signal_15m_r'] = cal.get_macd_signal_realtime(
        #         df['close_15m'],
        #         df['close_15m_r'],
        #         df['delim_15m'],
        #         count, fast, slow, signal)

        df['macd_signal_30m'] = cal.get_macd_signal(
                df['close_30m'],
                df['delim_30m'],
                count, fast, slow, signal)
        # df['macd_signal_30m_r'] = cal.get_macd_signal_realtime(
        #         df['close_30m'],
        #         df['close_30m_r'],
        #         df['delim_30m'],
        #         count, fast, slow, signal)

        df['macd_signal_1h'] = cal.get_macd_signal(
                df['close_1h'],
                df['delim_1h'],
                count, fast, slow, signal)
        # df['macd_signal_1h_r'] = cal.get_macd_signal_realtime(
        #         df['close_1h'],
        #         df['close_1h_r'],
        #         df['delim_1h'],
        #         count, fast, slow, signal)

        fast_1d   =  7
        slow_1d   = 80
        signal_1d =  7

        df['macd_signal_1d'] = cal.get_macd_signal(
                df['close_1d'],
                df['delim_1d'],
                count, fast_1d, slow_1d, signal_1d)
        # df['macd_signal_1d_r'] = cal.get_macd_signal_realtime(
        #         df['close_1d'],
        #         df['close_1d_r'],
        #         df['delim_1d'],
        #         count, fast_1d, slow_1d, signal_1d)

        # df['macd_osc_1d'] = cal.get_macd_oscillator(
        #         df['close_1d'],
        #         df['delim_1d'],
        #         count, fast_1d, slow_1d, signal_1d)
        # df['macd_osc_1d_r'] = cal.get_macd_oscillator_realtime(
        #         df['close_1d'],
        #         df['close_1d_r'],
        #         df['delim_1d'],
        #         count, fast_1d, slow_1d, signal_1d)


        end = datetime.now()
        diff = (end - start).total_seconds()
        speed = count / diff
        print("[ macd signal c ]")
        print(f"elapsed time : {diff: 12.2f} s")
        print(f"speed        : {speed: 12.2f}")
        print()
        print()




    # ret_df = df.loc[
    #     #:,
    #     (df['datetime'] >= datetime(2022, 2, 27, 8, 30)) & \
    #             (df['datetime'] <= datetime(2022, 2, 28, 10)),
    #     (
    #         'close',
    #         'close_1d',
    #         'close_1d_r',
    #         'macd_signal_1d',
    #         'macd_signal_1d_r',
    #         'macd_osc_1d',
    #         'macd_osc_1d_r',
    #     )
    # ]
    # print(ret_df[:80])
    #print(ret_df[:25])



#    with open("python_result.csv", "w") as f:
#        print(ret_df, file = f)

    # end = datetime.now()
    # diff = (end - global_start).total_seconds()
    # speed = count / diff
    # print("[ total ]")
    # print(f"elapsed time : {diff: 12.2f} s")
    # print(f"speed        : {speed: 12.2f}")
    # print()
    # print()




if __name__ == "__main__":
    test = TestMacd()
    test.test_example()

