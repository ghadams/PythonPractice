import random
file = open('sowpods.txt', 'r')
#print(file.read())
words = file.readlines()

def game():
    wrong = 0
    word = words[random.randint(0, len(words)-1)].lower()
    gw = ['_']*(len(word)-1)
    guessed = []
    print("Your word is " + " ".join(gw))

    while(wrong < 6 and '_' in gw):
        letter = input("Guess a letter: ")
        while(not letter.isalpha() or letter in guessed):
            if not letter.isalpha():
                letter = input("Bad Input. Guess a letter: ")
            else:
                letter = input("{} already guessed.\nGuess a letter: ".format(letter))

        guessed.append(letter.lower())
        c = 0
        for index in range(0, len(word)):
            char = word[index]
            if char == letter:
                gw[index] = char
                c += 1

        if c == 0:
            print("Your letter did not appear in the word")
            wrong += 1
            print("You have {} more wrong guesses".format(6-wrong))
        else:
            print("{} appeared in the word {} times".format(letter, c))
            print(" ".join(gw))

    if '_' not in gw:
        print("---Congrats, you win! You guessed the word {}---".format(word))
    else:
        print("The word was {}".format(word))
        print("------You lost------")


while 1:
    game();
