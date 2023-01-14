from load_json import*


def requirement1():
    global db, data_store
    key_word = input("Please enter keyword that you want to search for: ")
    key_word = key_word.split()
    keyWord = ""
    for i in key_word:
        keyWord = keyWord + "\"" + i + "\""
    key_id = data_store.find({"$text": {"$search":keyWord}}, {"score": {"$meta": "textScore"}}).sort([("score", {"$meta": "textScore"})])
    for i in key_id:
        print(i["id"] + "   " + i["title"] + "   " + i["year"] + "   " + i["venue"])
    user_inp = input("Please enter id of an article that you want to select: ")
    user_input = "\"" + user_inp + "\""
    art_id = data_store.find({"$text": {"$search": user_input}})
    for i in art_id:
        if (i["id"] == user_inp):
            print("More Information about selected song.")
            print(i)
        else:
            print("Selected song is referenced by this article.")
            print(i["id"])
            print(i["title"])
            print(str(i["year"]))
    return

def requirement2():
    global db, data_store
    key_word = input("Please enter keyword that you want to search for: ")
    trial = data_store.aggregate([{"$unwind":{"path":"$authors"}}, {"$match":{"authors":{"$regex": key_word, "$options": "i"}}} , {"$group": {"_id":"$authors","cnt":{"$sum":1}}}])
    for i in trial:
        print(str(i["cnt"]) + "  " +i["_id"])
    user_input = input("Please enter full name of author that you want to search for: ")
    aut = data_store.find({"authors": user_input}).sort([("year",-1)])
    for i in aut:
        cnt = str(i["year"])
        print(cnt + "   " + i["title"] + "   " + i["venue"] )
    return

def requirement3():
    global db, data_store
    while True:
        try:
            user_input = int(input("Please enter number of venue list you want to get: "))
            break
        except:
            print("Please enter integer value only.")

    venue_info = data_store.aggregate([{"$group": {"_id": "$venue", "id_cnt":{"$sum":1}, "ID": {"$addToSet": "$id"}}}])
    venue_final = {}
    venue_ref = {}
    for i in venue_info:
        if (i["_id"] == ""):    # this is preventing the code to count empty venues
            continue
        cnt = 0 
        lit = []
        for ii in i["ID"]:
             trial = data_store.count_documents({"references":ii})
             cnt = cnt + trial
        lit.append(cnt)
        
        x = int(i["id_cnt"]) + 1
        lit.append(int(i["id_cnt"]))
        venue_final[i["_id"]] = lit 
        venue_ref[i["_id"]] = cnt

    temp_dict = sorted(venue_ref.items(), key = lambda x:x[1], reverse=True)
    prim_dict = dict(temp_dict)
    count = 1
    for key in prim_dict:
        string = venue_final[key]
        print("Number of articles Reference: " + str(string[0]) + "; Number of articles:  " + str(string[1]) + "; venue name: " + key)
        if (count == user_input):
            break
        count = count + 1 
    return 
    
def requirement4():
    global db, data_store
    unique_id = input("Please enter id: ")
    while True:
        uniq_id = data_store.count_documents({"id": unique_id})
        if (uniq_id == 0):
            break
        else:
            unique_id = input("ENTERED ID IS NOT UNIQUE:- Please enter id: ")
    tit = input("Please enter title: ")
    while True:
        try:
            num_author = int(input("Please enter how many authors has contributed to this article: "))
            break
        except:
            print("Please enter integer value only.")
    aut = []
    for i in range(num_author):
        name_author = input("Please enter author name: ")
        aut.append(name_author)
    while True:
        try:
            yea = int(input("Please enter year: "))
            break
        except:
            print("Please enter integer value only.")
    yea = str(yea)
    abst = ""
    venu = ""
    ref = []
    citat = 0
    data_store.insert_one({"abstract":abst, "authors": aut, "n_citation": citat, "references":ref, "title":tit, "venue":venu, "year":yea, "id":unique_id})
    a = data_store.find({"id":unique_id})
    for i in a:
        print(i)
    return

def call_function():
    global db, data_store
    keep_going = True
    while (keep_going == True):
        while True:
            try:
                user_input = int(input("Please select one of the following options: 1) Search for articles, 2) Search for authors, 3) List the venues, 4) Add an article or 0) to go back to main menu adn end program. "))
                break
            except:
                print("Please enter integer value only.")
        if (user_input == 1):
            requirement1()
        elif (user_input == 2):
            requirement2()
        elif (user_input == 3):
            requirement3()
        elif (user_input == 4):
            requirement4()
        elif (user_input == 0):
            return
        else:
            print("No options for this input. Try again !!!")
    return 

def main():
    global db, data_store
    db = json_call()
    data_store = db["dblp"]
    call_function()
    return 

if __name__ == "__main__":
    main()
