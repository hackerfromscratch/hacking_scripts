#!/usr/bin/python3.7
import resource

init = 0

while True:
    print("chose an option : ")
    print("option 1 : hash a text")
    print("option 2 : brute force to find a hash")
    init = int(input("> "))
    while init == 1:
        text_to_hash = input("enter the text you want to hash : ")
        hash_type = input("enter the hash methode you want to use : ")
        if text_to_hash != '' and hash_type != '' :            
            the_hash = resource.hashMod.hash_text(text_to_hash ,hash_type)
            print(the_hash)
            
            init = 0
    while init == 2:
        wd = input("name of the word list : ")
        hash_to_guess = input("hash to guess : ")
        methode = input("hash methode used : ")
        print("->__>__>__>__>")
        print("->__>__>__>__>")
        print("runnig...")
        resource.hashMod.brute_force(wd,hash_to_guess,methode)
        init = 0
    break

