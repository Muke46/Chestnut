import tkinter as tk
import re

root = tk.Tk()
root.title("Tk Example")
root.config(bg="skyblue")
root.minsize(200, 200)  # width, height



# Create Text Frame widget
textFrame = tk.Frame(root, width=200, height=200)
textFrame.grid(row=0, column=0, padx=10, pady=5)



v=tk.Scrollbar(textFrame, orient='vertical')
v.pack(side=tk.RIGHT, fill='y')
t = tk.Text(textFrame, width=20, height=20, yscrollcommand=v.set)
v.config(command=t.yview)
t.pack()

commands=[
    "newline",
    "betty"
]


def add_highlighter(*args):
   for tag in t.tag_names():
       t.tag_remove(tag, "1.0", "end")
   text = t.get('1.0', "end").splitlines()
   for i, line in enumerate(text):
        #find all the backslashes, that indicate a command

        for m in re.finditer(r"\\([^\\ ]+)", line):
            if m.group(1) in commands:
                t.tag_add(f"{i}{m.start()}", f"{i+1}.{m.start()}",f"{i+1}.{m.end()}")
                t.tag_config(f"{i}{m.start()}", background= "white", foreground= "blue")

            
   
t.bind('<KeyRelease>', add_highlighter)

def updateLayout(*args):
    root.update()
    width=root.winfo_width()
    print (root.winfo_height())
    textFrame.config(width=int(width/2))

root.bind("<Configure>", updateLayout)

tk.Button(textFrame, text= "Highlight", command= add_highlighter).pack()

# Create Preview Frame widget
previewFrame = tk.Frame(root, width=200, height=400)
previewFrame.grid(row=0, column=1, padx=10, pady=5)

# Create Settings Frame widget
settingsFrame = tk.Frame(root, width=200, height=100)
settingsFrame.grid(row=1, column=0, padx=10, pady=5)


root.mainloop()