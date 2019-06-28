'''
기본 로그인 처리부
login
    - 로그인 화면 이동
    - session['login'] 값 검사
        - 유저 정보 검사 후 처리
        - 이메일 없을시 > 이메일 입력받음 
            - 수정중, 이메일 없을시 로그인 무효
        - 프로파일 조회후 값이 없을시 입력 폼으로
loginCheck
    -  Oauth 로그인으로 얻은 정보 조회하여 필요 혹은 완료값 반환

input{info}
    - 필요 정보 입력 폼

logout
    - 세션 정리, 유저 로그아웃 기능
'''


from .common import *

def index(request):
    if 'login' in request.session:
        if request.session['login']:
            check = loginCheck(request)
            if check == "email":
                return HttpResponseRedirect("/user/require/email/")
            elif check == "fail":
                try:
                    del request.session['login']
                    del request.session['loginToken']
                except:
                    return render(request, 'user/login.html')                
            else:
                return render(request, 'user/login.html')
    if request.GET:
        return render(request, 'user/login.html', dict(request.GET))
    return render(request, 'user/login.html')

def login(request):    
    if 'login' in request.session:
        if request.session['login']:
            check = loginCheck(request)
            if check == "email":
                return HttpResponseRedirect("/user/require/email/")
            elif check == "fail":
                try:
                    del request.session['login']
                    del request.session['loginToken']
                except:
                    return render(request, 'user/login.html')     
            elif check =="profile":
                return HttpResponseRedirect("/user/require/profile/")           
            else:
                return render(request, 'user/login.html')   
    if request.GET:
        return render(request, 'user/login.html', dict(request.GET))
    return render(request, 'user/login.html')

def loginCheck(request):
    if 'email' in request.session:
        email = request.session['email']
    else:
        return "fail"
    
    if 'loginToken' not in request.session:
        return "fail"

    if email == "require_userEmail":
        return "email"        
    else:
        try:
            user = User.objects.get(email= email)
            user.lastAccess = timezone.now()
            user.save()
        except:
            user = User(email=email)
            user.save()
        if not user.name or not user.phoneNumber:
            print("require Profile!")    
        if not user.walletAddress:
            print("require walletAddress!")
            return "profile"

    

def inputEmail(request):
    if 'login' not in request.session:         
        return HttpResponseRedirect('/user/login/?msg='+'please login first!'+'&status=Warning')

    if request.method == 'GET':
        if request.session['login']:
            return render(request, 'user/inputEmail.html')
        else:
            return HttpResponseRedirect('/user/login/?msg='+'please login first!'+'&status=Warning')
    else :
        email = request.POST['email']
        try:
            user = User.objects.get(email=email)
            return HttpResponseRedirect('/user/require/email')
        except:
            if 'email' in request.session:
                request.session['email']  = email

        return HttpResponseRedirect('/user/login/')

def inputProfile(request):
    if request.method =='GET':        
        
        return render(request, 'user/modify/profile.html')        
    else:
        print(request.POST)
        form = UserProfileForm(request.POST)
        if  form.is_valid():
            print("test msg")
            user = User.objects.get(email = request.session['email'])
            user.name = request.POST['name']
            user.phoneNumber = request.POST['phoneNumber']
            user.walletAddress = request.POST['walletAddress']
            user.save()
        return HttpResponseRedirect('/user/login/')

def logout(request):
    print("logout...")
    del request.session['login']
    if 'kakao' in request.session['loginToken']:
        print("kakao logout...")
        headers={
            "Authorization": "Bearer "+re.sub('(kakao).',"",request.session['loginToken'])
        }
        requests.post('https://kapi.kakao.com/v1/user/logout', headers=headers)
        del request.session['email']
        del request.session['loginToken']
        print("success!")
    else :
        print("facebook logout...")
        del request.session['email']
        del request.session['loginToken']
    
    print("Logout successful! redirect login page...")
    return HttpResponseRedirect('/user/login/')