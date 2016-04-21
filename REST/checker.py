def checkCriterias(criterias):
    orderOperator=[2,5,6,9,12,13,14]
    a = 0
    numCri = 0
    numOpe = 0
    for item in range(len(criterias)):
        if criterias[item].type != 'operatorcriteria':
            numCri +=1 
            lastCriPo = item
        else:
            numOpe +=1
    numTotal = numCri + numOpe
    if numTotal == len(criterias) and numCri == numOpe+1:
        if lastCriPo%2 == 1:
            orderOperator = range(2,numTotal-1,2)
            orderOperator.append(numTotal-1)
        elif lastCriPo%2 == 0:
            orderOperator = range(2,numTotal-1,2)
            orderOperator.append(numTotal-1)
        for item in range(len(criterias)):
            
            if item in orderOperator:
                if criterias[item].type != 'operatorcriteria':
                    raise NameError('Error in the criterias. There is an criteria in an operator')
            elif not item in orderOperator:
                a =+1
                if criterias[item].type == 'operatorcriteria':
                    raise NameError('Error in the criterias. There is an operator in an criteria')
            else:
                p = 0

            if item == len(criterias)-1:
                if criterias[item].type != 'operatorcriteria':
                    raise NameError('Error in the criterias. No last operator')
    elif numCri <= numOpe:
        raise NameError('Error in the criterias. Not enough criterias')
    else:
        raise NameError('Error in the criterias. Not enough operators for criterias')

def prueba(a):
    if a == 0:
         return 0
    else:
        return prueba(a-1) + prueba (a-2)
def checkCriterias(criterias):
    stack = []
    a = ''
    for item in range(len(criterias)):
        if criterias[item].type != 'operatorcriteria':
            stack.append(0)
        if criterias[item].type == 'operatorcriteria':  
            stack.append(1) 
    item = 0
    p = 0
    a = ''
    while item < len(stack):
        go = item
        if 1 == stack[item]:
            if stack[item-2] == 0 and stack[item-1]:
                stack.pop(item-2)
            else:
                print 
            item = 0
        item+=1
    if len(stack)==1 and stack[0] == 0:
        return 'WOOOOORKING'
    else:
        raise NameError('Error in criterias')

























def checkCriterias(criterias):
    stack = []
    a = ''
    for item in range(len(criterias)):
        if criterias[item].type != 'operatorcriteria':
            stack.append(0)
        if criterias[item].type == 'operatorcriteria':  
            stack.append(1) 
    item = 0
    p = 0
    a = ''
    while item <= len(stack):
        go = item
        if '001' in a:
            for ran in range(go-1,go-4,-1):
                stack.pop(ran)
                go=ran
            if go < 0:
                go = 0
            stack.insert(go,0)
            a=''
            item = 0
        else:
            try:
                a+=str(stack[item])
            except IndexError:
                pass
            item+=1
    if len(stack)==1 and stack[0] == 0:
        return 'WOOOOORKING'
    else:
        raise NameError('Error in criterias')