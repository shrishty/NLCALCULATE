import nltk
from nltk import load_parser
from nltk.stem.wordnet import WordNetLemmatizer 

#sentence = """Beth has 106 crayons. Beth gives 54 crayons away to Jen. How many crayons does Beth have left?"""
#sentence = """Cindy has 1215 cookies . Paul has 1112 cookies . They both brought them to school for a party. How many cookies did they have in total?"""
#sentence = """Raina has 5 bottles. Raina gave 2 bottles to Nithya. Shilpa has 10 bottles. Shilpa gave 3 bottles to Raina. Shilpa gave 1 bottles to Nithya. How many bottles does Raina have?"""
#sentence = "Paul got 479 crayons. At the end of the school year, Paul only had 134 crayons left. How many crayons had been lost or given away by Paul?"
#sentence = "There were 50 apples in a basket. 20 apples were taken out from the basket . How many apples are left in the basket."
#sentence = "Meena has 40 apples. Meena has 10 mangoes. Riya has 20 mangoes. Riya gave 10 mangoes to Meena. How many mangoes are there in total? "

sentence = "Meera bought 20 pencils. Meera has given 10 pencils to Shyam. Meera bought 5 pencils. What are the total number of pencils that Meera has?"

lmtzr = WordNetLemmatizer()
sublist = ['give', 'given','gave', 'gives', 'throw','threw', 'lost', 'delete','deleted', 'left','loose', 'away', 'out']
addlist = ['has', 'acquire', 'take', 'get', 'got', 'bought']
universalsum = ['altogether', 'all', 'total']
l1 = sentence.split('.')
print l1

subjects = {}
flag = 1

for y in l1:
    tokens = nltk.word_tokenize(y)
    tagged = nltk.pos_tag(tokens)
    print tagged
    la = nltk.chunk.ne_chunk(tagged)
    
    ques = 0
    sub1 = ""
    sub2 = ""
    obj = ""
    objcount = 0
    flag = 0
    ques = 0
    givento = 0
    inflag = 0
    
    for x in tagged:
        if(x[1] == 'NNP' or x[1] == 'NN'):       # Proper noun, singular
            if givento == 1:
                sub2 = x[0]
            else:
                sub1 = x[0]
        elif(x[1] == 'TO'):                      # to
            givento = 1
        elif(x[1] == 'NNS'):                     # Plural noun
            obj = lmtzr.lemmatize(x[0])
        elif(x[1] == 'IN' and ques != 1):        # for, from, in etc    
            if(x[0] == 'in'):
                flag = 1
                inflag = 1
            if(x[0] == 'from'):
                flag = 2
                inflag = 1
        elif(x[1] == 'VBZ'):                     # Verb, 3rd person singular present
            if(x[0] in addlist):
                flag = 1
            if(x[0] in sublist):
                flag = 2
        elif(x[1] == 'VBD'):                     # Verb, past tense
            if(x[0] in addlist):
                flag = 1
            if(x[0] in sublist):
                flag = 2
        elif(x[1] == 'VBN'):                     # Verb, past participle
            if(x[0] in addlist):
                flag = 1
            if(x[0] in sublist):
                flag = 2            
        elif(x[1] == 'CD'):                      # Cardinal number
            objcount = int(x[0]) 
        elif(x[1] == 'WRB' or x[1] == 'WP'):     # Whadverb
            ques  = 1
        elif(x[1] == 'RB' and x[0] in universalsum):      # RB Adverb
            flag = 3
        elif(x[1] == 'JJ' and x[0] in universalsum):      # JJ Adjective
            flag = 3

    if y:
        print sub1, sub2, obj, objcount
        if(sub1 != "" and (sub1, obj) not in subjects.keys() and givento != 1):
            subjects[sub1, obj] = 0
        if(sub2 != "" and (sub2, obj) not in subjects.keys()):
            subjects[sub2, obj] = 0
        if(givento == 1):
            if(sub1 != "" and obj != "" and sub2 != ""):
                subjects[sub1, obj] = subjects[sub1, obj] - objcount
                subjects[sub2, obj] = subjects[sub2, obj] + objcount
        elif(flag == 1 and ques != 1):
            subjects[sub1, obj] = subjects[sub1, obj] + objcount
        elif(flag == 2 and ques != 1):
            subjects[sub1, obj] = subjects[sub1, obj] - objcount
        elif(ques == 1):
            if(flag == 3):
                sum = 0
                for i in subjects:
                    if i[1] == obj:
                        sum = sum + subjects[i]
                print sum
            else:
                if((sub1, obj) in subjects.keys()):
                    print subjects[sub1, obj]
                else:
                    print "Reached Exception1"
        else:
            print "Reached Exception2"
    
        
#for x in subjects:
#   print x, subjects[x]

#cp = load_parser('grammars/book_grammars/sql0.fcfg')
#query = 'Paul got a box of 479 crayons for his birthday'
#trees = cp.nbest_parse(query.split())
#answer = trees[0].node['SEM']
#q = ' '.join(answer)
#print q
