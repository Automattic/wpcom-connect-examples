# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################

import gluon.contrib.simplejson as simplejson
import datetime, random, string
import urllib, urllib2
import requests


JOE_OFFLINE = True

def list_blog():
    '''
    # https://developer.wordpress.com/docs/api/console/
    GET /sites/60332471
    https://public-api.wordpress.com/rest/v1/sites/60332471
    
    https://developer.wordpress.com/docs/oauth2/
    https://developer.wordpress.com/docs/oauth2/#making-an-api-call
    
    <?php
    $access_key = "YOUR_API_TOKEN";
    $curl = curl_init( "https://public-api.wordpress.com/rest/v1/me/" );
    curl_setopt( $curl, CURLOPT_HTTPHEADER, array( 'Authorization: Bearer ' . $access_key ) );
    curl_exec( $curl );
    ?>
    
    NO GOOD just auth no work done -> https://github.com/Automattic/wpcom-connect-examples
    
    convert CURL to python
        http://stackoverflow.com/questions/3516250/translating-curl-to-python-urllib2
        http://stackoverflow.com/questions/1990976/convert-a-curl-post-request-to-python-only-using-standard-libary
        http://stackoverflow.com/questions/4348061/how-to-use-python-urllib2-to-send-json-data-for-login/7469725#7469725
        
        http://stackoverflow.com/search?q=CURLOPT_HTTPHEADER+python
        google: python urllib http headers
        google: python urllib2 http headers
        
        http://stackoverflow.com/questions/7933417/how-do-i-set-headers-using-pythons-urllib
            import urllib2
            req = urllib2.Request('http://www.example.com/')
            req.add_header('Referer', 'http://www.python.org/')
            resp = urllib2.urlopen(req)
            content = resp.read()
            
        https://developers.google.com/fusiontables/docs/articles/oauthfusiontables
        
        
        https://docs.python.org/2.7/howto/urllib2.html
            "If you do not pass the data argument, urllib2 uses a GET request. "
                Data can also be passed in an HTTP GET request by encoding it in the URL itself. This is done as follows:
        
    '''
    UID = auth.user.id      #current user id == 1 for jcwell
    cur_blog_id = db.auth_user[UID].cur_blog_id
    access_token = db.userblogs[cur_blog_id].access_token
    blog_id = db.userblogs[cur_blog_id].blog_id
    
    base_url = 'https://public-api.wordpress.com/rest/v1/sites/' + blog_id
    payload = {}
    payload['http_envelope'] = 'true'
    url_values = urllib.urlencode(payload)
    full_url = base_url + '?' + url_values
    req = urllib2.Request(full_url)   
    req.add_header('Authorization', 'Bearer ' + access_token)
    rsp = urllib2.urlopen(full_url)
    the_info_page = rsp.read()
    
    m = ''
    m += "db.auth_user[UID].cur_blog_id = %s||"%(db.auth_user[UID].cur_blog_id)
    m += "db.userblogs[cur_blog_id].blog_id = %s||"%(db.userblogs[cur_blog_id].blog_id)
    m += "db.userblogs[cur_blog_id].blog_url = %s||"%(db.userblogs[cur_blog_id].blog_url)
    m += " || ||"
    
    m += "the_info_page = %s||"%(the_info_page)

    content = BEAUTIFY(m.split('||'))   
   
    if JOE_OFFLINE: return dict(message="offline for now")  
    return dict(content=content)     

result = '''
    140501 Thu 07:28PM Pacific 
        Wpcomconn
        db.auth_user[UID].cur_blog_id = 3
        db.userblogs[cur_blog_id].blog_id = 13425697
        db.userblogs[cur_blog_id].blog_url = http://joedorocak.wordpress.com
        the_info_page = {"code":200,"headers":[{"name":"Content-Type","value":"application\/json"}],"body":{"ID":13425697,"name":"Joe Dorocak&#039;s Blog","description":"Notes to Myself &amp; Others","URL":"http:\/\/joedorocak.wordpress.com","jetpack":false,"subscribers_count":0,"is_private":false,"is_following":false,"meta":{"links":{"self":"https:\/\/public-api.wordpress.com\/rest\/v1\/sites\/13425697","help":"https:\/\/public-api.wordpress.com\/rest\/v1\/sites\/13425697\/help","posts":"https:\/\/public-api.wordpress.com\/rest\/v1\/sites\/13425697\/posts\/","comments":"https:\/\/public-api.wordpress.com\/rest\/v1\/sites\/13425697\/comments\/","xmlrpc":"https:\/\/joedorocak.wordpress.com\/xmlrpc.php"}}}}

    140430 Wed 12:27PM Pacific 

        page:
        db.auth_user[auth.user.id].blogs = [{"access_token": "GhW2uSCNbQzRHh%)&c8wi1Y1SdKdDFzKatUZqJMjlzhcqf%U#dYxCjT6X*y0l@A^", "blog_id": "60332471", "blog_url": "http://joeexperiment.wordpress.com"}]
        blogsStr = [{"access_token": "GhW2uSCNbQzRHh%)&c8wi1Y1SdKdDFzKatUZqJMjlzhcqf%U#dYxCjT6X*y0l@A^", "blog_id": "60332471", "blog_url": "http://joeexperiment.wordpress.com"}]
        the_page = {"code":200,"headers":[{"name":"Content-Type","value":"application\/json"}],"body":{"ID":60332471,"name":"My Blog","description":"This WordPress.com site is the cat\u2019s pajamas","URL":"http:\/\/joeexperiment.wordpress.com","jetpack":false,"subscribers_count":0,"is_private":false,"is_following":false,"meta":{"links":{"self":"https:\/\/public-api.wordpress.com\/rest\/v1\/sites\/60332471","help":"https:\/\/public-api.wordpress.com\/rest\/v1\/sites\/60332471\/help","posts":"https:\/\/public-api.wordpress.com\/rest\/v1\/sites\/60332471\/posts\/","comments":"https:\/\/public-api.wordpress.com\/rest\/v1\/sites\/60332471\/comments\/","xmlrpc":"https:\/\/joeexperiment.wordpress.com\/xmlrpc.php"}}}}

    '''    
    
    
oldway ='''
    blogsStr = db.auth_user[UID].blogs
    
    blogsL = simplejson.loads(blogsStr)
    blogD = blogsL[0]                     #TODO: let user select which blog 
    access_key = blogD['access_token']
    
    # Our Goal -> https://public-api.wordpress.com/rest/v1/sites/60332471?http_envelope=true
    base_url = 'https://public-api.wordpress.com/rest/v1/sites/' + blogD['blog_id']

    # https://docs.python.org/2.7/howto/urllib2.html    # this KLUDGE REALLY EXISTS !!!
    
    payload = {}
    payload['http_envelope'] = 'true'
    url_values = urllib.urlencode(payload)
    full_url = base_url + '?' + url_values
    req = urllib2.Request(full_url)   
    req.add_header('Authorization', 'Bearer ' + access_key)
    rsp = urllib2.urlopen(full_url)
    the_page = rsp.read()
    '''
    

def set_current_blog():
    UID = auth.user.id      #current user id == 1 for jcwell
    db.auth_user[UID] = dict(cur_blog_id=request.args[1])
    cur_blog_id = db.auth_user[UID].cur_blog_id
    m = ''
    m += "request.args[0] = %s||"%(request.args[0])
    m += "request.args[1] = %s||"%(request.args[1])
    m += "db.auth_user[UID].cur_blog_id = %s||"%(db.auth_user[UID].cur_blog_id)
    m += "cur_blog_id = %s||"%(cur_blog_id)
    m += "db.userblogs[cur_blog_id].owner_uid = %s||"%(db.userblogs[cur_blog_id].owner_uid)
    m += "db.userblogs[cur_blog_id].blog_id = %s||"%(db.userblogs[cur_blog_id].blog_id)
    m += "db.userblogs[cur_blog_id].blog_url = %s||"%(db.userblogs[cur_blog_id].blog_url)
    m += "db.auth_user[UID].first_name = %s||"%(db.auth_user[UID].first_name)
    m += "db.auth_user[UID].last_name = %s||"%(db.auth_user[UID].last_name)
    
    content = BEAUTIFY(m.split('||'))   
   
    if JOE_OFFLINE: return dict(content="offline for now")  
    return dict(content=content)      
result = '''
    140501 Thu 07:14PM Pacific 
        Set Current Blog
        request.args[0] = userblogs
        request.args[1] = 3
        db.auth_user[UID].cur_blog_id = 3
        cur_blog_id = 3
        db.userblogs[cur_blog_id].owner_uid = 1
        db.userblogs[cur_blog_id].blog_id = 13425697
        db.userblogs[cur_blog_id].blog_url = http://joedorocak.wordpress.com
        db.auth_user[UID].first_name = Joe
        db.auth_user[UID].last_name = Codeswell

    140501 Thu 07:07PM Pacific 
        Set Current Blog
        request.args[0] = userblogs
        request.args[1] = 3
        db.auth_user[UID].cur_blog_id = 3
        curblogid = 3
        db.userblogs[curblogid].owner_uid = 1
        db.userblogs[curblogid].blog_id = 13425697
        db.userblogs[curblogid].blog_url = http://joedorocak.wordpress.com
        db.auth_user[UID].first_name = Joe
        db.auth_user[UID].last_name = Codeswell

    140501 Thu 06:52PM Pacific 
        Set Current Blog
        request.args[0] = userblogs
        request.args[1] = 3
        db.auth_user[UID].cur_blog_id = 3

    140501 Thu 02:34PM Pacific 
        Set Current Blog
        request.args[0] = userblogs
        request.args[1] = 3

'''    
    
@auth.requires_login()      
def select_blog():
    ''' https://joecodeswell.com/wpcomconn/default/select_blog/auth_user
        https://joecodeswell.com/wpcomconn/default/select_blog
        
        http://web2py.com/books/default/chapter/29/07/forms-and-validators#SQLFORM-grid
        Example 30 -> http://www.web2py.com/init/default/examples#form_examples
        
        see: http://web2py.com/books/default/chapter/29/06/the-database-abstraction-layer#Serializing-Rows-in-views
                linkto
    '''
    UID = auth.user.id      #current user id == 1 for jcwell

    # blogsStr = db.auth_user[auth.user.id].blogs
    # blogsL = simplejson.loads(blogsStr)
    
    works_but_too_much = '''        
    form = SQLFORM.smartgrid(db.auth_user,linked_tables=['blogs'],
                             user_signature=False)
    '''
    
    #records = SQLTABLE(db().select(db.userblogs.owner_uid==auth.user.id),headers='fieldname:capitalize')
    # uid = auth.user.id
    # records = SQLTABLE(db().select(db.userblogs.owner_uid==uid),
        # #headers='fieldname:capitalize'
        # )
    # db.purchase.product_id==form.vars.product_id
    #records = SQLTABLE(db().select(db.userblogs.ALL),headers='fieldname:capitalize')
    #form=[]
    
    
    # http://web2py.com/books/default/chapter/29/06/the-database-abstraction-layer#Query--Set--Rows
    # http://joecodeswell.wordpress.com/web2py-notes/#DALBasics 
    # define_table, insert, count, delete, update
    #    query=(db.person.id==id)
    
    rows = db(db.userblogs.owner_uid==UID).select()
    form=[]
    #trs = SQLTABLE(rows, linkto=generate_url(id))
    trs = SQLTABLE(rows, truncate=100, columns=['userblogs.id', 'userblogs.blog_id', 'userblogs.blog_url', ], linkto=URL(f='set_current_blog'))   # see https://groups.google.com/forum/#!searchin/web2py/linkto/web2py/FXwUCUvk5uo/-zQo6nzwO38J
    #trs = SQLTABLE(rows, linkto=URL(f='set_current_blog'))   # see https://groups.google.com/forum/#!searchin/web2py/linkto/web2py/FXwUCUvk5uo/-zQo6nzwO38J
     
    
    if JOE_OFFLINE: return dict(form=form, records="offline for now")  
    return dict(trs=trs)
    
# def generate_url(id):
    # return URL(f='set_current_blog', args=[id])
    
    
result = ''' 
140501 Thu 02:34PM Pacific 
    Click on a userblogs.id to select it as the Current Blog
    userblogs.id	userblogs.blog_id	userblogs.blog_url
    1	60332471	http://joeexperiment.wordpress.com
    3	13425697	http://joedorocak.wordpress.com
    
    when clicked made RESULT for set_current_blog at same time == 140501 Thu 02:34PM Pacific 

140430 Wed 04:24PM Pacific 
    page:
    User registration form
    []
    Current users
    userblogs.id	userblogs.owner_uid	userblogs.blog_id	userblogs.access_token	userblogs.blog_url
    1	Joe Codeswell (1)	60332471	GhW2uSCNbQzRH...	http://joeexp...
'''    

@auth.requires_login()      
def connected():
    """
    Joe says:
        this URL gets called twice by wordpress.com
            1. when user clicks on allow 
            2. after 
                rsp_token_request = requests.post("https://public-api.wordpress.com/oauth2/token", params=payload)
        How to distinguish between the 2?
            Can the 'state' variable be of some help?
   
        Why does the client_id come back "client_id" parameter is missing."
    
    NO LONGER a translation of [BUT TAKES HINTS FROM]:
        https://github.com/Automattic/wpcom-connect-examples/blob/master/flask/run.py
            def connected():
    Following http://developer.wordpress.com/docs/oauth2/
        Once the user has authorized the request, he or she will be redirected to the redirect_url. 
           The request will look like the following:
                http://developer.wordpress.com/?code=cw9hk1xG9k

        This is a time-limited code that your application can exchange for a full authorization token. 
        To do this you will need to pass the code to the token endpoint by making a POST request to the token endpoint: 
            You are required to pass 
                client_id, 
                client_secret, and 
                redirect_uri for web applications. 
                    These parameters have to match the details for your application, and 
                        the redirect_uri must match the redirect_uri used during the Authorize step (above). 
                grant_type has to be set to "authorization_code". 
                code must match the code you received in the redirect.
            https://public-api.wordpress.com/oauth2/token.
                $curl = curl_init( "https://public-api.wordpress.com/oauth2/token" );
                curl_setopt( $curl, CURLOPT_POST, true );
                curl_setopt( $curl, CURLOPT_POSTFIELDS, array(
                    'client_id' => your_client_id,
                    'redirect_uri' => your_redirect_url,
                    'client_secret' => your_client_secret_key,
                    'code' => $_GET['code'], // The code from the previous request
                    'grant_type' => 'authorization_code'
                ) );
                curl_setopt( $curl, CURLOPT_RETURNTRANSFER, 1);
                $auth = curl_exec( $curl );
                $secret = json_decode($auth);
                $access_key = $secret->access_token;   
            
        google: web2py make a post request
            https://groups.google.com/forum/#!topic/web2py/h6KycJlhJSY
                https://github.com/kennethreitz/requests
                    http://docs.python-requests.org/en/latest/user/quickstart/#make-a-request
        
    """
    
    # http://docs.python-requests.org/en/latest/user/quickstart/#passing-parameters-in-urls
    UID = auth.user.id      #current user id == 1 for jcwell

    code = request.vars.code
    if not code:
        redirect(URL('index'))
        
    state = request.vars.state
    if not state:
        return dict(message='Warning! State variable missing after authorization.')

    if (not session.state):
        return dict(message='Warning! No session.atate! WHY NOT??? variable missing after authorization.')
    
    if state != session.state:
        return dict(message='Warning! State mismatch. Authorization attempt may have been compromised. This: ' + state + ' should be: ' + session.state)
    
    payload = { 'client_id': '34759', 
                'client_secret': wpcc_consts['client_secret'],
                'redirect_uri': 'http://joecodeswell.com/wpcomconn/default/connected',
                'grant_type': 'authorization_code',
                'code': request.vars.code,
    }
    rsp_token_request = requests.post("https://public-api.wordpress.com/oauth2/token", data=payload)
   
    if not 'Response [200]' in str(rsp_token_request): 
        return dict(message='Problem! "Response [200]" not in response!')
    
    
    rows = db(db.userblogs.owner_uid==UID).select()

    cmdLine = '''
        In [1]: query=(db.userblogs.owner_uid==1)

        In [2]: records = db(query).select(orderby=db.userblogs.blog_id)   
        
        In [4]: type(records)
        Out[4]: gluon.dal.Rows        

        In [5]: len(records)
        Out[5]: 1

        In [6]: records.first()
        Out[6]: <Row {'blog_id': '60332471', 'owner_uid': 1L, 'access_token': 'GhW2uSCNbQzRHh%)&c8wi1Y1SdKdDFzKatUZqJMjlzhcqf%U#
        dYxCjT6X*y0l@A^', 'blog_url': 'http://joeexperiment.wordpress.com', 'id': 1L}>

        In [7]: jsond = {u'access_token': u'GhW2uSCNbQzRHh%)&c8wi1Y1SdKdDFzKatUZqJMjlzhcqf%U#dYxCjT6X*y0l@A^', u'token_type': u'
        bearer',u'blog_id': u'60332471', u'blog_url': u'http://joeexperiment.wordpress.com', u'scope': u''}

        In [8]: blogid = jsond['blog_id']

        In [9]: # search db for exisitng blogid

        In [10]: len(db(db.userblogs.blog_id==jsond['blog_id']).select())
        Out[10]: 1

        In [11]: db(db.userblogs.blog_id==jsond['blog_id']).select().first().access_token
        Out[11]: 'GhW2uSCNbQzRHh%)&c8wi1Y1SdKdDFzKatUZqJMjlzhcqf%U#dYxCjT6X*y0l@A^'

        In [12]:
    '''
    oldway = '''
        uid = auth.user.id  # this for online
        blogsStr = db.auth_user[uid].blogs
        
        blogsL = simplejson.loads(blogsStr)
        #jsond = {u'access_token': u'GhW2uSCNbQzRHh%)&c8wi1Y1SdKdDFzKatUZqJMjlzhcqf%U#dYxCjT6X*y0l@A^', u'token_type': u'bearer',u'blog_id': u'60332471', u'blog_url': u'http://joeexperiment.wordpress.com', u'scope': u''}
        jsond = rsp_token_request.json()  # this for online
        # need to check if blog_id is already in blogsL    ALSO MAYBE NOT
        authed_blogd = {k:jsond[k] for k in ('blog_id','access_token', 'blog_url') if k in jsond}
        blogsL.append(authed_blogd)
        newBlogsStr = simplejson.dumps(blogsL)
        db.auth_user[uid] = dict(blogs=newBlogsStr)
        db.auth_user[uid].blogs
    '''
    
    jsond = rsp_token_request.json()   

    # maintain the userblogs table
    # is the blog_id in the response is already in the db?
    blogid_row = db(db.userblogs.blog_id==jsond['blog_id']).select().first()  # is unique => len == 1 or 0
    if blogid_row: 
        # yes it is in the db -> just update the access_token
        db.userblogs[blogid_row.id] = dict(access_token=blogid_row.access_token)
    else:
        # no it is NOT in the db -> insert a new item
        authed_blogd = {k:jsond[k] for k in ('blog_id','access_token', 'blog_url') if k in jsond}
        authed_blogd['owner_uid'] = UID
        db.userblogs.insert(**authed_blogd)
    
    
    # debug stuff  
    
    m = ''
    m += "(not session.state) == True = %s||"%((not session.state) == True)
    m += "session.state = %s||"%(session.state)
    m += "request.vars.code = %s||"%(request.vars.code)
    m += "request.vars.state = %s||"%(request.vars.state)
    m += "session.tempcode = %s||"%(session.tempcode)
    m += "rsp_token_request = %s||"%(rsp_token_request)
    m += "type(rsp_token_request) = %s||"%(type(rsp_token_request) )
    m += "str(rsp_token_request) = %s||"%(str(rsp_token_request) )
    m += "not 'Response [200]' in str(rsp_token_request) = %s||"%(not 'Response [200]' in str(rsp_token_request) )
    m += "not 'Response [400]' in str(rsp_token_request) = %s||"%(not 'Response [400]' in str(rsp_token_request) )
    m += " || ||"
    
    m += "rsp_token_request.request = %s||"%(rsp_token_request.request)
    #m += "rsp_token_request.data = %s||"%(rsp_token_request.data)
    m += "rsp_token_request.request.headers = %s||"%(rsp_token_request.request.headers)
    m += "rsp_token_request.url = %s||"%(rsp_token_request.url )
    m += " || ||"
    
    m += "rsp_token_request.json() = %s||"%(rsp_token_request.json() )
    m += "type(rsp_token_request.json()) = %s||"%(type(rsp_token_request.json()) )    
    m += "rsp_token_request.json().has_key('error_description') = %s||"%(rsp_token_request.json().has_key('error_description') )
    if rsp_token_request.json().has_key('error_description'):
        m += "rsp_token_request.json()['error_description'] = %s||"%(rsp_token_request.json()['error_description'] )
    
    m += "rsp_token_request.json().has_key('access_token') = %s||"%(rsp_token_request.json().has_key('access_token') )    
    if rsp_token_request.json().has_key('access_token'):
        m += "rsp_token_request.json()['access_token'] = %s||"%(rsp_token_request.json()['access_token'] )
    m += " || ||"
    
    
    content = BEAUTIFY(m.split('||'))
    
    if JOE_OFFLINE: return dict(message="offline for now")  
    return dict(content=content)      
    
Result = ''' 
    140501 Thu 12:34PM Pacific 
        navbar: http://joecodeswell.com/wpcomconn/default/connected?code=U85pE2uqXX&state=2014-05-0119.50.32.794784_6UYF5D03WWZPMP7QUKXXW43E56RHKS
        
        userblogs csv
            userblogs.id,userblogs.owner_uid,userblogs.blog_id,userblogs.access_token,userblogs.blog_url
            1,1,60332471,GhW2uSCNbQzRHh%)&c8wi1Y1SdKdDFzKatUZqJMjlzhcqf%U#dYxCjT6X*y0l@A^,http://joeexperiment.wordpress.com
            3,1,13425697,HSFx%(hNSbQzke$MNoNBT7vMgNwLiNQf6G0JI)%J$$8yrk8SnfAvVLA*4KMFo6u(,http://joedorocak.wordpress.com

        page
            (not session.state) == True = False
            session.state = 2014-05-0119.50.32.794784_6UYF5D03WWZPMP7QUKXXW43E56RHKS
            request.vars.code = U85pE2uqXX
            request.vars.state = 2014-05-0119.50.32.794784_6UYF5D03WWZPMP7QUKXXW43E56RHKS
            session.tempcode = None
            rsp_token_request = <Response [200]>
            type(rsp_token_request) = <class 'requests.models.Response'>
            str(rsp_token_request) = <Response [200]>
            not 'Response [200]' in str(rsp_token_request) = False
            not 'Response [400]' in str(rsp_token_request) = True
            rsp_token_request.request = <PreparedRequest [POST]>
            rsp_token_request.request.headers = CaseInsensitiveDict({'Content-Length': '217', 'Content-Type': 'application/x-www-form-urlencoded', 'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', 'User-Agent': 'python-requests/2.3.0 CPython/2.7.5 Linux/2.6.32-358.2.1.el6.x86_64'})
            rsp_token_request.url = https://public-api.wordpress.com/oauth2/token
            rsp_token_request.json() = {u'access_token': u'HSFx%(hNSbQzke$MNoNBT7vMgNwLiNQf6G0JI)%J$$8yrk8SnfAvVLA*4KMFo6u(', u'token_type': u'bearer', u'blog_id': u'13425697', u'blog_url': u'http://joedorocak.wordpress.com', u'scope': u''}
            type(rsp_token_request.json()) = <type 'dict'>
            rsp_token_request.json().has_key('error_description') = False
            rsp_token_request.json().has_key('access_token') = True
            rsp_token_request.json()['access_token'] = HSFx%(hNSbQzke$MNoNBT7vMgNwLiNQf6G0JI)%J$$8yrk8SnfAvVLA*4KMFo6u(


    RESULT 140430 Wed 10:45AM Pacific: 
        navbar: http://joecodeswell.com/wpcomconn/default/connected?code=F4HJ8QMLFV&state=2014-04-3017.41.09.656468_Y04L8P7N4IFPM7QO3J9JTDG32R5N6H    

        auth_user csv:
            auth_user.id,auth_user.first_name,auth_user.last_name,auth_user.email,auth_user.password,auth_user.registration_key,auth_user.reset_password_key,auth_user.registration_id,auth_user.blogs
            1,Joe,Codeswell,joecodeswell@gmail.com,"pbkdf2(1000,20,sha512)$86c554b53dfdd453$b3b60797dfdc7042e175123f2cf7a6452cb75558",,,,"[{""access_token"": ""GhW2uSCNbQzRHh%)&c8wi1Y1SdKdDFzKatUZqJMjlzhcqf%U#dYxCjT6X*y0l@A^"", ""blog_id"": ""60332471"", ""blog_url"": ""http://joeexperiment.wordpress.com""}]"

            see C:\1d\web2pyStuff\db_auth_user.csv
            
        page:
        (not session.state) == True = False
        session.state = 2014-04-3017.41.09.656468_Y04L8P7N4IFPM7QO3J9JTDG32R5N6H
        request.vars.code = F4HJ8QMLFV
        request.vars.state = 2014-04-3017.41.09.656468_Y04L8P7N4IFPM7QO3J9JTDG32R5N6H
        session.tempcode = None
        rsp_token_request = <Response [200]>
        type(rsp_token_request) = <class 'requests.models.Response'>
        str(rsp_token_request) = <Response [200]>
        not 'Response [200]' in str(rsp_token_request) = False
        not 'Response [400]' in str(rsp_token_request) = True
        rsp_token_request.request = <PreparedRequest [POST]>
        rsp_token_request.request.headers = CaseInsensitiveDict({'Content-Length': '217', 'Content-Type': 'application/x-www-form-urlencoded', 'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', 'User-Agent': 'python-requests/2.3.0 CPython/2.7.5 Linux/2.6.32-358.2.1.el6.x86_64'})
        rsp_token_request.url = https://public-api.wordpress.com/oauth2/token
        rsp_token_request.json() = {u'access_token': u'GhW2uSCNbQzRHh%)&c8wi1Y1SdKdDFzKatUZqJMjlzhcqf%U#dYxCjT6X*y0l@A^', u'token_type': u'bearer', u'blog_id': u'60332471', u'blog_url': u'http://joeexperiment.wordpress.com', u'scope': u''}
        type(rsp_token_request.json()) = <type 'dict'>
        rsp_token_request.json().has_key('error_description') = False
        rsp_token_request.json().has_key('access_token') = True
        rsp_token_request.json()['access_token'] = GhW2uSCNbQzRHh%)&c8wi1Y1SdKdDFzKatUZqJMjlzhcqf%U#dYxCjT6X*y0l@A^    
            
            
            
            
        uid = 1 # uid = auth.user.id
        blogsStr = db.auth_user[uid].blogs
        import simplejson
        blogsL = simplejson.loads(blogsStr)
        jsond = {u'access_token': u'GhW2uSCNbQzRHh%)&c8wi1Y1SdKdDFzKatUZqJMjlzhcqf%U#dYxCjT6X*y0l@A^', u'token_type': u'bearer',
         u'blog_id': u'60332471', u'blog_url': u'http://joeexperiment.wordpress.com', u'scope': u''}
        # jsond = rsp_token_request.json()
        # need to check if blog_id is already in blogsL    ALSO MAYBE NOT
        authed_blogd = {k:jsond[k] for k in ('blog_id','access_token', 'blog_url') if k in jsond}
        blogsL.append(authed_blogd)
        newBlogsStr = simplejson.dumps(blogsL)
        db.auth_user[uid] = dict(blogs=newBlogsStr)
        db.auth_user[uid].blogs







    '''


index_markmin = '''
### Wpcommconn is an app for communicating with WordPress.com
- To get back here - click menu.Welcome 
- To Authorize a Blog - click menu.Authblog 
- 
'''

def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    response.flash = T("Welcome to Joe Codeswell.com!")
    content = XML(MARKMIN(T(index_markmin)))
    return dict(content=content)

@auth.requires_login()
def authorize_blog():
    """
   See: 
    http://developer.wordpress.com/docs/
    https://developer.wordpress.com/docs/api/console/
        GET   /sites/joecodeswell.wordpress.com/posts/?numbe

    NO MORE BASED ON FLASK Example - **INSTEAD** based on theory == http://developer.wordpress.com/docs/oauth2/
    FOLLOWING theory: http://developer.wordpress.com/docs/oauth2/
        
        1. To begin, you will need to send the user to the authorization endpoint.
            https://public-api.wordpress.com/oauth2/authorize?client_id=your_client_id&redirect_uri=your_url&response_type=code
                client_id: should be set to your application’s client id.
                    wpcc_consts['client_id']
                response_type: should always be set to 'code'    #jnote: no qoutes
                redirect_uri: should be set to the URL that the user will be redirected back to 
                                after the request is authorized. 
                                    The redirect_uri should be [the one] set in the applications manager.
                                        The redirect to your application will include a code which you will need in the next step. 
                                            If the user has denied access to your app, the redirect will include ?error=access_denied
                                    
         
        
    """
    
    # from gluon.debug import dbg
    # dbg.set_trace() # stop here
    
    
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(30))
    state = str(datetime.datetime.now()).replace(':', '.').replace(' ', '') + '_' + state
    session.state = state
    
    params = {
        "response_type": "code",
        "client_id": wpcc_consts['client_id'],
        "redirect_uri": URL(f='connected', scheme='http', host='joecodeswell.com', url_encode=False),
        "state": state,
    }
    
    authorize_url_0 = URL(a='oauth2', c='authorize', f='', vars=params, scheme='https', host='public-api.wordpress.com', url_encode=False)
    
    authorize_url =  authorize_url_0.replace('wpcomconn/', '',1)
   
    thehtml = XML(
        '<html><body><h2>Connect FROM JoeCodeswell.com TO WordPress.com</h2><a href="' +
        authorize_url +
        '"><img src="//s0.wp.com/i/wpcc-button.png" width="231" /></a></body></html>'
    ).xml()
    
    #thehtml = XML('<html><body><h2>' + "auth.user.id = %s"%(auth.user.id ) + '</h2></body></html>')
    #thehtml = XML('<html><body><h2>' + "auth.user.email = %s"%(auth.user.email ) + '</h2></body></html>')
    return thehtml
    

    
    
@auth.requires_login()      
    
    
    
    
  
def test():
    pass
    # import requests
    
    # r = requests.get('https://github.com/timeline.json')
    # m =   " request.vars.code = %s/n"%(request.vars.code)
    # m +=  " session.tempcode   = %s/n"%(session.tempcode )
    # if JOE_OFFLINE: return dict(message="offline for now")  
    # return dict(content=content)      


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())

@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())
