"""
Explain : 
    rdb is a No-SQL db like redis for save key/val pair on database with
    expiration time, it used for caching.

Data Structure:
    {
        "a" : ValObj,
        "b" : ValObj,
        "c" : ValObj,
        ...
        "A" : ValObj,
        "B" : ValObj,
        "C" : ValObj,
        ...
    }

    ValObj : 
        - key
        - value
        - data
        - exp

    
"""



from datetime import timedelta, datetime
from string import ascii_lowercase, ascii_uppercase
import pickle

class ValObj:
    """
        ValObject Where the data is stored with its key and val.
        Attrs : 
            - key [ data key name]
            - val [data val, any type of data]
            - exp [the time of epiration ]
    """

    next = None

    def __init__(self, key, val, exp) -> None:
        self.key = key
        self.val = val
        # set the expiration time of the object to 1 hr by default
        self.exp = (datetime.now() + timedelta(seconds=exp or  60 * 60)).timestamp()

    def __repr__(self) -> str:
        return f"ValObj(key={self.key}, val={self.val}, epx_mins={self.exp})"


class cache :

    def __init__(self) : 
        
        try :
            with open('temp.bin','rb') as binary_file :
                self.__db_core = pickle.load(binary_file)
                binary_file.close()
        except FileNotFoundError:
            self.__db_core = {
                i : None
                for i in [j for j in ascii_lowercase+ascii_uppercase]
            }
            

    def __update_binary (self):
        # print('writing data to binary')
        with open ('temp.bin', 'wb') as binary_file :
            pickle.dump(self.__db_core, binary_file)
            binary_file.close()  

            
        
    def set (self, key, val,exp=None):
        """
            Set element on cache
                Attrs :
                    - key [String Value]
                    - val [save data as]
                    - exp [the total secnods ] 
        """
        router = str(key)[0]
        if self.__db_core[router] is None :
            self.__db_core[router] = ValObj(
                key=key,
                val=val,
                exp=exp
            )
        else:
            val_obj:ValObj = self.__db_core[router]
            while val_obj : 
                if val_obj.next == None:
                    val_obj.next = ValObj(
                        key=key,
                        val=val,
                        exp=exp
                    )
                    break
                val_obj = val_obj.next
        self.__update_binary()
        

    def __view(self, obj:ValObj) : 
        """
            View if not Expiration or Delete it if expired
        """
        current_time = datetime.now().timestamp()
        if current_time > obj.exp:
            self.delete(obj.key)
            return None
        return obj.val
    
    def get(self, key) : 
        """
            Get Element from cache
        """
        router = str(key)[0]
        obj_val = self.__db_core[router]
        while obj_val:
            if obj_val.key == key: 
                return self.__view(obj_val)
            obj_val = obj_val.next

    def delete (self, key) :
        """
            Delete element from cache
        """
        router = str(key)[0]
        obj_val:ValObj = self.__db_core[router]
        prevoius = None
        while obj_val:

            if obj_val.key == key: 
                if prevoius:
                    prevoius.next = obj_val.next
                else:
                    self.__db_core[router] = obj_val.next
                self.__update_binary()
                break

            prevoius = obj_val
            obj_val = obj_val.next


cache = cache()