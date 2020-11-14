import numpy as np
import math
from collections import OrderedDict
import nltk

class BagBot:
    #determines how important unknown words are for the bigram probabilites, higher means unknown words are more important
    bigram_smoothing_parameter = 0.0
    #determines hwo important the bigram function is in the result of the overall function
    bigram_lambda = 0.0
    #determines how important unknown words are for the unigram probabilities, higher means unknown words are more important
    unigram_smoothing_parameter = 0.0
    #chance of a question being a statement or an answer
    question_prior = 0.5


    #storing information from training for easy and fast reference
    uni_questionUnique = 0
    uni_questionTotal = 0
    uni_answerUnique = 0
    uni_answerTotal = 0
    bi_questionUnique = 0
    bi_questionTotal = 0
    bi_answerUnique = 0
    bi_answer_total = 0

    #Each dictionary of words and bigram phrases stored as {phrase: Count()}
    bigram_question_dictionary = {}
    bigram_answer_dictionary = {}
    unigram_question_dictionary = {}
    unigram_answer_dictionary = {}
    
    #list of nltk stop words
    stopWords = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]

    def ___init___(self, question_prior):
        self.questionProb = question_prior

    def train(self, train_set, train_labels, dev_set, unigram_smoothing_parameter=.4, bigram_smoothing_parameter=.009, bigram_lambda=.5,pos_prior=0.8):
        """
        sets the unigram and bigram positive and negative dictionaries given the training set

        train_set - List of list of words corresponding with each movie review
        example: suppose I had two reviews 'like this movie' and 'i fall asleep' in my training set
        Then train_set := [['like','this','movie'], ['i','fall','asleep']]

        train_labels - List of labels corresponding with train_set
        example: Suppose I had two reviews, first one was positive and second one was negative.
        Then train_labels := [1, 0]

        dev_set - List of list of words corresponding with each review that we are testing on
                It follows the same format as train_set

        unigram_smoothing_parameter - The smoothing parameter for unigram model (same as above) --laplace (1.0 by default)
        bigram_smoothing_parameter - The smoothing parameter for bigram model (1.0 by default)
        bigram_lambda - Determines what fraction of your prediction is from the bigram model and what fraction is from the unigram model. Default is 0.5
        pos_prior - The prior probability that a word is positive.
        
        positive(1) represents that the input is a question, negative(0) represents that the input is an answer
        """
        #presetting inputs

        self.bigram_smoothing_parameter = bigram_smoothing_parameter
        self.bigram_lambda = bigram_lambda
        self.unigram_smoothing_parameter = unigram_smoothing_parameter
        self.question_prior = pos_prior


        #Monogram Variables
        positiveDictionary = {}
        posUniqueCount = 0
        posTotalCount = 0
        
        negUniqueCount = 0
        negTotalCount = 0
        negativeDictionary = {}
        
        #Bigram Variables
        BigramPositiveDictionary = {}
        bigramPosUniqueCount = 0
        bigramPosTotalCount = 0
        
        bigramNegUniqueCount = 0
        bigramNegTotalCount = 0
        BigramNegativeDictionary = {}
        
        #Creating the monogram BoW


        for i in range(len(train_set)):
            if train_labels[i] == 1:
                for j in nltk.sent_tokenize(train_set[i]):
                    if j in self.stopWords:
                        continue
                    if j in positiveDictionary:
                        positiveDictionary[j] = positiveDictionary[j] + 1
                    else:
                        positiveDictionary[j] = 1
                        posUniqueCount += 1
                    posTotalCount += 1
                    #totalCount += 1

            if train_labels[i] == 0:
                for j in nltk.sent_tokenize(train_set[i]):
                    if j in self.stopWords:
                        continue
                    if j in  negativeDictionary:
                        negativeDictionary[j] = negativeDictionary[j] + 1
                    else:
                        negativeDictionary[j] = 1
                        negUniqueCount += 1
                    negTotalCount += 1


        #Creating the bigram BoW
        for i in range(len(train_set)):
            for j in range(len(nltk.sent_tokenize(train_set[i])) - 1):
                bigram_label = (nltk.sent_tokenize(train_set[i])[j], nltk.sent_tokenize(train_set[i])[j + 1])
                if bigram_label[0] in self.stopWords and bigram_label[1] in self.stopWords:
                    continue
                if(train_labels[i] == 1):
                    bigramPosTotalCount += 1
                    if bigram_label in BigramPositiveDictionary:
                        BigramPositiveDictionary[bigram_label] += 1
                    else:
                        bigramPosUniqueCount += 1
                        BigramPositiveDictionary[bigram_label] = 1
                if(train_labels[i] == 0):
                    bigramNegTotalCount += 1
                    if bigram_label in BigramNegativeDictionary:
                        BigramNegativeDictionary[bigram_label] += 1
                    else:
                        bigramNegUniqueCount += 1
                        BigramNegativeDictionary[bigram_label] = 1
        
        self.bigram_answer_dictionary = BigramNegativeDictionary
        self.bigram_question_dictionary = BigramPositiveDictionary
        self.unigram_question_dictionary = positiveDictionary
        self.unigram_answer_dictionary = negativeDictionary

        self.uni_answerTotal = negTotalCount
        self.uni_answerUnique = negUniqueCount
        self.uni_questionUnique = posUniqueCount
        self.uni_questionTotal = posTotalCount

        self.bi_answer_total = bigramNegTotalCount
        self.bi_answerUnique = bigramNegUniqueCount
        self.bi_questionTotal = bigramPosTotalCount
        self.bi_questionUnique = bigramPosUniqueCount
        return



    def findAccuracy(self, dev_set, dev_labels):
        """
        Determines the accuracy of the model given its training

        dev_set: the set that a prediction will be made on (1 == question, 0 == statement/answer)

        dev_labels: whether each set is actually a question or a statement (1 == question, 0 == statement/answer)
        """
        predictions = []



        for i in range(len(dev_set)):

            bigram_positive_probability = 0
            bigram_negative_probability = 0
            total_positive_probability = 0
            total_negative_probability = 0
            uni_posMultiSum = 0
            uni_negMultiSum = 0


            for j in range(len(dev_set[i]) - 1):
                dev_bigram = (dev_set[i][j],dev_set[i][j+1])
                if dev_bigram[0] in self.stopWords and dev_bigram[1] in self.stopWords:
                    continue
                #bigram probabilities
                if dev_bigram in self.bigram_question_dictionary:
                    bigram_positive_probability += math.log((self.bigram_question_dictionary[dev_bigram] + self.bigram_smoothing_parameter) / (self.bi_questionTotal + self.bigram_smoothing_parameter * (self.bi_questionUnique + 1)))
                else:
                    bigram_positive_probability += math.log((self.bigram_smoothing_parameter) / (self.bi_questionTotal + self.bigram_smoothing_parameter * (self.bi_questionTotal + 1)))
                
                if dev_bigram in self.bigram_answer_dictionary:
                    bigram_negative_probability += math.log((self.bigram_answer_dictionary[dev_bigram] + self.bigram_smoothing_parameter) / (self.bi_answer_total + self.bigram_smoothing_parameter * (self.bi_answerUnique + 1)))
                else:
                    bigram_negative_probability += math.log((self.bigram_smoothing_parameter) / (self.bi_answer_total + self.bigram_smoothing_parameter * (self.bi_answerUnique + 1)))
            #mono probabilities
            for j in dev_set[i]:
                if j in self.stopWords:
                    continue
                if j in self.unigram_question_dictionary:
                    uni_posMultiSum +=  math.log((self.unigram_question_dictionary[j] + self.unigram_smoothing_parameter) / (self.uni_questionTotal + self.unigram_smoothing_parameter * (self.uni_questionUnique + 1)))  #conditional probability of P(W|positive)
                    #print(posMultiSum)
                else:  
                    uni_posMultiSum += math.log((self.unigram_smoothing_parameter) / (self.uni_questionTotal + self.unigram_smoothing_parameter * (self.uni_questionUnique + 1)))
                if j in self.unigram_answer_dictionary:
                    uni_negMultiSum +=  math.log((self.unigram_answer_dictionary[j] + self.unigram_smoothing_parameter) / (self.uni_answerTotal + self.unigram_smoothing_parameter * (self.uni_answerUnique + 1))) #conditional probability of P(W|negative)
                    #print(negMultiSum)
                else:
                    uni_negMultiSum += math.log((self.unigram_smoothing_parameter) / (self.uni_answerTotal + self.unigram_smoothing_parameter * (self.uni_answerUnique + 1)))
            
            # Insert check for final word in dictionary

            total_positive_probability = (1 - self.bigram_lambda) * (math.log(self.question_prior) + uni_posMultiSum) + (self.bigram_lambda) * (math.log(self.question_prior) + bigram_positive_probability)
            total_negative_probability = (1 - self.bigram_lambda) * (math.log(1 - self.question_prior) + uni_negMultiSum) + (self.bigram_lambda) * (math.log(1-self.question_prior) + bigram_negative_probability)
            
            if total_positive_probability > total_negative_probability:
                predictions.append(1)
            else:
                predictions.append(0)

        accuracy = 0.0
        for i in range(len(predictions)):
            if predictions[i] == dev_labels[i]:
                accuracy += 1

        return accuracy / len(dev_labels)  

    def isQuestion(self, input):
        """
        input - the user input to be analyzed given our class model
        """


        bigram_positive_probability = 0
        bigram_negative_probability = 0
        total_positive_probability = 0
        total_negative_probability = 0
        uni_posMultiSum = 0
        uni_negMultiSum = 0


        for j in range(len(input) - 1):
            dev_bigram = (input[j],input[j+1])
            if dev_bigram[0] in self.stopWords and dev_bigram[1] in self.stopWords:
                continue
            #bigram probabilities
            if dev_bigram in self.bigram_question_dictionary:
                bigram_positive_probability += math.log((self.bigram_question_dictionary[dev_bigram] + self.bigram_smoothing_parameter) / (self.bi_questionTotal + self.bigram_smoothing_parameter * (self.bi_questionUnique + 1)))
            else:
                bigram_positive_probability += math.log((self.bigram_smoothing_parameter) / (self.bi_questionTotal + self.bigram_smoothing_parameter * (self.bi_questionTotal + 1)))
            
            if dev_bigram in self.bigram_answer_dictionary:
                bigram_negative_probability += math.log((self.bigram_answer_dictionary[dev_bigram] + self.bigram_smoothing_parameter) / (self.bi_answer_total + self.bigram_smoothing_parameter * (self.bi_answerUnique + 1)))
            else:
                bigram_negative_probability += math.log((self.bigram_smoothing_parameter) / (self.bi_answer_total + self.bigram_smoothing_parameter * (self.bi_answerUnique + 1)))
        #mono probabilities
        for j in input:
            if j in self.stopWords:
                continue
            if j in self.unigram_question_dictionary:
                uni_posMultiSum +=  math.log((self.unigram_question_dictionary[j] + self.unigram_smoothing_parameter) / (self.uni_questionTotal + self.unigram_smoothing_parameter * (self.uni_questionUnique + 1)))  #conditional probability of P(W|positive)
                #print(posMultiSum)
            else:  
                uni_posMultiSum += math.log((self.unigram_smoothing_parameter) / (self.uni_questionTotal + self.unigram_smoothing_parameter * (self.uni_questionUnique + 1)))
            if j in self.unigram_answer_dictionary:
                uni_negMultiSum +=  math.log((self.unigram_answer_dictionary[j] + self.unigram_smoothing_parameter) / (self.uni_answerTotal + self.unigram_smoothing_parameter * (self.uni_answerUnique + 1))) #conditional probability of P(W|negative)
                #print(negMultiSum)
            else:
                uni_negMultiSum += math.log((self.unigram_smoothing_parameter) / (self.uni_answerTotal + self.unigram_smoothing_parameter * (self.uni_answerUnique + 1)))
        
        # Insert check for final word in dictionary

        total_positive_probability = (1 - self.bigram_lambda) * (math.log(self.question_prior) + uni_posMultiSum) + (self.bigram_lambda) * (math.log(self.question_prior) + bigram_positive_probability)
        total_negative_probability = (1 - self.bigram_lambda) * (math.log(1 - self.question_prior) + uni_negMultiSum) + (self.bigram_lambda) * (math.log(1-self.question_prior) + bigram_negative_probability)
        
        if total_positive_probability > total_negative_probability:
            return 1
        return 0