# -*- coding: utf-8 -*-
import os,sys,re

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
    for files in os.listdir(filedir):
        if os.path.isdir(filedir+files) is True and files != "Pass" :
            handlefiledir(filedir+files)
        if files.endswith('.log') is True and files.startswith('eclid') is False and files != '1.log':
            result=analysefile(filedir,files)
            #file1=open(''+filedir+'/'+'1'+'.log','w')
            #file1.writelines(result)
            #file1.close()

            import win32clipboard
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardText(result)
            win32clipboard.CloseClipboard()
            print result
    return result
    
if __name__ == "__main__":
    #filedir=r'\\cn-vmhost01\Share\Document\SQA\PPRO\Kingston\Nightly\520_29324'
    filedir=os.getcwd()
    handlefiledir(filedir)
    input("Input any key to quit")