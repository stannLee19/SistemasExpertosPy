from gtts import gTTS
import os

import nltk
import urllib.request
import re
from inscriptis import get_text
from nltk import word_tokenize, sent_tokenize
from googletrans import Translator

#nltk.download()

#articulo de wikipedia
#enlace = "https://en.wikipedia.org/wiki/Super_Bowl_LVII"

#html = urllib.request.urlopen(enlace).read().decode('utf-8')
text = "Super Bowl LVII was an American football game played to determine the champion of the National Football League (NFL) for the 2022 season. The American Football Conference (AFC) champion Kansas City Chiefs defeated the National Football Conference (NFC) champion Philadelphia Eagles, 38–35. The game was played on February 12, 2023, at State Farm Stadium in Glendale, Arizona. It was the fourth Super Bowl hosted by the Phoenix metropolitan area, and the third at this venue, with the most recent previously being Super Bowl XLIX in 2015.[6]"

article_text = text.replace("[ edit ]", "")
print("#############################################")

from nltk import word_tokenize, sent_tokenize
#Removing Square Brackets and Extra Spaces
article_text = re.sub(r'\[[0-60]*\]', ' ', article_text)
article_text = re.sub(r'\s+', ' ', article_text)

formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text )
formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)

#nltk.download()
#En esta parte hace la tokenizacion
sentence_list = nltk.sent_tokenize(article_text)

#En esta parte encuentra la frecuencia de las palabras
stopwords = nltk.corpus.stopwords.words('english')

word_frequencies = {}
for word in nltk.word_tokenize(formatted_article_text):
    if word not in stopwords:
        if word not in word_frequencies.keys():
            word_frequencies[word] = 1

#Calcula las frases que mas se repiten
sentences_socores = {}
for sent in sentence_list:
    for word in nltk.word_tokenize(sent.lower()):
        if word in word_frequencies.keys():
            if len(sent.split(' ')) < 30:
                if sent not in sentences_socores.keys():
                    sentences_socores[sent] = word_frequencies[word]
                else:
                    sentences_socores[sent] += word_frequencies[word]

maximum_frequncy = max(word_frequencies.values())

for word in word_frequencies.keys():
    word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)

#Realiza el resumen con las mejores frases
import heapq
summary_sentences = heapq.nlargest(7, sentences_socores, key=sentences_socores.get)

summary = ' '.join(summary_sentences)

#print(summary)
Traductor= Translator()
traducido = Traductor.translate(summary, dest= 'spanish')
print(traducido.text)



speech = gTTS(text=traducido.text,lang='es',slow=False)
speech.save('texto.mp3')
os.system("start texto.mp3")