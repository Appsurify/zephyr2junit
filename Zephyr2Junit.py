#!/usr/bin/env python3
#requires python>3.6

import xml.etree.ElementTree as ET

testsuitename = "Remedy"
filename = "ZFJ-Executions-04-22-2020.xml"

failedValue = ""
passedValue = "PASS"
skippedValue = "BLOCKED"
wipValue = "WIP"
unexecutedValue = "UNEXECUTED"
errorValue = ""


class TestResult:
    def __init__(self, name, issueKey, result, comment):
        self.name = issueKey + " " + name
        self.issueKey = issueKey
        self.result = result

def mapResults(resultValue):
    if resultValue.lower() == passedValue.lower():
        return "pass"
    if resultValue.lower() == skippedValue.lower():
        return "skipped"
    if resultValue.lower() == wipValue.lower():
        return "skipped"
    if resultValue.lower() == unexecutedValue.lower():
        return "skipped"
    if resultValue.lower() == errorValue.lower():
        return "error"
    if resultValue.lower() == failedValue.lower():
        return "failure"
    return "skipped"

tree = ET.parse(filename)
root = tree.getroot()

numPass = 0
numFail = 0
numSkip = 0
numError = 0

testresults = []

for elem in root:
    testSummary = elem.find("testSummary").text
    result = mapResults(elem.find("executionStatus").text)
    issueKey = elem.find("issueKey").text
    comment = elem.find("Comment").text
    if result == "pass":
        numPass = numPass + 1
    if result == "skipped":
        numSkip = numSkip + 1
    if result == "error":
        numError = numError + 1
    if result == "failure":
        numFail = numFail + 1
    print(result)
    print(issueKey)
    print(testSummary)
    test = TestResult(testSummary, issueKey, result, comment)
    testresults.append(test)
    
testsuites = ET.Element('testsuites')
testsuite = ET.SubElement(testsuites, 'testsuite')

testsuite.set('tests', str(numPass+numFail+numSkip+numError))
testsuite.set('errors', str(numError))
testsuite.set('failures', str(numFail))
testsuite.set('skipped', str(numSkip))
testsuite.set('name', str(testsuitename))

for testresult in testresults:
    test = ET.SubElement(testsuite, 'testcase')
    test.set('name', testresult.name)
    if testresult.result == "skipped":
        result = ET.SubElement(test, 'skipped')
    if testresult.result == "failure":
        result = ET.SubElement(test, 'failure')
        result.set('message', str(testresult.comment))
        result.set('type', str(testresult.comment))
        result.text = str(testresult.comment)

    if testresult.result == "error":
        result = ET.SubElement(test, 'error')
        result.set('message', str(testresult.comment))
        result.set('type', str(testresult.comment))
        result.text = str(testresult.comment)

# create a new XML file with the results
mydata = ET.tostring(testsuites)
myfile = open("junit.xml", "w")
myfile.write(mydata)
