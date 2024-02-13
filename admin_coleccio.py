from cataleg import Cataleg
from coleccio import Coleccio
from formularis import Nombre, pausar
from id import ID
from menu import Menu

class AdminColeccio(Menu):
	def __init__(self, coleccio_id: int, ref_coleccions: list[Coleccio], ref_cataleg: Cataleg, ids: ID):
		self.coleccio_id = coleccio_id
		self.ref_coleccions = ref_coleccions
		self.ref_cataleg = ref_cataleg
		self.ids = ids

		assert self.ids.existeix(self.coleccio_id), "L'ID no existeix"

		self.coleccio = None
		for l in self.ref_coleccions:
			if l.id == self.coleccio_id:
				self.coleccio = l
				break

		assert self.coleccio is not None, "El llibre que es vol administrar no existeix."

		super().__init__("Administrar col·lecció | " + (
				lambda t: t if len(t) <= 25 else (f'{t:.15}...'))(self.coleccio.nom))

	@Menu.menu(descr=lambda self: (f"{self.coleccio}\n{self.coleccio.descr}") if self.coleccio.descr is not None else str(self.coleccio))
	def __call__(self):
		pass

	@Menu.eina("Mostrar col·lecció", 1, cond=lambda self: len(self.coleccio) > 0)
	def mostrar_coleccio(self):
		assert self.coleccio is not None
		
		print(self.coleccio._quant())
		print()
		
		for p in self.coleccio:
			print(p)

		pausar(nova_linia=True)

	
	@Menu.eina("Afegir pel·lícula", 2)
	def afegir_pelicula(self):
		assert self.coleccio is not None
		
		self.ref_cataleg._mostrar()

		print()
		id = Nombre("ID de la pel·lícula", lambda n: self.ref_cataleg.ids.existeix(n), buit=True)()
		if id is None:
			return
		
		pelicula = None
		for p in self.ref_cataleg:
			if id == p.id:
				pelicula = p
				break
				
		assert pelicula is not None
		
		self.coleccio.afegir(pelicula)
				
	
	@Menu.eina("Treure pel·lícula", 3, cond=lambda self: len(self.coleccio) > 0)
	def treure_pelicula(self):
		pass
