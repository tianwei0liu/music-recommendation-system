#Tianwei Liu
#November 19, 2015



fileName = 'musicrecplus.txt'
def load(fileName):
    '''read the file in the database'''
    dictionary = {}
    file = open(fileName,'r')
    for line in file:
        [userName, bands] = line.strip().split(":")
        bandList = bands.split(",")
        bandList.sort()
        dictionary[userName] = bandList
    file.close()
    return dictionary


def save(fileName):
    '''save the user preferences to the file'''
    global D
    file = open(fileName,'w')
    users = D.keys()
    s = ''
    for user in users:
        s += user + ':'
        for a in D[user]:
            s += a + ','
        s = s[:-1] + '\n'
    file.write(s)
    file.close()
    

def getPref(userName):
    '''get the user's preference'''
    global D
    if userName in D:
        print("\nI see that you have used the system before.")
        print("Your music preferences include:")
        userPref = D[userName]
        print(userPref)
        m = []
        while(1):
            print('\nEnter "done" when done.')
            a = input('Please enter another artist or band that you like: ')
            a = a.title()
            a = a.strip()
            if a == 'Done':
                break
            m += [a]
        if m != []:
            D[userName] += m
            D[userName].sort()
    else:
        print("\nI see that you are a new user.")
        m = []
        while(1):
            print('\nPlease enter "done" when done')
            a = input('Please enter an artist or band that you like: ')
            a = a.title()
            a = a.strip()
            if a == 'Done':
                break
            m += [a]
        D[userName] = m
        D[userName].sort()


def getRec(userName):
    '''give the user his/her recommendations'''
    global D
    recommendations = []
    bestUser = ''
    for i in findBestUser(userName):
        bestUser = i
        userPref = D[userName]
        for j in drop(userPref,D[bestUser]):
            if j not in recommendations:
                recommendations  += [j]
    if len(recommendations) == 1:
        print('\nWe have found a recommendation for you:')
    else:
        print('\nWe have found',len(recommendations),'recommendations for you:')
    recommendations.sort()
    print(recommendations)
    
def findBestUser(userName):
    '''find a user whose tastes are closest to the current user.'''
    global D
    users = D.keys()
    usersPref = D[userName]
    bestUsers = None
    bestScore = -1
    for user in users:
        score = numMatches(usersPref,D[user])
        if score > bestScore and D[user] != D[userName]:
            bestScore = score
            bestUsers = [user]
        elif score == bestScore and D[user] != D[userName]:
            bestUsers += [user]
    return bestUsers

def numMatches(list1, list2):
    '''return the number of elements that match between two sorted lists'''
    matches = 0
    i = 0
    j = 0
    while i < len(list1) and j < len(list2):
        if list1[i] == list2[j]:
            matches += 1
            i += 1
            j += 1
        elif list1[i] < list2[j]:
            i += 1
        else:
            j += 1
    return matches

def drop(list1,list2):
    '''return a new list that contains only the elements in
    list 2 tha were NOT in list1'''
    list3 = []
    i = 0
    j = 0
    while i < len(list1) and j < len(list2):
        if list1[i] == list2[j]:
            i += 1
            j += 1
        elif list1[i] < list2[j]:
            i += 1
        else:
            list3.append(list2[j])
            j += 1
    return list3



def mostPopArt():
    '''print the most popular artist'''
    if len(findMostPopArt()) == 1:
        print('\nThe most popular artist:')
        print(findMostPopArt()[0])
    else:
        print('\nThe most popular artists:')
        l = ''
        for i in len(findMostPopArt()):
            l += findMostPopArt()[i] + ','
        print(l[:-1])

def popularity():
    '''return a dictionary that contains the information
    of the popularity of each artists and bands.'''
    global D
    dictionary = {}
    users = D.keys()
    for user in users:
        for i in range(len(D[user])):
            if D[user][i] not in dictionary:
                dictionary[D[user][i]] = 1
            else:
                dictionary[D[user][i]] += 1
    return dictionary

def findMostPopArt():
    '''return the most popular artists or bands.'''
    global P
    artists = P.keys()
    bestArt = None
    bestPop = 0
    for artist in artists:
        if P[artist] > bestPop:
            bestArt = [artist]
            bestPop = P[artist]
        elif P[artist] == bestPop:
            bestArt += [artist]
    return bestArt

def howPopArt():
    '''print the popularity of an artist.'''
    global P
    if len(findMostPopArt()) == 1:
        print('\nThe popularity of the most popular artist or band:')
    else:
        print('\nThe popularity of the most popular artists or bands:')
    print(P[findMostPopArt()[0]])


def userMostLikes(userName):
    '''return the users who like the most popular artist(s) and band(s).'''
    global D
    users = D.keys()
    b = []
    c = {}
    if userName[-1] == '$':
        for i in range(len(findMostPopArt())):
            a = findMostPopArt()[i]
            for user in users:
                if a in D[user]:
                    b += [user]
        print('The users who like the most popular artist(s) and band(s):')
        print(b)
    else:
        for j in range(len(findMostPopArt())):
            a = findMostPopArt()[j]
            for user in users:
                if a in D[user]:
                    c[user] = D[user]
        print('The users who like the most popular artist(s) and band(s) and their preferences:')
        print(c)

    
def main():
    ''' The main recommendation function '''
    global D,P,fileName
    print("Welcome to the music recommender system!")
    print('Please enter a "$" sign immediately after your name, if you want to opt out')
    print('the feature of outputing the preferences of the users who like the most popular artists and bands')
    userName = input('Please enter your name: ')
    userName = userName.strip()
    userName = userName.title()
    if userName[-1] == '$':
        print('Welcome',userName[:-1],'!')
    else:
        print('Welcome',userName,'!')
    D = load(fileName)
    P = popularity()
    letter = ''
    if userName not in D:
        getPref(userName)
    while 1:
        print('\ne - enter preferences')
        print('r - get recommendations')
        print('p - show most popular artists')
        print('h - how popular is the most popular')
        print('m - which user has the most likes')
        print('q - save and quit\n')
        letter = input('Enter a letter to choose an option: ')
        if letter == 'q':
            save(fileName)
            break
        elif letter == 'e':
            if userName[-1] == '$':
                getPref(userName[:-1])
            else:
                getPref(userName)
        elif letter == 'r':
            if userName[-1] == '$':
                getRec(userName[:-1])
            else:
                getRec(userName)
        elif letter == 'p':
            mostPopArt()
        elif letter == 'h':
            howPopArt()
        elif letter == 'm':
            userMostLikes(userName)
        else:
            print('\nSorry,',letter,'is illegitimate')
            print('Please enter a letter which is in the instructions below')



            

if __name__ == "__main__": main()
