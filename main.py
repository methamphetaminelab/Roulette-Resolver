import customtkinter as ctk

ctk.set_appearance_mode('Dark')
ctk.set_default_color_theme('blue')

class RouletteResolver(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title('Roulette Resolver')

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        window_width = 335
        window_height = 305
        pos_x = screen_width - window_width
        pos_y = 0

        self.geometry(f'{window_width}x{window_height}+{pos_x}+{pos_y}')

        self.wm_attributes('-topmost', 1)
        self.attributes('-alpha', 0.8)
        self.overrideredirect(True)

        self.hot_rounds = 0
        self.cold_rounds = 0

        self.entry_hot = ctk.CTkEntry(self, placeholder_text='HOT BULLETS', width=160)
        self.entry_hot.grid(row=0, column=0, padx=5, pady=5)

        self.entry_cold = ctk.CTkEntry(self, placeholder_text='COLD BULLETS', width=160)
        self.entry_cold.grid(row=1, column=0, padx=5, pady=5)

        self.init_button = ctk.CTkButton(self, text='FILL', command=self.fill_rounds, width=160)
        self.init_button.grid(row=2, column=0, padx=5, pady=2)

        self.hot_button = ctk.CTkButton(self, text='HOT', fg_color='red', command=self.remove_hot, width=160)
        self.hot_button.grid(row=3, column=0, padx=5, pady=2)

        self.cold_button = ctk.CTkButton(self, text='COLD', fg_color='gray', command=self.remove_cold, width=160)
        self.cold_button.grid(row=4, column=0, padx=5, pady=2)

        self.output_label1 = ctk.CTkLabel(self, text='', anchor='w')
        self.output_label1.grid(row=5, column=0, columnspan=3, padx=5, pady=5)

        self.output_label2 = ctk.CTkLabel(self, text='', anchor='w')
        self.output_label2.grid(row=6, column=0, columnspan=3, padx=5, pady=5)

        self.output_label3 = ctk.CTkLabel(self, text='', anchor='w')
        self.output_label3.grid(row=7, column=0, columnspan=3, padx=5, pady=5)

        self.bullet_labels = []
        self.bullet_states = []

    def fill_rounds(self):
        try:
            self.hot_rounds = int(self.entry_hot.get())
            self.cold_rounds = int(self.entry_cold.get())
            self.bullet_states = ['unknown'] * (self.hot_rounds + self.cold_rounds)
            self.update_output()
        except ValueError:
            self.output_label.configure(text='PLEASE ENTER CORRECT NUMBERS')

    def remove_hot(self):
        if self.hot_rounds > 0:
            self.hot_rounds -= 1
            self.bullet_states.pop(0)
            self.update_output()

    def remove_cold(self):
        if self.cold_rounds > 0:
            self.cold_rounds -= 1
            self.bullet_states.pop(0)
            self.update_output()

    def update_output(self):
        total_rounds = len(self.bullet_states)
        chance = (self.hot_rounds / total_rounds * 100) if total_rounds > 0 else 0.0

        ot1 = f'HOT BULLETS: {self.hot_rounds}'
        ot2 = f'COLD BULLETS: {self.cold_rounds}\n'
        ot3 = f'HOT BULLET CHANCE: {chance:.2f}%'

        self.output_label1.configure(text=ot1)
        self.output_label2.configure(text=ot2)
        self.output_label3.configure(text=ot3)
        self.update_bullets(total_rounds=total_rounds)

    def update_bullets(self, total_rounds):
        for label, button_h, button_c in self.bullet_labels:
            label.grid_forget()
            button_h.grid_forget()
            button_c.grid_forget()

        self.bullet_labels.clear()

        for round, state in enumerate(self.bullet_states):
            label_text = (round + 1) if state == 'unknown' else (f'{round + 1} HOT' if state == 'hot' else f'{round + 1} COLD')
            label_color = 'transparent' if state == 'unknown' else ('red' if state == 'hot' else 'gray')

            label = ctk.CTkLabel(self, text=label_text, fg_color=label_color, width=3)
            button_h = ctk.CTkButton(self, text='HOT', fg_color='red', command=lambda r=round: self.set_hot(r), width=18)
            button_c = ctk.CTkButton(self, text='COLD', fg_color='gray', command=lambda r=round: self.set_cold(r), width=18)

            label.grid(row=round, column=3, padx=5, pady=5)
            button_h.grid(row=round, column=4, padx=5, pady=5)
            button_c.grid(row=round, column=5, padx=5, pady=5)

            self.bullet_labels.append((label, button_h, button_c))

    def set_hot(self, round):
        self.bullet_states[round] = 'hot'
        self.update_output()

    def set_cold(self, round):
        self.bullet_states[round] = 'cold'
        self.update_output()

if __name__ == '__main__':
    app = RouletteResolver()
    app.mainloop()
