from tkinter import *
from Browser import *

def layout(txt,W):
    display_list=[]
    H,V=13,18
    c_x,c_y=H,V
    for c in txt:
        display_list.append((c_x,c_y,c))
        c_x+=H
        if c_x>=W-H:
            c_y+=V
            c_x=H 
            
    return display_list

class Browser:
    def __init__(self):
        self.windows = Tk()
        self.H, self.W =800, 800
        self.canvas=Canvas(
            self.windows,
            width=self.W,
            height=self.H 
        )
        self.canvas.pack()
        self.scroll=0
        self.display_list=[]
        self.windows.bind("<Down>", self.scrolldown)
        self.windows.bind("<Up>",self.scrollup)

    def scrollup(self,e):
        self.scroll +=100
        self.draw()

    def scrolldown(self,e):
        self.scroll-=100
        self.draw()
        

    def draw(self):
        self.canvas.delete(ALL)
        for x,y,c in self.display_list:
            self.canvas.create_text(x,y+self.scroll,text=c)

    def load(self,url):
        body =url.request()
        txt = self.lex(body)
        self.display_list=layout(txt,self.W)
        self.draw()

    def lex(self,body):
        #parse the content respond by url
        txt = ''
        in_tag=FALSE
        for c in body:
            if c=="<":
                in_tag=True
            elif c==">":
                in_tag=False
            elif not in_tag:
                txt+=c
        return txt




if __name__ =="__main__":
    import sys
    Browser().load(URL(sys.argv[1]))
    mainloop()


