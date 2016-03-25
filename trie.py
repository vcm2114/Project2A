# -*- coding: utf-8 -*-

class trie:
    """
        class trie defined by:
            - edge      : int for the edge's value
            - obj       : array of int for the objects in the node
            - attr      : array of int for the attributes in the node
            - children  : array of trie linked from down to the node
    """

    def __init__(self,edges=-1,objects=[],attributes=[],children=[]):
        self.edge=edges
        self.obj=objects
        self.attr=attributes
        self.children=children

    def __str__(self):
        return "--------------\nedge = "+str(self.edge)+"\nobj = "+str(self.obj)+"\nattr = "+str(self.attr)+"\nchildren = "+str(self.children)+"\n--------------\n"

    def add_attr(self,att):
        self.attr.append(att)

    def insert_trie(self,i,obj):
        # root case
        if len(obj)==0:
            self.add_attr(i)

        # if not root
        else:
            # if none children
            if len(self.children)==0:
                # add child
                self.children.append(trie(obj[0],self.obj+[obj[0]],[],[]))
                #if not last obj
                if len(obj)>1:
                    # recursive call
                    self.children[0].insert_trie(i,obj[1:])
                #if last obj
                else:
                    self.children[0].add_attr(i)

            # if children
            else:
                nc=len(self.children)
                j=0
                # find right index for children
                while j<nc and self.children[j].edge<obj[0]:
                    j+=1
                # if end of the list
                if j == nc:
                    self.children.append(trie(obj[0],self.obj+[obj[0]],[],[]))
                    if len(obj)>1:
                        self.children[j].insert_trie(i,obj[1:])
                    # if last obj
                    else:
                        self.children[j].add_attr(i)
                # if child already exists
                elif obj[0]==self.children[j].edge:
                    #if not last obj
                    if len(obj)>1:
                        self.children[j].insert_trie(i,obj[1:])
                    #if last obj
                    else:
                        self.children[j].add_attr(i)
                # if child does not exist
                else:
                    # add child
                    self.children.insert(j,trie(obj[0],self.obj+[obj[0]],[],[]))
                    # if not last obj
                    if len(obj)>1:
                        self.children[j].insert_trie(i,obj[1:])
                    # if last obj
                    else:
                        self.children[j].add_attr(i)

    def equivalence(self):
        list=[]
        # if node wih equivalence class
        for e in self.children:
            list+=e.equivalence()
        if len(self.attr)>0:
            return list+[(self.obj,self.attr)]
        else:
            return list



'''
t=trie()

print(t)
t.insert_trie('1',['3','7'])
t.insert_trie('4',['3','7'])
t.insert_trie('3',['3','5'])
t.insert_trie('10',['3','6'])
t.insert_trie('5',['1'])
t.insert_trie('7',['2','3'])
print(t.children[0])
print(t.children[1].children[0])
print(t.children[2].children[0])
print(t.children[2].children[1])
print(t.children[2].children[2])
l=t.equivalence()
print(l)'''
