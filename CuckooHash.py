import pytest
import math
import random
import string
from BitHash import BitHash, ResetBitHash

#"I hereby certify that this program is solely the result of my own work and is
#in compliance with the Academic Integrity policy of the course syllabus and 
#the academic integrity policy of the CS department.”

class Link(object):
    
    # init function
    def __init__(self, k, d):
        self.key = k
        self.data = d
        
    # str function
    def __str__(self):
        return self.key
    
class CuckooHash(object):
    
    # init function
    def __init__(self, size):
        # in the case of an odd sized array, which would create a float
        # i decided to round up instead of round down, just as a personal
        # choice
        self.__hashArray1 = [None] * math.ceil(size/2)
        self.__hashArray2 = [None] * math.ceil(size/2)
        self.__numKeys = 0                  # keeps track of how full the table is
        self.__sizeHash = len(self.__hashArray1) * 2 # correct size of both tables
        
        
    # return current number of keys in table    
    def __len__(self): return self.__numKeys
    
    
    # print both tables
    def print(self):
        for i in range(len(self.__hashArray1)):
            print(str(self.__hashArray1[i]) + "\t" + str(self.__hashArray2[i]))
    
    # grow hash function
    def __growHash(self):
        
        # double original size of hash table
        new = self.__sizeHash * 2
        
        # get new bit hash function
        ResetBitHash()
        
        # create new cuckoo hash with double size of old
        temp = CuckooHash(new)
        
        # loop through size of one table
        for i in range(self.__sizeHash//2):
            
            # if location is not none, then insert into proper place
            if self.__hashArray1[i]:
                temp.insert(self.__hashArray1[i].key, self.__hashArray1[i].data)
                
            # do same for second hash table
            if self.__hashArray2[i]:
                temp.insert(self.__hashArray2[i].key, self.__hashArray2[i].data)
         
        # set all main functions to temp functions       
        self.__hashArray1 = temp.__hashArray1
        self.__hashArray2 = temp.__hashArray2
        self.__numKeys = temp.__numKeys
        self.__sizeHash = temp.__sizeHash
        
    
    # hashes key and returns two hash functions    
    def hashFunction(self, k):
        
        # hash twice
        one = BitHash(k)
        two = BitHash(k, one)
        
        # mod each hash by length of table
        oneHash = one % len(self.__hashArray1)
        twoHash = two % len(self.__hashArray1)
        
        # return tuple with hashed key
        return oneHash, twoHash
    
    # inserts key/data pair into hash table
    # does not accept repeats of doubles
    # if tables are 60% full or more or insertion has been through 61 cycles
    # without sucess, then the table doubles
    def insert(self, k, d):
        
        #check for doubles
        if self.find(k): return True
        
        # create new link with key and data
        l = Link(k, d)        
        
        # keep track of how many cycles have happened without insertion
        cycles = 0
        
        
        # loop until key/data has been inserted
        while True: 
            
            # if cycles has reached its max or table is at 60% capacity or more
            # then grow hash table
            # the number 61 was chosen since the visulization that was posted
            # on cuckoo hash used 16 cycles and you suggested around 50
            # so since i had been testing with 16 this whole time i decided to
            # swap the numbers and use 61
            if cycles >= 61 or self.__numKeys / self.__sizeHash >= .6:
                self.__growHash()
            
            # get hashed key from current link    
            oneHash, twoHash = self.hashFunction(l.key)
            
            # checks first hash table in oneHash position, if it's empty then
            # we place it there and insertion has succeeded
            # we return True and add one to numKeys
            if self.__hashArray1[oneHash] == None:
                self.__hashArray1[oneHash] = l
                self.__numKeys += 1
                return True
            
            # if oneHash in table 1 was was not empty, then we swap the link being
            # inserted with the link currently in that position and hash the
            # new link
            l, self.__hashArray1[oneHash] = self.__hashArray1[oneHash], l
            oneHash, twoHash = self.hashFunction(l.key)
            
            # if the twoHash position in table two is empty then
            # we place it there and insertion has succeeded
            # we return True and add one to numKeys
            if self.__hashArray2[twoHash] == None:
                self.__hashArray2[twoHash] = l
                self.__numKeys += 1
                return True
            
            # if twoHash in table 2 was not empty, then we swap the link being
            # inserted with the link currently in that position and hash the
            # new link 
            l, self.__hashArray2[twoHash] = self.__hashArray2[twoHash], l
            oneHash, twoHash = self.hashFunction(l.key)
            
            # if we have reached this point then we have completed a full cycle 
            # without a successful insertion. if this happens 61 times then
            # we grow hash
            cycles += 1
                              
    
    # looks at both places where the key can be. since it can only be in two
    # places, if its not found in either spot then it's not in the table
    # return True if found and False if not
    def find(self, k):
        
        # if both arrays are empty then return false right away
        if self.__numKeys == 0:
            return False
        
        # hash the key
        oneHash, twoHash = self.hashFunction(k)
        
        # check if key is in either table and then return True
        if self.__hashArray1[oneHash] != None and self.__hashArray1[oneHash].key == k or \
           self.__hashArray2[twoHash] != None and self.__hashArray2[twoHash].key == k:
            return True
        
        # if not return False
        return False
    
    
    # similar to find. key can only be in one of two place so once it's found
    # it just gets set to none and return True
    # if key is not found then we return False
    def delete(self, k):
        # hash the key
        oneHash, twoHash = self.hashFunction(k)
        
        # check if key is in the first array
        if self.__hashArray1[oneHash] and self.__hashArray1[oneHash].key == k:
            # if so, set it to None, subract from numKeys and return
            self.__hashArray1[oneHash] = None
            self.__numKeys -= 1
            return True
        
        # if not in the first array, check second    
        elif self.__hashArray2[twoHash] and self.__hashArray2[twoHash].key == k:
            # if so, set it to None, subtract from numKeys and return
            self.__hashArray2[twoHash] = None
            self.__numKeys -= 1
            return True
        
        # if we got here, the key was not in either table    
        return None
