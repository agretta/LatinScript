import sys;
import re;
import time;
import linecache;

#WORD CONSISTS OF PREFIX+STEM+INFLECTION+TACKON+SUFFIX
#CREDIT GOES TO WILLIAM WHITAKERS WORDS FOR DICTONARY ENTRIES

##########################################################################imaline#!#################################################################################################
#-- =  ignore line

UNIQUES = dict();
STEMS = dict();
TACKONS = dict();
PREFIXES = dict();
SUFFIXES = dict();
INFLECTIONS = dict();


defbreak = "################################################################################\n";
    #debug log that really dosnt debug, it just prints, eventually to a different window for reasons
def debug(output):
    print(output);

def searchUNIQUES(input):
# unique words
# no principal parts
#FORMAT 
#word
#TYPE   DECLENSION/CONJUNCTION  VARIANT   DEPENDS ON TYPE...
#DEFENITION
    if input in UNIQUES:
        debug("\n" + UNIQUES.get(input)+ "\n");
        return 1;
    return -1;

def STEMSSEARCH2(input):
    #debug("Searching Stems")
    list = [];
    for stem in STEMS:
        if stem in input:
            list.append(stem)
    if list is not None:
        stm = max(list, key=len);
        out = STEMS.get(stm)
        for i in out:
            #debug(i)
            placement =  re.search("[0-9]*$", i)
            if placement is not None:            
                placement = int(placement.group(0))
                #debug(placement);
                inflect = input.replace(stm, "")
                output = "\n" +defbreak + stm+ "." + inflect + "\n"+ searchDEF('Data\DICTL.txt', placement)
                trueOut = getInflect(input, re.search( "(V|ADJ|N|PRO|PREP|INTERJ|ADV) {1,}\d \d" , i), inflect , output)
                debug(trueOut);
        return 1;    
    return -1;
    

def getInflect(word, type,inflect, out):
    if type is not None:
        type = type.group(0)
        splitter = re.search(" {1,}",type)
        typeList= type.split(splitter.group(0))
        #debug(inflect)
        #debug("Type: " + type)
        list = []
        list = INFLECTIONS.get(inflect)
        #out = ""
        temp = ""
        #debug("Type: " + type)
        #debug(typeList[0] + " Nums: " + typeList[1])
        if list is not None:
	        for i in list:
	            line = re.match(typeList[0] + " {1,}" + typeList[1], i)
	            #debug(line)
	            if line is not None and i is not None:
	                #line = line.group(0)
	                temp += (i + "\n")
	        if temp is not "":
	            return out+temp;
	        else:
	        	return "";            
    else:
        debug("This isnt a word")
        return -1


#Gets def of stem
def searchDEF(file , lineNumber):
    line = linecache.getline(file, lineNumber);
    return line;


#TESTING SITE : regex101
def loadDictonaries():
    #TODO
    
    #PREFIXES.update(ldFileThreeLine('ADDONS.txt', "(?<=^PREFIX ).+\b$"));                                   #lookbehind for thing after PREFIX
    #PREFIXES.update(ldFileThreeLine('ADDONS.txt', "(?<=^PREFIX ).+$"));  

    PREFIXES.update(ldFileThreeLine('Data\ADDONS.txt', "^(PREFIX).+"));                                   #lookbehind for thing after PREFIX


    SUFFIXES.update(ldFileThreeLine('Data\ADDONS.txt', "^(SUFFIX).+"));

    TACKONS.update(ldFileThreeLine('Data\ADDONS.txt',  "^(TACKON).+"));

    STEMS.update(ldFile('Data\STEMS.txt',"\t?.+|\w.+", "^\w+"));                                             #POSSIBLE OVERRIDING??

    UNIQUES.update(ldFileThreeLine(r'Data\UNIQUES.txt', "^\w+")); 


    INFLECTIONS.update(ldInflections('Data\INFLECTIONS.txt', "[a-z]+"));
    
    stored = "";

def ldInflections(filename , regexT):
    newS = dict();
    if regexT != "":
        debug("Loading " + filename);
        
        f = open(filename);
        for line in f:
            l = re.search( "^--.*$", line)
            #debug(l);
            if l is None:                            
                #debug(leline)
                a = re.search(regexT ,line);             #meaningful variable names
                #debug(a);
                if a is not None:                        ## MAKE NONE-CHECKING INTO SEPERATE FUNCTION LATER
                    a = a.group(0);
                    if newS.get(a) is not None:
                        newS[a].append(line);
                    #debug(a);
                    else:
                        newS[a] = [line];

    return newS;        
    debug("Wheres your regex?");

def ldFileThreeLine(filename, regexT):  #This one is for smaller files that DONT WORK FOR SOME REASON
    newS = dict();
    if regexT != "":
        debug("Loading " + filename);
        
        f = open(filename);
        for line in f:
            l = re.search( "^--.*$", line)
            #debug(l);
            if l is None:
                leline = line+f.readline()+f.readline();               
                #debug(leline)
                a = re.search(regexT ,leline);             #meaningful variable names
                #debug(a);
                if a is not None:                        ## MAKE NONE-CHECKING INTO SEPERATE FUNCTION LATER
                    a = a.group(0);
                    #debug(a);
                    b =  leline;
                    newS[a] = b;

    return newS;        
    debug("Wheres your regex?");



#this is for REALLY big files to read n stuff so it dosent take years to read
def ldFile(filename, regexT , regexK):

    if regexT != "":
        debug("Loading " + filename);
        newS = dict();
        with open(filename, 'r') as f:
            for line in f:
               
               #debug(line);
               a = re.search(regexT ,line);             #meaningful variable names
               
               if a is not None:                        ## MAKE NONE-CHECKING INTO SEPERATE FUNCTION LATER
                   a = a.group(0);
                  # debug(a);
                   b =  re.search(regexK ,a);

                   if b is not None:
                       #debug(b);
                       b = b.group(0);
                       #a = re.sub(regexK , "", a);     #is this really nessesary ?
                       if newS.get(b) is not None:
                            newS[b].append(a);
                        #debug(a);
                       else:
                            newS[b] = [a];

        return newS;        
    debug("Wheres your regex?");






def tests():
    debug("These are hard coded tests")
    debug(search("eundem"));
    debug(search("aforet"));
    debug(search("mensuum"));
    debug(search("vult"));
    debug(search("ec"));
    debug(search("mare"))
    debug(search("corporo"))
    debug(search("manus"))
    debug(search("abactus"))
    #debug("BEEEP");

def search(input):
    if searchUNIQUES(input) > 0:
        return;
    elif STEMSSEARCH2(input) > 0:
        return;

def getInput():
    return input("\n" +defbreak+"Type EXIT to exit script\nPlease Write your word to be translated here:" )

class Script:
    debug("Loading Dictonary"); # tiny men are loading the dictonary with the words, this takes a while.
    loadDictonaries();
    #debug(PREFIXES)
    #debug(SUFFIXES)
    #debug(TACKONS)
    #debug(INFLECTIONS.get("es"))
    tests();
    #debug("Type EXIT to exit script")
    
    while True:

        inpt = getInput();
        if inpt == 'EXIT':
            #debug(inpt)
            sys.exit();
        else:
            search(inpt)
            
        
        #input = "";
        #input = input()
        #top quality testing
        #tests();     
        #searchUNIQUES(input);

       # if searchSTEM(input) != -1:
        #    time.sleep(60);
         #   sys.exit(0);
        #debug("No word made");
    

    



def oldCode():


    
###########
    while(f.readline() != ''):
        prefixes.append(f.readline());
    f.close();
    debug(prefixes);
    


    for x in range(0,len(prefixes)):
        fullWord = prefixes[x];
        if fullWord in input:
            prefix = ''.join(re.findall(fullWord, input));
            input = re.sub(fullWord, '', input);
            break;

    for x in range(0,len(suffixes)):
        fullWord = prefixes[x];
        if fullWord in input:
            prefix = ''.join(re.findall(fullWord, input));
            input = re.sub(fullWord, '', input);
            break;

    for x in range(0,len(tenseEndings)):
        fullWord = prefixes[x];
        if fullWord in input:
            prefix = ''.join(re.findall(fullWord, input));
            input = re.sub(fullWord, '', input);
            break;

    for x in range(0,len(prefixes)):
        fullWord = prefixes[x];
        if fullWord in input:
            prefix = ''.join(re.findall(fullWord, input));
            input = re.sub(fullWord, '', input);
            break;

    debug(input);
    debug(prefix);


