from django.shortcuts import render , redirect
import requests
from bs4 import BeautifulSoup
import operator
from collections import Counter
from .models import ProModel
from django.contrib import messages

# Create your views here.
def frequency(request):
    return render(request,"frequency.html")


def start(url):
        wordlist = []
        rem = ['a','an','continue','hold','remain','occur','transpire','may','can','will','do','say','go','get','make','know','think',
            'take','see','come','want','look','use','find','give','tell','when','now','how','also','not','as','up','here','there',
            'so','very','immediately','initially','additionally','nearby','extremely','greatly','time','year','people','day','man',
            'thing','woman','work','child','life','world','way','back','I','you','your','he','she','them','their','her','him','me','my',
            'it','its','our','these','this','that','those','who','what','which','all','jest','even','first','many','one','two','some',
            'like','other','more','new','any','down','and','or','if','because','but','than','of','in','to','for','with','on','by','out'
            ,'into','about','at','the','is','are','am']
        source_code = requests.get(url).text
        soup = BeautifulSoup(source_code, 'html.parser')
        for each_text in soup.findAll():
            content = each_text.text
            words = content.lower().split()
            for each_word in words:
                if each_word in rem:
                    continue
                else:
                    wordlist.append(each_word)
        topp = clean_wordlist(wordlist)
        return topp

def clean_wordlist(wordlist):
        clean_list = []
        for word in wordlist:
            symbols = '!@#$%^&*()_-+={[}]|\;:"<>?/., '
            for i in range(0, len(symbols)):
                word = word.replace(symbols[i], '')
            if len(word) > 0:
                clean_list.append(word)
        ttt = create_dictionary(clean_list)
        return ttt

def create_dictionary(clean_list):
        word_count = {}
        for word in clean_list:
            if word in word_count:
                word_count[word] += 1
            else:
                word_count[word] = 1
        c = Counter(word_count)
        top = c.most_common(10)
        return top

def result(request):
    url = request.POST["url"]
    if ProModel.objects.filter(url = url).exists():
        top = ProModel.objects.filter(url = url)[0].data
        sorted_top = dict(sorted(top.items(), key=operator.itemgetter(1), reverse=True))
        context = {'top':sorted_top}
        messages.add_message(request, messages.ERROR, "URL is already processed")
        return render(request,"result.html",context)
    top = start(url)
    top = dict(top)
    user = ProModel(url = url , data = top).save()
    context = {"top":top}
    return render(request,"result.html",context)