from whoosh.index import create_in
from whoosh.fields import *
from whoosh import index
import os.path
from whoosh.qparser import QueryParser
import sys
import os
from parseJSON import doingJSON, listJson, doingTxt
    
class whooshFinder:
    def __init__(self, filename):
        if not os.path.exists("indexdir"):
            os.mkdir("indexdir")
        global schema
        global ix
        schema = Schema(title=TEXT(stored=True), content=TEXT(stored = True))
        ix = index.create_in("indexdir", schema)

        writer = ix.writer()
        #doingsplit = listJson(filename)
        doingsplit = doingTxt(filename)
        global lines
        lines = {}
        for i in doingsplit:
            #writer.add
            temp = ""
            words = i["patterns"].split()
            tag = ""
            inside = ""
            for j in words:
                temp += j
                if temp[-1] == '.':
                    inside += temp
                    temp = ""
                    if tag != "":
                        writer.add_document(title=tag, content=inside)
                        lines[tag] = inside
                        inside = ""
                        tag = ""
                    continue
                if temp[-1] == '?':
                    tag = temp
                    temp = ""
                temp += " "
                
        writer.commit()
        

    def whooshFind(self, check):
        endpoint = ""
        scores = []
        total = 0.0
        if check != "":
            with ix.searcher() as searcher:
                query = QueryParser("title", ix.schema).parse(check)
                results = searcher.search(query)
        
                for r in results:
                    endpoint += lines[r["title"]].replace('\n', '')
                    #print (r, r.score
                if len(endpoint) == 0:
                    return ["No Sentences Found."]
                # What terms matched in each hit?
        return endpoint

if __name__ == "__main__":
    find = whooshFinder("woosh_data.txt")
    while True:
        check = input ("Enter keywords: ")
        if check == 'stop':
            break
        print(find.whooshFind(check))
        #print(listJson("test_math.json"))
