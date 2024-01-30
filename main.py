from tkinter import *
import tkinter.font
from Browser import *

class Browser:
    def __init__(self):
        #setting windows
        self.windows = Tk()
        global H,W
        H,W=800,800



        #setting canvas
        self.canvas=Canvas(
            self.windows,
            width=W,
            height=H 
        )
        self.canvas.pack()

        #for dispaly text content and scroll function setting
        self.scroll=0
        self.display_list=[]
        
        #monitor the action of user*(scroll down/up of browser windows)
        self.windows.bind("<Down>", self.scrolldown)
        self.windows.bind("<Up>",self.scrollup)

        #the font setting in canvas
        self.bi_times=tkinter.font.Font(
            family="Times",
            size =16,
            weight="bold",
            slant="italic"
        )

        
#function for scroll up and down
    def scrollup(self,e):
        self.scroll +=100
        self.draw()

    def scrolldown(self,e):
        self.scroll-=100
        self.draw()
        
#to display the content
    def draw(self):
        x,y =200,225
        self.canvas.delete(ALL)
        for x,y,c,f in self.display_list:
            if y >self.scroll+H:continue
            elif y+18 <self.scroll:continue
            else:
                self.canvas.create_text(x,y+self.scroll,text=c,font=f,anchor="nw")
#load the content from url and analyst the content by lex(),display content by draw()
                
    def load(self,url):

        body =url.request()
        tokens = self.lex(body)
        self.display_list=Layout(tokens).display_list
        self.draw()

    def lex(self,body):
        #parse the content respond by url
        out =[]
        buffer=''
        in_tag=FALSE
        for c in body:
            if c=="<":
                in_tag=True
                if buffer : out.append(Text(buffer))
                buffer=""

            elif c==">":
                in_tag=False
                out.append(Tag(buffer))
                buffer=""
            else:
                buffer+=c

        if not(in_tag) and buffer:
            out.append(Text(buffer))
                
        return out
    
class Text:
    def __init__(self,txt):
        self.text=txt
class Tag:
    def __init__(self,tag):
        self.tag=tag


class Layout:
    #arrange the content
    def __init__(self,tokens):
        self.display_list=[]
        global X,Y
        X,Y=13,18
        self.c_x=X
        self.c_y=Y
        self.weight='normal'
        self.style= 'roman'
        self.size = 16
        self.line =[]
        #parse the content by token
        for tok in tokens:
            self.token(tok)

        #add he base line for display
        self.flush()
            
    def token(self,tok):
        #layout the txt,use word to set the font, and if tag(filt the different size/font for txt),change the setting information
        if isinstance(tok,Text):
            for word in tok.text.split():
                print('set word')
                self.word(word) 
        elif tok.tag == "i":
            self.style = "italic"
        elif tok.tag == "/i":
            self.style = "roman"
        elif tok.tag == "b":
            self.weight = "bold"
        elif tok.tag == "/b":
            self.weight = "normal"
        elif tok.tag == "small":
            self.size -= 2
        elif tok.tag == "/small":
            self.size += 2
        elif tok.tag == "big":
            self.size += 4
        elif tok.tag == "/big":
            self.size -= 4
        elif tok.tag=='br':
            self.flush()
        elif tok.tag=='/p':
            self.flush()
            self.c_y+=Y

#to set the font
    def word(self,word):
        #the font set
        print(self.size,self.style)
        
        font = tkinter.font.Font(
            size=self.size,
            weight=self.weight,
            slant=self.style,
        )
        w = font.measure(word)
        #srire line of words with list
        self.line.append((self.c_x,word,font))

        #if full fill in line ,add an base line
        if self.c_x+W>W-X:
            self.flush()

#set the base line
    def flush(self):
        #set the place for words in lines[]
        if not self.line:return
        max_ascent= max([font.metrics("ascent")
                         for x,word,font in self.line])
        baseline=self.c_y+1.25*max_ascent
        
        for x,word,font in self.line:
            y=baseline-font.metrics("ascent")
            self.display_list.append((x,y,word,font))

        max_descent = max([font.metrics("descent")for x,word,font in self.line])

        #update the layout's X,Y and line list
        self.c_y=baseline+1.25*max_descent
        self.c_x =X
        self.line=[]





if __name__ =="__main__":
    import sys
    Browser().load(URL(sys.argv[1]))
    mainloop()

