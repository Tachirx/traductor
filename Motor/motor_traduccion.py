import requests
from deep_translator import GoogleTranslator
from deep_translator.exceptions import (
    RequestError, TooManyRequests, TranslationNotFound, NotValidLength, LanguageNotSupportedException
)

class MotorTraduccion:
    def __init__(self):
       
        self.traductor = GoogleTranslator()

    def traducir(self, texto, l_origen, l_destino):
        try:
            if not texto.strip():
                return ""
            if len(texto) > 5000:
                #  límite nativo de 5000 caracteres
                raise NotValidLength(texto, min_chars=1, max_chars=5000)
            
            # instancia y actualiza los idiomas
            self.traductor.source = l_origen
            self.traductor.target = l_destino
            resultado = self.traductor.translate(text=texto) 
            
            if not resultado:
                raise TranslationNotFound(texto)
            return resultado
        except requests.exceptions.RequestException:
            raise Exception("Sin conexión a internet, verificar la conexión de red (RequestException)")
        except RequestError:
            raise Exception("Sin conexión a internet, verificar la conexión red")
        except TooManyRequests:
            raise Exception("Demasiadas solicitudes, espere un momento")
        except LanguageNotSupportedException:
            raise Exception("Idioma no soportado")
        except NotValidLength:
            raise Exception("Texto ingresado demasiado largo")
        except TranslationNotFound:
            raise Exception("No se encontró traducción, intente con un texto diferente")
        except Exception as e:
            raise Exception(f"Error desconocido: {str(e)}")
