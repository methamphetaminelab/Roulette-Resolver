import customtkinter as ctk

ctk.set_appearance_mode('Dark')
ctk.set_default_color_theme('blue')

class RouletteResolver(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title('Roulette Resolver')

        screenWidth = self.winfo_screenwidth()
        screenHeight = self.winfo_screenheight()

        windowWidth = 335
        windowHeight = 305
        posX = screenWidth - windowWidth
        posY = 0

        self.geometry(f'{windowWidth}x{windowHeight}+{posX}+{posY}')

        self.wm_attributes('-topmost', 1)
        self.attributes('-alpha', 0.8)
        self.overrideredirect(True)

        self.hotRounds = 0
        self.coldRounds = 0

        self.entryHot = ctk.CTkEntry(self, placeholder_text="HOT BULLETS", width=160)
        self.entryHot.grid(row=0, column=0, padx=5, pady=5)

        self.entryCold = ctk.CTkEntry(self, placeholder_text="COLD BULLETS", width=160)
        self.entryCold.grid(row=1, column=0, padx=5, pady=5)

        self.initButton = ctk.CTkButton(self, text="FILL", command=self.fillRounds, width=160)
        self.initButton.grid(row=2, column=0, padx=5, pady=2)

        self.hotButton = ctk.CTkButton(self, text="HOT", fg_color="red", command=self.removeHot, width=160)
        self.hotButton.grid(row=3, column=0, padx=5, pady=2)

        self.coldButton = ctk.CTkButton(self, text="COLD", fg_color="gray", command=self.removeCold, width=160)
        self.coldButton.grid(row=4, column=0, padx=5, pady=2)

        self.outputLabel1 = ctk.CTkLabel(self, text="", anchor="w")
        self.outputLabel1.grid(row=5, column=0, columnspan=3, padx=5, pady=5)

        self.outputLabel2 = ctk.CTkLabel(self, text="", anchor="w")
        self.outputLabel2.grid(row=6, column=0, columnspan=3, padx=5, pady=5)

        self.outputLabel3 = ctk.CTkLabel(self, text="", anchor="w")
        self.outputLabel3.grid(row=7, column=0, columnspan=3, padx=5, pady=5)

        self.bulletLabels = []
        self.bulletStates = []

    def fillRounds(self):
        try:
            self.hotRounds = int(self.entryHot.get())
            self.coldRounds = int(self.entryCold.get())
            self.bulletStates = ['unknown'] * (self.hotRounds + self.coldRounds)
            self.updateOutput()
        except ValueError:
            self.outputLabel.configure(text='PLEASE ENTER CORRECT NUMBERS')

    def removeHot(self):
        if self.hotRounds > 0:
            self.hotRounds -= 1
            self.bulletStates.pop(0)
            self.updateOutput()

    def removeCold(self):
        if self.coldRounds > 0:
            self.coldRounds -= 1
            self.bulletStates.pop(0)
            self.updateOutput()

    def updateOutput(self):
        totalRounds = len(self.bulletStates)
        chance = (self.bulletStates.count('hot') / totalRounds * 100) if totalRounds > 0 else 0.0

        ot1 = (f'HOT BULLETS: {self.hotRounds}')

        ot2 = (f'COLD BULLETS: {self.coldRounds}\n')
        ot3 = (f'HOT BULLET CHANCE: {chance:.2f}%')

        self.outputLabel1.configure(text=ot1)
        self.outputLabel2.configure(text=ot2)
        self.outputLabel3.configure(text=ot3)
        self.updateBullets(totalRounds=totalRounds)

    def updateBullets(self, totalRounds):
        for label, button_h, button_c in self.bulletLabels:
            label.grid_forget()
            button_h.grid_forget()
            button_c.grid_forget()

        self.bulletLabels.clear()

        for round, state in enumerate(self.bulletStates):
            label_text = (round + 1) if state == "unknown" else (f"{round + 1} HOT" if state == 'hot' else f"{round + 1} COLD")
            label_color = "transparent" if state == "unknown" else ("red" if state == 'hot' else "gray")

            label = ctk.CTkLabel(self, text=label_text, fg_color=label_color, width=3)
            button_h = ctk.CTkButton(self, text="HOT", fg_color="red", command=lambda r=round: self.setHot(r), width=18)
            button_c = ctk.CTkButton(self, text="COLD", fg_color="gray", command=lambda r=round: self.setCold(r), width=18)

            label.grid(row=round, column=3, padx=5, pady=5)
            button_h.grid(row=round, column=4, padx=5, pady=5)
            button_c.grid(row=round, column=5, padx=5, pady=5)

            self.bulletLabels.append((label, button_h, button_c))

    def setHot(self, round):
        self.bulletStates[round] = 'hot'
        self.updateOutput()

    def setCold(self, round):
        self.bulletStates[round] = 'cold'
        self.updateOutput()

if __name__ == '__main__':
    app = RouletteResolver()
    app.mainloop()
