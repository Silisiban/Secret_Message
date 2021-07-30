# Secret Message Encoder / Decoder.

# Imports
import string;
import random;
import pickle
 
# Defines
alphaList = [];
randomIndexList = [];
decodeDict = {};

#***************************************************************************************************************************************************************************
# Get's a list of all the characters in the alphabet and dumps them with pickle and loads them back.
def GetAlphabet():
    tempString = string.ascii_lowercase;
    tempString = list(tempString);
    
    with open(".code/alphabet.code",'wb') as file:
        pickle.dump(tempString, file)
    
    return tempString; 
#***************************************************************************************************************************************************************************

#***************************************************************************************************************************************************************************
# Creates a random list of a lenght of 26 of numbers between 0 and 25 making sure there is no duplicates. Pickle dumps and reads back in.
def MakeRandomIndexList():
    randList = [];
    randNum = 0;

    while len(randList) < 26:
        randNum = random.randint(0,25);
        if randNum not in randList:
            randList.append(randNum);
    
    with open('.code/random_index.code','wb') as file:
        pickle.dump(randList, file);
            
    return randList;
#***************************************************************************************************************************************************************************

#***************************************************************************************************************************************************************************
# Creates a Decoder Dictionary by combining the alphabet list and the random index list. pickle dumps and reads back in.
def CreateDecodeDict(alphaList, randomIndexList):
    for x in range(len(alphaList)):
        decodeDict.update({alphaList[x]: randomIndexList[x]});
    
    with open(".code/decode.code","wb") as file:
        pickle.dump(decodeDict, file);
    
    return dict(decodeDict);
#***************************************************************************************************************************************************************************

#***************************************************************************************************************************************************************************
# Handles loading the pickled files to assign the proper list variables.  Only is called if user is encoding or decoding a message.
def LoadLists():
    with open('.code/alphabet.code','rb') as file:
        alphaList = pickle.load(file);

    with open('.code/random_index.code','rb') as file:
            randomIndexList = pickle.load(file);

    with open(".code/decode.code","rb") as file:
        decodeDict = pickle.load(file);

    return alphaList, randomIndexList, decodeDict;
#***************************************************************************************************************************************************************************

#***************************************************************************************************************************************************************************
# Opens the newmessage.txt file and reads it's content's. Gets the characters orginal index from alphaList. Check's that against the decodeDict
# based on the index and grabs the key or character from decodeDict and builds a encoded message that it writes to encodedmessage.txt.
def EncodeMessage(path,alphaList,decodeDict):    
    startMessage = [];
    finishedMessage = [];

    # Read contents of newmessage.txt and add it to the list by index of the character from alphaList. If not a valid alphabet character just add the current value.
    with open(path, 'r') as encode:
        for char in encode.read().lower():    
            if char not in alphaList:
                startMessage.append(char);                
            else:
                charIndex = alphaList.index(char);
                startMessage.append(charIndex);

    # Takes the startMessage list and uses the index to find the key(character) in decodeDict and add's that character to finishedMessage list. 
    for val in startMessage:
        if isinstance(val, int):
            for key,value in decodeDict.items():
                if val == value:
                    finishedMessage.append(key);
        else:
            finishedMessage.append(val);

    # Takes each list item in finishedMessage and builds a string and writes it to encodedmessage.txt. This will both create a file and overwrite.
    messageString = "";
    for char in finishedMessage:
        messageString += char;
    
    with open('.txt/encodedmessage.txt', 'w') as encodedmessage:
        encodedmessage.write(messageString);
#***************************************************************************************************************************************************************************

#***************************************************************************************************************************************************************************
# Decodes the encodedmessage.txt file and put's it back into its orginal form.
def DecodeMessage(path, decodeDict, alphaList):    
    decodeCharacters = [];    
    decodeList = [];
    decodedMessage = "";

    # Reads the encodedmessage.txt file and puts each character into a list.
    with open(path,'r') as decode:
        decodeCharacters = list(decode.read());

    # Checks if the character is in the decodeDict if it is finds the index of that character and adds it to decodeList. If not it adds the current value.        
    for character in decodeCharacters:
        if character in decodeDict:
            for key, value in decodeDict.items():
                if character == key:
                    decodeList.append(value);
    
        else:
            decodeList.append(character);
    
    # Checks the type of each item in decodeList for int or str. if int it runs that against alphaList to get the proper character. if not adds whatever the character is.
    for x in decodeList:
        if isinstance(x,int):
            for index, value in enumerate(alphaList):
                if x == index:
                    decodedMessage += value;
        else:
            decodedMessage += x;

    # Takes the decodedMessage and writes it to decodedmessage.txt.
        with open('.txt/decodedmessage.txt','w') as decode:
            decode.write(decodedMessage);
#***************************************************************************************************************************************************************************

#***************************************************************************************************************************************************************************
# Main Function Handles user input and call's nessessary funcitons to assign vars or create new values.
def Main():
    print("*********************************")
    print("*   Press 1 to Encode Message.  *")
    print("*   Press 2 to Decode Message   *")
    print("*   Press 3 to Create new Key   *")
    print("*********************************")
    choice = input();
    print("");
    
    if choice == '1' or choice == '2':
        alphaList, randomIndexList, decodeDict = LoadLists();
        
        if choice == '1':            
            EncodeMessage('.txt/newmessage.txt',alphaList, decodeDict);
            print("Your Message Was Encoded Succsessfully... Please Select What you would like to do next. \n")
            Main()
        elif choice == '2':
            DecodeMessage('.txt/encodedmessage.txt', decodeDict, alphaList);  
            print("Your Message Was Decoded Succsessfully... Please Select What you would like to do next. \n")
            Main()
    elif choice == '3':
        alphabet = GetAlphabet();
        randomIndex = MakeRandomIndexList();
        CreateDecodeDict(alphabet, randomIndex);
        print("You have created a new key. Please select what you would like to do next. \n")
        Main()
#***************************************************************************************************************************************************************************

#***************************************************************************************************************************************************************************
# Calls the main function. 
Main();
#***************************************************************************************************************************************************************************

