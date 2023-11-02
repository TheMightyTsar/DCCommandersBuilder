'''
Módulo destinado a la definición de Excepciones
personalizadas usadas en reviewHandler.py
'''


class ModuloNoPermitido(Exception):

    def __init__(self, modulos_invalidos, *args, **kwargs):
        self.modulos_invalidos = modulos_invalidos
        super().__init__(*args, **kwargs)

    def imprimir_modulos_invalidos(self):
        for m in self.modulos_invalidos:
            print("- " + m)


class FuncionNoPermitida(Exception):

    def __init__(self, funciones_invalidas, *args, **kwargs):
        self.funciones_invalidas = funciones_invalidas
        super().__init__(*args, **kwargs)

    def imprimir_funciones_invalidas(self):
        for m in self.funciones_invalidas:
            print("- " + m)
