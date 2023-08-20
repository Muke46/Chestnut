from fpdf import FPDF
import json

debugBorder=0

settings={
    "debugBorder": 0,
    "ch": 8,
    "Lmargin": 45,
    "Rmargin": 45,
    "Tmargin": 30,
    "txt_dim": 9.5,
    "h1_dim" : 14,
    "font"   : "LaTex",
    "fontB"  : "LaTex",
    "fontI"  : "LaTex",
    "resourcesFolder": r".\Resources",
    "itemizeMarks": ['•']
}

class renderer(FPDF):
    def __init__(self, settings):
        super().__init__()
        self.settings = settings
        settings['pageWidth']= 210 - settings['Lmargin'] - settings['Rmargin']
        self.headersN=[]
        self.figN=0
        self.tableN=0

        self.set_margins(left=settings['Lmargin'], top=settings['Tmargin'], right=settings['Rmargin'])
        self.add_page()

    def Rheader(self,item):
        #load settings from dictionary or default values
        h = item["h"] if "h" in item else self.settings['ch']
        w = item["w"] if "w" in item else 0
        border = item["border"] if "border" in item else self.settings['debugBorder']
        fontSize = item["fontSize"] if "fontSize" in item else self.settings['h1_dim']
        depth = item["depth"] if "depth" in item else None
        align = item["align"] if "align" in item else 'L'

        #get the text from the item
        txt=item['text']

        #if depth is specified, writhe the chapter number
        if depth != None:
            #If it's at the same level of the previous one, increase by one
            if len(self.headersN)== depth: 
                self.headersN[-1]+=1
            else:
                #if it's a new entry at this depth, add a counter in headersN
                if len(self.headersN) < depth:
                    self.headersN.append(0)
                #if the previous level was deeper, cut headersN and increase the now last value
                if len(self.headersN) > depth: #go back a level
                    self.headersN = self.headersN[0:(depth-1)]
                    self.headersN[-1]+=1
                    self.figN=0
                    self.tableN=0

            #build the strings of the numbers (ex 1.1.2.1)
            numbers=''
            for i, n in enumerate(self.headersN):
                numbers += str(self.headersN[i]+1)+'.'
            
            #add the numbers to the text
            txt = numbers + ' ' + txt

            #compute the size, it has a linear decrease which is capped
            #TODO: parametersize the size in the settings
            if depth<5: fontSize=fontSize-depth
            else: fontSize=10
            
        #set the font to bold and as bis as the self.settings
        #TODO parameterize the font
        self.set_font(self.settings['fontB'], '', fontSize)

        #draw the header
        self.cell(w=w, h=h, txt=txt, border=border,ln=1, align=align, fill = False, link = '')

    
    def Rtext(self, item):
        #load settings from dictionary or default values
        h = item["h"] if "h" in item else self.settings['ch']/2 #TODO add new parameter
        w = item["w"] if "w" in item else 0 #equivalent to fill page
        border = item["border"] if "border" in item else self.settings['debugBorder']
        fontSize = item["fontSize"] if "fontSize" in item else self.settings['txt_dim']
        align = item["align"] if "align" in item else 'J'

        #get the text from the item
        txt=item['text']

        #set the font to bold and as bis as the self.settings
        self.set_font(self.settings['font'], '', fontSize)

        #draw the header
        self.multi_cell(w=w, h=h, txt=txt, border=border, align=align, fill = False)

    
    def Ritemize(self,items, depth=0):
        #elements, w=5, h=None, txt='', border=None, align='J', fill=False, link='', spacing=0, mark='•'
        w = item["w"] if "w" in item else 5
        h = item["h"] if "h" in item else self.settings['ch']/2
        border = item["border"] if "border" in item else self.settings['debugBorder']

        #choose the simbol
        #TODO alternative styles, like numbers, letters, etc
        mark = settings['itemizeMarks'][depth] if len(settings['itemizeMarks'])>depth else settings['itemizeMarks'][-1]

        for i, el in enumerate(items):
            #add a mark unless the item is another itemize
            if el['type'] != "itemize": self.cell(w=w, h=h, txt=mark, align='C', border=border, ln=0)
            else:self.cell(w=w, h=h, txt='', border=border, ln=0)
            #render the item
            self.renderItem(el)
    
    def command(self, cmd):
        match cmd["command"]:
            case "vspace":
                self.ln(cmd["amount"])

    def Rimage(self, item):
        #TODO check if the image+caption fits to avoid split them
        #Render on a second pdf, check the height
        #check if the image can fit in the page
        #if not, new page
        availableSpace = item["availableSpace"] if "availableSpace" in item else self.settings["pageWidth"]
        w = item["w"] if "w" in item else 0
        h = item["h"] if "h" in item else 0
        align = item["align"] if "align" in item else 'L'

        if align=="C" and w!=0:
            self.x=self.x+availableSpace/2-w/2
        self.image(name=settings["resourcesFolder"]+item["path"], w=w)
        self.x=self.settings["Lmargin"]
        #caption
        if "caption" in item:
            caption = f'Figure {self.figN+1}: {item["caption"]}'
            #for i, n in enumerate(self.headersN):
            #    caption += str(self.headersN[i]+1)+'.'
            #caption+=str(self.figN)
            self.figN+=1
            el={"text": caption, "align":'C'}
            self.Rtext(el)

    def Rgrid(self, item):
        rows=item['size'][0]
        coloumns=item['size'][1]
        w=settings["pageWidth"]/coloumns

        for row in item["elements"]:
            tmp=renderer(self.settings)
            tmp.add_font('LaTeX', '', ".\Fonts\cmunrm.ttf", uni=True)
            heights=[]
            for el in row:
                ybefore = tmp.get_y()
                el["w"]=w
                tmp.renderItem(el)
                heights.append(tmp.get_y()-ybefore)
            
            y=self.y
            for elN, el in enumerate(row):
                x=self.settings["Lmargin"]+elN*w
                y1=y+max(heights)/2-heights[elN]/2
                self.x=x
                self.y=y1
                el["w"]=w
                el["availableSpace"]=self.settings["pageWidth"]/2
                self.renderItem(el) 
                self.rect(x, y, w, max(heights))
        tmp.output(f'./tmp.pdf', 'F')

    def renderItem(self, item):
        match item['type']:
            case "cmd":
                self.command(item)
            case "header":
                self.Rheader(item)
            case "text":
                self.Rtext(item)
            case "itemize":
                self.Ritemize(items=item['elements'])
            case "image":
                self.Rimage(item)
            case "grid":
                self.Rgrid(item)
            case _:
                print(f"Warnings, command {item['type']} not recognized")
    

pdf = renderer(settings)
pdf.add_font('LaTeX', '', ".\Fonts\cmunrm.ttf", uni=True)

def itemize(pdf, elemetsList):
    pdf.set_font('LaTeX', '', 9.5)
    for el in elemetsList:
        pdf.cell(w=10, h=8, txt='•', border=debugBorder, ln=0)
        pdf.cell(w=0, h=8, txt=el['text'], border=debugBorder, ln=1)


sourceFile=r".\test.json"
destFile=r".\out.pdf"
resourcesFolder=r".\Resources"

source = json.load(open(sourceFile, "r"))



for i, item in source.items():
    pdf.renderItem(item)

pdf.output(f'./output.pdf', 'F')