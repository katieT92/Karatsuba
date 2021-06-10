
######################################################################################
#                                        Globals                                     #
######################################################################################

minInputValue = 1           # user must enter number for A and B >= 1
maxInputValue = 1000        # user must enter number for A and B <= 1000
minInputOption = 1          # user must enter option number >= 1
maxInputOption = 3          # user must enter option number <= 3
quitOption = 3              # option number to quit
task1 = "simplify term2"    # arg to solveListPlaceCalculations(task): simplify 2nd term
task2 = "add terms"         # arg to solveListPlaceCalculations(task): add all terms


##########################################################################################
#                                     Main Algorithms                                    #
##########################################################################################


#####################################   Karatsuba   ######################################

def karatsuba_mult(A, B):

  # Ensure A & B are same length after term2 simplification in callee
  while len(A) > len(B):
    B.insert(0,0)
  while len(B) > len(A):
    A.insert(0,0)

  # Base Case Handler
  n = len(A)
  if n == 1:
    return [int(x) for x in str(A[0] * B[0])]

  # Ensure list lengths are even for evenly dividing in half
  if n % 2 == 1:
    n += 1
    A = [int(digit) for digit in str(convertListToInt([str(digit) for digit in A])).zfill(n)]
    B = [int(digit) for digit in str(convertListToInt([str(digit) for digit in B])).zfill(n)]

  # Created for reuse of list halves
  listHalves = [ (A[:n//2], A[n//2:]), (B[:n//2], B[n//2:]) ]

  term1 = karatsuba_mult(listHalves[0][0], listHalves[1][0])
  term2 = karatsuba_mult(addListHalves(listHalves[0][0], listHalves[0][1]), addListHalves(listHalves[1][0], listHalves[1][1]))
  term3 = karatsuba_mult(listHalves[0][1], listHalves[1][1])

  term2 = [int(digit) for digit in sumElementsInList(appendZeros(solveListPlaceCalculations(term1, term2, term3, task1)))]

  #Append respective # of 0's to term1 and term2
  for i in range(n):
    term1.append(0)
    halfN = n//2
    if i < halfN:
      term2.append(0)

  return [int(digit) for digit in sumElementsInList(appendZeros(solveListPlaceCalculations(term1, term2, term3, task2)))]


###################   Exponentiation: Decrease by Constant Factor   ######################

def expo(A, B):
  if B == 0:
    return [1]
  elif B % 2 == 1:
    expoResult = expo(A,(B-1)//2)
    return karatsuba_mult(  karatsuba_mult(expoResult, expoResult),  [int(digit) for digit in str(A)]  )

  else:
    expoResult = expo(A, B//2)
    return karatsuba_mult(expoResult, expoResult)



##########################################################################################
#                             Karatsuba Helper Functions                                 #
##########################################################################################

# Returns list of ints resulting from adding first and second half list elements together
def addListHalves(firstHalf, secondHalf):
  length = len(firstHalf)
  sum = 0
  for digit in range(length):
    sum += ( (firstHalf[digit] + secondHalf[digit]) * (10**(length-1-digit)) )
  return [int(digit) for digit in str(sum)]


# Creates an array whose elements are the result of running the appropriate operations (+,-),
# specified by the task argument, on the corresponding indices of list1, list2, and list3.
def solveListPlaceCalculations(list1,list2,list3,task):
  resolvedList = []
  listPairLen = [(list1,len(list1)), (list2,len(list2)), (list3,len(list3))]
  rangeLen = max([listPairLen[0][1], listPairLen[1][1], listPairLen[2][1]])

  for i in range(rangeLen):
    total = 0
    for pair in range(len(listPairLen)):
      list = listPairLen[pair][0]
      listLen = listPairLen[pair][1]
      if listLen <= rangeLen and listLen > i:
        if task == task1:
          if pair == 1:
            total += list[listLen-1-i]
          else:
            total -= list[listLen-1-i]
        else:
          total += list[listLen-1-i]
    resolvedList.insert(0,total)
  return resolvedList


# Appends respective # of 0's to lists[]' elements
def appendZeros(list):
  for i in range(len(list)):
    calculation = [digit for digit in str(list[i])]
    if listNumRepresentationIsNegative(calculation):
      calculation = joinIdx1and2(calculation)
    for e in range(len(list) - 1 - i):
      calculation.append('0')
    list[i] = convertListToInt(calculation)
  return list


# Determines if the list has negative sign in index 0, indicating negative number
def listNumRepresentationIsNegative(list):
  return list[0] == '-'


# Used when listNumRepresentationIsNegative is true. Makes first element in list '-x', which
# can easily be parsed to an int as opposed to first element being '-' and second being 'x'
def joinIdx1and2(list):
  list[0] += list[1]
  list.pop(1)
  return list


# Converts a list of ints to a single int
def convertListToInt(list):
  list_string = "".join(list)
  return int(list_string)


# Sum elements in operandsList[] and return as finalList[]
def sumElementsInList(operandsList):
  total = 0
  for i in range(len(operandsList)):
    total += operandsList[i]
  finalList = [digit for digit in str(total)]

  if listNumRepresentationIsNegative(finalList):
    finalList = joinIdx1and2(finalList)
  return finalList



##########################################################################################
#                                 Console and I/O Routines                               #
##########################################################################################


# Validate that the input value from user is in valid range
def validateInputValue(inInput, letter):
  validated = False
  while not validated:
    validInput = validateInt(inInput)
    if validInput >= minInputValue and validInput <= maxInputValue:
      return validInput
    print("\nError: Input out of range.")
    inInput = input("Enter value (1-1000) for {}: ".format(str(letter)))


# Validate the input option from user is in valid range
def validateInputOption(inInput):
  validated = False
  while not validated:
    validInput = validateInt(inInput)
    if validInput >= minInputOption and validInput <= maxInputOption:
      return validInput
    print("\nError: Input out of range.")
    inInput = input("Enter option number (1, 2, or 3): ")


# Validate that input values from user are ints where required
def validateInt(inInput):
  validated = False
  while not validated:
    try:
      userInput = int(inInput)
      return userInput
    except ValueError:
      print("\nError: Input must be an integer.")
      inInput = input("Enter integer value: ")


#Print options menu
def printMenu():
  print("\n--------------------")
  print("         Menu         ")
  print("--------------------")
  print("1. Task 1")
  print("2. Task 2")
  print("3. Quit")


# Print user defined settings
def printSettings(A, B, option):
  print("\n--------------------")
  print("       Settings       ")
  print("--------------------")
  print("A: " + str(A))
  print("B: " + str(B))
  print("Option: " + str(option))
  print("--------------------\n")


# Call respective Main Algorithms
def executeOption(A, B, option):
  listA = [int(digit) for digit in str(A)]
  listB = [int(digit) for digit in str(B)]
  if option == 1:
    result = karatsuba_mult(listA, listB)
    print("{op1} * {op2} = ".format(op1=A, op2=B), end='')
    for i in result:
      print(i, end='')
  else:
    result = expo(A,B)
    lenResult = len(result)
    print("{op1} ^ {op2} = ".format(op1=A, op2=B), end='')
    if lenResult <= 10: # if the result is a number with <= 10 digits we will print list elements normally
      for i in result:
        print(i, end='')
    else: # for readability, we will add scientific notation to numbers with more than 10 digits in their list
      print("{firstNum}.".format(firstNum=result[0]), end='')
      for i in range(1,10):
        print(result[i], end='')
      print("e+{len}".format(len=lenResult-1), end='')
  print("\n")



##########################################################################################
#                                          Main                                          #
##########################################################################################

while True:
  print("\nEnter two positive integers, A and B, both <= 1000.")
  A = validateInputValue(input("\nEnter value (0-1000) for A: "), "A")
  B = validateInputValue(input("\nEnter value (0-1000) for B: "), "B")
  printMenu()
  option = validateInputOption(input("\nEnter option number (1, 2, or 3): "))
  printSettings(A, B, option)
  if option == quitOption:
    break
  executeOption(A, B, option)