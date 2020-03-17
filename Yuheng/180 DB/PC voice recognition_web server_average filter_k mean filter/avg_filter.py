import os 
import math
import numpy as np
import networkx as nx
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from timeit import default_timer as timer
start = timer()


alphabet_list = ["a","b","c","d","e","f","g","h",
                "i","j","k","l","m","n","o","p",
                "q","r","s","t","u","v","w","x","y","z"]

def alphabet_counter (alphabet, word):
    # count how many times an alphabet appears in a word
    counter = 0
    for x in word:
        if x == alphabet:
            counter = counter + 1; 
    return counter

def word_percent (word):
    # convert a word to 26 slots percent matrix 
    word_length = len(word)
    percent_matrix = [0]*26
    index = 0
    for i in alphabet_list:
        num = alphabet_counter(i,word)
        percent_matrix[index] = num/word_length
        index = index + 1
    return percent_matrix

# calculate the alphabet percent for each voice command
armor_matrix = word_percent("armor")
explode_matrix = word_percent("explode")
antibiotic_matrix = word_percent("antibiotic")
surrender_matrix = word_percent("surrender")

def sum_differ(matrix_a,matrix_b):
    # sum up the absolute value of difference of each element in two matrix 
    sum = 0
    for i in range (26):
        sum = sum + abs(matrix_a[i]-matrix_b[i])
    return sum

def differ_matrix (word):
    # return a matrix contain the different among input word and 4 other voice command
    difference = [0]*4
    input = word_percent(word)
    difference[0] = sum_differ(input,armor_matrix)
    difference[1] = sum_differ(input,explode_matrix)
    difference[2] = sum_differ(input,antibiotic_matrix)
    difference[3] = sum_differ(input,surrender_matrix)
    return difference

def filtered_word (word):
    l = differ_matrix(word)
    minimum_index = l.index(min(l))
    if minimum_index == 0:
        return "armor"
    if minimum_index == 1:
        return "explode"
    if minimum_index == 2:
        return "antibiotic"
    if minimum_index == 3:
        return "surrender"


sound_armor = [ "baur","boar","bohr","bore",
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

sound_explode = ["blowed","bode","brode","chode","coad","code","coed",
                 "crowed","flowed","gloede","glowed","goad","goedde",
                 "goede","grode","knode","knowed","load","lode","moad",
                 "mode","moede","mowed","node","ode","owed","showed",
                 "shrode","slowed","snowed","stowed","strode","thode",
                 "toad","toed","towed","abode","bestowed","bestrode",
                 "busload","commode","corrode","decode","encode","erode",
                 "forebode","implode","kanode","methode","outmode","plateaued",
                 "reload","swallowed","unload","episode","overflowed","overload"]

sound_antibiotic = ["biotic","chaotic","despotic","erotic",
                    "exotic","hypnotic","narcotic","neurotic",
                    "niotic","otik","psychotic","quixotic","robotic",
                    "abiotic","astronautic","idiotic","nuerotoxic",
                    "patriotic","semiotic","symbiotic","unpatriotic"]

sound_surrender = ["bender", "blender", "brender", "brendor", "ender", 
                    "fender", "gender", "kender", "lender", "mender",
                    "pender", "render", "schlender", "sender", "skender",
                    "slender", "spender","splendor","stender","tender",
                    "vendor", "wender", "yender", "zehnder", "zender",
                    "allender","amender","attender","callender","cavender",
                    "challender", "challenger","contender", "defender",
                    "deffender", "engender","offender","pretender","suspender",
                    "transgender"]


def test_group_correctness(word,w_list):
    # For each group of ambigious list, calculate the percentage of 
    # correct filtering
    matrix = [0]*len(w_list)
    index = 0
    for i in w_list:
        if filtered_word(i) == word:
            matrix[index] = 1
        index = index + 1
    print(matrix.count(1)/len(w_list))
    return matrix

end = timer()
print("---average filter processing time: ",end - start)

# print(test_group_correctness("armor",sound_armor))  
# print(test_group_correctness("explode",sound_explode))  
# print(test_group_correctness("antibiotic",sound_antibiotic))
# print(test_group_correctness("surrender",sound_surrender))

# correctness = [0.6,0.8070175438596491,0.9523809523809523,0.975]
# print(sum(correctness)/len(correctness))
# plt.plot(correctness)
# plt.xlabel("Word")
# plt.ylabel("Possibility")
# plt.title("Possiblity of contributing to right command")
# plt.show()

# print(word_percent("blowed"))
# print(differ_matrix("blowed"))


# sound = sound_armor + sound_explode + sound_antibiotic + sound_surrender

# print(len(sound))

# def filtered_word_matrix():
#     # This function would generate a matrix whose
#     # row is all the possible ambigious words in total
#     # column is 4 voice command: armor 0, explode 1, 
#     # antibiotic 2, surrender 3
#     sound_match = np.zeros((len(sound),4))
#     row = 0

#     for i in sound:
#         if filtered_word(i) == "armor":
#             sound_match[row,0] = 1
#         if filtered_word(i) == "explode":
#             sound_match[row,1] = 1
#         if filtered_word(i) == "antibiotic":
#             sound_match[row,2] = 1
#         if filtered_word(i) == "surrender":
#             sound_match[row,3] = 1   
#         row = row + 1
#     return sound_match
    


