#!/bin/bash
#!coding=utf8
import os

import tornado.ioloop
import tornado.web
from tornado import httpclient
from tornado.escape import json_decode, json_encode
from fnmatch import fnmatch

remote_addr=os.getenv("remote_addr","http://127.0.0.1:4440")

authtoken=os.getenv("authtoken", "authtoken")

pswd=os.getenv("pswd", "pswd")

request_url="%s/api/1/job/{job_id}/run"%(remote_addr)


handler_map={
	# git_ssh_url:{refs: job_id}
	"git@gitee.com:xxx/xxxxxxxx.git":{ 
		"refs/*": "xxxx-xxxx-xxxx-xxxx-xxxxxxx"
	},

}

def lookup(git_ssh_url, ref):
	"""
	根据 git_ssh_url， ref + handler_map 找到对应的job_id
	返回值：
		None  找不到
		string 找到了
	"""
	if git_ssh_url in handler_map:
		for ref_pat in handler_map[git_ssh_url]:
			if fnmatch(ref, ref_pat):
				return handler_map[git_ssh_url][ref_pat]

	return None


class GiteeHookHandler(tornado.web.RequestHandler):
	@tornado.gen.coroutine
	def post(self):
		body = json_decode(self.request.body)
		if body["hook_name"] == "push_hooks":
			print("push")
			print(body["ref"])
			print(body["repository"]["git_ssh_url"])
			print(body["password"])

			if body["password"] != pswd:
				self.write("password not match")
				return

			job_id = lookup(body["repository"]["git_ssh_url"], body["ref"])
			if not job_id:
				self.write("NotFound\n")
				return

			http_client = httpclient.AsyncHTTPClient()
			try:
				# self.request.uri
				response = yield http_client.fetch(request_url.format(job_id=job_id), 
					method='POST', 
					body=json_encode({}),
					headers={'Content-Type':'text/xml;charset=UTF-8', "X-Rundeck-Auth-Token":authtoken})
				self.write(response.body)
			except httpclient.HTTPError as e:
				# HTTPError is raised for non-200 responses; the response
				# can be found in e.response.
				self.write("Error: " + str(e))
			except Exception as e:
				# Other errors are possible, such as IOError.
				self.write("Error: " + str(e))
			http_client.close()

		
class MainHandler(tornado.web.RequestHandler):
	def get(self):
		self.write("Hello, World!")
		
def make_app():
    return tornado.web.Application([
		(r"/", MainHandler),
		(r"/git/hooks", GiteeHookHandler)
	])

if __name__ == "__main__":
	app = make_app()
	app.listen(3000, xheaders=True)
	tornado.ioloop.IOLoop.current().start()
