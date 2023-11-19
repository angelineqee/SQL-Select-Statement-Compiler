#Lexical Analysis
#Create a Token class to verify each token
class Token:
    TYPE = None
    VALUE = None

#create a Lexer class for lexical analysis
class Lexer:
    
    #create lists to define every symbols, keywords and operators
    listType = ['*','(',')', '=','<>','!=','>','<','>=','<=',',',';']
    KEYWORDS = ['SELECT', 'FROM', 'WHERE','AND','OR']
    NUM_COMPARISON_OP = ['=','<>','!=','<','>','<=','>=']
    STR_COMPARISON_OP = ['=','<>','!=']
    
    #assign a number for each of the symbols, keywords and operators
    SELECT = 1
    FROM = 2
    WHERE = 3
    AND = 4
    OR = 5
    INT_LIT = 6
    IDENT = 7
    EQUAL_OP = 8
    NOT_EQUAL_OP = 9
    LARGER_OP = 10
    SMALLER_OP = 11
    LARGER_EQ_OP = 12
    SMALLER_EQ_OP = 13
    ASTERISK = 14
    LEFT_PAREN = 15
    RIGHT_PAREN = 16
    COMMA = 18
    SEMICOLON = 19
    STRING = 20

    #create a token object and a list to store the lexeme
    token = Token()
    lexemeList = list()
    
    #create a flag to indicate whether all tokens are valid or not
    valid = 1

    #This function is to tokenize the input string
    def analyzer(self, inputString):
        def getIdent(input, index):
            count = index
            #To get the words separated by whitespace
            while(count < len(input) and input[count] != ' ' and input[count] != '\n'):
                if(input[count] in self.listType or input[count] in self.KEYWORDS):
                    return input[index:count]
                count += 1
            return input[index:count]
        
        def getString(input, index):
            count = index+1
            #To get all characters including whitespace until another single quote found or endOfFile
            while(input[count] != '\'' ):
                count += 1
                if(count >= len(input)):
                    print('!ERROR: Unterminated string literal')
                    self.valid = 0
                    break
            return input[index:count+1]

        #switchOp function to map the symbols to the corresponding token
        def switchOp(x):
            default = lambda x: x
            return {
                '*': (self.ASTERISK, '*'),
                '(': (self.LEFT_PAREN, '('),
                ')': (self.RIGHT_PAREN, ')'),
                '=': (self.EQUAL_OP, '='),
                '<>': (self.NOT_EQUAL_OP, '<>'),
                '!=': (self.NOT_EQUAL_OP, '!='),
                '>': (self.LARGER_OP, '>'),
                '<': (self.SMALLER_OP, '<'),
                '>=': (self.LARGER_EQ_OP, '>='),
                '<=': (self.SMALLER_EQ_OP, '<='),
                ',': (self.COMMA, ','),
                ';': (self.SEMICOLON, ';')
            }.get(x, (None, x))  # Fix the default case
        
        #switchKeywords function to map the keywords to the corresponding token
        def switchKeywords(x):
            default = lambda x: x
            return {
                'SELECT': (self.SELECT,'SELECT'),
                'FROM': (self.FROM, 'FROM'),
                'WHERE': (self.WHERE, 'WHERE'),
                'AND': (self.AND, 'AND'),
                'OR':(self.OR,'OR')
            }.get(x,(None,x))

        i = 0

        #tokenize the input string
        while i < len(inputString):
            newToken = Token()
            #check whether the character is not a space or new line
            if (inputString[i] != ' ' and inputString[i] != '\n') :  
                #check whether the input string is alphanumeric or an underscore
                if (inputString[i].isalnum() or inputString[i] == '_'):
                    ident = getIdent(inputString, i)
                    #check whether the input string is a keyword
                    if ident.upper() in self.KEYWORDS:
                        newToken.TYPE = switchKeywords(ident)[0]
                        newToken.VALUE = switchKeywords(ident)[1]
                    #check whether the input string is a number
                    elif self.isNum(ident):
                        newToken.TYPE = self.INT_LIT
                        newToken.VALUE = ident
                    #else it will fall under identifier category
                    else:
                        #an identifier cannot start with a number
                        if (self.isNum(ident[0])):
                            newToken.TYPE = None
                            newToken.VALUE = ident
                            self.valid = 0
                        else:
                            newToken.TYPE = self.IDENT
                            newToken.VALUE = ident
                    #append the token lexeme list and update the index
                    self.lexemeList.append(newToken)
                    i += (len(ident) - 1)
                    
                #tokenize all the things as string in the single quote
                elif(inputString[i] == '\''):
                    string = getString(inputString, i)
                    newToken.TYPE = self.STRING 
                    newToken.VALUE = string
                    self.lexemeList.append(newToken)
                    i += (len(string) - 1)

                #check whether the input form a <=, >= or <> then it will be tokenize as a whole 
                elif inputString[i:i+2] in ('<=', '>=', '<>'):
                    newToken.TYPE = switchOp(inputString[i:i+2])[0]
                    newToken.VALUE = switchOp(inputString[i:i+2])[1]
                    self.lexemeList.append(newToken)
                    i += 1
                    
                #if the character is a single charactor operator 
                else:
                    newToken.TYPE = switchOp(inputString[i])[0]
                    newToken.VALUE = switchOp(inputString[i])[1]
                    self.lexemeList.append(newToken)
            i += 1

    #isNum function is to check whether the input is a number
    def isNum(self, n):
        try:
            int(n)
            return True
        except ValueError:
            return False

    #getNext is to get the next token from the lexeme list
    def getNext(self):
        if len(self.lexemeList) > 0:
            output = self.lexemeList.pop(0)
            #Uncomment the following line to check the tokenisation process
            print("Next token is: %s Next lexeme is %s" % (output.TYPE, output.VALUE))
            return output
        else:
            tmpToken = Token()
            tmpToken.TYPE = -100
            tmpToken.VALUE = "Fail"
            return tmpToken

# read from text file
text = open('C:/Users/Angeline/OneDrive/Documents/CPT316/test.txt','r')
content = text.read()

#create an instance for the Lexer class
tokenize = Lexer()

#analyse the content of the file by calling the analyzer function
tokenize.analyzer(content)

#print the tokenize lexemes
for token in tokenize.lexemeList:
    print(f"Type: {token.TYPE}, Value: {token.VALUE}")
    if(token.TYPE == None):
        print("Invalid token")
    
#Syntax Analysis
class Parser:
    lexer = Lexer()
    token = Token()
    nextToken = None
    #a flag to determine whether the input is accepted by the grammar or not
    accepted = 1 
    #a counter to check the number of open parentheses, to ensure balance parentheses
    openParenNum = 0 
    
    #Compile function
    def compile(self,inputString):
        self.lexer.lexemeList.clear()
        self.lexer.analyzer(inputString)
        for token in self.lexer.lexemeList:
            if(token.TYPE == None):
                self.lexer.valid = 0
            if(token.TYPE == self.lexer.LEFT_PAREN):
                self.openParenNum += 1
            if(token.TYPE == self.lexer.RIGHT_PAREN):
                self.openParenNum -=1
        if(self.lexer.valid == 0):
            print('!ERROR: Invalid token(s) found, unable to parse')
        else:
            self.getNextToken()
            self.selectStatement()
    
    #Start of SELECT statement
    def selectStatement(self):
        if(self.nextToken.TYPE == self.lexer.SELECT):
            #print("Entering SELECT")
            self.getNextToken()
            if(self.nextToken.TYPE == self.lexer.IDENT):
                self.identifier()
                #Check if there is more than one columns selected
                self.selectList()
            elif(self.nextToken.TYPE == self.lexer.ASTERISK):
                self.getNextToken()
            else:
                print("!ERROR: Lexeme: " + self.nextToken.VALUE + ", Columns to be selected not specified")
                self.accepted = 0
                self.getNextToken()
        else:
            print("!ERROR: Lexeme: " + self.nextToken.VALUE + ", A select statement must start with SELECT")
            self.accepted = 0
            self.getNextToken()
            
        self.fromStatement()
        self.getNextToken()
        
        #Check if there is any following condition 
        #If there is no WHERE specified and it is not the end of file, there should be another select statement
        if(self.endOfQuery()):
            self.printResult()
        #If there is a WHERE condition
        else:
            self.whereStatement()
            self.getNextToken()
            if(self.nextToken.TYPE != self.lexer.SEMICOLON and self.nextToken.TYPE != -100):
                print("Unexpected token " + self.nextToken.VALUE)
                self.accepted = 0
                self.printResult()
        

    #Check FROM statement, executed after select
    def fromStatement(self):
        if(self.nextToken.TYPE == self.lexer.FROM):
            #print("Entering FROM")
            self.getNextToken()
            if(self.nextToken.TYPE != self.lexer.IDENT):
                print("!ERROR: Lexeme: " + self.nextToken.VALUE + ", Table name if not specified")
                self.accepted = 0
        else:
            print("!ERROR: Lexeme: " + self.nextToken.VALUE + ", A select statement must follow with a FROM")
            self.accepted = 0
        
    #Check WHERE statement, executed after 
    def whereStatement(self):
        if(self.nextToken.TYPE == self.lexer.WHERE):
            print("Entering WHERE")
            self.getNextToken()
            self.condInParen()
        else:
            print("!ERROR: Lexeme: " + self.nextToken.VALUE + ", Missing semicolon")
            self.accepted = 0
            self.printResult()
        
    #To check if the condition is in parentheses
    def condInParen(self):
        if(self.nextToken.TYPE == self.lexer.IDENT):
            self.condition()
            self.getNextToken()
            self.conditionList()
        elif(self.nextToken.TYPE == self.lexer.LEFT_PAREN):
            self.getNextToken()
            self.condInParen()
            if(self.nextToken.TYPE == self.lexer.RIGHT_PAREN):
                print('Parentheses closed')
                self.getNextToken()
                self.conditionList()
            else:
                print("!ERROR: Lexeme: " + self.nextToken.VALUE + ", Missing closed parenthesis")
                self.accepted = 0
                self.getNextToken()
                
        else:
            print("!ERROR: Lexeme: " + self.nextToken.VALUE + ", Invalid condition")
            self.accepted = 0
            self.getNextToken()
        
    #WHERE condition
    def condition(self):
        print('Checking WHERE conditions')
        if(self.nextToken.TYPE == self.lexer.IDENT):
            self.getNextToken()
            #To determine whether a string or a number is being compared
            if(self.nextToken.VALUE in self.lexer.STR_COMPARISON_OP):
                self.compareStr()
            elif(self.nextToken.VALUE in self.lexer.NUM_COMPARISON_OP):
                self.compareNum()
            else:
                print("!ERROR: Lexeme: " + self.nextToken.VALUE + ", Invalid condition")
                self.accepted = 0
        else:
            print("!ERROR: Lexeme: " + self.nextToken.VALUE + ", Missing identifier")
            self.accepted = 0
        
    #WHERE conditions list
    def conditionList(self):
        if(self.nextToken.TYPE == self.lexer.AND or self.nextToken.TYPE == self.lexer.OR):
            print('Checking list of conditions')
            self.getNextToken()
            self.condInParen()
        elif(self.nextToken.TYPE != self.lexer.RIGHT_PAREN and self.nextToken.TYPE != self.lexer.SEMICOLON):
            print('!ERROR: Logical operator/Closed parenthesis/Semicolon expected')
        elif(self.nextToken.TYPE == self.lexer.SEMICOLON):
            self.printResult()
        else:
            print('No more condition')
            
    #Compare string
    def compareStr(self):
        self.getNextToken()
        #Since string comparison operations (equal and not equal) can be used in number comparison too,
        if(self.isNumber()):
            return
        elif(self.isString()):
            return
        else:
            print("!ERROR: Lexeme: " + self.nextToken.VALUE + ", Incompatible type, number/string is expected")
            self.accepted = 0
    
    #Compare number
    def compareNum(self):
        self.getNextToken()
        if(self.isNumber()):
            return
        else:
            print("!ERROR: Lexeme: " + self.nextToken.VALUE + ", Incompatible type, number is expected")
            self.accepted = 0
    
        
    #Checking select list, comma means there are more columns to be selected
    def selectList(self):
        while(self.nextToken.TYPE == self.lexer.COMMA):
            print("Checking select list")
            self.getNextToken()
            self.identifier()
            
    #Check end of query
    def endOfQuery(self):
        if(self.nextToken.TYPE == self.lexer.SEMICOLON):
            return True
        
    #Check identifier  
    def identifier(self):
        if(self.nextToken.TYPE != self.lexer.IDENT):
            print("!ERROR: Lexeme: " + self.nextToken.VALUE + "\nAn identifier is expected")
            self.accepted = 0
        self.getNextToken()
        
    #Check whether the token is a number, used in condition to simplify the code
    def isNumber(self):
        if(self.nextToken.TYPE == self.lexer.INT_LIT):
            return True

    #Check whether the token is a string
    def isString(self):
        if(self.nextToken.TYPE == self.lexer.STRING):
            return True
             
    #Get next token from the list of lexemes
    def getNextToken(self):
        self.nextToken = self.lexer.getNext() 
                
    #Print result
    def printResult(self):
        if(self.openParenNum != 0):
            self.accepted = 0
            print("Imbalance parentheses")
        if (parser.accepted == 1):
            print("The input is accepted \n")
        else:
            print("The input has syntax error \n")

#create an instance for Parser class
parser = Parser()

#analyse the content of the file by calling the compile function
parser.compile(content)



