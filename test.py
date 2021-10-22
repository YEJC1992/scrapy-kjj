import re


test = '0.13mg/kg'
num = re.findall(r'\d+\.*\d*',test)
newTest = test.replace(num[0],'')
print(num)
print(newTest)