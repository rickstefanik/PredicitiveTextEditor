#!/usr/bin/env python3

import sys
#import getch
import os
import operator
#import requests
import string
import re
import timeit
import time
from tkinter import *

t = ""
benchmarking = False
debugging = False

def usage(status=0):
    print("Usage: " + sys.argv[0] + ' -h -d -b -f InputFileToLearnFrom -t InputFileToType -s NumberOfSuggestions -d')
    print("\t-h help mode")
    print("\t-d debug mode")
    print("\t-b benchmarking mode")
    time.sleep(1)
    exit(status)




def print_suggestions(ret):
    global debugging
    if debugging:
        for i, r in enumerate(ret):
            print(str(i + 1)  + ": " + str(r))

def get_suggestions_string(ret):
    global debugging
    r2 = ""
    for i, r in enumerate(ret):
        r2 = r2 + str(i + 1)  + ": " + str(r) + "\n"
    return r2


def get_internet_words(word, InternetWords, l):
    global debugging
    ret = []
    for k in InternetWords:
        if k.startswith(word):
            if (k not in ret) and (not k.isspace()) and (len(k) > 0):
                ret.append(k)
        if len(ret) == l:
            return ret
    return ret

def get_all_words(word, AllWords, l):
    global debugging
    ret = []
    if len(AllWords) > 0:
        sortedAllWords = sorted(AllWords.items(), key = operator.itemgetter(1), reverse=True)
        for i in sortedAllWords:
            if i[0].startswith(word):
                if (i[0] not in ret) and (not i[0].isspace()) and (len(i[0]) > 0):
                    ret.append(i[0])
                if (len(ret) == l):
                    return ret
    return ret


def get_our_words(word, OurWords, l):
    global debugging
    ret = []
    if len(OurWords) > 0:
        sortedOurWords = sorted(OurWords[prevWord].items(), key = operator.itemgetter(1), reverse=True)
        if debugging:
            print("In get_our_words")
            print(sortedOurWords)
        for i in sortedOurWords:
            if debugging:
                print("List entry: " + str(i))
            if i[0].startswith(word):
                if (i[0] not in ret) and (not i[0].isspace()) and (len(i[0]) > 0):
                    ret.append(i[0])
                if (len(ret) == l):
                    return ret
    return ret


def handle_no_prevWord(iWords):
    global debugging
    ret = []
    for i in iWords:
        ret.append(i)
    return ret

def handle_not_in_OurWords(aWords, iWords, l):
    global debugging
    ret = []
    for a in aWords:
        ret.append(a)

    if len(ret) < l: 
        for i in iWords:
            if i not in ret:
                ret.append(i)
            if (len(ret) == l):
                return ret
    return ret

def handle_in_OurWords(oWords, aWords, iWords, l):
    global debugging
    if debugging:
        print ("In handle_in_OurWorlds")
    ret = []
    for o in oWords:
        ret.append(o)

    if len(ret) < l:
        for a in aWords:
            if a not in ret:
                ret.append(a)
            if len(ret) == l:
                return ret
    if len(ret) < l:
        for i in iWords:
            if i not in ret:
                ret.append(i)
            if len(ret) == l:
                return ret
    return ret


def get_suggestions(prevWord, word, OurWords, AllWords, InternetWords, l):
    global debugging
    if debugging:
        print("prevWord: " + prevWord + "\tword: " + word)
    iWords = get_internet_words(word, InternetWords, l)
    if prevWord == "":
        return handle_no_prevWord(iWords)
    
    aWords = get_all_words(word, AllWords, l)
    if prevWord not in OurWords:
        return handle_not_in_OurWords(aWords, iWords, l)
    
    oWords = get_our_words(word, OurWords, l)
    return handle_in_OurWords(oWords, aWords, iWords, l)

def remove_prefix(s, pre):
    if s.startswith(pre):
        return s[len(pre):]
    return s

def strip_punctuation(s):
    return ''.join(ch for ch in s if ch not in string.punctuation).rstrip()

def key_pressed(char):
	global debugging
	global t
	if (len(char) > 0):
		if (char.isdigit() == False) and (ord(char) != 127) and (ord(char) != 8) and (char != '`'):
			t = t + char
		if debugging:
			os.system("clear")
			#print_suggestions()
			print(t)
			print(str(ord((char))))
	return char


def update_dictionaries():
    global debugging
    global InternetWords
    global AllWords
    global OurWords
    global word
    global prevWord
    if debugging:
        print("word: " + word)
    if prevWord != "":
        if debugging:
            print("In prevWord != """)
        if prevWord in OurWords:
            if debugging:
                print ("prevWord is " + prevWord + " word is: " + word + ".  In the if block")
            if word in OurWords[prevWord]:
                OurWords[prevWord][word] = OurWords[prevWord][word] + 1
            else:
                OurWords[prevWord][word] = 1
        else:
            if debugging:
                print ("prevWord is " + prevWord + " word is: " + word + ".  In the else block")
            OurWords[prevWord] = {}
            OurWords[prevWord][word] = 1

    if word in AllWords:
        AllWords[word] = AllWords[word] + 1
    else:
        AllWords[word] = 1
    if debugging:
        print("\nAllWords:")
    for q in AllWords:
        if debugging:
            print(q + ": " + str(AllWords[q])) 
       
    if debugging:
        print("Key: " + word + " Value: " + str(AllWords[word]))
        print("\nOurWords:")
    for p in OurWords:
        for w in OurWords[p]:
            if debugging:
                print(p + ": (" + w + ": " + str(OurWords[p][w]) + ")") 
    if debugging:
        print("")
    prevWord = word
    word = ""

def save_file(filename = ''):
    global debugging
    global t
    global e
    global inSaveText
    global file_text
    inSaveText = False
    toAdd = ''
    f_name = filename
    if f_name == '':
        toAdd = '\n'
        f_name = e.get()
        e.destroy()
        #e = Entry(root, text = "", width = 50)
        #e.pack()
        e = Entry(root, text = "", width = 20)
        e.grid(row = 5, column = 0, sticky = SW)

    if f_name =='':
        if debugging:
            print("error")
    else:
        if debugging:
            print(f_name)
        f = open(f_name, "w")
        f.write(t + toAdd)
        f.close()
        if debugging:
            print('File saved')
        file_text = Label(root, text="File Saved!", font="Helvetica 18 bold", wraplength = 300, bg = "grey", fg = "white")
        file_text.grid(row = 2, column= 2, columnspan = 2, sticky = NSEW)


def read_file(filename):
    global debugging
  #  print("In read file")
    start = time.time()
    global word
    global prevWord
    f = -1
    try:
    	f = open(filename, "r")
    except:
        print("File could not be opened")
        return -1
    iString = ''
    for l in f:
        iString = iString + l
    h = iString.split()
    input_words = [strip_punctuation(word) for word in h]
    if debugging:
        print(input_words)
    for i in range(0, len(input_words) - 1):
        if debugging:
            print (input_words[i] + ": " + input_words[i+1])
        word = input_words[i+1]
        prevWord = input_words[i]
        update_dictionaries()
    end = time.time()
#    if (testing):
#        print("inside read_file")
#        print("Time to type file: " + str(end - start) + "s")
    return str(end - start)


def return_to_text():
    global fontSize
    global debugging
    global e
    global inSaveText
    global file_text
    inSaveText = False
    print(fontSize.get())
    oldText = e.get()
    if debugging:
        print("oldText: " + oldText)
    e.destroy()
    if debugging:
        print("oldText: " + oldText)
    #e = Entry(root, width = 50)
    #e.pack()
    e = Entry(root, text = "", width = 20)
    e.grid(row = 5, column = 0, sticky = SW)
    e.insert(0, oldText)
    #e['text'] = oldText
    file_text.destroy()


def close_window():
    root.destroy()

def get_key(event):
    global debugging
    global word
    global t
    global prevWord
    global OurWords
    global AllWords
    global InternetWords
    global numSuggestions
    global e
    global prevEntryLength
    global inSaveText
    global file_text

    currentEntryLength = len(e.get())
    if (currentEntryLength != prevEntryLength) and (currentEntryLength != 0):
        inSaveText = True
        prevEntryLength = currentEntryLength

        if ord(event.char) == 7:
            if debugging:
                print("hit escape key")
            return_to_text()
        return

    if inSaveText:
        return

    c = key_pressed(event.char)
    #if (c != ' ') and (len(c) > 0):
    if len(c) == 0:
	    return
    if c != ' ':
        if (ord(c) == 127) or (ord(c) == 8):
            if debugging:
                print("inside backspace")
            t = t[:-1]
            word = word[:-1]

            if debugging:
                os.system("clear")
                print(t)


        if (not c.isdigit()) and (ord(c) != 127) and (ord(c) != 8):
            word = word + c
            word = strip_punctuation(word)

        r = get_suggestions(prevWord, word, OurWords, AllWords, InternetWords, numSuggestions)
        print_suggestions(r)
        
        if c.isdigit():
        #    print("inside isdigit")
            if int(c) > len(r):
                return
            if len(r) <= 0:
                return
            wordToBeTyped = r[int(c) - 1]
            if debugging:
                print("wordToBeTyped: " + wordToBeTyped)
            wordToBeTyped = remove_prefix(wordToBeTyped, word)
            t = t + wordToBeTyped + ' '
            if debugging:
                os.system("clear")
                print(t)
            word = word + wordToBeTyped
            update_dictionaries()
            #prevWord = word + wordToBeTyped
            #word = ""
        if debugging:
            print(str(ord(c)))

    else:
        update_dictionaries()
    r = get_suggestions(prevWord, word, OurWords, AllWords, InternetWords, numSuggestions)
    suggestionString = get_suggestions_string(r) 
    if debugging:
        print_suggestions(r)
    real_text['text'] = t
    sugg_text['text'] = suggestionString
    file_text.destroy()



def get_key_from_file(ch):
    global debugging
    global word
    global t
    global prevWord
    global OurWords
    global AllWords
    global InternetWords
    global numSuggestions
    global e
    global prevEntryLength

    currentEntryLength = len(e.get())
    if (currentEntryLength != prevEntryLength) and (currentEntryLength != 0):
        prevEntryLength = currentEntryLength

        if ord(ch) == 7:
            if debugging:
                print("hit escape key")
            return_to_text()
        return


    c = key_pressed(ch)
    if c != ' ':
        if (ord(c) == 127) or (ord(c) == 8):
            if debugging:
                print("inside backspace")
            t = t[:-1]
            word = word[:-1]

            if debugging:
                os.system("clear")
                print(t)


        if (not c.isdigit()) and (ord(c) != 127) and (ord(c) != 8):
            word = word + c
            word = strip_punctuation(word)

        r = get_suggestions(prevWord, word, OurWords, AllWords, InternetWords, numSuggestions)
        print_suggestions(r)
        
        '''if c.isdigit():
        #    print("inside isdigit")
            if int(c) > len(r):
                return

            wordToBeTyped = r[int(c) - 1]
            if debugging:
                print("wordToBeTyped: " + wordToBeTyped)
            wordToBeTyped = remove_prefix(wordToBeTyped, word)
            t = t + wordToBeTyped + ' '
            if debugging:
                os.system("clear")
                print(t)
            word = word + wordToBeTyped
            update_dictionaries()
            #prevWord = word + wordToBeTyped
            #word = ""'''
        if debugging:
            print(str(ord(c)))

    else:
        update_dictionaries()
    r = get_suggestions(prevWord, word, OurWords, AllWords, InternetWords, numSuggestions)
    suggestionString = get_suggestions_string(r)
    if debugging:
        print_suggestions(r)
    real_text['text'] = t
    sugg_text['text'] = suggestionString
    #time.sleep(.5)


def type_file(filename):
    global debugging
    start = time.time()
    global word
    global prevWord
    f = -1 
    try:
    	f = open(filename, "r")
    except:
        print("File could not be opened")
        return -1
    iString = ''
    for l in f:
        iString = iString + l
    for c in iString:
        get_key_from_file(c)
    end = time.time()
    return str(end - start)
    #h = iString.split()
    #input_words = [strip_punctuation(word) for word in h]
    #print(input_words)
    #for i in range(0, len(input_words) - 1):
    #    print (input_words[i] + ": " + input_words[i+1])
    #    word = input_words[i+1]
    #    prevWord = input_words[i]
    #    update_dictionaries()


def change_font_size(fontSize):
    global t
    global real_text
    global fontType
    real_text.destroy()
    real_text = Label(root, text=t, font = fontType.get() + ' ' + fontSize + ' bold', wraplength = 300, bg = "grey", fg = "white")
    real_text.grid(row = 4, column= 0, columnspan = 5, sticky = N+E+S+W)
    
def change_font_type(fontType):
    global t
    global real_text
    global fontSize
    real_text.destroy()
    real_text = Label(root, text=t, font = fontType + ' ' + fontSize.get() + ' bold', wraplength = 300, bg = "grey", fg = "white")
    real_text.grid(row = 4, column= 0, columnspan = 5, sticky = N+E+S+W)

    


#URL = "https://raw.githubusercontent.com/first20hours/google-10000-english/master/google-10000-english.txt"
#InternetWords = requests.get(URL).text.splitlines()

iwFile = open("./common_words.txt", "r")
InternetWords = [w.rstrip() for w in iwFile]
iwFile.close()
AllWords = {}
OurWords = {}

prevWord = ""
word = ""
prevEntryLength = 0;

numSuggestions = 3

input_learning_file = ''
input_typing_file = ''

inSaveText = False

#parse command line arguments
argind = 1
while (argind < len(sys.argv)):
    if (sys.argv[argind] == '-h'):
        usage(0)
    if (sys.argv[argind] == '-d'):
        debugging = True
    if (sys.argv[argind] == '-b'):
        benchmarking = True
    elif (sys.argv[argind] == '-s'):
        argind = argind + 1
        if (argind >= len(sys.argv)):
            usage(1)
        numSuggestions = int(sys.argv[argind])
    elif (sys.argv[argind] == '-f'):
        argind = argind + 1
        if (argind >= len(sys.argv)):
            usage(1)
        input_learning_file = sys.argv[argind]
    elif (sys.argv[argind] == '-t'):
        argind = argind + 1
        if (argind >= len(sys.argv)):
            usage(1)
        input_typing_file = sys.argv[argind]
    else:
        usage(1)

    argind = argind + 1





root = Tk()
root.geometry('900x500')

root.rowconfigure(4, weight = 1)
root.columnconfigure(8, weight = 1)

p1 = PanedWindow(master = root, bg = "grey", orient=VERTICAL)
p1.grid(row = 4, column = 0, columnspan=5, sticky = N+E+S+W)

p2 = PanedWindow(master = root, bg = "grey",orient=VERTICAL)
p2.grid(row = 4, column = 4, columnspan=5, sticky = N+E+S+W)


fontSize = StringVar(root)
fontSize.set("18")

fontType = StringVar(root)
fontType.set("Helvetica")



file_text = Label(root, text="File Saved!", font="Helvetica 18 bold", wraplength = 300, bg = "grey", fg = "white")
file_text.grid(row = 2, column= 2, columnspan = 2, sticky = NSEW)
file_text.destroy()

real_text = Label(root, text="Welcome to the Text Predictor", font = "Helvetica 18 bold", wraplength = 300, bg = "grey", fg = "white")
real_text.grid(row = 0, columnspan = 5, sticky = "NW")

p1.add(real_text)

sugg_text = Label(root, font = "Helvetiva 16", text="Suggestions" )
sugg_text.grid(row = 4, column = 6, sticky= W)

p2.add(sugg_text)

root.bind('<Key>', get_key)

button = Button (root, text = "Exit", font = 'Helvetica 16 bold', fg = "blue", bg = "grey", command = close_window)
button.grid(row = 5, column = 8, sticky = SE)

saveButton = Button (root, text = "Save", font = 'Helvetica 16 bold', fg = "blue", bg = "grey", command = save_file)
saveButton.grid(row = 5, column = 1, sticky = SE)

returnButton = Button (root, text = "Return to Typing", font = 'Helvetica 16 bold', fg = "blue", bg = "grey", command = return_to_text)
returnButton.grid(row = 5, column = 2, sticky = S)


e = Entry(root, text = "", width = 20)
e.grid(row = 5, column = 0, sticky = SW)
toFileName = e.get()


fontSizeLabel  = Label(root, font = "Helvetiva 14", text="Font Size" )
fontSizeLabel.grid(row = 5, column = 7, sticky = E)
fontSizeOptions = OptionMenu(root, fontSize, "10", "12", "14", "16", "18", "20", "22", command = change_font_size)
fontSizeOptions.grid(row = 5, column = 8, sticky = W)

fontTypeLabel  = Label(root, font = "Helvetiva 14", text="Font Type" )
fontTypeLabel.grid(row = 5, column = 5, sticky= E)
fontTypeOptions = OptionMenu(root, fontType, "Helvetica", "Times", "Arial", "Courier", "Serif",  command = change_font_type)
fontTypeOptions.grid(row = 5, column = 6)


'''#parse command line arguments
argind = 1
while (argind < len(sys.argv)):
    if (sys.argv[argind] == '-h'):
        usage(0)
    if (sys.argv[argind] == '-d'):
        debugging = True
    if (sys.argv[argind] == '-b'):
        benchmarking = True
    elif (sys.argv[argind] == '-s'):
        argind = argind + 1
        if (argind >= len(sys.argv)):
            usage(1)
        numSuggestions = int(sys.argv[argind])
    elif (sys.argv[argind] == '-f'):
        argind = argind + 1
        if (argind >= len(sys.argv)):
            usage(1)
        input_learning_file = sys.argv[argind]
    elif (sys.argv[argind] == '-t'):
        argind = argind + 1
        if (argind >= len(sys.argv)):
            usage(1)
        input_typing_file = sys.argv[argind]
    else:
        usage(1)

    argind = argind + 1'''

elapsed1 = 0
elapsed2 = 0

if (input_learning_file != ''):
    if debugging:
        print("input learning file being read")
    elapsed1 = read_file(input_learning_file)
    if elapsed1 == -1:
        exit(1)
  #  if (testing):
  #      print("Time to learn from file: " + str(elapsed1) + "s")

word = ""
prevWord = ""

if (input_typing_file != ''):
    elapsed2 = type_file(input_typing_file)
    if elapsed2 == -1:
    	exit(1)
 #   if (testing):
 #       print("Time to type file: " + str(elapsed2) + "s")

if (benchmarking):
    #print("Time to learn from file: " + str(elapsed1) + "s")
    #print("Time to type file: " + str(elapsed2) + "s")
    save_file('TestingSaveFile.txt')
    close_window()

#type_file("lyrics.txt")
root.mainloop()
