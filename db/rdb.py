from datetime import timedelta, datetime
from string import ascii_lowercase, ascii_uppercase
import pickle

"""
pickle :
  - to write/read data from the binary file

timedelta, datetime:
  - to set the expiration as timestamps and compare it to current time.

ascii_lowercase, ascii_uppercase:
  - to set all the keys to alphatical order and setting the value to None

"""

class ValObj:
    """
        ValObject Where the data is stored with its key and val.
        Attrs : 
            - key [ data key name]
            - val [data value , any type of data]
            - exp [the time of expiration from the db]
            
    """

    next = None # our pointer

    def __init__(self, key, val, exp) -> None:
        self.key = key
        self.val = val
        self.exp = (datetime.now() + timedelta(seconds=exp or  60 * 60)).timestamp()

    def __repr__(self) -> str:
        return f"ValObj(key={self.key}, val={self.val}, epx_mins={self.exp})"

# Main Cache Model
class cache :

    def __init__(self) : 
        """
            We need to read a binary file which is called temp.bin 
            which we will save the data on it to save the data from lose.
            if we not found this binary file that mean that we didn't use 
            write any data on the file yet, so we will create our Hash Table
            and inside each key on it we will set None
        """
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
        """
            For any inserting new data we need our binary file to
            be updated
        """
        with open ('temp.bin', 'wb') as binary_file :
            pickle.dump(self.__db_core, binary_file)
            binary_file.close()  
    
    def set (self, key, val,exp=None):
        """
            set is a method to save element on cache.
            
            we detect the router which the key in the hash table 
            to know where we will save the data
            and the router is the first char in the key,
            first of all we detect the value of this router if none 
            that this value with this key is the first one so we will create our object
            and pass the data on it.

            if not none, that mean there is an object already exists on it and we need 
            to create that object and add it on the tail of the linked list which we 
            build.

                Attrs :
                    - key [String Value]
                    - val [any type of data ]
                    - exp [the total seconds to expire from db] 
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
            for check in the current ValObject, if its time expired
            we will delete it
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
            Delete element from cache and update the binary file
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

cache = cache() # init the cache model to build and make our hash table ready to use