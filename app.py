from flask import Flask, render_template, request
import numpy as np
from scipy.stats import norm

app = Flask(__name__)

def black_scholes(S, K, T, r, sigma, option_type):
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    if option_type == 'call':
        option_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    elif option_type == 'put':
        option_price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    else:
        option_price = None
    
    return option_price

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    S = float(request.form['S'])
    K = float(request.form['K'])
    T = float(request.form['T'])
    r = float(request.form['r'])
    sigma = float(request.form['sigma'])
    option_type = request.form['option_type']
    
    option_price = black_scholes(S, K, T, r, sigma, option_type)
    
    return render_template('result.html', option_price=option_price)

if __name__ == '__main__':
    app.run(debug=True)
