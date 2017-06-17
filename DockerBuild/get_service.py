#!python

import os
import urllib
import urllib2
import json
import time
import base64
import string
import sys

apiname = os.environ.get('RANCHER_USER')
apikey = os.environ.get('RANCHER_PASSWORD')
apiendpoint = os.environ.get('RANCHER_ENDPOINT')

if len(sys.argv) != 2:
	print("must have 1 argument")
	exit(1)

targetstack = sys.argv[1]

if apiname == '':
	print("error: RANCHER_USER is empty")
	exit(1)
if apikey == '':
	print("error: RANCHER_PASSWORD is empty")
	exit(1)
if apiendpoint == '':
	print("error: RANCHER_ENDPOINT is empty")
	exit(1)
if targetstack == '':
	print("error: TARGET_SERVICE is empty, TARGET_SERVICE = 'stack-name'")
	exit(1)

if apiendpoint[-1] !='/':
        apiendpoint += '/'
	
print("API-USERNAME: " + apiname)
print("API-KEY: " + apikey)
print("API-ENDPOINT: " + apiendpoint)
print("TARGET-STACK: " + targetstack)

ip_list = []
 
def list_all_dict(dict_a):
	if isinstance(dict_a,dict): 
		for x in range(len(dict_a)):
            		key = dict_a.keys()[x]
            		value = dict_a[key]
			if key.startswith("feidai.entrypoint"):
				print"%s : %s" %(key,value)
				return True

            		if(list_all_dict(value) == True):
				return True

def get_service_desc_by_label(name, key, endpoint, stack):
	credential = urllib.urlencode({"username" : name, "password" : key})
	request = urllib2.Request(endpoint + "environments?" + credential)
	base64key = base64.encodestring('%s:%s' % (apiname, apikey)).replace('\n', '')
	request.add_header("Authorization", "Basic %s" % base64key)
	try:
		response = urllib2.urlopen(request)
	except IOError, e:
		print("Get stack info error: " + str(e.code))
		return null
	response = response.read()
	data = json.loads(response)

	if os.path.exists(r'public_ip.txt'):
		os.remove('public_ip.txt')	

	for sk in data["data"]:
		if sk["name"] == stack:
			request = urllib2.Request(sk["links"]["services"] + "?" + credential)
			request.add_header("Authorization", "Basic %s" % base64key)
			try:
				response = urllib2.urlopen(request)
			except IOError, e:
				print("Get service info error: " + str(e.code))
				return null
			response = response.read()
			data = json.loads(response)


			for svc in data["data"]:
			#	print "svc ---------" + str(svc)
				config = svc["launchConfig"]
			#	if(list_all_dict(config) == True):
				endpoint = svc["publicEndpoints"]
				if not endpoint:
					continue


			#	print "endpoint ----------"  + str(endpoint)
				for endpointitem in endpoint:
					ip_list = str("%s:%s" %(endpointitem["ipAddress"], endpointitem["port"]))
					print "ip_list ==================================" + str(ip_list)

					f=open('public_ip.txt','a')
					print >>f,ip_list
					f.close()
			break


get_service_desc_by_label(apiname, apikey, apiendpoint, targetstack)
