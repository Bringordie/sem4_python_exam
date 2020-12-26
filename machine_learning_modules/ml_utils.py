import pandas as pd
from plotly.offline import iplot
import plotly.graph_objects as go
import numpy as np
from sklearn.preprocessing import StandardScaler

def performance_summary(model, x_test, y_test):
    
    y_hat=model.predict(x_test)
    
    df_summary=pd.DataFrame(y_hat, columns=["y_hat"])
    df_summary["y_true"]=y_test
    df_summary["abs_error"]=np.abs(df_summary.y_true-df_summary.y_hat)
    df_summary["error"]=df_summary.y_hat-df_summary.y_true
    df_summary["relative_error"]= df_summary["error"]/df_summary.y_true
    df_summary["relative_abs_error"]= df_summary["abs_error"]/df_summary.y_true
    
    share_within_5pct=(df_summary.query("relative_abs_error<0.05").shape[0]/df_summary.shape[0])*100
    
    print("{:.2f}% : Share of forecasts within 5% absolute error\n".format(share_within_5pct))
    print("{:.0f}   : Mean absolute error \n".format(df_summary.abs_error.mean()))
    print("{:.2f}% : Mean absolute percentage error\n".format(df_summary.relative_abs_error.mean()*100))

def plot_loss(history, starting_epoch,previous_val_loss, min_loss, max_loss, plot_name):
    
        trace0=go.Scatter(
                y=history.history['loss'][starting_epoch:],
                x=history.epoch[starting_epoch:],
                mode='lines',
                marker=dict(
                color="blue",
                size=5,
                opacity=0.5
                ),
                name="Training Loss"
            )

        trace1=go.Scatter(
                y=history.history['val_loss'][starting_epoch:],
                x=history.epoch[starting_epoch:],
                mode='lines',
                marker=dict(
                color="red",
                size=5,
                opacity=0.5
                ),
                name="Validation Loss"
            )

        data=[trace0, trace1]
        figure=go.Figure(
            data=data,
            layout=go.Layout(
                title=plot_name,
                yaxis=dict(title="Loss",range=(min_loss,max_loss)),
                xaxis=dict(title="Epoch",range=(starting_epoch,history.epoch[-1])),
                legend=dict(
                    x=0.57,
                    y=1,
                    traceorder="normal",
                    font=dict(
                        family="sans-serif",
                        size=12,
                        color="black"
                    ),
                bgcolor=None,

            )))
        iplot(figure)

def predict_followers(model, watch_time, stream_time, peak_viewers, average_viewers):
    data = {'Watch time': [watch_time], 'Stream time': [stream_time], 'Peak viewers': [peak_viewers], 'Average viewers': [average_viewers]}
    data_arr = pd.DataFrame(data, columns = ['Watch time', 'Stream time', 'Peak viewers', 'Average viewers']).to_numpy()
    scaler = StandardScaler()
    data_arr_trans = scaler.fit_transform(data_arr)
    q = model.predict(data_arr_trans)
    return int(q[0])
