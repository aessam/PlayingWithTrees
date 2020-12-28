from os import system

class Node():
    def __init__(self, value, parent):
        self.left = None
        self.right = None
        self.parent = parent
        self.lheight = 0
        self.rheight = 0
        self.value = value
        self.fix_heights()

    def bridth_first(self, tdarray, level):
        if level not in tdarray:
            tdarray[level] = []
        addMore = 0
        if self.parent:
            addMore = self.parent.value * 1000
        tdarray[level].append(self.value + addMore)
        if self.left:
            self.left.bridth_first(tdarray, level + 1)
        if self.right:
            self.right.bridth_first(tdarray, level + 1)

    def fix_heights(self):
        parent = self.parent
        steps = 0
        while parent:
            steps += 1
            if parent.parent:
                if parent.parent.left == parent:
                    parent.parent.lheight = max(steps, parent.parent.rheight, parent.parent.lheight)
                if parent.parent.right == parent:
                    parent.parent.rheight =  max(steps, parent.parent.rheight, parent.parent.lheight)
            parent = parent.parent

class Tree():
    def __init__(self):
        self.root = None
        self.stack = None
        self.stack = []
    
    def __generate_snapshot(self, pairs, counter):
        res = "graph ethane {"
        res += 'graph [bb="0,0,755,407"];'
        for p in pairs:
            res += f' {p[0]} -- {p[1]} [label="{p[2]}"];'
        res += "}"
        open(f"_tree{counter}.dot", "w").write(res)
        system(f"dot -Tpng _tree{counter}.dot -o tree{counter}.png")

    def go_through_all(self):
        nextItem = self.root
        navi = []
        navi.append(nextItem)
        pairs = []
        counter = 0
        while nextItem:
            nextItem = navi.pop() if len(navi) > 0 else None
            if nextItem and nextItem.left:
                navi.append(nextItem.left) 
                pairs.append((nextItem.value, nextItem.left.value, f"L {nextItem.lheight}"))
                # counter += 1
                # self.__generate_snapshot(pairs, counter)
            if nextItem and nextItem.right:
                navi.append(nextItem.right)
                pairs.append((nextItem.value, nextItem.right.value, f"R {nextItem.rheight}"))
                # counter += 1
                # self.__generate_snapshot(pairs, counter)
            # print(nextItem.value if nextItem else "nope")
        self.__generate_snapshot(pairs, counter)


    def dig_left_stack(self, purposedLeft=None):
        nextLeft = self.root
        if purposedLeft:
            nextLeft = purposedLeft
        while nextLeft:
            self.stack.append(nextLeft)
            nextLeft = nextLeft.left


    def next(self, should_reinit = False):
        if not self.stack and should_reinit:
            self.dig_left_stack()
        if len(self.stack) > 0:
            lastPopped = self.stack.pop()
            if lastPopped.right:
                self.dig_left_stack(lastPopped.right)
            return lastPopped.value
        
        
    def batch_insert(self, items):
        for i in items:
            self.insert(i)
        # items = sorted(items)
        # for i in range(len(items)):
        #     index = int(len(items)/2)
        #     self.insert(items[index])
        #     del items[index]

    def insert(self, val):
        activeNode = self.root
        while activeNode:
            if val == activeNode.value:
                raise ValueError("Node value already exist")
            elif val > activeNode.value:
                if activeNode.right:
                    activeNode = activeNode.right
                else:
                    activeNode.right = Node(val, activeNode)
                    activeNode = None
            else:
                if activeNode.left:
                    activeNode = activeNode.left
                else:
                    activeNode.left = Node(val, activeNode)
                    activeNode = None
        
        if not self.root:
            self.root = Node(val, activeNode)

tree = Tree()
tree.batch_insert([7, 3, 1, 2, 5, 6, 4, 36, 27, 26, 28, 0, 50, 75, 45])
tree.insert(460)
tree.insert(500)
tree.insert(450)
tree.insert(510)
tree.batch_insert(list(range(320, 440, 10)))
tree.batch_insert(list(range(150, 300, 10)))

tree.go_through_all()
f = tree.next(True)
while f != None:
    print(f)
    f = tree.next()
# print(tree.root.height)
# result = {}
# tree.root.bridth_first(result, 0)
# print(result)

