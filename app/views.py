from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
import pickle
import numpy as np
import pandas as pd



model_path_odis='models/pipeodismen.pkl'
pipe_odis=pickle.load(open(model_path_odis,'rb'))

def t20_pridict(request):
    if request.method=='POST':
       batting_team=request.POST['batting_team']
       bowling_team=request.POST['bowling_team']
       city=request.POST['city']
       current_score=request.POST['current_score']
       overs=request.POST['overs']
       wickets=request.POST['wickets']
       last_ten=request.POST['last_ten']
       fields=[batting_team,bowling_team,city,current_score,overs,wickets,last_ten]
       if batting_team==bowling_team:
           return render(request,'index.html',{'Error':'Batting Team And Bowling Team Can not Be same'})
       if not None in fields:
            overs=float(overs)
            if overs>=10 and overs<=49:
                wickets=float(wickets)
                current_score=float(current_score)
                last_ten=float(last_ten)
                balls_left=300-(overs*6)
                wickets_left=10-wickets
                crr=current_score/overs
                input=pd.DataFrame([[batting_team,bowling_team,city,current_score,balls_left,wickets_left,crr,last_ten]],columns=['batting_team','bowling_team','city','current_score','balls_left','wickets_left','crr','last_ten'])
                result=pipe_odis.predict(input)[0]
                result=np.round(result,0)
                result_dict={'Batting_team':batting_team,
                             'Bowling_team':bowling_team,
                             'Current_Runs':current_score,
                             'overs':overs,
                             'wickets':wickets,
                             'result':result}
                return render(request,'index.html',{'dict':result_dict})
            else:
                return render(request,'index.html',{'Error':'Overs Must be Between 10 and 49'}) 
       return render(request,'index.html',{'Error':'Please Type Correct Input'})          
    return render(request,'index.html')