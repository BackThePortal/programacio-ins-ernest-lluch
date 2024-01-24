from dataclasses import dataclass 
from typing import Optional
from formularis import Text

@dataclass
class Plat:
  nom: str
  preu: int
  veg: bool

  def __str__(self):
    return ("(V) " if self.veg else "") + f"{self.nom} - {self.preu/100:.2f}€"



  