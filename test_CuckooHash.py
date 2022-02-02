from CuckooHash import *

# tests insert functiom
def test_insert():
   
    # create cuckoo hash of 100 initially
    c = CuckooHash(100)
    
    numkeys = 0
    
    # adds 400 words of randomly chosen letters
    for i in range(400):
        c.insert(''.join(random.choice(string.ascii_letters) for j in range(random.randint(3,12))), i)
        numkeys +=1 
        
    # check to make sure number of keys inserted is correct
    assert numkeys == 400
    
    # checks again but this time with a larger set of numbers
    h = CuckooHash(5000)
    
    numkeys = 0
    for i in range(6500):
        h.insert(''.join(random.choice(string.ascii_letters) for j in range(random.randint(3,12))), i)
        numkeys +=1 
    assert numkeys == 6500    
    
# tests the delete function        
def test_delete():
    
    # create cuckoo hash of 100 initially
    c = CuckooHash(100)
    
    # create a set to store words added
    a = set()
    missing = 0
    numkeys = 0
    
    # adds 400 words of randomly chosen letters to the set
    for i in range(400):
        a.add(''.join(random.choice(string.ascii_letters) for j in range(random.randint(3,12))))
        
    
    # loop through set and add all the words to cuckoo hash 
    for i in a:
        c.insert(i, 1)
        numkeys += 1 
    
    # loop through set again and delete all the words in the cuckoo hash    
    for i in a:
        c.delete(i)
        numkeys -= 1
    
    # make sure that all keys were deleted    
    assert numkeys == 0
    
    
    # checks again but this time with a larger set of numbers
    h = CuckooHash(1000)
    b = set()
    missing = 0
    
    numkeys = 0
    for i in range(8000):
        b.add(''.join(random.choice(string.ascii_letters) for j in range(random.randint(3,12))))
        
        
    for i in b:
        h.insert(i, 1)
        numkeys += 1 
        
    for i in b:
        h.delete(i)
        numkeys -= 1
        
    assert numkeys == 0    
    
# tests the find function
def test_find():
    
    # create cuckoo hash of 10 initially
    c = CuckooHash(10)
    
    # create a set to store words added
    a = set()
    missing = 0
    numkeys = 0
    
   # adds 400 words of randomly chosen letters to the set
    for i in range(400):
        a.add(''.join(random.choice(string.ascii_letters) for j in range(random.randint(3,12))))
        numkeys += 1 
    
    # loops through set and searches for all words    
    for i in a:
        c. insert(i, 1)
        c.find(i)
        if c.find(i) == False:
            missing += 1
    
    # checks to make sure no words are missing    
    assert missing == 0
    
    
    # checks again but this time with a larger set of numbers 
    h = CuckooHash(1000)
    b = set()
    missing = 0
    
    numkeys = 0
    for i in range(60000):
        a.add(''.join(random.choice(string.ascii_letters) for j in range(random.randint(3,12))))
        numkeys += 1 
        
    for i in b:
        h. insert(i, 1)
        h.find(i)
        if h.find(i) == False:
            missing += 1 
            
    assert missing == 0

# tests a simple cuckoo hash
def test_small():
    
    # # create cuckoo hash of 10 initially
    c = CuckooHash(10)
    size = 0
    
    # insert a bunch of words and increment size
    c.insert("hi", 1)
    size +=1
    c.insert("hello", 2)
    size += 1
    c.insert("hotdogs", 3)
    size += 1
    c.insert("lemonade", 4)
    size += 1
    
    # check to make sure size is correct
    assert len(c) == size
    
    # search for words that were inserted
    assert c.find("lemonade") == True
    assert c.find("hello") == True
    
    # search for words that were not inserted
    assert c.find("blanket") == False
    assert c.find("pie") == False
    
    # delete a word in cuckoo hash
    c.delete("lemonade")
    size -= 1
    
    # try to find recently deleted word
    assert c.find("lemonade") == False
    
    # try to delete word that is not in cuckoo hash
    assert c.delete("dishes") == None
    
    # make sure lenght is correct after deletion
    assert len(c) == size
    
    # insert more words to cause tables to grow
    c.insert("note", 5)
    size += 1
    c.insert("pen", 6)
    size += 1
    c.insert("orange", 7)
    size += 1
    c.insert("green", 8)
    size += 1
    c.insert("water", 9)
    size += 1
    c.insert("salad", 10)
    size += 1
    c.insert("banana", 11)
    size += 1
    c.insert("vase", 12)
    size += 1
    
    # make sure size is still correct
    assert size == len(c)
    
    # search for words again
    assert c.find("salad") == True
    assert c.find("computer") == False
    
    # insert word that was already inserted
    c.insert("vase", 13)
    
    # make sure vase wasn't able to be inserted again
    assert size == len(c)
    
    # delete word
    assert c.delete("banana") == True
    size -= 1
    
    # check size one last time
    assert size == len(c)
    
def test_torture():
    
    # create cuckoo hash of 100 initially 
    h = CuckooHash(100)
    
    # create a set to store words added 
    a = set()
    numkeys = 0
    
    # open document of words
    f = open("wordlist.txt", "r")
    
    # convert the words into a list
    lists = list(f)
    
    # adds 6500 random words from list to set and hash table
    for i in range(6500):
        word = random.choice(lists)
        h.insert(word, 1)
        a.add(word)
    
    # loop through and count how many words were found (doubles might have 
    # occured)
    for word in a:
        if h.find(word):
            numkeys +=1
    
    # check to make sure actual size is same as reported size       
    assert numkeys == len(h)
    
    # loop through and delete every word
    for word in a:
        h.delete(word)
        numkeys -= 1
    
    # make sure that actual size is same as reported size
    assert len(h) == numkeys
    
        
    f.close()    
      

pytest.main(["-v", "-s", "test_CuckooHash.py"])