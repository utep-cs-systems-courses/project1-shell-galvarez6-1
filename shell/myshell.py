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
    #test to see if split works
    #print(command[0])
    #if the user wants to terminte the shell they can type the command exit
    #to break the while loop
    if command[0] == "exit":
        print('\n'+'\033[1m' + "Leaving Shell..")
        break

    #if the user types cd to change directory
    elif command[0] == "cd":
        #if directory not there return an Error
        #else if append command[1] to current working directory
        #path_to =  os.getcwd()+command[1]
        #then change director using
        #os.chdir("/Users/gillie/Documents/fallOS")


##############################
    #use path to look for file
    #path = os.environ["PATH"]
    #test
    #print(path)
##############################

##############################
    #get the pid of the current process
    pid = os.getpid()
    #create a child process
    rc = os.fork()
    #if the fork faild return return the pid of the
    #parent with an encoded string with %d and .encode()
    #pid greater than 0 represents the parent
    if rc < 0:
        os.write(2, ("forkfailed, pid of failed %d: " % rc).encode())
        #exit(1) means there was a problem and the scritp is exiting
        sys.exit(1)
    #if the pid returns 0 then the fork was successful in
    #creating a child process
    #elif is pythons else if
    elif rc == 0:
        #os.write(1, ("I am child.  My pid==%d.  Parent's pid=%d\n" % (os.getpid(), pid)).encode())
        #from p3-exec you execute commands in the child
        args_from_shell = command
        for dir in re.split(":", os.environ['PATH']): # try each directory in the path
            program = "%s/%s" % (dir, args_from_shell[0])
            os.write(1, ("Child:  ...trying to exec %s\n" % program).encode())
            try:
                os.execve(program, args_from_shell, os.environ) # try to exec program
            except FileNotFoundError:             # ...expected
                pass                              # ...fail quietly

        os.write(2, ("Child:    Could not exec %s\n" % args_from_shell[0]).encode())
        sys.exit(1)
    #return the pid of the parent
    else:
        #os.write(1, ("I am parent.  My pid=%d.  Child's pid=%d\n" % (pid, rc)).encode())
        #make the parent wait for the child process to die
        os.wait()
##############################
