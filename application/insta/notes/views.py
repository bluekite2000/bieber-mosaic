from django.utils import simplejson
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError
from django.middleware.csrf import  get_token
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.conf import settings

import os
from pymos.core import build_mosaic




	


def upload_page(request):
	ctx=RequestContext(request,{
	'csrf_token':get_token(request),
	})	
	return render_to_response( 'upload_page.html', ctx )

def write_to_disk(uploaded,filename,raw_data):
	try:
		from io import FileIO, BufferedWriter
		with BufferedWriter(FileIO(filename,"w")) as dest:
			if raw_data:
				foo=uploaded.read(1024)
				while foo:
					dest.write(foo)
					foo=uploaded.read(1024)
			else:
				for c in uploaded.chunks():
					dest.write(c)
	except IOError:
		return False
		

	
	
def process_upload(uploaded,filename,raw_data):
	#import pdb
	#pdb.set_trace()
	path=settings.MEDIA_ROOT+'/input/'

	input_pic=path+filename
	write_to_disk(uploaded,	input_pic,raw_data)
	output_pic=path+'mosaic_'+filename

	build_mosaic(input_path=input_pic,output_path=output_pic,collection_path=path,zoom=10,fuzz=100,thumb_size=30,new_colormap=True)
	return True
	
		
def ajax_upload (request):
	if request.method == "POST":
		if request.is_ajax():
			upload=request
			is_raw=True
			try:
				filename=request.GET['qqfile']
				success=process_upload(upload,filename,is_raw)
			except KeyError:
				return HttpResponseBadRequest("Ajax request not valid")
		else:
			is_raw=False
			if len(request.FILES)==1:
				upload=request.FILES.value()[0]
			else:
				raise Http404("Bad upload")
			filename=upload.name
		
		
		
		import json
		ret_json={'success':success,}
		return HttpResponse(json.dumps(ret_json))