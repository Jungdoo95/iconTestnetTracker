'''
kakao Oauth 처리부
'''

from .common import *

def kakaoLogin(request):
    url = "https://kauth.kakao.com/oauth/authorize"
    params={
        "client_id":"ce9e623119a6eaf17429360798694f13",
        "redirect_uri":"http://localhost:8000/user/login/kakao/response",
        "response_type":"code"
    }
    kakaoOauthUrl = createRedirectURL(url, params)
    return HttpResponseRedirect(kakaoOauthUrl);

def kakaoLoginResponse(request):
    queryString = dict(request.GET)

    try:
        if queryString['code']:
            params={
                "grant_type": "authorization_code",
                "client_id": "ce9e623119a6eaf17429360798694f13",
                "redirect_uri":"http://localhost:8000/user/login/kakao/response",
                "code": queryString['code'],
            }
            headers={
                "Content-type":"application/x-www-form-urlencoded;charset=utf-8"
            }

            res = requests.post("https://kauth.kakao.com/oauth/token", headers=headers, params=params)
            token = res.json()
            print(token)
            email = kakaoEmailRequest(request, token['access_token'])
            print("Email >> "+email)
            if email == "require_kakao_accoutEmail":
                print("kakao Email Request!")
                url = "https://kauth.kakao.com/oauth/authorize"
                params={
                    "client_id":"ce9e623119a6eaf17429360798694f13",
                    "redirect_uri":"http://localhost:8000/user/login/kakao/response",
                    "response_type":"code",
                    "scope":"account_email"
                }
                return HttpResponseRedirect(createRedirectURL(url, params));
            elif email=="require_userEmail":                
                pass
            else:            
                request.session['email'] = email
                request.session['loginToken']="kakao."+token['access_token']
            request.session['login'] = True
            return HttpResponseRedirect('/user/login')
        else:
            return HttpResponseRedirect('/user/login/?msg='+'kakao login fail'+'&status=fail')
    except:
        return HttpResponseRedirect('/user/login/?msg='+'kakao login fail'+'&status=fail')
        
def kakaoEmailRequest(request, token):
    params='property_keys=["kakao_account.email"]'
    headers={
        "Authorization": "Bearer "+token,
        "Content-type" : "application/x-www-form-urlencoded;charset=utf-8"
    }
    res = requests.post("https://kapi.kakao.com/v2/user/me", headers=headers, data=params)
    print(res)
    print("Profile test >> ")    
    print(res.json())
    print(res.json()['id'])
    # request.session['code'] = res.json()['id']
    try:
        print("email check...")
        print(res.json()['kakao_account']['email'])
        if res.json()['kakao_account']['email']:
            print("kakao email true..")
            return res.json()['kakao_account']['email']
    except:
        print("email not found...")
        try:
            print("email require true...?")
            if res.json()['kakao_account']['email_needs_agreement']:
                return "require_kakao_accoutEmail"
        except:
            print("user email require...")
            return "require_userEmail"