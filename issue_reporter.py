# -*- coding: utf-8 -*-
import os,sys,re,time
from splinter import Browser 
import win32clipboard

def findzip(location, filetype='.zip'):
    filename = ''
    if len(os.listdir(location)) == 1 :
        return '1'
    for files in os.listdir(location):
        if files.endswith(filetype):
            filename = files
    return filename

def getserial(filename):
    f=open(filename,'r')
    for line in f:
        pattern1=re.compile(r'.*<SerialNumber>(.*)</SerialNumber>')
        match1=pattern1.match(line)
        if match1:
            SerialNumber=match1.group(1)            
            if SerialNumber != 'None':
                return 'SerialNumber             :'+' '+SerialNumber
            else:
                return ''
        else:
            pass
    f.close()

def getconfig(filename):
    f=open(filename,'r')
    for line in f:
        pattern1=re.compile(r'.*<ConfigId>(.*)</ConfigId>')
        match1=pattern1.match(line)
        if match1:
            config=match1.group(1)            
            if config != 'None':
                return 'ConfigId                 :'+' '+config
            else:
                return ''
        else:
            pass
    f.close()

def getcapacity(filename):
    f=open(filename,'r')
    for line in f:
        pattern1=re.compile(r'.*<LogicalCapacity>.* \((.*?)\)</LogicalCapacity>.*')
        match1=pattern1.match(line)
        if match1:
            LogicalCapacity=int(match1.group(1))/1000/1000/1000
            return LogicalCapacity
    f.close()

def getmodelname(filename):
    f=open(filename,'r')
    for line in f:
        pattern1=re.compile(r'.*<Model>(.*)</Model>.*')
        match1=pattern1.match(line)
        if match1:
            Model=match1.group(1)
            return Model
    f.close() 

def getrevname(filename):
    f=open(filename,'r')
    for line in f:
        pattern1=re.compile(r'.*<FirmwareRevision>(.*)</FirmwareRevision>.*')
        match1=pattern1.match(line)
        if match1:
            FirmwareRevision=match1.group(1)
            return FirmwareRevision
    f.close()    

def getstreamname(filename):
    f=open(filename,'r')
    for line in f:
        pattern1=re.compile(r'.*<AccurevVersion>(.*)</AccurevVersion>.*')
        match1=pattern1.match(line)
        if match1:
            stream=match1.group(1).split(':')[-1]
            if stream.startswith('/home'):
                return match1.group(1).split(':')[-2]
            else:
                return  stream
    f.close() 

def getscriptname(filename):
    f=open(filename,'r')
    for line in f:
        pattern1=re.compile(r'.*<Script>(.*)</Script>.*')
        match1=pattern1.match(line)
        if match1:
            script=match1.group(1)
        pattern2=re.compile(r'.*<Arguments>(.*)</Arguments>.*')
        match2=pattern2.match(line)
        if match2:
            arguements=match2.group(1)
            return  script+' '+arguements
    f.close() 

def getfileresult(filename):
    f=open(filename,'r')
    for line in f:
        pattern1=re.compile(r'.*<Result>(\w{4})</Result>')
        match1=pattern1.match(line)
        if match1:
            test_result=match1.group(1)
            return test_result
    f.close() 
    
def analysefile(filedir,filename):
    wholedir=filedir+filename
    str1=''
    str1='''
Board Info:
Device Model Number      : %s                            
Device Firmware Revision : %s
Capacity                 : %s G
%s
%s

Stream/Build:
%s

Script/Steps:
%s

Expect Result:
Pass

Actual Result
%s

{noformat}

{noformat}
    ''' %     (getmodelname(wholedir),
    getrevname(wholedir),
    getcapacity(wholedir), 
    getserial(wholedir),
    getconfig(wholedir),
    getstreamname(wholedir),
    getscriptname(wholedir), 
    getfileresult(wholedir))
    
    return str1

def handlefiledir(filedir):
    result=''
    if filedir.endswith('\\') is False:
        filedir=filedir+'\\'    
    zip_name=''
    for files in os.listdir(filedir):    
        if os.path.isdir(filedir+files) is True and files != "Pass" :
            handlefiledir(filedir+files)
        if files.endswith('.log') is True and files.startswith('eclid') is False and files != '1.log':
            result=analysefile(filedir,files)
            zip_name=files
            #file1=open(''+filedir+'/'+'1'+'.log','w')
            #file1.writelines(result)
            #file1.close()
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardText(result)
            win32clipboard.CloseClipboard()
            print result
    print findzip(filedir, '.zip')
    if findzip(filedir, '.zip') == '':
        str_zip='7z a %s.zip %s\\* -x!*.zip -x!*.tmp' %(zip_name,filedir)
        print str_zip
        os.system(str_zip)
        #os.system('7z a %s.zip %s/*.log -r' %(files,filedir))
    return zip_name

def mp540(browser):
        browser.fill('summary', '[MP540] Test failed while running  %s' %getscriptname(filedir+'\\'+zipname))

        browser.find_by_id('components-textarea').fill('Firmware')
        browser.find_by_css(".aui-list-item-link").first.click()
 

        browser.find_by_id('versions-textarea').fill('5.4.0')
        browser.find_by_css('.aui-list-item-li-5-4-0 > a:nth-child(1)').first.click()

        browser.select('customfield_10210', 'MP5.4.0')
        browser.find_by_css(".aui-list-item-link").first.click()

        browser.check('customfield_10172')             #Repeatable failure

        browser.check('customfield_10022')             #Release
        
        browser.fill('environment', 'SSDT')
        browser.check('customfield_10173')             #Interal Found

        browser.select('customfield_10021','10042')    #Firmware
        #browser.select('customfield_10021:1','-1')     #None

        #browser.uncheck('customfield_10063')             #Uncheck Client
        browser.find_by_id('customfield_10063-2').first.uncheck() #Uncheck Enterprise 

        browser.choose('customfield_10064', 'B02')

        #browser.find_by_value('jtan').first.click()    #Assignee
        
        #browser.find_by_id('assignee-single-select').first.click() 
        browser.find_by_id('assignee-field').fill('Lin Feng Chen')
        browser.find_by_css(".aui-iconised-link").first.click()

        browser.check('customfield_10185')             #ssdt

def mp550(browser):
        browser.fill('summary', '[MP550] Test failed while running  %s' %getscriptname(filedir+'\\'+zipname))

        browser.find_by_id('components-textarea').fill('Firmware')
        browser.find_by_css(".aui-list-item-link").first.click()
 


        browser.find_by_id('versions-textarea').fill('E.A.4')
        browser.find_by_css('.aui-list-item-li-e-a-4 > a:nth-child(1)').first.click()

        browser.select('customfield_10210', '11481')  #FL Project

        browser.check('customfield_10172')             #Repeatable failure

        browser.check('customfield_10022')             #Release
        
        browser.fill('environment', 'SSDT')
        browser.check('customfield_10173')             #Interal Found

        browser.select('customfield_10021','10042')     #Firmware
        #browser.select('customfield_10021:1','-1')     #None

        browser.find_by_id('customfield_10063-1').first.uncheck() #Uncheck Client 
        browser.uncheck('customfield_10063')             #Uncheck Client

       

        browser.choose('customfield_10064', '10241') #B01
        browser.check('customfield_10185')  #ssdt   

        browser.find_by_id('assignee-field').fill('Joe Tan')
        browser.find_by_css(".aui-iconised-link").first.click()
        
def mp560(browser):

        browser.fill('summary', '[MP560] Test failed while running  %s' %getscriptname(filedir+'\\'+zipname))

        browser.find_by_id('components-textarea').fill('Firmware') 
        browser.find_by_css(".aui-list-item-link").first.click()
 
        browser.find_by_id('versions-textarea').fill('F.1.3')   #version        
        browser.find_by_css('.aui-list-item-li-f-1-3 > a:nth-child(1)').first.click()

        browser.select('customfield_10210', '11481')  #FL Project

        browser.check('customfield_10172')             #Repeatable failure

        browser.check('customfield_10022')             #Release
        
        browser.fill('environment', 'SSDT')
        browser.check('customfield_10173')             #Interal Found

        browser.select('customfield_10021','10042')     #Firmware
        #browser.select('customfield_10021:1','-1')     #None

        browser.find_by_id('customfield_10063-1').first.uncheck() #Uncheck Client 
        browser.uncheck('customfield_10063')             #Uncheck Client

        browser.choose('customfield_10064', '10241') #B01
        browser.check('customfield_10185')  #ssdt   

        browser.find_by_id('assignee-field').fill('Lin Feng Chen')
        browser.find_by_css(".aui-iconised-link").first.click()
                

def asd(browser):
        browser.fill('summary', '[ASD] Test failed while running  %s' %getscriptname(filedir+'\\'+zipname))

        browser.find_by_id('components-textarea').fill('Firmware')
        browser.find_by_css(".aui-list-item-link").first.click()

        browser.find_by_id('versions-textarea').fill('I.6.3')
        browser.find_by_css('.aui-list-item-li-i-6-3 > a:nth-child(1)').first.click()
 
        #browser.select('customfield_10210', 'ASD/Oracle DLC') #FL Project
        browser.select('customfield_10210', '10733')

        browser.check('customfield_10172')             #Repeatable failure

        browser.check('customfield_10022')             #Release
        
        browser.fill('environment', 'SSDT')
        browser.check('customfield_10173')             #Interal Found

        browser.select('customfield_10021','10042')    #Firmware
        #browser.select('customfield_10021:1','-1')     #None

        browser.find_by_id('customfield_10063-1').first.uncheck() #Uncheck Client 
        browser.uncheck('customfield_10063')             #Uncheck Client

        browser.choose('customfield_10064', 'B01')

        #browser.find_by_value('mewei').first.click()    #Assignee
        #browser.find_by_id('assignee-single-select').first.click() 
        browser.find_by_id('assignee-field').fill('Meng Wei')
        browser.find_by_css(".aui-iconised-link").first.click()

        browser.check('customfield_10185')             #ssdt

def report_issue(filedir,zipname):
    sleep_time=10000
    with Browser() as browser: 
        # Visit URL 
        #browser.cookies.add({'name': 'JSESSIONID'})
        #cookie = {"JSESSIONID": "DE42290DCB7B328E9123DB9CB28BB1AD"}
        #cookie = {"name": "JSESSIONID",'value':'DE42290DCB7B328E9123DB9CB28BB1AD','path':'/','domain':'jira.sandforce.com'}
        #browser.cookies.add(cookie)
        #browser.cookies.add({'path': '/'})
        #browser.cookies.add({'name': 'JSESSIONID'})
        #browser.cookies.all()
        #import cookielib
        #cj = cookielib.CookieJar()
        
        url = "http://jira.lsi.com/secure/CreateIssue.jspa?pid=10020&issuetype=1&Create=Create" 
        #url = "http://jira.sandforce.com/secure/CreateIssue.jspa?pid=10020&issuetype=1&Create=Create" 
        browser.visit(url)
        # print cj
        # for c in cj:
        #     print "11"
        #     browser.cookies.add({"name":c.name,"value":c.value})
        # print browser.cookies.all()
        # time.sleep(sleep_time)
        try:
            #browser.fill('summary', '[MP550]')
            browser.fill('summary', '[MP540]')
        except:
            browser.click_link_by_text('log in')
            browser.fill('os_username','yoxu')
            browser.fill('os_password','Lsi201312')
            browser.check('os_cookie')
            browser.find_by_name('login').first.click()

        eval(sys.argv[1])(browser)
        #eval('mp540')(browser)
        #mp550(browser)
        # #browser.fill('summary', '[MP550] Test failed while running  %s' %getscriptname(filedir+'\\'+zipname))
        # browser.fill('summary', '[MP540] Test failed while running  %s' %getscriptname(filedir+'\\'+zipname))
        # browser.find_by_id('components-textarea').fill('Firmware')

        # #browser.find_by_id('versions-textarea').fill('E.A.3')
        # #browser.find_by_id('versions-textarea').fill('5.4.0')
 
        # #browser.select('customfield_10210', 'MP5.5.0') #FL Project
        # browser.select('customfield_10210', 'MP5.4.0')

        # browser.check('customfield_10172')             #Repeatable failure

        # browser.check('customfield_10022')             #Release
        
        # browser.fill('environment', 'SSDT')
        # browser.check('customfield_10173')             #Interal Found

        # browser.select('customfield_10021','10042')    #Firmware
        # browser.select('customfield_10021:1','-1')     #None

        # #browser.uncheck('customfield_10063')             #Uncheck Client
        # #browser.uncheck('customfield_10063-2')           #Uncheck Enterprise 

        # browser.choose('customfield_10064', 'B01')
        # #browser.choose('customfield_10064', 'B02')

        # #browser.find_by_value('jtan').first.click()    #Assignee
        # browser.find_by_value('lichen').first.click()

        # browser.check('customfield_10185')             #ssdt
        
        win32clipboard.OpenClipboard()
        result=win32clipboard.GetClipboardData()
        win32clipboard.CloseClipboard()
        browser.fill('description',result )
        str_zipname=findzip(filedir, '.zip')
        browser.attach_file('tempFilename',filedir+'\\'+str_zipname )
        
        time.sleep(sleep_time)
    
if __name__ == "__main__":
    #filedir=r'\\cn-vmhost01\Share\Document\SQA\PPRO\Kingston\Nightly\520_29324'
    filedir=os.getcwd()
    #filedir = r'\\cn-vmhost01.sandforce.com\Share\Document\SQA\PPRO\MP560\F13\nightly\25358\TestSetFeature'
    #zipname=''
    zipname=handlefiledir(filedir)
    report_issue(filedir,zipname)
    #input("Input any key to quit")
   # add cookie (no way for now)
   # use template for Test jira, 550 jira, 517 jira, ASD jira, kingston jira
   # use GUI