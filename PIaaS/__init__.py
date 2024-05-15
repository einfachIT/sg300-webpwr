from flask import Flask, render_template, request
import os
import subprocess

app = Flask(__name__)
#app.config.from_object('PIaaS.config.DefaultConfig')
app.config.from_object('config.DefaultConfig')
#print(app.config)


@app.route('/')
def index():
  pwr_ports = []
  for n in range (49, 57):
    port_num = len(pwr_ports) + 1
    pwr_port = {
      'id' : n,  
      'port_num' : port_num,
      'state' :  get_state(n)
    }
    pwr_ports.append(pwr_port)
    print(pwr_ports)
  return render_template('index.html', pwr_ports=pwr_ports)
  
@app.route('/state/<port_num>')
def get_state(port_num):
  print(app.config)
  cmd = 'snmpget -v 2c -c ' + app.config['SNMP_COMMUNITY'] + ' ' + app.config['SWITCH_IP'] + ' 1.3.6.1.2.1.105.1.1.1.3.1.' + str(port_num)
  print(cmd)
  proc = subprocess.Popen([cmd], stdout=subprocess.PIPE, shell=True)
  (out, err) = proc.communicate()
  out = out.decode('utf-8')
  print(out)
  if out.endswith('1\n'):
    state = 'an'
  elif out.endswith('2\n'):
    state = 'aus'
  else:
    state = 'error'
  return state

@app.route('/turn_on/<port_num>', methods = ['GET', 'POST'])
def turn_on(port_num):
  cmd = 'snmpset -v 2c -c ' + app.config['SNMP_COMMUNITY'] + ' ' + app.config['SWITCH_IP'] + ' 1.3.6.1.2.1.105.1.1.1.3.1.' + str(port_num) + ' i 1'
  proc = subprocess.Popen([cmd], stdout=subprocess.PIPE, shell=True)
  (out, err) = proc.communicate()
  out = out.decode('utf-8')
  if out.endswith('1\n'):
    state = "ok"
  else:
    state = "error"
  print(request.url)
  return state

@app.route('/turn_off/<port_num>', methods = ['GET', 'POST'])
def turn_off(port_num):
  cmd = 'snmpset -v 2c -c ' + app.config['SNMP_COMMUNITY'] + ' ' + app.config['SWITCH_IP'] + ' 1.3.6.1.2.1.105.1.1.1.3.1.' + str(port_num) + ' i 2'
  proc = subprocess.Popen([cmd], stdout=subprocess.PIPE, shell=True)
  (out, err) = proc.communicate()
  out = out.decode('utf-8')
  if out.endswith('2\n'):
    state = "ok"
  else:
    state = "error"
  return state

