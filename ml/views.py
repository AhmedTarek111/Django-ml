from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
import pandas as pd
import pickle
from .models import Iris
from .forms import IrisForm
from .serializers import IrisSerializers


def iris_prediction(request):
    if request.method == "POST":
        form = IrisForm(request.POST)
        if form.is_valid():    
            form.save(commit=False)
            sepal_length=form.cleaned_data['sepal_length']
            sepal_width=form.cleaned_data['sepal_width']
            petal_length=form.cleaned_data['petal_length']
            petal_width=form.cleaned_data['petal_width']
            model= pd.read_pickle("model.pickle")
            prediction = model.predict([[sepal_length,sepal_width,petal_length,petal_width]])
            result = prediction[0]  
            form.instance.classifcation =result 
            form.save()        
            return render(request ,'iris.html' , {'form':form,'result':result})
            
        
    else:
        form = IrisForm()
    return render(request ,'iris.html' , {'form':form})

# api 
class IrisPredictionAPI(GenericAPIView):
    serializer_class =IrisSerializers
    def post(self,request,**kwargs):
        
            sepal_length=request.data['sepal_length']
            sepal_width=request.data['sepal_width']
            petal_length=request.data['petal_length']
            petal_width=request.data['petal_width']
            
            model= pd.read_pickle("model.pickle")
            prediction = model.predict([[sepal_length,sepal_width,petal_length,petal_width]])
            result = prediction[0]  
            
            Iris.objects.create(
                sepal_length=sepal_length,
                sepal_width=sepal_width,
                petal_length=petal_length,
                petal_width=petal_width,
                classifcation = result
            )
            return Response({'result': result})