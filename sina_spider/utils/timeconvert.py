
month = (
            'Janurary','February',
            'March' ,
            'April' ,
            'May' ,
            'June' ,
            'July' ,
            'August',
            'September' ,
            'October' ,
            'November',
            'December' 
        )


monthdict = { k[:3]:str(i+1) for i, k in enumerate(month) }

def utc2datetime(utc):
    '''
    @param: utctime: like 'Sun Oct 30 00:00:16 +0800 2016'  \n
    @return: datetime: like '2016-10-30 00:00:16'
    '''
    utc = utc.split(' ')
    datetime = '-'.join((utc[-1],monthdict[utc[1]],utc[2]))+' '+utc[3]
    return datetime
    

if __name__ == '__main__':
    a = utc2datetime('Sun Oct 30 00:00:16 +0800 2016')
    print(a)

