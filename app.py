from flask import Flask, render_template, request
import ipaddress

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    cidr_input = request.form['cidr']
    try:
        ip1,temp=cidr_input.split("/")
        network = ipaddress.IPv4Network(cidr_input, strict=False)
        network_address = str(network.network_address)
        broadcast_address = str(network.broadcast_address)
        subnet_mask = str(network.netmask)
        ip_class = get_ip_class(network)
        return render_template('result.html',ipaddr=ip1, 
                               network=network_address, 
                               broadcast=broadcast_address, 
                               subnet=subnet_mask,
                               ip_class=ip_class)
    except ValueError:
        return "Invalid CIDR notation. Please enter a valid CIDR."

def get_ip_class(network):
    first_octet = int(str(network.network_address).split('.')[0])
    if 1 <= first_octet <= 126:
        return 'A'
    elif 128 <= first_octet <= 191:
        return 'B'
    elif 192 <= first_octet <= 223:
        return 'C'
    elif 224 <= first_octet <= 239:
        return 'D'
    elif 240 <= first_octet <= 255:
        return 'E'

if __name__ == '__main__':
    app.run(debug=True)
