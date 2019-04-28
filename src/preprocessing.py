import pandas as pd
from pipeline import Procedure
from datetime import datetime
import numpy as np
from chainer.datasets import TupleDataset



class PreprocessingProcedure2D(Procedure):
    
    def run(self, x):
        ohlc_dict = {
            'Open':'first',
            'High':'max',
            'Low':'min',
            'Close':'last',
            'Volume_(Currency)':'sum'
        }
        return self.preprocessing(x, ohlc_dict)

    def preprocessing(self, df, how):
        dataset = []
        df.loc[:, "datetime"] = pd.to_datetime(df['Timestamp'], unit='s')
        df_d = df.set_index("datetime")

        df_accept = df_d.loc[datetime(2013, 8, 1):]
        df_b_a = df_accept.bfill()
        df_resampled = df_b_a.resample('60min', how=how)
        X = []
        y = []
        for n in range(100):
            x_base = df_resampled.iloc[n:n+60, :]
            x_base = x_base - x_base.head(1).iloc[0]
            min_date = x_base.index[0]
            max_date = x_base.index[-1]
            unit = df_b_a.loc[min_date:max_date]
            unit_normalize = unit - unit.head(1).iloc[0]
            x = []
            x.append(x_base)
            # x.append(unit_normalize.resample('1min', how=how))
            # x.append(unit_normalize.resample('5min', how=how))
            # x.append(unit_normalize.resample('15min', how=how))
            # x.append(unit.resample('30min', how=how))
            y.append(df_resampled["Close"].iloc[n+61] - unit["Close"].iloc[0])
            X.append(x_base.values.flatten())
        X = pd.concat(X)
        return X, y
            
