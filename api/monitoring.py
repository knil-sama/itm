from flask import make_response
import flask_restful
import matplotlib
import matplotlib.pyplot as plt
import datetime as dt
import matplotlib.dates as md
import io
import api

class Monitoring(flask_restful.Resource):
    def get(self):
        """
        Returns:
           Stats of succes and error
        """
        result_cursor = api.CLIENT["image_bank"].monitoring.find({})
        list_result = list(result_cursor)
        list_date = [result["execution_date"] for result in list_result]
        list_success = [result["success"] for result in list_result]
        list_error= [result["error"] for result in list_result]
        if list_date:
            plt.rcParams['figure.figsize'] = [15,10]
            x=md.date2num(list_date)
            fig, ax=plt.subplots()
            ax.xaxis_date()
            ax.hist(x,weights=list_error, histtype='bar', alpha= 0.5,label="error")
            ax.hist(x,weights=list_success, histtype='bar', alpha= 0.5, label="sucess")
            xtformat = md.DateFormatter('%H:%M:%S')
            xtinter = md.MinuteLocator(byminute=[0], interval=1)
            xtmin = md.MinuteLocator(byminute=[30], interval=1)
            ax.xaxis.set_major_formatter(xtformat)
            ax.xaxis.set_major_locator(xtinter)
            ax.xaxis.set_minor_locator(xtmin)
            ax.set_xlim([min(x),max(x)])
            plt.legend(loc='upper right')
            plt.xticks(x)
            fake_file = io.BytesIO()
            plt.savefig(fake_file, format="png", dpi=fig.dpi)
            response=make_response(fake_file.read())
            response.headers.set('Content-Type', 'image/png')
            response.headers.set(
                'Content-Disposition', 'attachment', filename='monitoring.png')
            return response
        else:
            return {"message":"Nothing to monitor yet"}, 200
