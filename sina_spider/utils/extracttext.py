from re import findall

def extracttext(string):
    start_ptr= 0
    end_ptr = 0
    num = 0
    loc = 0
    detected = False
    for i in string:
        if i == '<':
            if not detected:
                start_ptr = loc
            detected = True
            num+=1
        elif i == '>':
            num-=1
            end_ptr = loc
        if num == 0 and detected: 
            return extracttext(' '.join((string[:start_ptr],string[end_ptr+1:])))
        loc+=1

    return string
 


def main():
    print(extracttext('<<sadad 递四方】【>=]>[]速ag<rha递>'))
    print(extracttext('asasfg'))
    print(extracttext('<>asasfg'))
    print(extracttext('asasfg<>'))

if __name__ == '__main__':
    main()