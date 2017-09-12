class UserSet(object):
    _user_set = set()

    def __init__(self):
        self.add_user(username , password)  # add your account information
       

    @property
    def user_set(self):
        return sorted(self._user_set)

    def add_user(self, user, password):
        self._user_set.add((str(user), str(password)))



if __name__ == '__main__':
    print(UserSet().user_set)
