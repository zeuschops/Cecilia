## Start the initial connection and database handler
from Database.DatabaseHandler import DatabaseHandler
import os

db_handler = DatabaseHandler('database-test.sqlite')
if 'database.sqlite' in os.listdir('./'):
    db_handler = DatabaseHandler('database.sqlite')

## Start the flask API portion of this application
from flask import Flask, Response, request
import json

app = Flask(__name__)

@app.route('/')
def home():
    return Response(status=403)

@app.route('/get/<codename>/<data>')
def get_by_codename(codename:str, data:str):
    return db_handler.fetch_from_codename(codename, [data])

@app.route('/get/codenames')
def get_all_codenames():
    return db_handler.fetch_codenames()

@app.route('/post/new-codename', methods=['POST'])
def add_endpoint():
    codename = ""
    url = ""
    request_headers = {}
    post_req_json = list(request.form.to_dict(flat=False))[0].replace("'", '"')
    post_req_json = json.loads(post_req_json)
    if 'url' in list(post_req_json):
        url = post_req_json['url']
    if 'codename' in list(post_req_json):
        codename = post_req_json['codename']
    token_name = ''
    for i in list(post_req_json):
        if 'token' in i:
            request_headers = post_req_json[i]
    if len(url) == 0 or len(codename) == 0 or len(list(request_headers)) == 0:
        return {}
    return db_handler.add_codename(codename, url, request_headers)

@app.route('/ipsw/<iphone_name>/latest')
def ios_request(iphone_name:str) -> dict:
    return db_handler.fetch_latest_ipsw(iphone_name)

@app.route('/ipsw/<iphone_name>/<ios_version>')
def ios_version_request(iphone_name:str, ios_version:str) -> dict:
    return db_handler.fetch_ipsw_version(iphone_name.replace('-', ' '), ios_version)

@app.route('/ipsw/devices')
def ios_fetch_devices():
    return db_handler.fetch_all_ipsw_devices()

## SumReel endpoints -- because I want 1 API to rule them all..
@app.route('/riot/account/by-name/<region>/<name>')
def riot_account_by_name(region:str, name:str):
    return db_handler.fetch_riot_account_by_name(name)

#Regions:
#   NA1 - https://na1.api.riotgames.com
#   EUW - https://euw1.api.riotgames.com

#@app.route('/riot/account/by-accountId/<region>/<accountId>')
#<region>/lol/summoner/v4/summooners/by-account/<accountId>

#@app.route('/riot/matches/by-id/<region>/<id>')
#<region>/lol/match/v4/matches/<id>

#@app.route('/riot/matchlist/by-account/<region>/<accountId>')
#<region>/lol/match/v4/matchlists/by-account/<accountId>

#@app.route('/riot/news')


#This is a bit silly, but I need the IP address of the local device that's a cross-platform solution. I also need to focus on one specific network use-case.
import subprocess
import os
import socket

if __name__ == "__main__":
    developer_only_mode = False
    port = 20090

    #context = ('austinbennett.dev.crt', 'austinbennett.dev.pem')
    context = None

    if developer_only_mode:
        app.run(host='127.0.0.1', port=port, ssl_context=context)
    elif 'nt' in os.name:
        sp = str(subprocess.run('ipconfig', capture_output=True).stdout)[2:-1].replace('\\r', '').replace('\\n', '\n').replace('\n\n\n', '\n').replace('\n\n', '\n')
        ip_addr = sp[sp.index('IPv4 Address'):sp.index('Subnet')].split(': ')[1].split('\n')[0]
        app.run(host=ip_addr, port=port, ssl_context=context)
    else:
        ip_addr = socket.gethostbyname(socket.gethostname())
        app.run(host=ip_addr, port=port,ssl_context=context)
