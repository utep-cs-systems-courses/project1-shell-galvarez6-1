import os
import re
import sys

#we need an infinte loop to keep the shell running and allow the user to
#input commands, 1 means true
while 1:
    #use an indicator to show the shell is running and the user
    #can input commands

    #input takes in user input returns a list of the inputs for each letter
    command =  input("$ ")
    #take the string the user entered and parse each word by white space
    command = command.split()


    path = os.environ["PATH"]
    print(command[0])
    print(path)
    #if the user wants to terminte the shell they can type the command exit
    #to break the while loop
    if command[0] == "exit":
        print('\n'+'\033[1m' + "Leaving Shell..")
        break
