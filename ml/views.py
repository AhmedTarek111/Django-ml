from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
import pandas as pd
import pickle
from .models import Iris
from .forms import IrisForm


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


