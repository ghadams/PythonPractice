import random

#Function to print instructions
def printinfo():
    print("Type 1, 2, or 3")
    print("1) Rock")
    print("2) Paper")
    print("3) Scissors")

def game():
    user = input("\nRock, paper, scissors, shoot! ")
    while(user not in ['1','2','3']):
        print("\nInvalid input")
        printinfo()
        user = input("")
    outcome(int(user), random.randrange(0, 3))


rock = {'rock':0,'paper':-1,'scissors':1}
paper = {'rock':1,'paper':0,'scissors':-1}
scissors = {'rock':-1,'paper':1,'scissors':0}
options = [rock, paper, scissors]
names = ['rock', 'paper', 'scissors']
score = [0,0]
#Test if a beats b
def outcome(a, b):
    pick = names[a-1]
    aipick = names[b]
    outcomedict = options[a-1]
    r = outcomedict[aipick]
    if r == -1:
        print("Oh no! You chose {} and the AI chose {}".format(pick,aipick))
        score[1] += 1
    elif r == 0:
        print("Draw! You and the AI chose {}".format(pick))
    elif r == 1:
        print("You win! You chose {} and the AI chose {}".format(pick,aipick))
        score[0] += 1
    print("You {} - {} AI".format(score[0], score[1]))


print("Let's Play Rock, Paper, Scissors!\n")
printinfo()
while 1:
    game()
