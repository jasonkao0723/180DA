import os 
import math
import numpy as np
import random
from matplotlib import pyplot as plt
from avg_filter import word_percent
from avg_filter import sum_differ
from timeit import default_timer as timer
start = timer()


# set up four groups 
sound_armor = [ "armor","baur","boar","bohr","bore",
                "chore","clore","coar","core","corps",
                "doerr","dohr","door","dore","dorr","drawer",
                "faure","floor","flore","for","fore","four","glor","glore",
                "goar","gore","gorr","hoar","hoare","hoerr","horr","knorr",
                "kohr","laur","laure","loar","loehr","lohr","lore","moar",
                "mohr","moore","more","morr","nohr","nor","oar","ohr","ore",
                "orr","paw","poor","pore","porr","pour","raw","roar","roehr",
                "rohr","saur","schnorr","schor","schorr","score","shore","shorr",
                "smore","snore","soar","sore","sour","spaur","spore","stoehr","stohr",
                "store","storr","straw","sure","swore","thor","tore","torr","torre","tour",
                "vore","war","warr","woehr","wore","yore","your",
                "coleslaw","contour","decor","delore","deplore","devor",
               "dior","elnore","explore","farmer","gabor","galore","igor","implore","inscore",
               "inshore","jambor","labore","lahore","lalor","lamaur","lazor",
               "lenore","livor","longcor","mazor","melor","minotaur","ngor",
               "noncore","offshore","outpour","outscore","postwar","prewar",
               "rapport","restore","roquemore","rumore","sedor","senor","therefore",
               "timor","tremor"]

# set up three groups 
sound_explode = ["explode","blowed","bode","brode","chode","coad","code","coed",
                 "crowed","flowed","gloede","glowed","goad","goedde",
                 "goede","grode","knode","knowed","load","lode","moad",
                 "mode","moede","mowed","node","ode","owed","showed",
                 "shrode","slowed","snowed","stowed","strode","thode",
                 "toad","toed","towed","abode","bestowed","bestrode",
                 "busload","commode","corrode","decode","encode","erode",
                 "forebode","implode","kanode","methode","outmode","plateaued",
                 "reload","swallowed","unload","episode","overflowed","overload"]

# set up two groups 
sound_antibiotic = ["antibiotic","biotic","chaotic","despotic","erotic",
                    "exotic","hypnotic","narcotic","neurotic",
                    "niotic","otik","psychotic","quixotic","robotic",
                    "abiotic","astronautic","idiotic","nuerotoxic",
                    "patriotic","semiotic","symbiotic","unpatriotic"]

# set up three groups 
sound_surrender = [ "surrender","bender", "blender", "brender", "brendor", "ender", 
                    "fender", "gender", "kender", "lender", "mender",
                    "pender", "render", "schlender", "sender", "skender",
                    "slender", "spender","splendor","stender","tender",
                    "vendor", "wender", "yender", "zehnder", "zender",
                    "allender","amender","attender","callender","cavender",
                    "challender", "challenger","contender", "defender",
                    "deffender", "engender","offender","pretender","suspender",
                    "transgender"]


def representative_list_initializer (num_group,w_list):
    # This function set the number of groups and 
    # choose random words as representatives first 
    array = []
    for i in range(num_group):
        array.append(word_percent(random.choice(w_list)))
    return array

def map_generator (num_group,w_list,pivot_array):
    map = np.zeros((len(w_list),num_group))
    row = 0
    for word in w_list:
        array = [0]*num_group 
        index = 0
        for pivot in pivot_array:
            array[index] = sum_differ(word_percent(word),pivot_array[index])
            index = index + 1  
        col = array.index(min(array))
        map[row,col] = 1
        row = row + 1
    return map

def distributor(num_group,w_list,map):
    all_word = [[] for x in range (num_group)]
    index = 0
    for row in map:
        col = 0
        for i in row: 
            if i == 1:
                break
            col = col + 1  
        all_word[col].append(w_list[index])
        index = index + 1

    for i in all_word:
        if i == []:
           i == i.append(random.choice(w_list))

    return all_word

def word_average (w_list):
    accum = [0]*26
    for word in w_list:
        accum = [sum(x) for x in zip(word_percent(accum), word_percent(word))]
    new = [x/len(w_list) for x in accum]
    return new 

def array_average(p_list):
    accum = [0]*26
    for word in p_list:
        accum = [sum(x) for x in zip(accum, word)]
    new = [x/len(p_list) for x in accum]
    return new 


def representative_list_generator(num_group, sorted_list):
    representative = []
    for i in range (num_group):  
        new = word_average(sorted_list[i])
        representative.append(new)
    return representative


def flash(num_group,rounds,w_list):
    pivot = representative_list_initializer (num_group,w_list)
    for i in range (rounds):
        map = map_generator(num_group,w_list,pivot)
        list_ = distributor(num_group,w_list,map)
        pivot = representative_list_generator(num_group,list_)
    pivot = array_average(pivot)
    return pivot


# print(armor_repre)
# print(explode_repre)
# print(antibiotic_repre)
# print(surrender_repre)

def kmean_differ_matrix (word,armor_repre,explode_repre,antibiotic_repre,surrender_repre):
    # return a matrix contain the different among input word and 4 other voice command
    difference = [0]*4
    input = word_percent(word)
    difference[0] = sum_differ(input,armor_repre)
    difference[1] = sum_differ(input,explode_repre)
    difference[2] = sum_differ(input,antibiotic_repre)
    difference[3] = sum_differ(input,surrender_repre)
    return difference

def Kmean_filtered_word (word,armor_repre,explode_repre,antibiotic_repre,surrender_repre):
    l = kmean_differ_matrix(word,armor_repre,explode_repre,antibiotic_repre,surrender_repre)
    minimum_index = l.index(min(l))
    if minimum_index == 0:
        return "armor"
    if minimum_index == 1:
        return "explode"
    if minimum_index == 2:
        return "antibiotic"
    if minimum_index == 3:
        return "surrender"

################################ part used for main.py ###########################################

armor_repre = flash(4,10,sound_armor)
explode_repre = flash(2,10,sound_explode)
antibiotic_repre = flash(2,10,sound_antibiotic)
surrender_repre = flash(2,10,sound_surrender)

# print(armor_repre)
# print(explode_repre)
#print(antibiotic_repre)
print(surrender_repre)

def kmean_differ_matrix_use (word):
    # return a matrix contain the different among input word and 4 other voice command
    difference = [0]*4
    input = word_percent(word)
    difference[0] = sum_differ(input,armor_repre)
    difference[1] = sum_differ(input,explode_repre)
    difference[2] = sum_differ(input,antibiotic_repre)
    difference[3] = sum_differ(input,surrender_repre)
    return difference

def Kmean_filtered_word_use (word):
    l = kmean_differ_matrix_use(word)
    minimum_index = l.index(min(l))
    if minimum_index == 0:
        return "armor"
    if minimum_index == 1:
        return "explode"
    if minimum_index == 2:
        return "antibiotic"
    if minimum_index == 3:
        return "surrender"

#####################################################################################################

def Kmean_test_group_correctness(word,w_list,armor_repre,explode_repre,antibiotic_repre,surrender_repre):
    # For each group of ambigious list, calculate the percentage of 
    # correct filtering
    matrix = [0]*len(w_list)
    index = 0
    for i in w_list:
        if Kmean_filtered_word(i,armor_repre,explode_repre,antibiotic_repre,surrender_repre) == word:
            matrix[index] = 1
        index = index + 1
    score = matrix.count(1)/len(w_list)
    return matrix,score

end = timer()
print("---k-mean clustering filter processing time: ",end - start)

def superimposed_graph(rounds):
    correctness = [0]*4
    accum = [0]*4
    for i in range(rounds):

        armor_repre = flash(4,10,sound_armor)
        explode_repre = flash(2,10,sound_explode)
        antibiotic_repre = flash(2,10,sound_antibiotic)
        surrender_repre = flash(2,10,sound_surrender)

        correctness[0] = Kmean_test_group_correctness("armor",sound_armor,armor_repre,explode_repre,antibiotic_repre,surrender_repre)[1]
        correctness[1] = Kmean_test_group_correctness("explode",sound_explode,armor_repre,explode_repre,antibiotic_repre,surrender_repre)[1]
        correctness[2] = Kmean_test_group_correctness("antibiotic",sound_antibiotic,armor_repre,explode_repre,antibiotic_repre,surrender_repre)[1]
        correctness[3] = Kmean_test_group_correctness("surrender",sound_surrender,armor_repre,explode_repre,antibiotic_repre,surrender_repre)[1]
        
        
        accum = [sum(x) for x in zip(accum, correctness)]
        

        plt.plot(correctness)
        plt.xlabel("voice command")
        plt.ylabel("Possibility")
        plt.title("k-mean possiblity of contributing to right command- 100 rounds")
    plt.show()
    
    accum = [x/rounds for x in accum]
    val = 0
    for j in range(len(correctness)):
        val = val + accum[j]
    val = val/4
    print(val)


#superimposed_graph(100)
