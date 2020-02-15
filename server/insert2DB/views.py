from django.http import HttpResponse
from .models import Data
from django.shortcuts import render
from django.utils import timezone
from .oracle import oracle, oracleTrain

#For getting all items in data collection
def index(request):
	latest_data_list = Data.objects.order_by('-pubDate')
	output = ', '.join([a.schoolName for a in latest_data_list])
	return HttpResponse(output)

#Getting a single schools data in collection
def singleData(request, schoolName, departmentName):
	data = Data.objects.get(schoolName=schoolName, departmentName=departmentName)
	return HttpResponse(data)

#Upload new data for a school in collection
def uploadData(request):
	markovModel = oracleTrain(request)
	newData = Data(data=request.POST.get('data'), schoolName=request.POST.get('schoolName'), departmentName=request.POST.get('departmentName'), markovModel=markovModel, pubDate=timezone.now())
	newData.save()
	return HttpResponse(newData)

#Send a schools data to the oracle
def testOracle(request):
	output = oracle(request)
	return HttpResponse(output)
