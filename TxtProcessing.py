from fpdf import FPDF
import re

commandPattern=r'\\([^\\{}\s]+)(?=[\\{}\s]|$)' #after a backslash, terminated with a space or an opening square or curly bracket
optionsPattern = r'\[([^[\]]+)\]'   #between square brackets
argumentsPattern = r'\{([^}]*)\}'   #between curly brackets

settings={
    "Lmargin": 45,
    "Rmargin": 45,
    "Tmargin": 30,
    "txt_dim": 9.5,
    "h1_dim" : 14,
}

def header1(pdf, cmd, opt, arg):
    pdf.set_font('LaTeX', '', 14)
    pdf.cell(80, 8, arg, align='L')
    pdf.ln(8)

def writeText(pdf, textBuffer):
    pdf.set_font('LaTeX', '', 9.5)
    pdf.multi_cell(w=0,h=4, txt=textBuffer)
    pdf.ln(8)

commandsList={
    "h1": header1
}

sourceFile=r"C:\Files\LaTeX2\test.txt"
destFile=r"C:\Files\LaTeX2\out.pdf"

source = open(sourceFile, "r")

# Generate PDF
pdf = FPDF()
pdf.set_margins(left=45, top=30, right=45)
pdf.add_page()
pdf.add_font('LaTeX', '', "C:\Files\LaTeX2\Fonts\cmunrm.ttf", uni=True)

with open(sourceFile) as file:
    source = [line.rstrip() for line in file]

i=0
textBuffer=''
previousWasText=0

while(i<len(source)):
    line=source[i]
    print(f"{i}: {line}")

    if line.replace("\n", "").replace(" ", "")=='' or i==len(source): #is the line empty or the end of the file?
        #if there is something in the buffer, write it
        if previousWasText: writeText(pdf, textBuffer)
        textBuffer=''
        previousWasText=0
        #update line counter
        i+=1
        continue

    if line.replace(' ','')[0]=="\\": #is the start of a command?

        if previousWasText: writeText(pdf, textBuffer)
        textBuffer=''
        previousWasText=0

        #TODO: multiline commands
        #extract the commands parameters
        command=re.findall(commandPattern, line)[0]
        options=re.findall(optionsPattern, line)
        arguments=re.findall(argumentsPattern, line)
        print(f"found command: {command} with options: {options} and argument: {arguments}")
        if command not in commandsList:
            print(f'line: {i}: command {command} not recognized')
            #update line counter
            i+=1
            continue
        commandsList[command](pdf=pdf, cmd=command, opt=options, arg=arguments[0])


        #elaborate command

        #update line counter
        i+=1
        continue

    #if the line doesn't start with a \ and it's not empyt, it's considered text
    if previousWasText: textBuffer += " "
    textBuffer += line
    previousWasText=1
    #update line counter
    i+=1
    if i==len(source): writeText(pdf, textBuffer)

pdf.output(f'./example.pdf', 'F')
exit()


source.close()

exit()

# cell height
ch = 8

class PDF(FPDF):
    def __init__(self):
        super().__init__()
        self.add_font('LaTeX', '', "C:\Files\LaTeX2\Fonts\cmunrm.ttf", uni=True)
    def header(self):
        self.set_font('LaTeX', '', 9.5)
        self.cell(0, 8, 'Python implementation of tree-search algorithms        Dennis Loi [70/83/65264]', 0, 1, 'L')
        self.line(45,37,165,37)
    def footer(self):
        self.set_y(-15)
        self.set_font('LaTeX', '', 9.5)
        self.cell(0, 8, f'Page {self.page_no()}', 0, 0, 'C')





pdf.ln(5)
pdf.set_font('LaTeX', '', 14)
pdf.cell(80, ch, '1 Introduction', align='L')
pdf.ln(8)

pdf.set_font('LaTeX', '', 9.5)
pdf.multi_cell(w=0,h=4, txt=text)
pdf.ln(ch)

pdf.set_font('LaTeX', '', 14)
pdf.cell(40, ch, '2   What is a Tree Search algorithm?', align='L')
pdf.ln(8)

pdf.set_font('LaTeX', '', 9.5)

pdf.multi_cell(w=0, h=4, txt=text2)

pdf.ln(ch)

# Table Header
pdf.set_font('LaTeX', '', 16)
pdf.cell(40, ch, 'Feature 1', 1, 0, 'C')
pdf.cell(40, ch, 'Feature 2', 1, 1, 'C')


pdf.output(f'./example.pdf', 'F')