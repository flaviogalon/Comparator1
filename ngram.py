import collections
import sys
import matplotlib.pyplot as plt


def classify_sent(sent_cnt, rel_prob1, rel_prob2):
	score1 = 0.0
	score2 = 0.0

	for k, v in sent_cnt.iteritems():
		score1 += rel_prob1.get(k, 0.0)*v
		score2 += rel_prob2.get(k, 0.0)*v
	return score1, score2

def classify_text_table(test_input, rel_prob1, rel_prob2, n, label):
	print "Begin classify_text_table", label
	correct_lang = 0
	wrong_lang = 0
	for sentence in test_input:
		sent_cnt = create_sentence_counter(sentence, n)
		score1, score2 = classify_sent(sent_cnt, rel_prob1, rel_prob2)
		#print "Score1: ", score1
		#print "Score2: ", score2
		if score1 > score2:
			#print "Sentence from language 1\n"
			if label == 1:
				correct_lang += 1
			else:
				wrong_lang += 1
		elif score1 < score2:
			#print "Sentence from language 2\n"
			if label == 2:
				correct_lang += 1
			else:
				wrong_lang += 1
		else:
			print "Impossible to identify"
		
	return correct_lang, wrong_lang

def classify_confusion_matrix (test_input_1, test_input_2, rel_prob1, rel_prob2, n):
	print "Begin classify_confusion_matrix"
	correct_lang_1, wrong_lang_1 = classify_text_table(test_input_1, rel_prob1, rel_prob2, n, 1)
	correct_lang_2, wrong_lang_2 = classify_text_table(test_input_2, rel_prob1, rel_prob2, n, 2)

	print "\tlang 1\tlang 2"
	print "lang 1\t", correct_lang_1, "\t", wrong_lang_1
	print "lang 2\t", wrong_lang_2, "\t", correct_lang_2
	print "\nPrecision for language 1: ", float(correct_lang_1)/(correct_lang_1+wrong_lang_2)
	print "Recall for language 1: ", float(correct_lang_1)/(correct_lang_1+wrong_lang_1)
	print "Precision for language 2: ", float(correct_lang_2)/(correct_lang_2+wrong_lang_1)
	print "Recall for language 2: ", float(correct_lang_2)/(correct_lang_2+wrong_lang_2)
	print "Accuracy: ", float(correct_lang_1+correct_lang_2)/(correct_lang_1+correct_lang_2+wrong_lang_1+wrong_lang_2)

	accuracy = float(correct_lang_1+correct_lang_2)/(correct_lang_1+correct_lang_2+wrong_lang_1+wrong_lang_2)
	return accuracy
	
def classify_text(test_input, rel_prob1, rel_prob2, n):
	#print rel_prob1
	for sentence in test_input:
		sent_cnt = create_sentence_counter(sentence, n)
		score1, score2 = classify_sent(sent_cnt, rel_prob1, rel_prob2)
		print "Score1: ", score1
		print "Score2: ", score2
		if score1 > score2:
			print "Sentence from language 1\n"
		elif score1 < score2:
			print "Sentence from language 2\n"
		else:
			print "Impossible to identify"
		
	return
	
def relevant_prob(prob_dic_a, prob_dic_b, min):
	rel_prob1 = {}
	rel_prob2 = {}
	
	for k, v in prob_dic_a.iteritems():
		if abs(v - prob_dic_b.get(k, 0.0)) > min:
			rel_prob1[k] = v
	for k, v in prob_dic_b.iteritems():
		if abs(v - prob_dic_a.get(k, 0.0)) > min:
			rel_prob2[k] = v
	print "Ngramas first language: ", len(prob_dic_a)
	print "Relevant ngrams first language: ", len(rel_prob1)
	print "Difference: ", len(prob_dic_a)-len(rel_prob1)
	print "Ngramas second language: ", len(prob_dic_b)
	print "Relevant ngrams second language: ", len(rel_prob2)
	print "Difference: ", len(prob_dic_b)-len(rel_prob2)
	#print rel_prob
	return rel_prob1,rel_prob2
	
def get_prob(cnt):
	s = sum(cnt.itervalues())

	prob_dic = {}

	for k, v in cnt.iteritems():
		prob_dic[k] = v/float(s)
	#print prob_dic
	#print sum(prob_dic.itervalues())
	return prob_dic
	
def get_prob_minus_1(cnt, cnt_minus_1,n):
	s = sum(cnt.itervalues())

	prob_dic = {}

	for k, v in cnt.iteritems():
		#prob_dic[k] = v/float(s)
		prob_dic[k] = float(v)/cnt_minus_1[k[:n-1]]
	##print prob_dic
	#print sum(prob_dic.itervalues())
	return prob_dic

def create_sentence_counter(sentence, n):
	cnt = collections.Counter()
	
	myNgrams = Ngrams(sentence, n)
	for ngram in myNgrams:
		cnt[ngram] += 1
	return cnt
	
def create_text_counter(input, n):
	cnt = collections.Counter()
	
	for sentence in input:
		myNgrams = Ngrams(sentence, n)
		for ngram in myNgrams:
			cnt[ngram] += 1
	return cnt

def create_text_counter_minus_1(input, n):
	cnt = collections.Counter()
	cnt_minus_1 = collections.Counter()
	
	for sentence in input:
		myNgrams, myNgrams_minus_1 = Ngrams_minus_1(sentence, n)
		for ngram in myNgrams:
			cnt[ngram] += 1
		for ngram in myNgrams_minus_1:
			cnt_minus_1[ngram] += 1
	#print cnt, cnt_minus_1
	return cnt, cnt_minus_1

def set_difference(cnt1, cnt2, n, ms):
	c1 = set(cnt1.iterkeys())#Converts the dictionaires to sets
	c2 = set(cnt2.iterkeys())
	
	dif1 = c1.difference(c2) #c1-c2
	dif2 = c2.difference(c1) #c2-c1
	
	cnt_d1 = collections.Counter()
	cnt_d2 = collections.Counter()
	
	for item in dif1:
		cnt_d1[item] = cnt1[item]
	for item in dif2:
		cnt_d2[item] = cnt2[item]
	
	return cnt_d1, cnt_d2
	
def Ngrams(sentence, n):
	myNgrams = [sentence[i:i+n] for i in range(len(sentence) - n+1)]
	return myNgrams
	
def Ngrams_minus_1(sentence, n):
	myNgrams = [sentence[i:i+n] for i in range(len(sentence) - n+1)]
	myNgrams_minus_1 = [sentence[i:i+n-1] for i in range(len(sentence) - n+1)]

	return myNgrams, myNgrams_minus_1

def runprogram(text1,text2,n,test_text_1,test_text_2,min):
    input1 = open(text1)
    input2 = open(text2)

	#cnt1 = create_text_counter(input1, n)#Dictionaire of ngrams for the first collection
	#cnt2 = create_text_counter(input2, n)#Dictionaire of ngrams for the second collection

    cnt1, cnt1_minus_1 = create_text_counter_minus_1(input1, n)#Dictionaire of ngrams for the first collection
    cnt2, cnt2_minus_1 = create_text_counter_minus_1(input2, n)#Dictionaire of ngrams for the second collection

    #cnt_d1, cnt_d2 = set_difference(cnt1, cnt2, n, ms)
    #print "lengths: ", len(cnt_d1), len(cnt_d2)


    #prob_dic1 = get_prob(cnt1)
    #prob_dic2 = get_prob(cnt2)
    prob_dic1 = get_prob_minus_1(cnt1, cnt1_minus_1,n)
    prob_dic2 = get_prob_minus_1(cnt2, cnt2_minus_1,n)

    rel_prob1, rel_prob2 = relevant_prob(prob_dic1, prob_dic2, min)
    probtoprint1 = len(rel_prob1)
    probtoprint2 = len(rel_prob2)


    test_input_1 = open(test_text_1)
    test_input_2 = open(test_text_2)
    #classify_text(test_input, rel_prob1, rel_prob2, n)
    #classify_text_table(test_input_1, test_input_2, rel_prob1, rel_prob2, n)
    datatoprint = classify_confusion_matrix(test_input_1, test_input_2, rel_prob1, rel_prob2, n)
    #	print '\nMost common ngrams in ', text1, ' but not in ', text2, '\n', cnt_d1.most_common(ms)
    #	print '\nMost common ngrams in ', text2, ' but not in ', text1, '\n', cnt_d2.most_common(ms)
    return datatoprint,probtoprint1, probtoprint2


def main():
    text1 = sys.argv[1]
    text2 = sys.argv[2]
    n = int(sys.argv[3])
    #ms = int(sys.argv[4])
    test_text_1 = sys.argv[4]
    test_text_2 = sys.argv[5]
    min = 0.0001
    analysis = []
    plotthr = []
    plotpre = []
    plotsn1 = []
    plotsn2 = []
    auxcount = 0


    print "Begin main"
    #datatoprint = runprogram(text1,text2,n,test_text_1,test_text_2,min)
    #print 'N-grams:',n,'Precision:',datatoprint,'Threshold:',min

    while min <= 0.001:
        datatoprint,probtoprint1,probtoprint2 = runprogram(text1,text2,n,test_text_1,test_text_2,min)
        analysis.append((n,datatoprint,min))
        plotpre.append(datatoprint)
        plotthr.append(min)
        plotsn1.append(probtoprint1)
        plotsn2.append(probtoprint2)
        auxcount = auxcount + 1
        min = min + 0.0001
    print analysis

    f1 = plt.figure()
    ax1 = f1.add_subplot(111)
    ax1.plot(plotthr,plotpre,'black')
    #plt.plot(plotthr,plotpre,'black')
    plt.xscale('log')
    plt.xlabel('Threshold')
    plt.ylabel('Accuracy')
    plt.savefig('plot1.png')

    f2 = plt.figure()
    ax2 = f2.add_subplot(111)
    ax2.plot(plotthr,plotsn1,'green')
    ax2.plot(plotthr,plotsn2,'blue')
    plt.xscale('log')
    plt.xlabel('Threshold')
    plt.ylabel('Number of significant N-Grams')
    plt.savefig('plot2.png')

    plt.show()




if __name__ == "__main__":
    main()
	
