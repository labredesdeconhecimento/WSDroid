# coding: utf-8

from flask import request, jsonify, abort
import psutil
import subprocess
import re

def usage():
    if request.method == 'GET':
    
        resp = jsonify(get_index())
        resp.status_code = 200
        
        return resp
        
        
def list_hd(index=None):

    if request.method == 'GET':
        if index:
            dic = get_index().get('hardDisk').get(index)
            if not dic:
                abort(404)
        else:    
            dic = get_index().get('hardDisk')
            
        dic.update({'status' : 200})    
        resp = jsonify(dic)
        resp.status_code = 200
        
        return resp
        
    else:
        abort(404)


def list_mem():

    if request.method == 'GET':
        dic = get_index().get('memory')
        dic.update({'status' : 200})
        
        resp = jsonify(dic)
        resp.status_code = 200
        
        return resp
    else:
        abort(404)
    
def list_cpu():

    if request.method == 'GET':
        dic = get_index().get('cpu')
        dic.update({'status' : 200})
        
        resp = jsonify(dic)
        resp.status_code = 200
        
        return resp
    else:
        abort(404)

def list_network():

    if request.method == 'GET':    
        dic = get_index().get('netw')
        dic.update({'status' : 200})
        
        resp = jsonify(dic)
        resp.status_code = 200
        
        return resp
    else:
        abort(404)
               

def list_network(index=None):

    if request.method == 'GET':
        if index:
            dic = get_index().get('netw').get(index)
            if not dic:
                abort(404)
        else:    
            dic = get_index().get('netw')
            
        dic.update({'status' : 200})    
        resp = jsonify(dic)
        resp.status_code = 200
        
        return resp
    else:
        abort(404)
            
              
def get_index():

    dic_ret = {}
    dic_ret.update({'status' : 200})     
    
    # Coleta informação de memória
    mem = psutil.virtual_memory()
    dic_ret.update({ 'memory' : mem._asdict() })
        
    # Coleta informação do HD
    hd = {}
    for i in psutil.disk_partitions():
        aux = {}
        aux.update(i._asdict())
        aux.update(psutil.disk_usage(i.mountpoint)._asdict())
        hd.update({ i.device.rsplit('/',1)[1] : aux})
            
    dic_ret.update({'hardDisk' : hd})
        
    # Coleta informação do CPU
    cpu = {}
    cpu.update(psutil.cpu_times()._asdict())
    cpu.update({'percent' : psutil.cpu_percent()})
        
    dic_ret.update({'cpu' : cpu})
        

    # Coleta so dados da rede
    dic_main = {}
        
    net = psutil.network_io_counters(pernic=True)
    
    for i in net.iterkeys():
        dic = {}
        dic.update(net.get(i)._asdict())
        
        try:
            addr = subprocess.check_output(["/sbin/ifconfig", i])
            ip = re.search(r'inet end.: (.*?) .*Masc:(.*)', addr, re.M).group(1)
            mask = re.search(r'inet end.: (.*?) .*Masc:(.*)', addr, re.M).group(2)
            dic.update({'ipv4' : ip, 'masc' : mask})
            
        except:
            pass
        
        dic_main.update({i : dic})
    
    dic_ret.update({'netw' : dic_main})

    return dic_ret
