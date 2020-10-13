import numpy as np
import math
from collections import OrderedDict


stopWords = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]
def statement_or_question(train_set, train_labels, dev_set, smoothing_parameter=1.0, pos_prior=1.0):
    """
    train_set - List of list of words corresponding with each movie review
    example: suppose I had two reviews 'like this movie' and 'i fall asleep' in my training set
    Then train_set := [['like','this','movie'], ['i','fall','asleep']]

    train_labels - List of labels corresponding with train_set
    example: Suppose I had two reviews, first one was positive and second one was negative.
    Then train_labels := [1, 0]

    dev_set - List of list of words corresponding with each review that we are testing on
              It follows the same format as train_set

    smoothing_parameter - The smoothing parameter --laplace (1.0 by default)
    pos_prior - The prior probability that a word is positive. You do not need to change this value.

    positive(1) represents that the input is a question, negative(0) represents that the input is a statement
    """
    
    # TODO: Write your code here

    # Creating the bag of words for both the positive and negative cases
    positiveDictionary = {}
    posUniqueCount = 0
    posTotalCount = 0
    
    negUniqueCount = 0
    negTotalCount = 0
    negativeDictionary = {}
    #totalCount = 0


    for i in range(len(train_set)):
        if train_labels[i] == 1:
            for j in train_set[i]:
                if j in stopWords:
                    continue
                if j in positiveDictionary:
                    positiveDictionary[j] = positiveDictionary[j] + 1
                else:
                    positiveDictionary[j] = 1
                    posUniqueCount += 1
                posTotalCount += 1
                #totalCount += 1

        if train_labels[i] == 0:
            for j in train_set[i]:
                if j in stopWords:
                    continue
                if j in  negativeDictionary:
                    negativeDictionary[j] = negativeDictionary[j] + 1
                else:
                    negativeDictionary[j] = 1
                    negUniqueCount += 1
                negTotalCount += 1
                #totalCount += 1


    return []
    """
    #Creating set of predictions on dev_set
    predictions = []
    for i in range(len(dev_set)):
        #print(dev_set[i])
        posMultiSum = 0.0
        negMultiSum = 0.0
        for j in dev_set[i]:
            if j in stopWords:
                continue
            if j in positiveDictionary:
                posMultiSum +=  math.log((positiveDictionary[j] + smoothing_parameter) / (posTotalCount + smoothing_parameter * (posUniqueCount + 1)))  #conditional probability of P(W|positive)
                #print(posMultiSum)
            else:  
                posMultiSum += math.log((smoothing_parameter) / (posTotalCount + smoothing_parameter * (posUniqueCount + 1)))
            if j in negativeDictionary:
                negMultiSum +=  math.log((negativeDictionary[j] + smoothing_parameter) / (negTotalCount + smoothing_parameter * (negUniqueCount + 1))) #conditional probability of P(W|negative)
                #print(negMultiSum)
            else:
                negMultiSum += math.log((smoothing_parameter) / (negTotalCount + smoothing_parameter * (negUniqueCount + 1)))
        positiveProb = math.log(pos_prior) + posMultiSum
        negativeProb = math.log(1 - pos_prior) + negMultiSum


        if positiveProb > negativeProb:
            predictions.append(1)
        else:
            predictions.append(0)        

    # return predicted labels of development set
    return predictions
    """

def bigramBayes(train_set, train_labels, dev_set, unigram_smoothing_parameter=.4, bigram_smoothing_parameter=.009, bigram_lambda=.5,pos_prior=0.8):
    """
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
    
    positive(1) represents that the input is a statement, negative(0) represents that the input is a question
    """
    # TODO: Write your code here
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
            for j in train_set[i]:
                if j in stopWords:
                    continue
                if j in positiveDictionary:
                    positiveDictionary[j] = positiveDictionary[j] + 1
                else:
                    positiveDictionary[j] = 1
                    posUniqueCount += 1
                posTotalCount += 1
                #totalCount += 1

        if train_labels[i] == 0:
            for j in train_set[i]:
                if j in stopWords:
                    continue
                if j in  negativeDictionary:
                    negativeDictionary[j] = negativeDictionary[j] + 1
                else:
                    negativeDictionary[j] = 1
                    negUniqueCount += 1
                negTotalCount += 1


    #Creating the bigram BoW
    for i in range(len(train_set)):
        for j in range(len(train_set[i]) - 1):
            bigram_label = (train_set[i][j],train_set[i][j + 1])
            if bigram_label[0] in stopWords and bigram_label[1] in stopWords:
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
    

    #Creating predictions
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
            if dev_bigram[0] in stopWords and dev_bigram[1] in stopWords:
                continue
            #bigram probabilities
            if dev_bigram in BigramPositiveDictionary:
                bigram_positive_probability += math.log((BigramPositiveDictionary[dev_bigram] + bigram_smoothing_parameter) / (bigramPosTotalCount + bigram_smoothing_parameter * (bigramPosUniqueCount + 1)))
            else:
                bigram_positive_probability += math.log((bigram_smoothing_parameter) / (bigramPosTotalCount + bigram_smoothing_parameter * (bigramPosTotalCount + 1)))
            
            if dev_bigram in BigramNegativeDictionary:
                bigram_negative_probability += math.log((BigramNegativeDictionary[dev_bigram] + bigram_smoothing_parameter) / (bigramNegTotalCount + bigram_smoothing_parameter * (bigramNegUniqueCount + 1)))
            else:
                bigram_negative_probability += math.log((bigram_smoothing_parameter) / (bigramNegTotalCount + bigram_smoothing_parameter * (bigramNegUniqueCount + 1)))
        #mono probabilities
        for j in dev_set[i]:
            if j in stopWords:
                continue
            if j in positiveDictionary:
                uni_posMultiSum +=  math.log((positiveDictionary[j] + unigram_smoothing_parameter) / (posTotalCount + unigram_smoothing_parameter * (posUniqueCount + 1)))  #conditional probability of P(W|positive)
                #print(posMultiSum)
            else:  
                uni_posMultiSum += math.log((unigram_smoothing_parameter) / (posTotalCount + unigram_smoothing_parameter * (posUniqueCount + 1)))
            if j in negativeDictionary:
                uni_negMultiSum +=  math.log((negativeDictionary[j] + unigram_smoothing_parameter) / (negTotalCount + unigram_smoothing_parameter * (negUniqueCount + 1))) #conditional probability of P(W|negative)
                #print(negMultiSum)
            else:
                uni_negMultiSum += math.log((unigram_smoothing_parameter) / (negTotalCount + unigram_smoothing_parameter * (negUniqueCount + 1)))
        
        # Insert check for final word in dictionary

        total_positive_probability = (1 - bigram_lambda) * (math.log(pos_prior) + uni_posMultiSum) + (bigram_lambda) * (math.log(pos_prior) + bigram_positive_probability)
        total_negative_probability = (1 - bigram_lambda) * (math.log(1 - pos_prior) + uni_negMultiSum) + (bigram_lambda) * (math.log(1-pos_prior) + bigram_negative_probability)
        
        if total_positive_probability > total_negative_probability:
            predictions.append(1)
        else:
            predictions.append(0)
    return predictions