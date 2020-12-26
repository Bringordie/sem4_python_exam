import pandas as pd

def get_streamer_info_from_CSV_top1000():
    df1 = pd.read_csv('data/streamers1-100.csv')
    df2 = pd.read_csv('data/streamers101-200.csv')
    df3 = pd.read_csv('data/streamers201-300.csv')
    df4 = pd.read_csv('data/streamers301-400.csv')
    df5 = pd.read_csv('data/streamers401-500.csv')
    df6 = pd.read_csv('data/streamers501-600.csv')
    df7 = pd.read_csv('data/streamers601-700.csv')
    df8 = pd.read_csv('data/streamers701-800.csv')
    df9 = pd.read_csv('data/streamers801-900.csv')
    df10 = pd.read_csv('data/streamers901-1000.csv')
    frames = [df1, df2, df3, df4, df5, df6, df7, df8, df9, df10]
    combined = pd.concat(frames)
    x_train = combined[['Watch time', 'Stream time', 'Peak viewers', 'Average viewers']]
    y_train = combined['Followers']
    
    return x_train, y_train

def get_streamer_info_from_CSV_9_10000():
    df1 = pd.read_csv('data/streamers9001-9100.csv')
    df2 = pd.read_csv('data/streamers9101-9200.csv')
    df3 = pd.read_csv('data/streamers9201-9300.csv')
    df4 = pd.read_csv('data/streamers9301-9400.csv')
    df5 = pd.read_csv('data/streamers9401-9500.csv')
    df6 = pd.read_csv('data/streamers9501-9600.csv')
    df7 = pd.read_csv('data/streamers9601-9700.csv')
    df8 = pd.read_csv('data/streamers9701-9800.csv')
    df9 = pd.read_csv('data/streamers9801-9900.csv')
    df10 = pd.read_csv('data/streamers9901-10000.csv')
    frames = [df1, df2, df3, df4, df5, df6, df7, df8, df9, df10]
    combined = pd.concat(frames)
    x_train = combined[['Watch time', 'Stream time', 'Peak viewers', 'Average viewers']]
    y_train = combined['Followers']
    
    return x_train, y_train