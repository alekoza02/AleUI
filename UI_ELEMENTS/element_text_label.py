from UI_ELEMENTS.base_element import BaseElementUI
from UI_ELEMENTS.shapes import RectAle, LineAle, CircleAle, SurfaceAle
from UI_ELEMENTS.font import Font


class Label_text(BaseElementUI):
    def __init__(self, x, y, w, h, origin=None, text="Hello world! Sono proprio felicio", use_latex_font=False, text_centered_x=True, text_centered_y=True, performant=False):
        super().__init__(x, y, w, h, origin, performant)

        # shape
        self.shape.add_shape("bg", RectAle("0cw", "0ch", "100cw", "100ch", [60, 60, 60], 0, 0))
        self.shape.add_shape("text_surface", SurfaceAle("0cw", "0ch", "100cw", "100ch"))

        # text info (geometrical)
        self.text_centered_x = text_centered_x
        self.text_centered_y = text_centered_y

        # text info (logical)
        self.text = text
        self.font = Font(28, use_latex_font)
        self.update_text()


    def update_text(self):
        self.shape.shapes["text_surface"].fill((0, 0, 0, 0))

        rendered_text = self.font.font_pyg_r.render(self.text, True, [148, 177, 255])

        x_offset, y_offset = 0, 0

        if self.text_centered_y:
            y_offset = self.shape.shapes["text_surface"].h.value / 2 - rendered_text.get_height() / 2

        if self.text_centered_x:
            x_offset = self.shape.shapes["text_surface"].w.value / 2 - rendered_text.get_width() / 2

        self.shape.shapes["text_surface"].blit(rendered_text, (x_offset, y_offset))


    def analyze_coordinate(self, w_screen, h_screen, w_viewport, h_viewport, w_container=None, h_container=None, offset_x=0, offset_y=0) -> None:
        super().analyze_coordinate(w_screen, h_screen, w_viewport, h_viewport, w_container, h_container, offset_x, offset_y)
        self.update_text()



# class SubStringa:
#     def __init__(self, colore, bold, italic, apice, pedice, highlight, testo) -> None:
        
#         self.colore: tuple[int] = colore
        
#         self.bold: bool = bold
#         self.italic: bool = italic
#         self.apice: bool = apice
#         self.pedice: bool = pedice
#         self.highlight: bool = highlight
        
#         self.testo: str = testo


#     def end(self, font:pygame.font.Font):
#         lung = font.size(self.testo)
#         return lung[0]


#     @staticmethod
#     def analisi_caratteri_speciali(frase):

#         risultato = frase

#         for indice, segno in diction.simboli.items():
#             if indice in risultato: risultato = risultato.replace(indice, segno)

#         return risultato


#     @staticmethod
#     def start_analize(frase: str):
        
#         def flatten(lst):

#             flattened_list = []
#             for item in lst:
#                 if isinstance(item, list):
#                     flattened_list.extend(flatten(item))  # Recursively flatten nested lists
#                 else:
#                     flattened_list.append(item)
#             return flattened_list

#         start = SubStringa(None, False, False, False, False, False, frase)

#         substringhe = start.analisi()

#         sub_flatten = flatten(substringhe)

#         risultato = [elemento for elemento in sub_flatten if elemento.testo != ""]

#         return risultato


#     def analisi(self):
        
#         substringhe_create = []

#         formattatori=(r"\h{", r"\^{", r"\_{", r"\b{", r"\i{", r"\#")
#         lookup_lenghts = {
#             r"\h{": 3,
#             r"\^{": 3,
#             r"\_{": 3,
#             r"\b{": 3,
#             r"\i{": 3,
#             r"\#": 9,
#         }

#         # h = highlight
#         # ^ = apice
#         # _ = pedice
#         # b = bold
#         # i = italic
#         # # = hex color

#         formattatori_trovati = []

#         primo_formattatore = None

#         valvola = 0

#         if "{" in self.testo:

#             for i in range(len(self.testo)):
                
#                 # controlla se viene trovato un formattatore tra tutti i formattatori disponibili
#                 for formattatore in formattatori:

#                     # se la substringa che va da i a i + len(form.) è uguale al form. -> trovato un candidato
#                     if self.testo[i:i+len(formattatore)] == formattatore:

#                         # se questa è la prima volta che si trova un formattatore, me lo segno
#                         if primo_formattatore is None:
#                             primo_formattatore = i
                        
#                         # in generale, tengo traccia dei formattatori trovati, così da sapere quando finisce la parentesi
#                         formattatori_trovati.append([formattatore, i])
#                         break

#                 if self.testo[i] == "}":
#                     for j in range(len(formattatori_trovati),0,-1):
#                         if len(formattatori_trovati[j-1]) == 2:
#                             formattatori_trovati[j-1].append(i)
#                             break

#                 # controllo se il primo formattatore è stato chiuso
#                 if len(formattatori_trovati) > 0 and len(formattatori_trovati[0]) == 3:

#                     # controllo pre formattatore, presenza di testo default
#                     if formattatori_trovati[0][1] > valvola:
#                         substringhe_create.append(SubStringa(self.colore, self.bold, self.italic, self.apice, self.pedice, self.highlight, self.testo[valvola:formattatori_trovati[0][1]]))


#                     # gestione del tag                    
#                     ris = SubStringa(self.colore, self.bold, self.italic, self.apice, self.pedice, self.highlight, None)
#                     ris.testo = self.testo[formattatori_trovati[0][1] + lookup_lenghts[formattatori_trovati[0][0]]: formattatori_trovati[0][2]]
                    
#                     match formattatori_trovati[0][0]:
#                         case r"\h{": ris.highlight = True
#                         case r"\^{": ris.apice = True
#                         case r"\_{": ris.pedice = True
#                         case r"\b{": ris.bold = True
#                         case r"\i{": ris.italic = True
#                         case r"\#": ris.colore = MateUtils.hex2rgb(self.testo[formattatori_trovati[0][1] + 2 : formattatori_trovati[0][1] + 8])


#                     # controllo figli
#                     depth_controllo = ris.analisi()
#                     if len(depth_controllo) == 0:
#                         substringhe_create.append(ris)
#                     else:
#                         substringhe_create.append(depth_controllo)


#                     # ripristino il ciclo
#                     valvola = formattatori_trovati[0][2] + 1
#                     formattatori_trovati = []
#                     primo_formattatore = None


#         substringhe_create.append(SubStringa(self.colore, self.bold, self.italic, self.apice, self.pedice, self.highlight, self.testo[valvola:]))
        
#         return substringhe_create