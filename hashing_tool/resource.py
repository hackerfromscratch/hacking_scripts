#!/usr/bin/python3.7
import hashlib
import random

class hashMod():
    def hash_text(text,methode):
        hash_hash = hashlib.new(methode)
        text = text.encode("utf_8")
        hash_hash.update(text)
        hash_hash.digest()
        return hash_hash.hexdigest()

    def brute_force(wd, hash_to_guess, methode):
        try:
            directory = "wordlists/"
            
            wd = directory + wd
            with open (wd, "r") as wd_list:
                wd_list = wd_list.read()                
                tab = wd_list.split('\n')
        except Exception as e:
            print(e)
            print("words list not found")
            pass
        i = 0
        while i != (len(tab)+1):
            hash_test = hashMod.hash_text(tab[i],methode)
            if hash_to_guess == hash_test:
                print("found it !")
                print(f"the hash is equivalent to the word : {tab[i]}")
                print(i)
                break

            i += 1
                    


