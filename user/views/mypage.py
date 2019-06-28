from .common import *
from ..forms import *

@loginCheckDeco
def mypage(request):
    if request.method == 'GET':
        # 마이페이지 이동시
        user = User.objects.get(email= request.session['email'])
        userInfo = user.to_dict()
        return render(request, 'user/mypage/mypage.html', userInfo);
    else:
        # 수정사항 전송시
        print(request.POST)
        form = UserMypageForm(data=request.POST)
        user = User.objects.get(email=request.session['email'])        
        if form.is_valid():            
            user = form.update(user,commit=False)
            user.save()
            return HttpResponseRedirect('/user/mypage/')
        else:
            print("Check value")
            userInfo = user.to_dict()
            userInfo['msg'] = "Please Check Infomation"
            return render(request, 'user/mypage/mypage.html', userInfo)
    
