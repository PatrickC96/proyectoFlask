from flask import Flask, make_response
#from flask import render_template
import matplotlib.pyplot as plt
import io
import base64

import numpy as np
import matplotlib.animation as animation

app = Flask(__name__)

@app.route('/plot')
def build_plot():

    img = io.BytesIO()

    y = [1,2,3,4,5]
    x = [0,2,1,3,4]
    plt.plot(x,y)
    plt.savefig(img, format='png')
    img.seek(0)

    plot_url = base64.b64encode(img.getvalue()).decode()

    return '<img src="data:image/png;base64,{}">'.format(plot_url)

if __name__ == '__main__':
    app.debug = True
    app.run()
