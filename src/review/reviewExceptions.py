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
