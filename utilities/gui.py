
import tkinter as tk
import tkinter.font as tkFont
from tkinter import font
from utilities.match import filter_list_by_match

import tkinter as tk
import tkinter.font as tkFont

class RichLabel(tk.Text):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.configure(borderwidth=0, highlightthickness=0)

        # Salvo colori di default
        self._default_bg = self.cget("background")
        self._default_fg = self.cget("foreground")

        # Colori per lo stato "selezionato"
        self._selection_bg = "#3399FF"
        self._selection_fg = "#FFFFFF"
        self._selection_Bfg = "#111111"

        # Configurazione font grassetto
        default_font = tkFont.nametofont(self.cget("font"))
        bold_font = tkFont.Font(**default_font.configure()) # type: ignore
        bold_font.configure(weight="bold")
        self.tag_configure("bold", font=bold_font, foreground=self._selection_Bfg)

        # Rendo read-only
        self.configure(state="disabled")

    def insert(self, richText: str):
        self.configure(state="normal")
        self.delete("1.0", tk.END)
        chunks = richText.split('*')  # split su * per le parti in grassetto
        for i, chunk in enumerate(chunks):
            if i % 2 == 1:
                super().insert(tk.END, chunk, 'bold')
            else:
                super().insert(tk.END, chunk)
        self.configure(state="disabled")

    def setSelection(self, selection: bool = False):
        """
        Se selection=True, applica colori di evidenziazione;
        altrimenti ripristina i colori di default.
        """
        if selection:
            self.configure(
                background=self._selection_bg,
                foreground=self._selection_fg
            )
        else:
            self.configure(
                background=self._default_bg,
                foreground=self._default_fg
            )


class App:
    def __init__(self, master:tk.Tk, dataset:list[str]):
        self.master = master
        self.dataset = dataset
        master.title("Esempio Input e Lista Customizzata")

        # Variabile di testo per l'input
        self.text_var = tk.StringVar()
        self.text_var.trace_add("write", self.on_input_change)

        # Entry a singola linea
        self.entry = tk.Entry(master, textvariable=self.text_var)
        self.entry.pack(padx=10, pady=0, fill='x')
        master.after(0, self.entry.focus_force)

        # Canvas scrollabile + Frame interno per righe custom
        self.canvas = tk.Canvas(master, borderwidth=0)
        self.scrollbar = tk.Scrollbar(master, orient="vertical", command=self.canvas.yview)
        self.list_frame = tk.Frame(self.canvas)
        self.list_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.canvas.create_window((0, 0), window=self.list_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True, padx=(10,0), pady=5)
        self.scrollbar.pack(side="right", fill="y", pady=0)

        self.selector:int = -1
        self.filtered:list[str] = []

        
    def on_input_change(self, *args):
        match = self.text_var.get()
        self.update_list(match)

    def update_selection(self):
        children:list[RichLabel] = self.list_frame.winfo_children() # type: ignore
        for (i, child) in enumerate(children):
            child.setSelection(True if i == self.selector else False)

    def update_list(self, match=''):
        """
        Aggiorna la lista di stringhe nella listbox.
        :param items: lista di stringhe da visualizzare
        """
        
        for child in self.list_frame.winfo_children():
            child.destroy()

        self.filtered = filter_list_by_match(list=self.dataset, match=match)
        if len(self.filtered) == 0:
            self.selector = -1
        else:
            self.selector = 0


        for text in self.filtered:
            # Crea un RichLabel per ogni riga
            rich = RichLabel(self.list_frame, height=1, wrap="word")
            rich.insert(text)
            rich.pack(fill="x", padx=5, pady=0)

        self.update_selection()

    def on_up(self, Event):
        if len(self.filtered) != 0 and self.selector > 0:
            self.selector -= 1
            self.update_selection()

    def on_down(self, Event):
        if len(self.filtered) != 0 and len(self.filtered)-1 > self.selector:
            self.selector += 1
            self.update_selection()

    def on_enter(self, Event):
        if self.selector != -1:
            self.master.__dict__['resultData'] = self.filtered[self.selector].replace('*', '')
            self.master.destroy()


            
def app_run(availableList:list[str]):
    root = tk.Tk()
    root.__dict__['resultData'] = None

    def force_exit(Event):
        root.__dict__['resultData'] = None
        root.destroy()

    # Rimuove barra del titolo e bordi nativi
    root.overrideredirect(True)

    # Dimensioni e posizione (esempio 400×200 px, centrata)
    width, height = 400, 200
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f"{width}x{height}+{x}+{y}")

    
    # --- Bind generali sulla finestra ---
    root.bind("<Escape>", force_exit)
    root.bind("<FocusOut>", force_exit)


    # Contenuto di test (puoi personalizzare)
    # label = tk.Label(root, text="Premi ESC o clicca fuori per uscire", font=("Helvetica", 14))
    # label.pack(expand=True)

    # Assicura che la finestra catturi subito il focus
    root.focus_force()


    app = App(root, availableList)
    # Esempio di inizializzazione con markup per grassetto
    app.update_list()

        # Usa bind_all per intercettare i tasti anche se il widget non è direttamente focalizzato
    root.bind_all("<Up>", app.on_up)
    root.bind_all("<Down>", app.on_down)
    root.bind_all("<Return>", app.on_enter)

    root.mainloop()
    return root.__dict__['resultData']
