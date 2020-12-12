from whoosh.index import create_in
from whoosh.fields import *
from whoosh import index
import os.path
from whoosh.qparser import QueryParser
import sys
import os
from parseJSON import doingJSON, listJson
    
class whooshFinder:
    def __init__(self):
        if not os.path.exists("indexdir"):
            os.mkdir("indexdir")
        global schema
        global ix
        schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT(stored = True))
        ix = index.create_in("indexdir", schema)

        writer = ix.writer()
        temp = ""
        doingsplit = listJson("test_math.json")
        for i in doingsplit:
            writer.add_document(content=i["patterns"])
        writer.commit()
        

    def whooshFind(self, check):
        endpoint = []
        scores = []
        total = 0.0
        if check != "":
            with ix.searcher() as searcher:
                query = QueryParser("content", ix.schema).parse(check)
                results = searcher.search(query)
        
                for r in results:
                    endpoint.append(r['content'].replace('\n', ''))
                    #print (r, r.score)
                    scores.append(r.score)
                    total += r.score
                    # Was this results object created with terms=True?
                    #if results.has_matched_terms():
                        # What terms matched in the results?
                        #print(results.matched_terms())
                if len(endpoint) == 0:
                    return ["No Sentences Found."]
                average = (float)(total/len(endpoint))
                # What terms matched in each hit?
        together = []
        for i in range(len(endpoint)):
            if scores[i] > average:
                together = together + endpoint[i].split(".")
                together.remove('')
        return endpoint[0]

if __name__ == "__main__":
    find = whooshFinder()
    while True:
        check = input ("Enter keywords: ")
        if check == 'stop':
            break
        print(find.whooshFind(check))
        #print(listJson("test_math.json"))
