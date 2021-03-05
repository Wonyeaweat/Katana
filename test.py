import os
if __name__ == '__main__':
    os.system('solve.exe')
    res = list()
    with open('./Analyze/result.dat', 'r') as file:
        lines = file.readlines()
        for i in lines:
            res.append(list(filter(None,i.split(" "))))
    print(res)