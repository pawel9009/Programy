WIN = 21
lista =[]
class TreeNode:
    def __init__(self,value):
        self.children=[]
        self.value= value
        self.parent=None
        self.owner=0
        self.depth=0
        self.num=[1,2,3]
        self.vin=0

    def add_child(self,child):
        child.parent = self
        child.value+=self.value
        self.children.append(child)
        child.depth=self.depth+1
        lista.append(child)

    def take_child(self):
        return self.children

    def tak(self,dep):
        if self.depth==dep:
            add(self)


    def get_level(self):
        level = 0
        p = self.parent
        while p:
            level+=1
            self.owner+=1
            p=p.parent
        return level

    def print_tree(self):
        # print("antagonista"if self.owner%2==0 else"protagonista")
        if(self.value==WIN):
            print("Wygrana", "Protagonista"if self.get_level()%2==0 else "Antagonista")
        elif(self.value>WIN):
            print("przegrana")

        print("   "*self.depth, f"głębokość - {self.depth}, value {self.value} - ","P"if self.get_level()%2==0 else "A")
        if self.children:
            for child in self.children:
                child.print_tree()

        # for child in root.children:
        #     for x in range(len(child.num)):
        #         child.add_child(TreeNode(child.num[x]))
        # return root

    # def rek(self,dept):
    #     for node in self.children:
    #         if self.depth > 5:
    #             return
    #         else:
    #             node.tak(dept)
    #             return self.rek(dept+1)
# def rek(children):
#     for x in children:
#         print(x.value)
#     for node in children:
#         if node.value>WIN and node.vin ==0:
#             node.vin=1
#         elif node.value<WIN and node.vin==0:
#             node.add_child(TreeNode(4))
#             node.add_child(TreeNode(5))
#             node.add_child(TreeNode(6))
#             return add(node.children)
def add(root):
    for x in range(3):
        root.add_child(TreeNode(root.num[x]))
    return root

def build_product_tree():
    root = TreeNode(0)
    root.tak(0)
    tak=1
    flaga=True
    while flaga:
        for x in lista:
            if x.depth == tak:
                add(x)

        tak+=1
        if tak>1:
            flaga=False

    print(len(lista))

    # for node in new:
    #     add(node)
    #     cos = node.children
    #     for x in cos:
    #         x.tak()


    # while x<7:
    #     for child in new:
    #         new = add(child)
    #     new=new.children
    #     x+=1


    # for child in new:
    #     new=add(child)
    #     for c in new.children:
    #         old = add(c)
    #         for a in old.children:
    #             old = add(a)
    return root


root = build_product_tree()
root.print_tree()
print(len(lista))