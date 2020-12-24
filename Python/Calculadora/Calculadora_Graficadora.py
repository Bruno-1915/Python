#!/usr/bin/env python
# coding: utf-8

# In[1]:


import PySimpleGUI as sg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk


# In[705]:


class Toolbar(NavigationToolbar2Tk):
    def __init__(self, *args, **kwargs):
        super(Toolbar, self).__init__(*args, **kwargs)

class calculadora:
    
    
    def __init__(self):
        self.operadores_binarios = ['^','*', '/', '+', '-']
        self.operadores_unarios = ['sqrt', 'e', 'log', 'cos', 'sin', 'tan', 'cosh', 'sinh', 'tanh']
        self.operadores_problematicos = ['cosh', 'sinh', 'tanh']
        self.nuevos = False
        self.l = []
        self.font = ("Helvetica", 20)
        self.size = (int(sg.Window.get_screen_size()[0]/2), int(sg.Window.get_screen_size()[1]/2))
        self.reset()
    
    #Definimos los elementos de la ventana
    def reset(self, *args):
        sg.theme('DarkAmber')
        self.name = "Calculadora"   
        self.layout1 = [  [sg.Text(font = self.font), sg.InputText(font = self.font, key = "Entrada", justification ="center")]]
      
        self.layout2 = self.operadoresBotones()
        
        self.layout3 = [ [sg.Button('7', font = ("Helvetica", 20)),sg.Button('8', font = ("Helvetica", 20)),
            sg.Button('9', font = ("Helvetica", 20))],
                   [sg.Button('4', font = ("Helvetica", 20)),sg.Button('5', font = ("Helvetica", 20)),
            sg.Button('6', font = ("Helvetica", 20))],
            [sg.Button('1', font = ("Helvetica", 20)),sg.Button('2', font = ("Helvetica", 20)), sg.Button('3', font = ("Helvetica", 20))],
             [sg.Button('0', font = ("Helvetica", 20)),sg.Button('.', font = ("Helvetica", 20))
              ,sg.Button('j', font = ("Helvetica", 20))]]
        
        self.layout4 = [ [sg.Text(size = (30, 4), font = ("Helvetica", 20), key = 'Resultado')]]
        
        self.layout5 = [ [sg.Button('=', font = ("Helvetica", 20), size = (2,5), bind_return_key=True)] ]
        
        self.layout6 = [ [sg.Button('AC', font = ("Helvetica", 20), size = (2,5))] ]
        
        self.layout7 = [ [sg.Button("DEL", font = ("Helvetica", 20), size = (2,5))] ]
        
        self.layout8 = [ [sg.Button('Salir', font = ("Helvetica", 20))] ]
        
        self.menu_def = [['Menu', ['Inicio', 'Nueva Funcion', ['Unaria'], 'Funciones','Salir',]],
                ['Modo', ['Calculadora', 'Graficadora']],]

        
        self.layout = [[sg.Column(self.layout1)], [sg.Text('_'*107)],
        [sg.Column(self.layout2), sg.VerticalSeparator(), sg.Column(self.layout3), sg.VerticalSeparator(),
         sg.Column(self.layout5), sg.VerticalSeparator(), sg.Column(self.layout6), sg.VerticalSeparator(), sg.Column(self.layout7)],
        [sg.Text('_'*107)], [sg.Column(self.layout8)], [sg.Menu(self.menu_def)]]
        
    def operadoresBotones(self):
        operadores = self.operadores_binarios + self.operadores_unarios
        l = 0
        lista_completa = []
        a = []
        while l < len(operadores):
            a.append(sg.B(operadores[l], font = self.font))
            if (l+1)%5 == 0:
                lista_completa.append(a)
                a = []
            l += 1
        lista_completa.append(a)
        lista_completa.append([sg.B('(', font = self.font), sg.B(')', font = self.font)])
        lista_completa.append([sg.B('Izquierda', font = self.font), sg.B('Derecha', font = self.font)])
        
        return lista_completa
        
        
    # Esta función nos permite ver de que tipo numérico es un argumento de tipo string.
    # Si no es posible convertirlo a numérico devuelve str
    def tipo(self, x, bandera = False) -> type:
        try:
            int(x)
            return int
        except:
            try:
                float(x)
                return float
            except:
                try:
                    complex(x)
                    if bandera:
                        return complex(x)
                    else:
                        return complex
                except:
                    try:
                        X = x.split('+')
                        x = X[1] + '+' + X[0]
                        complex(x)
                        if bandera:
                            return complex(x)
                        else:
                            return complex
                    except:
                        try:
                            X = x.split('-')
                            x = X[1] + '-' + X[0]
                            complex(x)
                            if bandera:
                                return complex(x)
                            else:
                                return complex
                        except:
                            return str
                        
    # Aquí añadimos una operación unaria
    def agregar_unario(self, operador:str):
        if operador in self.operadores_unarios:
            sg.Popup("El operador ya se encuentra en mi lista",title = "Mensaje",  font = self.font)
        else:
            self.operadores_unarios.append(operador)
            self.l.append(operador)
            self.nuevos = True
            
            ## Si el operador nuevo comparte caracteres con alguna función ya existente también
            ## se agrega a la lista de operadores problematicos
            for i in self.operadores_unarios:
                if i in operador:
                    self.operadores_problematicos.append(operador)
                    break

    def evaluate(self, x: str): 
        import numpy as np
        ## Algunas funciones comparten caracteres, para evitar errores esas funciones se convierten en 
        ## mayusculas, así se ignoraran mientras se tratan las no problematicas
        a = []
        if x == '':
            return ''
        for i in self.operadores_problematicos:
            if i in x:
                a.append((i, i.upper()))
                x = x.replace(i,i.upper())
                
        for i in self.operadores_unarios:
            if i in x:
                x = x.replace(i, 'np.'+i)
        x = x.replace('^', '**')
        
        ## Regresamos a minusculas las funciones problemtaticas para evaluarlas
        for i in a:
            x = x.replace(i[1], 'np.' + i[0])
        
        if self.tipo(eval(x)) == str:
            return "Error"
        else:
            temp = eval(x)
            if temp == 0:
                return 0
            else:
                return temp
            
    def graficar(self, *args, rango = (-1, 1), show = True, borrar = False):
        import matplotlib.pyplot as plt
        import numpy as np
        
        if args != '' or args != ' ':
        
            if borrar:
                plt.plot((-1,1))
                plt.clf()

            else:
                for x in args:
                    x = self.parse(x)
                    label = x
                    x = x.replace(' ','')
                    x = x[x.find('=')+1:]
                    X = [i for i in np.linspace(rango[0], rango[1], 5000)]
                    Y = [x.replace('X', str(i)) for i in X]
                    try:
                        Y = [self.evaluate(i) for i in Y]
                    except:
                        print(x)
                        sg.Popup("No pude entender la entrada.\nVerifica que la función que ingresaste este en mis opciones",
                                title = "Mensaje", font = self.font)
                        break
                    plt.plot(X, Y, label = label)
                plt.grid()
                plt.legend()
#                 if show:
#                     plt.show()
                
    def parse(self, x):
        temp = x.count('X')
        l = 0
        ll=0
        while l < temp:
            ll = x.find('X',ll)
            try:
                float(x[ll-1])
                x = x[:ll] + x[ll:].replace('X', '*X', 1)
                ll+=2
            except:
                None
            l += 1
        return x
        
        
    # run_calc se encarga de correr la calculadora
    def run_calc(self):
        # Cada vez que se corre debemos reiniciar los layouts
        if self.nuevos:
            self.reset()
        else:
            self.reset()
        temp = 0

        sg.theme('DarkAmber')
        window = sg.Window('Calculadora', self.layout)
        sg.theme('DarkAmber')
        operacion = ''
        entrada = ''
        lugar = 'derecha'
        
        while True:
    
            event, values = window.read(timeout = 1000)
            
            if event == "Inicio":
                window.close()
                self.run()
                break
                
            elif event == "Unaria":
                window.close()
                funcion = sg.popup_get_text('Ingrese la nueva función',title = "Mensaje",  font = self.font)
                self.agregar_unario(funcion)
                self.run_calc()
                break
                
            elif event == "Calculadora":
                continue
                
            elif event == "Graficadora":
                window.close()
                self.run_graf()
                break
                
            elif event == "Funciones":
                self.lista_funciones()
                continue
            
            if event == sg.TIMEOUT_KEY:
                entrada = values["Entrada"].replace("__TIMEOUT__",'')
                continue
                
            if event == sg.WIN_CLOSED or event == 'Salir': 
                window.close()
                break
            if event == 'Izquierda':
                lugar = 'izquierda'
                continue
            elif event == 'Derecha':
                lugar = 'derecha'
                continue
            elif event == "DEL":
                entrada = entrada[0:-1]
                window["Entrada"].update(entrada)
                continue
            
            if event != '=' and event != "AC":
                if lugar == 'izquierda':
                    entrada = str(event) + entrada
                else:
                    entrada = entrada + str(event)
                window["Entrada"].update(entrada)
                
            elif event == "AC":
                entrada = ""
                window["Entrada"].update(entrada)
                
                
            elif event == '=':
                try:
                    try:
                        entrada = values['Entrada']
                    except:
                        entrada = ''
                    entrada = str(self.evaluate(entrada))
                    window["Entrada"].update(entrada)
                except:
                    entrada = "Error"
                    window["Entrada"].update(entrada)            
                

            if temp == 0:
                temp = 0

        window.close()
    


        
    def run_graf(self):
        #menu_def = [['Menu', ['Nueva Funcion', ['Unaria'],], 'Funciones'],
                #['Modo', ['Calculadora', 'Graficadora']],]
        
        layout = [
            [sg.T('Entrada', font = ("Helvetica", 15) )],
            [sg.I('', key = '-funcion-')],
            [sg.T("Las funciones deben tener el siguiente formato: 'y = X'", font = ("Helvetica", 15))],
            [sg.T("La variable X debe ir en mayuscula y cada función va separada por una coma", font = ("Helvetica", 15))],
            [sg.B('Graficar', font = ("Helvetica", 15), bind_return_key=True)],
            [sg.T("Rango: ", font = ("Helvetica", 15)), sg.I("", key = '-range-')],
            [sg.T("El rango debe ser una tupla", font = ("Helvetica", 15))],
            [sg.B("Ingresar Rango", font = ("Helvetica", 15))],
            [sg.T('Controls:', font = ("Helvetica", 15))],
            [sg.Canvas(key='controls_cv')],
            [sg.T('Figura:', font = ("Helvetica", 15))],
            [sg.Column(
                layout=[
                    [sg.Canvas(key='fig_cv',
                               # it's important that you set this size
                               size=(400 * 2, 400)
                               )]
                ],
                background_color='#DAE0E6',
                pad=(0, 0)
            )],
            [sg.B('Borrar', font = ("Helvetica", 15))],
            [sg.B('Salir', font = ("Helvetica", 15))],
            [sg.Menu(self.menu_def)]

        ]

        window = sg.Window('Gráfica', layout)
        rango = (-1, 1)
        graficar_por_rango = False
        while True:
            event, values = window.read(timeout = 1)
            
            if event == "Inicio":
                window.close()
                self.run()
                break
                
            elif event == "Unaria":
                window.close()
                funcion = sg.popup_get_text('Ingrese la nueva función', title = "Mensaje", font = self.font)
                self.agregar_unario(funcion)
                self.run_graf()
                break
            
            elif event == "Calculadora":
                window.close()
                self.run_calc()
                break
                
            elif event == "Graficadora":
                continue
            
            elif event == "Funciones":
                self.lista_funciones()
                continue
                
            if event == "Ingresar Rango":
                if values["-range-"]!='':
                    temp = values["-range-"]
                    temp = temp.split(',')
                    temp[0] = temp[0].replace('(','')
                    temp[0] = temp[0].replace(' ','')
                    temp[1] = temp[1].replace(')','')
                    temp[1] = temp[1].replace(' ','')
                    try:
                        rango = (float(temp[0]), float(temp[1]))
                        if values["-funcion-"] == '':
                            None
                        else:
                            graficar_por_rango = True
                    except:
                        sg.Popup("El valor de rango no fue válido", title = "Mensaje", font = self.font)
                        continue
                
            if event in (sg.WIN_CLOSED, 'Salir'):  # always,  always give a way out!
                window.close()
                break

            if event is "Graficar" or graficar_por_rango:
                graficar_por_rango = False
                plt.figure(1)
                fig = plt.gcf()
                DPI = fig.get_dpi()
                fig.set_size_inches(404 * 2 / float(DPI), 404 / float(DPI))
                temp = self.graficar(values["-funcion-"], rango = rango, show = False);
                if temp != None:
                    sg.Popup(temp, title = "Mensaje", font = self.font)

                draw_figure_w_toolbar(window['fig_cv'].TKCanvas, fig, window['controls_cv'].TKCanvas)
                
            if event == "Borrar":
                self.graficar(borrar = True)
                try:
                    draw_figure_w_toolbar(window['fig_cv'].TKCanvas, fig, window['controls_cv'].TKCanvas)
                except:
                    None
                
        window.close()
        
    def run(self):
        layout = [[sg.T("")],[sg.T("")],[sg.T("Bienvenido a la Calculadora y Graficadora", font = self.font)],[sg.T("")],[sg.T("")],
                  [sg.B('Calculadora', font = self.font, focus = True)], [sg.B('Graficadora', font = self.font)],
                 [sg.T("")],[sg.T("")],[sg.T("")],[sg.T("")],[sg.T("")],[sg.T("Por Bruno Martínez", font = self.font)],
                 [sg.B("Salir", font = self.font)]]
        w, h = sg.Window.get_screen_size()
        window = sg.Window("Bienvenido", layout, size = (int(w/2), int(h/2)), element_justification='c')
        while True:
            event, values = window.read()

            if event in (sg.WIN_CLOSED, None, 'Salir'):  # always,  always give a way out!
                window.close()
                break
            
            if event == "Calculadora":
                window.close()
                self.run_calc()
                break
                
            if event == "Graficadora":
                window.close()
                self.run_graf()
                break

        window.close()           
        
        
    def lista_funciones(self):
        layout1 = [ [sg.Listbox(values = calc.operadores_unarios, size = (10, 15))] ]
        layout2 = [ [sg.Listbox(values = calc.operadores_binarios, size = (10, 15))] ]
        layout = [[sg.Column(layout1), sg.VerticalSeparator(), sg.Column(layout2)],
                 [sg.B("Salir", bind_return_key=True)]]

        window = sg.Window("Funciones", layout)

        while True:
            event, values = window.read()

            if event in (sg.WIN_CLOSED, None, 'Salir'):  # always,  always give a way out!
                window.close()
                break

        window.close()        
        
        
######### FIN DE CLASE CALCULADORA ###########
        
def draw_figure_w_toolbar(canvas, fig, canvas_toolbar):
    if canvas.children:
        for child in canvas.winfo_children():
            child.destroy()
    if canvas_toolbar.children:
        for child in canvas_toolbar.winfo_children():
            child.destroy()
    figure_canvas_agg = FigureCanvasTkAgg(fig, master=canvas)
    figure_canvas_agg.draw()
    toolbar = Toolbar(figure_canvas_agg, canvas_toolbar)
    toolbar.update()
    figure_canvas_agg.get_tk_widget().pack(side='right', fill='both', expand=1)


# In[706]:


calc = calculadora()


# In[707]:


calc.run()


# In[ ]:




