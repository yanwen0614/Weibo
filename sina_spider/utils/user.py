from os import sep as ossep

class UserSet(object):
    _user_set = set()

    def __init__(self):
        f = open(ossep.join('.','sina_spider','utils','userlist'), encoding='UTF-8')
        for line in f.readlines():
            self.add_user(*line[:-1].rsplit(' '))  
            '''add your account information at userlist file 
            like this :
            username1 password1
            username2 password2
            '''
        

    @property
    def user_set(self):
        return sorted(self._user_set)

    def add_user(self, user, password):
        self._user_set.add((str(user), str(password)))



if __name__ == '__main__':
    print(UserSet().user_set)
