from __future__ import print_function, unicode_literals
from PyInquirer import style_from_dict, Token, prompt, Separator
from pprint import pprint
from art import *
import os
import tarfile
from art import *
from colorama import Fore, Back, Style
from colorama import init
import re
import pandas as pd
import openpyxl
#################################################################
init(convert=True)
#pint program name
tprint('<<<Tar Analysis 2.0>>>')
#ask for folder name
print(Fore.CYAN)
name = input("Please enter the Tar folder name: ")
print(Style.RESET_ALL)
#so we dont have to tipe .tar.gz
namet = name + ".tar.gz"
#open and unzip tar folder
tar = tarfile.open(namet,"r:gz")
tar.extractall()
tar.close()
################################################################
#CLI to ask what errors to look for 
style = style_from_dict({
    Token.Separator: '#cc5454',
    Token.QuestionMark: '#673ab7',
    Token.Selected: '#cc5454',  # default
    Token.Pointer: '#673ab7',
    Token.Instruction: '',  # default
    Token.Answer: '#f44336',
    Token.Question: '',
})
questions = [
    {
        'type': 'checkbox',
        'message': 'Please select errors to look for',
        'name' : 'variables',
        'choices': [
            Separator('= Errors to look for ='),
            {
                'name': 'FAILED VALIDATION!!',
                'checked': True
            },
            {
                'name': 'FAILED VALIDATION while executing command',
            },
            {
                'name': 'FAILED VALIDATION - Reported',
            },
            {
                'name': '***err',
            },
            {
                'name': 'FAIL**',
            },
            {
                'name': 'err-disable',
            },
            {
                'name': 'Write your own',
            },
             {
                'name': '->Make Excel report',
            },
            Separator('= Enter a Command and print switch log for it ='),
            {
                'name': 'Enter Command :',
            },
        ],
        'validate': lambda answer: 'You must choose at least one error to look for.' \
            if len(answer) == 0 else True
    }
]

answers = prompt(questions, style=style)
###################################################################
#reads for new entry
if 'Write your own' in answers["variables"]:
    own = input("Please enter the error you are looking for: ")
    answers["variables"] = [own if i=='Write your own' else i for i in answers["variables"]]
    
###################################################################
#reads for command to search output 
if 'Enter Command :' in answers["variables"]:
    cmd = input("please enter Command to output log:")
    cmd = cmd+''
###################################################################
#opens all the files and writes line by line in log.txt document
logs = open('logs.txt',"w+")
for path, subdirs, files in os.walk(name):
        for i in files:
            filename = os.path.join(path, i)
            ### writing to text file
            with open(filename) as infile:
                for line in infile:
                    logs.write(line)
###################################################################
#look up for text line by line 
#### varibles
count = 0
corner = ''
fails = []
switch = []
switchNumber = 'first777#$'
#opens text file to read line by line
with open("logs.txt") as L:
    for line in L:
    # look for corner
        if 'Corner Name :' in line and 'PST' not in line and line not in corner:
            corner = line
            count = 0
            print(Fore.BLACK)
            print (Back.WHITE+'                     >  '+corner)
            print(Style.RESET_ALL)
    #Looks for Testcase number
        if 'TESTCASE START -' in line :
            testn = line
    # using re.py to search for switch number
        if 'TESTCASE START -' in line and switchNumber not in line:
            xx=[]
            count = 0
            xx =  re.search(r'\w\w\w\w\w\w\d(\d)?', line)
            switchNumber = str(xx.group())
            print (Fore.GREEN+(switchNumber))
            print(Style.RESET_ALL)
    #adding to list with errors
        for i in answers["variables"]:
            if i in line and i not in fails:
                fails.append(line)
        if len(fails) > 0 and 'TESTCASE END -' in line:
            count += 1
            print(Fore.YELLOW +str(count)+"--"+(testn))
            print(Style.RESET_ALL)
            print (*fails, sep = "\n")
    #clearing error list
        if 'TESTCASE END -' in line:
            fails.clear()
#################################################################
#looking for command output log
cmdLog = []
cmdStart = 10000000
ii = 0
full = 0
switchNumber1 = 'first777#$'
if 'Enter Command :' in answers["variables"]:
    print(Fore.BLACK)
    print (Back.RED+'Command Log Output')
    print(Style.RESET_ALL)
    with open("logs.txt") as B:
        for line in B:
            ii += 1
    # look for corner
            if 'Corner Name :' in line and 'PST' not in line and line not in corner:
                corner = line
                count = 0
                print(Fore.BLACK)
                print (Back.WHITE+'                     >  '+corner)
                print(Style.RESET_ALL)
    #Looks for Testcase number
            if 'TESTCASE START -' in line :
                testn = line
    # using re.py to search for switch number
            if 'TESTCASE START -' in line and switchNumber not in line:
                xx=[]
                count = 0
                xx =  re.search(r'\w\w\w\w\w\w\d(\d)?', line)
                switchNumber1 = str(xx.group())
                print (Fore.GREEN+(switchNumber1))
                print(Style.RESET_ALL)
    # looking for comand output
            if line.startswith(cmd) and line not in cmdLog:
                cmdLog.append(line)
                cmdStart = ii
                cmdStop = 10000000
                full = 1
            if ii >= cmdStart and ii < cmdStop and line not in cmdLog:
                cmdLog.append(line)
            if "*************************************************" in line or "--------------------------------------------------" in line or "--------------------------------------------------" in line:
                cmdStop = ii
            if 'TESTCASE END' and full == 1:
                cmdLog = list(filter(None, cmdLog))
                print(*cmdLog, sep = "\n")
                cmdLog.clear()
                full = 0
#################################################################
#this part is to make an excel report on test
##variables
"""testName = []
jobID = []
nameEx = name + ".xlsx"
if '->Make Excel report' in answers["variables"]:
    with open("logs.txt") as E:
        for line in E:
            if "job_name " in line and  len(testName)<1:
                testName.append(line)
            if "Starting Job Id " in line and len(jobID)<1:
                jobID.append(line)
                one = pd.Series([testName,jobID])
            if "Motherboard serial number" in line and line not in one:
                one.append(line)
            if "System derial number" in line and line not in one:
                one.append(line)
            if "Model number" in line and line not in one:
                one.append(line)
    w = pd.ExcelWriter(nameEx)
    one.to_excel(w,'Test Info')
    w.save()
    quit()

quit()
"""

