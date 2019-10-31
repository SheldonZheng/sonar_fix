import requests
import time
import json
import sys


def collectIssues(componentKeys,resolved,severities,types,pageSize):
    url = ('http://sonar.xxx.com/api/issues/search?componentKeys=%s&resolved=%s&severities=%s&types=%s&ps=%s') % (componentKeys,resolved,severities,types,pageSize)
    print(url)
    sonar_result = requests.get(url = url)
    #print(sonar_result.text)
    json_r = json.loads(sonar_result.text)
    return json_r['issues']

def dealIssues(issues,srcPath) :
    print(len(issues))
    for issue in issues:
        dealSingleIssue(issue,srcPath)


def dealSingleIssue(issue,srcPath):
    component = issue['component']
    rule = issue['rule']
    project = issue['project']
    textRange = issue['textRange']
    startLine = textRange['startLine'] - 1
    endLine = textRange['endLine'] - 1
    startOffset = textRange['startOffset']
    endOffset = textRange['endOffset']

    if project != 'clotho':
        return
    if rule != 'pmd:NeedBraceRule':
        return
    print(component)
    filePath = component.replace('clotho:','')
    filePath = srcPath + '/' + filePath
    print(filePath)
    lines = None
    with open(file = filePath,mode = 'r',encoding='utf-8') as f:
        print(f.tell())
        flines = f.readlines()
        print(flines[startLine])
        flines[startLine] = flines[startLine].replace('\n','') + ' {\n'
        print(flines[startLine])
        flines[startLine + 1] = flines[startLine + 1].replace('\n','') + ' }\n'
        lines = flines
    # if lines != None:
    #     with open(file = filePath,mode = 'w',encoding='utf-8') as f:
    #         f.writelines(lines)

    


if __name__ == "__main__":
    srcPath = sys.argv[1]
    print(srcPath)
    #issues is json objects
    issues = collectIssues('xxx','false','MAJOR','CODE_SMELL','500')
    dealIssues(issues,srcPath)


