from flask import Flask, render_template, request, url_for, redirect
from threading import Thread
from napalm import get_network_driver
from datetime import datetime
from getconfig import getConfig
from sshInfo import sshInfo
from validateIP import check_ip
from connectivity import ping_check
from lab4main import ospfConfig

ospf_configurations = {}

def create_app():
    app=Flask(__name__)

    @app.route('/')
    def index():
        return render_template('index.html', getConfig='/get-config', ospfConfig='/ospf-config', diffConfig='/diff-config')

    @app.route('/get-config')
    def get_Config():
        output = getConfig('sshInfo.json')
        return render_template('getconfig.html', index='/', ospfConfig='/ospf-config', diffConfig='/diff-config', output=output)

    @app.route('/ospf-config', methods=['GET','POST'])
    def ospf_Config():
        if request.method == 'POST':

            router_name = request.form['router_name']
            ip = request.form['ip']
            username = request.form['username']
            password = request.form['password']
            ospf_process_id = request.form['ospf_process_id']
            ospf_area_id = request.form['ospf_area_id']
            loopback_ip = request.form['loopback_ip']
            
            ospf_configurations[router_name] = {
                'username': username,
                'password': password,
                'ip': ip,
                'ospf_process_id': ospf_process_id,
                'ospf_area_id': ospf_area_id,
                'loopback_ip': loopback_ip
            }
            err_message = check_ip(loopback_ip)
            if not err_message:
                del ospf_configurations[router_name]
                return render_template('ospfconfig.html', dic = ospf_configurations, index='/', push='/push-ospf-config', err_message="Invalid Loopback IP address!")
            else:
                return render_template('ospfconfig.html', dic = ospf_configurations, index='/', push='/push-ospf-config')

        return render_template('ospfconfig.html', dic = ospf_configurations, index='/')

    @app.route('/push-ospf-config')
    def push_Config():
        # ospf_configurations = sshInfo('ospf.json')
        threads = []
        for router_conf in ospf_configurations.values():
            thread = Thread(target=ospfConfig, args=(router_conf,))
            threads.append(thread)
            thread.start()
        
        for t in threads:
            t.join()
            
        return 'idk'
        

    @app.route('/diff-config')
    def diff_Config():
        return render_template('diffconfig.html', index='/')

    @app.errorhandler(405)
    @app.errorhandler(404)
    def errorpage(e):
        return("Oops, something went wrong!")
    
    return app
    
def main():
    app = create_app()
    app.debug = True
    app.run(host='127.0.0.1', port=50000)

if __name__=='__main__':
    main()