from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout#导入验证登录注册的相关函数
from django.contrib.auth.forms import UserCreationForm,UserChangeForm,PasswordChangeForm#用户注册表单模块,用户修改模块,改密码表单模块
from django.contrib.auth.decorators import login_required#判断是否登录
# Create your views here.

@login_required(login_url='myauth:登录')#判断是否登录,如果末登陆就重定向到登录
def 个人中心(请求):
    内容 = {'用户':请求.user}
    return render(请求,'myauth/user_center.html',内容)

@login_required(login_url='myauth:登录')
def 编辑个人信息(请求):
    if 请求.method == 'POST':  # POST请求
        编辑表单 = UserChangeForm(请求.POST,instance=请求.user)
        if 编辑表单.is_valid():
            编辑表单.save()
            return redirect('myauth:个人中心')
    else:#GET请求
        编辑表单 = UserChangeForm(instance=请求.user)
    #先GET请求,如果POST请求表单错误,注册不成功,再是往下渲染
    内容 = {'编辑表单':编辑表单}
    return render(请求,'myauth/edit_profile.html',内容)

@login_required(login_url='myauth:登录')
def 修改密码(请求):
    if 请求.method == 'POST':  # POST请求
        改密表单 = PasswordChangeForm(data=请求.POST,user=请求.user)
        if 改密表单.is_valid():
            改密表单.save()
            return redirect('myauth:登录')
    else:#GET请求
        改密表单 = PasswordChangeForm(user=请求.user)
    #先GET请求,如果POST请求表单错误,注册不成功,再是往下渲染
    内容 = {'改密表单':改密表单,'用户':请求.user}
    return render(请求,'myauth/change_password.html',内容)
# ---------------------------------------------------------------------------------------- #

def 主页(请求):
    return render(请求,'myauth/home.html')

def 登录(请求):
    if 请求.method == 'POST':#POST请求
        用户=authenticate(请求,username=请求.POST['用户名'],password=请求.POST['密码'])#authenticate验证
        if 用户 is None:#登录失败
            return render(请求,'myauth/login.html',{'err':'用户名不存在!'})
        else:
            login(请求,用户)#登录成功,更新用户状态
            return redirect('myauth:主页')#登录成功,重定向到主页


    else:# get请求发回一个页面
        return render(请求,'myauth/login.html')

def 登出(请求):
    logout(请求)
    return redirect('myauth:主页')

def 注册(请求):
    if 请求.method == 'POST':  # POST请求
        注册表单 = UserCreationForm(请求.POST)
        if 注册表单.is_valid():
            注册表单.save()
            用户 = authenticate(username= 注册表单.cleaned_data['username'],password=注册表单.cleaned_data['password1'])
            login(请求,用户)
            return redirect('myauth:主页')
    else:#GET请求
        注册表单 = UserCreationForm()
    #先GET请求,如果POST请求表单错误,注册不成功,再是往下渲染
    内容 = {'注册表单':注册表单}
    return render(请求,'myauth/register.html',内容)