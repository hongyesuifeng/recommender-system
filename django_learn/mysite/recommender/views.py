from django.shortcuts import render
import subprocess


#from . import slopeone, userbased, itembased, svd, svdpp
#监听按钮的click事件，监听到了就ajax请求特定的接口
#接口在urls.py中配置好，映射到views.py中写好的方法
    
def recommender(request):
    title1 = "算法初始化"
    UserBased = 'UserBased'
    SlopeOne = 'SlopeOne'
    ItemBased = 'ItemBased'
    SVD = 'SVD'
    SVDPP = 'SVDPP'
    title21 = '预测用户'
    predict = '开始预测'
    title22 = '结果展示:'
    title31 = '计算误差'
    MAE = 'MAE'
    return render(request, 'recommender/recommender.html', {'title1': title1, 'UserBased':
        UserBased, 'SlopeOne': SlopeOne, 'ItemBased': ItemBased, 'SVD': SVD, 'SVDPP':
            SVDPP, 'title21': title21, 'predict': predict, 'title22': title22, 'title31':
                title31, 'MAE': MAE})
    
def sl(request):
    if request.method == 'POST':
        subprocess.check_call(['python', 'slopeone.py'])  

def us(request):
    if request.method == 'POST':
        subprocess.check_call(['python', 'userbased.py'])  

def it(request):
    if request.method == 'POST':
        subprocess.check_call(['python', 'itembased.py']) 

        
def sv(request):
    if request.method == 'POST':
        subprocess.check_call(['python', 'svd.py'])

def svp(request):
    if request.method == 'POST':
        subprocess.check_call(['python', 'svdpp.py']) 

    
#The view function passes a request to the template's render method.
#In the template, there is a {% csrf_token %} template tag inside each POST form that targets an internal URL.
#If you are not using CsrfViewMiddleware, then you must use csrf_protect on any views that use the csrf_token template tag, as well as those that accept the POST data.
#The form has a valid CSRF token. After logging in in another browser tab or hitting the back button after a login, you may need to reload the page with the form, because the token is rotated after a login.