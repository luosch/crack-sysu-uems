from cracker import Cracker
import getpass
import time

HEADER = '\033[95m'                                                        
OKBLUE = '\033[94m'                                                        
OKGREEN = '\033[92m'                                                       
WARNING = '\033[93m'                                                       
FAIL = '\033[91m'                                                          
ENDC = '\033[0m' 
UNDERLINE = '\33[4m'

if __name__ == "__main__":
    print(HEADER + "CRACK SYSU UEMS v0.1.0" + ENDC)
    print(HEADER + "Created by Sicheng Luo, SS@SYSU, 2015.09.11" + ENDC)
    print(HEADER + "Check source code via " + UNDERLINE + "https://github.com/luosch/crack-sysu-uems" + ENDC)
    print(HEADER + "If any suggestion, contact me via " + UNDERLINE + "me@lsich.com\n" + ENDC)

    user = input(WARNING + "account: " + ENDC)
    password = getpass.getpass(WARNING + "password: " + ENDC)

    # let the hacking begin
    iCracker = Cracker(user, password)

    isLogin = False
    while not isLogin:
        for i in range(1, 6):
            print(WARNING + "try to login, attempt times: %d" % i + ENDC)
            if iCracker.login():
                isLogin = True
                break

        if not isLogin:
            print(FAIL + "fail to login, please reset your information" + ENDC)
            user = input(WARNING + "account: " + ENDC)
            password = getpass.getpass(WARNING + "password: " + ENDC)
            iCracker.user = user
            iCracker.password = password

        else:
            print(OKBLUE + "let the hacking begin")

    totalNumbers = int(input(WARNING + "how many classes do you want: " + ENDC))
    courseList = []
    print(WARNING + "input %d courseID, they should look like '62000070151001'" % totalNumbers)
    for i in range(0, totalNumbers):
        courseList.append(input(WARNING + "courseID: " + ENDC))
    
    print(OKBLUE + "let the hacking begin" + ENDC)

    try_time = 1
    while True:
        print(WARNING + "\ntry %d time :)" % try_time + ENDC)
        try_time += 1
        for courseID in courseList:
            print(WARNING + "Select course %s" % courseID)
            iCracker.selectCourse(courseID)
            time.sleep(4)




