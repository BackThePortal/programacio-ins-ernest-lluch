from collections.abc import Callable
from typing import Generic, TypeVar
from formularis import Opcio, titol
from functools import wraps

T = TypeVar('T')  # Argument per cridar la funció per obtenir el titol
U = TypeVar('U')  # Clau per mostrar les opcions

# Classe que permet la creació simplificada d'administradors amb
# un menú dinàmic i decoradors.

# TODO #1
# La naturalesa dels decoradors trenca la recursivitat. Potser caldria
# arreglar-ho.
# De totes maneres la recursivitat afecta lleugerament el rendiment (encara
# que el python de per si ja és un llenguatge ineficient) i això pot forçar
# al programador a utilitzar un bucle enlloc d'una crida a si mateix.

# TODO #2
# Realment hauria d'utilitzar un decorador de classe enlloc d'una
# classe pare. Té més sentit.
class Administrador(Generic[T, U]):

  # Si el títol és dinàmic, es pot passar una funció per obtenir-lo i
  # especificar l'argument, que haurà de ser una referència a l'objecte
  # desitjat.
  def __init__(self, titol: str | Callable[[T], str], arg: T | None = None):
    self._titol = titol
    self.titol_arg = arg

  @property
  def titol(self) -> str:
    if callable(self._titol):
      assert self.titol_arg is not None
      return self._titol(self.titol_arg)
    else:
      return self._titol

  @staticmethod
  def menu(clau: Callable | None = None,
           descr: str | Callable[..., str] | None = None):
    """
    Mostra el menú amb les opcions que s'han configurat amb
    els decoradors. Totes les funcions paramètriques tenen com a
    argument la instància de la classe.
    El propi codi de la funció s'executa després de mostrar el
    títol i abans de mostrar les eines.
    L'existència del decorador permet escollir amb quin mètode
    el menú apareix.
    - clau: Funció  per determinar les eines que es mostren. Si és
    o retorna None, es mostren les eines amb la clau None.
    """

    def dec(func):

      @wraps(func)
      def wrapper(self): # self és la instància de la classe imperativa
        titol(self.titol, True)
        func(self)

        # https://stackoverflow.com/questions/34439/finding-what-methods-a-python-object-has

        _clau = clau(self) if callable(clau) else None
        
        # Filtrar els mètodes que tenen la clau corresponent i obtenir
        # l'ítem amb l'índex de l'ítem d'on s'ha obtingut si és una tupla
        def convertir(m):
          c = getattr(m, 'clau', -1)
          if c == -1:
            return False
          if type(c) == tuple:
            ind = None
            
            try:
              ind = c.index(_clau)
            except: # La clau no és a la tupla. No es mostra.
              return False

            # Trobar posició a la tupla en base a l'índex de la clau trobada
            return (m, m.pos[ind])
          elif c == _clau:
            
            # No és una tupla => m.pos és només un int
            return (m, m.pos)
          else:
            return False

          
        # Obtenir tots els mètodes de la classe i les posicions.
        metodes = [convertir(m) for k, m in self.__class__.__dict__.items()
           if callable(m)]

        # Filtrar valors falsos
        metodes = list(filter(lambda x: x is not False, metodes))
        
        
        # Ordenar els mètodes per la posició
        metodes.sort(key=lambda x: x[1])

        # Eliminar posició
        metodes = [m for m, i in metodes]

        # Obtenir el nom de l'opció i preparar la funció lambda que crida
        # la funció corresponent a opció amb els arguments corresponents.
        op = {m.nom: (lambda m: (lambda self: m(self, m.nom, m.descr)))(m) for m in metodes}
        
        
        if Opcio(None,
                 op,
                 self,
                 descr(self) if callable(descr) else descr,
                 refrescar=False,
                 sep=None)() != 0:
          wrapper(self)

      return wrapper

    return dec

  @staticmethod
  def eina(nom: str,
           pos: int | tuple[int, ...],
           clau: U | tuple[U] | None = None,
           descr: str | None = None):
    """
    Decorador que determina que una funció és una eina que forma
    part de l'administrador. Es mostrarà el títol amb el nom de
    l'eina i s'afegirà la funció a la llista d'eines amb la clau
    especificada.
    """

    # La sintaxi dels decoradors amb arguments és innecessàriament i estúpidament
    # complicada al python.
    # https://stackoverflow.com/questions/5929107/decorators-with-parameters

    # Generar decorador
    def dec(func):

      # Creador de la funció
      @wraps(func)
      def wrapper(self, _nom, _descr):
        titol(self.titol + " - " + _nom, True)
        if descr is not None:
          print(_descr)
        func(self)

        # self.eines[clau][nom] = lambda self: f(self, nom, descr, func)

      # Assegurar que clau i índex són els dos tuples o l'índex un nombre i la
      # clau no una tupla.
      assert type(clau) == type(pos) or (type(pos) == int and type(pos) != tuple)
      
      # Afegir propietats a la pròpia funció per poder trobar-les
      # més tard. Ignorar errors.
      wrapper.nom = nom
      wrapper.clau = clau
      wrapper.descr = descr
      wrapper.func = func
      wrapper.pos = pos
      return wrapper

    return dec
