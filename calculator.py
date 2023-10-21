class Node:
    def __init__(self, value):
        self.value = value  
        self.next = None 
    
    def __str__(self):
        return "Node({})".format(self.value) 

    __repr__ = __str__
                          
class Stack:
    def __init__(self):
        self.top = None
    
    def __str__(self):
        temp=self.top
        out=[]
        while temp:
            out.append(str(temp.value))
            temp=temp.next
        out='\n'.join(out)
        return ('Top:{}\nStack:\n{}'.format(self.top,out))

    __repr__=__str__


    def isEmpty(self):
        if self.top == None:
            return True

    def __len__(self): 
        trace = self.top
        count = 0
        while trace:
            count+=1
            trace=trace.next
        return count

    def push(self,value):
        new_top = Node(value)
        new_top.next = self.top
        self.top = new_top

     
    def pop(self):
        if not self.isEmpty():
            popped_node = self.top
            self.top = self.top.next
            popped_node.next = None
            return popped_node.value

    def peek(self):
        return self.top.value

class Calculator:
    def __init__(self):
        self.__expr = None


    @property
    def getExpr(self):
        return self.__expr

    def setExpr(self, new_expr):
        if isinstance(new_expr, str):
            self.__expr=new_expr
        else:
            print('setExpr error: Invalid expression')
            return None

    def _isNumber(self, txt):

        try:
            x=float(txt)
            return True
        except:
            return False




    def _getPostfix(self, txt):
        # vars
        postfixStack = Stack()
        operators = ['^','*','/','+','-','(',')']
        operators_no_p = ['^','*','/','+','-']

        ### i need to check if any numbers are not sperated by operators

        saw_space = False
        temp = ''
        for i in txt:
            if i.isnumeric() and temp.isnumeric() and saw_space:
                return None
            if i.isspace():
                saw_space = True
            else:
                saw_space = False
                temp = i


        ### delete spaces

        txt = txt.replace(' ', '')
        new_string = ''
        
        ### Insert spaces only around supported operators ###
        
        for char in txt:
            if char in operators:
                new_string += ' '+char+' '
            else:
                new_string += char

        ### create token_list ###
        token_list = new_string.split()
        
        ### make sure it is a valid expression ###
        if token_list.count('(') != token_list.count(')'):
            return None
        
        if token_list[-1] in operators_no_p:
            return None

        ### creates negative numbers ###
        for i in range(len(token_list)-2):
            if token_list[i] in operators:
                if token_list[i+1] == '-':
                    token_list[i+2] = '-'+token_list[i+2] 
                    token_list.pop(i+1)
        if token_list[0] == '-':
            token_list[1]='-'+token_list[1]
            token_list.pop(0)

        ### more validation ###
        for i in range(len(token_list)-1):
            if token_list[i] in operators_no_p and token_list[i+1] in operators_no_p:
                return None
            
        ### create dictionary to identitify opperation priority ###
        final_list = []

        opperation_priority = {}
        opperation_priority['^'] = 4
        opperation_priority['/'] = 3
        opperation_priority['*'] = 3
        opperation_priority['+'] = 2
        opperation_priority['-'] = 2
        opperation_priority['('] = 0

        ### traversing token list ###
        for token in token_list:
            #if token is number
            if self._isNumber(token):
                final_list.append(token)
            
            #push onto operator stack
            elif token == '(':
                postfixStack.push(token)
            #once you close parentheses add the tokens inside the parentheses onto the final list and remove them from the stack
            elif token == ')':
                top_token = postfixStack.pop()
                while top_token != '(':
                    final_list.append(top_token)
                    top_token = postfixStack.pop()
            #if token is normal opperator
            else:
                ### inserts the token according to its opperation_priority; highest on top ###
                while not postfixStack.isEmpty() and (opperation_priority[postfixStack.peek()] >= opperation_priority[token]):
                    final_list.append(postfixStack.pop())
                postfixStack.push(token)
                
        #leftover opperators
        while not postfixStack.isEmpty():
            final_list.append(postfixStack.pop())

        ### turn final_list into return_string ###
        return_list = []
        for i in final_list:
            if self._isNumber(i):
                return_list.append(str(float(i)))
            else:
                return_list += i
        return_string = " ".join(return_list)

        return return_string


    @property
    def calculate(self):
        if not isinstance(self.__expr,str) or len(self.__expr)<=0:
            print("Argument error in calculate")
            return None
        if self._getPostfix(self.getExpr) == None:
            return None
        txt = self._getPostfix(self.getExpr)
        calcStack = Stack()
        token_list = txt.split()
        i=0
        while i < len(token_list):
            token = token_list[i]
            if self._isNumber(token):
                calcStack.push(token)
                i+=1
            else:
                operand = str(calcStack.pop())
                operand2 = str(calcStack.pop())
                ### exponant rule ###
                if token == "^":
                    token_index = token_list.index(token)
                    sliced_after_token = token_list[token_index+1:]
                    if len(sliced_after_token)>1:
                        if sliced_after_token[1]=='^':
                            evaluation = pow(float(operand2),pow(float(operand),float(sliced_after_token[0])))
                            i += 3
                        else:
                            evaluation = pow(float(operand2),float(operand))
                            i +=1
                    else:
                        evaluation = pow(float(operand2),float(operand))
                        i +=1
                else:
                    evaluation = eval(operand2 + token + operand)
                    i+=1
                calcStack.push(evaluation)
                
        return calcStack.pop()

class AdvancedCalculator:

    def __init__(self):
        self.expressions = ''
        self.states = {}

    def setExpression(self, expression):
        self.expressions = expression
        self.states = {}#vars
    def getStates(self):
        return self.states

    def _isVariable(self, word):
        if word.isalpha():
            return True
        if word[:-1].isalpha():
            if word[-1].isalnum():
                return True
        return False
       

    def _replaceVariables(self, expr):
        ### checks for undiffend vars ###
        token_list = expr.split()
        for token in token_list:
            if self._isVariable(token):
                if token not in self.states.keys():
                    return None
        ### replace known vars ###
        for var in self.states.keys():
            if var in expr:
                expr = expr.replace(var,str(self.states[var]))
        
        return expr

    
    def calculateExpressions(self):
        try:
            self.states = {} 
            return_dict = {}
            calcObj = Calculator()
            expression_list = self.expressions.split(';')
            for expression in expression_list:
                if expression.count("=")==1:
                    equal_index = expression.index("=")
                    after_equal = expression[equal_index+1:]
                    before_equal = expression[:equal_index-1]
                    if not self._isVariable(before_equal):
                        self.states = {}
                        return None
                    calcObj.setExpr(self._replaceVariables(after_equal))
                    self.states[before_equal] = float(calcObj.calculate)
                    
                    return_dict[expression] = self.getStates().copy()
                else:
                    return_index = 6
                    after_return = expression[return_index:]
                    after_return = self._replaceVariables(after_return)
                    calcObj.setExpr(after_return)
                    
                    return_dict['_return_'] = float(calcObj.calculate)
            return return_dict
        except:
            return None
####example of Advanced Calculator
x = Calculator()
x.setExpr("(5  *     5  )  + ( -2 /2)^2 ")
print(x.calculate)

###example of Advanced Calculator
y = AdvancedCalculator()
y.setExpression('x1 = 5 * 5 + 97;x2 = 7 * ( x1 / 2 );x1 = x2 * 7 / x1;return x1 * ( x2 - 5 )')
print(y.calculateExpressions())