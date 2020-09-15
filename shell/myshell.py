import os
import re
import sys

#see if we can use the command prompt from bash shell
#call the prompt string from the shell using os.environ['PS1']
#where ps1 is the prompt string
#(re-worded) retrieve the prompt string from the parent process (shell)
#the prompt string for the python interpretor is '>>>'
#and then if there is no prompt string (null, nothing)
#set up a default prompt string, Python uses None to to define so
# we can use it to compare
#gave KeyError which means the key doesnt exist so we can use a try catch
#in python it is try except
try:
    cPrompt = os.environ['PS1']
except KeyError:
    cPrompt = "command$: "


def pipeCheck(list):
    a = '|'
    if a in list:
        return True
    else:
        return False

#we need an infinte loop to keep the shell running and allow the user to
#input commands, 1 means true
while 1:

    #use an indicator to show the shell is running and the user
    #can input commands

    #input takes in user input returns a list of the inputs for each letter
    command =  input('\033[1m' + cPrompt + '\033[0m' + "")
    #take the string the user entered and parse each word by white space
    command = command.split()
    #print(command)
    #test to see if split works
    #print(command[0])
    #if the user wants to terminte the shell they can type the command exit
    #to break the while loop
    if command[0] == "exit":
        print('\n'+'\033[1m' + "Leaving Shell..")
        print('\033[1m' + "Bye!" + '\n')
        break

    #if the user types cd to change directory
    elif command[0] == "cd":
        #check if the directory exist using isdir method of os
        # the path wanting to move to is the second one in the user input commands
        try:
            if os.path.isdir( os.getcwd() + '/' + command[1]):
                #else if append command[1] to current working directory
                #then change director using
                #os.chdir("name of the directory")
                os.chdir( os.getcwd() + '/' + command[1])
                print("\n " + '\033[94m' + '\033[1m' + "**Changed directory to: " + '\033[0m')
                print('\033[1m' + os.getcwd()+ '\033[0m')
            else:
                print('\033[1m' + "Directory doesn't exist" + '\033[0m')
        except:
            print(" input directory name!")

    elif command[0] == "pwd":
        #print the current working Directory
        print('\033[1m' + os.getcwd() + '\033[0m')

    #print the files and folders in a current Directory
    #in python os.listdir returns the names of files and folders

    elif (command[0] == "ls") and  (not pipeCheck(command)):
        #use a for loop to print each item in the currenet Directory
        print("\n " + '\033[1m' + "**files and folders**" + '\033[0m')
        for i in os.listdir():
            #print(i + "\t")
            #to help distinguish between a file and folder a folder is blue
            #like in emacs
            if os.path.isdir(os.getcwd() + '/' + i):
                print('\033[94m' + i + '\033[0m')
            else:
                print(i)
        print("\n")

    elif pipeCheck(command):
        #print("yes")



##############################

##execute
    #get the pid of the current process
    pid = os.getpid()
    #create a child process
    rc = os.fork()
    #if the fork faild return return the pid of the
    #parent with an encoded string with %d and .encode()
    #pid greater than 0 represents the parent
    if rc < 0:
        #os.write(2, ("forkfailed, pid of failed %d: " % rc).encode())
        #exit(1) means there was a problem and the scritp is exiting
        sys.exit(1)
    #if the pid returns 0 then the fork was successful in
    #creating a child process
    #elif is pythons else if
    elif rc == 0:
        #os.write(1, ("I am child.  My pid==%d.  Parent's pid=%d\n" % (os.getpid(), pid)).encode())
        #from p3-exec you execute commands in the child
        args_from_shell = command
        #to find the file to execute we travel through path
        #PATH locations are seperated by : so we parse the PATH string by ':' and not '/'
        for dir in re.split(":", os.environ['PATH']): # try each directory in the path
            program = "%s/%s" % (dir, args_from_shell[0])
            #os.write(1, ("Child:  ...trying to exec %s\n" % program).encode())
            try:
                os.execve(program, args_from_shell, os.environ) # try to exec program
            except FileNotFoundError:             # ...expected
                pass                              # ...fail quietly

        #os.write(2, ("Child:    Could not exec %s\n" % args_from_shell[0]).encode())
        sys.exit(1)
    #return the pid of the parent
    else:
        #os.write(1, ("I am parent.  My pid=%d.  Child's pid=%d\n" % (pid, rc)).encode())
        #make the parent wait for the child process to die
        os.wait()
##############################

##############################################
#there are two kinds of redirects
#inward and outward
#outward uses >
#while inward uses <
#we need to parse the string the users input to find the '>' '<'
#to determine what type of indirect to user
##############################################

##############################################
#pipes: the output of one file is the input of another
#this comes from what i understood in programming langues and software
#using os.pipes() in python
#this method returns file descriptors for read and write
r,w = os.pipe()
