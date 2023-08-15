from django.test import TestCase

# Create your tests here.

import requests
import xml.etree.ElementTree as ET


headers = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
'Accept-Encoding':'gzip, deflate',
'Accept-Language':'en-US,en;q=0.8',
'Cache-Control':'max-age=0',
'Connection':'keep-alive',
'Content-Length':'112',
'Content-Type':'application/x-www-form-urlencoded',
'User-Agent':"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.81 Safari/537.36",}

xml = """<?xml version="1.0" encoding="UTF-8"?>
            <!DOCTYPE protocol SYSTEM "https://www.paygate.co.za/payxml/payxml_v4.dtd">
                <protocol ver="4.0" pgid="10011013800" pwd="test">
                    <authtx cref="ABCX1j64564" cname="Patel Sunny" cc="5200000000000015" exp="032022" budp="0" amt="10000" cur="ZAR" cvv="123" 
                        rurl="http://localhost/pg_payxml_php_final.php" nurl="http://localhost/pg_payxml_php_notify.php" />
                </protocol>
      """
headers = {'Content-Type': 'application/xml'} # set what your server accepts

response = requests.post('https://www.paygate.co.za/payxml/process.trans', data=xml, headers=headers).text

tree = ET.fromstring(response)
print(tree)


# for node in tree.iter('authrx'):
#     sdesc = node.attrib.get('sdesc') # STATUS MESSAGE
#     tid = node.attrib.get('tid') # TRANSACTION ID
#     cref = node.attrib.get('cref') # REFERENCE NO. like invoice_no or sale_order_no
#     auth = node.attrib.get('auth')
#     rdesc = node.attrib.get('rdesc') # Result Code description.
#     print (sdesc, tid, cref)