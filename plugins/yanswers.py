import urllib
import urllib2
from xml.dom import minidom
from util import hook, http

def parseQuestion(ques):
    ques_ = {}
    for node in ques.childNodes:
        if node.nodeType == node.ELEMENT_NODE and not node.nodeName == 'Answers' :
            ques_.update(__getData(node.toxml()))
    return ques_

def __getData(node):
    i = node.find('>')
    j = node.rfind('<')
    k = node.find(' ')
    return {node[1:i]:node[i+1:j]}
class Answers:
    def __init__(self):
        self.appid = 'YahooDemo'

    def questionSearch(self, params):
        """Answers questionSearch wrapper"""
        baseUrl = 'http://answers.yahooapis.com/AnswersService/V1/questionSearch?appid='+self.appid+'&'
        finalUrl = baseUrl
        for k, v in params.items():
            finalUrl = finalUrl + urllib.quote(k) +'=' + urllib.quote(v) + '&'
        finalUrl = finalUrl[:len(finalUrl) - 1]
        site = urllib2.urlopen(finalUrl)
        xmlDoc = minidom.parse(site)
        questions = xmlDoc.getElementsByTagName('Question')
        qList = []
        for ques in questions:
            qList.append(parseQuestion(ques))
        answers = xmlDoc.getElementsByTagName('Answers')
        for ans in answers:
            qList.append(parseQuestion(ans))
        return qList


    def getByCategory(self, params):
        """Answers getByCategory wrapper"""
        baseUrl = 'http://answers.yahooapis.com/AnswersService/V1/getByCategory?appid='+self.appid+'&'
        finalUrl = baseUrl
        for k, v in params.items():
            finalUrl = finalUrl + urllib.quote(k) +'=' + urllib.quote(v) + '&'
        finalUrl = finalUrl[:len(finalUrl) - 1]
        #print finalUrl
        site = urllib2.urlopen(finalUrl)
        xmlDoc = minidom.parse(site)
        questions = xmlDoc.getElementsByTagName('Question')
        qList = []
        for ques in questions:
            qList.append(parseQuestion(ques))
        return qList

    def getByUser(self, params):
        """Answers getByUser wrapper"""
        baseUrl = 'http://answers.yahooapis.com/AnswersService/V1/getByUser?appid='+self.appid+'&'
        finalUrl = baseUrl
        for k, v in params.items():
            finalUrl = finalUrl + urllib.quote(k) +'=' + urllib.quote(v) + '&'
        finalUrl = finalUrl[:len(finalUrl) - 1]
        #print finalUrl
        site = urllib2.urlopen(finalUrl)
        xmlDoc = minidom.parse(site)
        questions = xmlDoc.getElementsByTagName('Question')
        qList = []
        for ques in questions:
            qList.append(parseQuestion(ques))
        return qList


    def getQuestion(self, params):
        """Answers getByUser wrapper"""
        baseUrl = 'http://answers.yahooapis.com/AnswersService/V1/getQuestion?appid='+self.appid+'&'
        finalUrl = baseUrl
        for k, v in params.items():
            finalUrl = finalUrl + urllib.quote(k) +'=' + urllib.quote(v) + '&'
        finalUrl = finalUrl[:len(finalUrl) - 1]
        #print finalUrl
        site = urllib2.urlopen(finalUrl)
        xmlDoc = minidom.parse(site)
        questions = xmlDoc.getElementsByTagName('Question')
        qList = []
        for ques in questions:
            qList.append(parseQuestion(ques))
        answers = xmlDoc.getElementsByTagName('Answer')
        for ans in answers:
            qList.append(parseQuestion(ans))
        return qList

@hook.command
def asearch(inp, say=None):
    try:
     query = inp.replace(".asearch ","")
    except:
     say("API returned no results. Try something else.")

    app = Answers()
    app.appid = 'EvEqBffV34HZbCrZ7CM1_2N77mhcG.okBb2BNEe7OfcEYXDC90fUia8IDzbt7GPQZC45AOBmlySiAhzuC0Tpsg--'

    try:
      questions = app.questionSearch({'query':query})
      qid = questions[0]['Link']
      qid = qid.replace("http://answers.yahoo.com/question/?qid=","")
      c = app.getQuestion({'question_id':qid})
    except:
      finalise = "Not found."

    try:
        questionAsked = c[0]['Content']
        questionAsked = questionAsked.replace("\n", " ")
        chosenAnswer = c[0]['ChosenAnswer']
        chosenAnswer = chosenAnswer.replace("\n", " ")
        finalise = "Q: %s -- A: %s" % (questionAsked, chosenAnswer)
        questionAsked = questionAsked.replace("&amp;", "&")
        questionAsked = questionAsked.replace("&lt;", "<")
        questionAsked = questionAsked.replace("&gt;", ">")
        questionAsked = questionAsked.replace("&quot;", "\"")
        chosenAnswer = chosenAnswer.replace("&amp;", "&")
        chosenAnswer = chosenAnswer.replace("&lt;", "<")
        chosenAnswer = chosenAnswer.replace("&lt;", "<")
        chosenAnswer = chosenAnswer.replace("&quot;", "\"")
        chosenAnswer = "\x0309[A]\x0F "+chosenAnswer
        questionAsked = "\x0309[Q]\x0F "+questionAsked

    except:
        questionAsked = "Invalid - no question."
        chosenAnswer = "No answer chosen yet."
        finalise = "Not found or not answered yet."

    say(questionAsked)
    say(chosenAnswer)
