import requests
from bs4 import BeautifulSoup
from win10toast import ToastNotifier
from time import time, sleep

def main():

	print("-"*30)
	print("-"*30)

	payload = {
		'busqueda[tipo_viaje]': '1', 
		'busqueda[origen]': '481',
		'busqueda[destino]': '255',
		'busqueda[fecha_ida]': '18/12/2021',
		'busqueda[fecha_vuelta]': '09/01/2022',
		'busqueda[cantidad_pasajeros][adulto]': 1,
		'busqueda[cantidad_pasajeros][jubilado]': 0,
		'busqueda[cantidad_pasajeros][discapacitado]': 0,
		'busqueda[cantidad_pasajeros][menor]': 0,
		'busqueda[cantidad_pasajeros][bebe]': 0
	}
	tiene_resultado = False

	for i in range(1,30,7):
		payload['busqueda[fecha_ida]'] = "{}/12/2021".format(i)

		r = requests.post('https://webventas.sofse.gob.ar/calendario.php', data=payload)
		soup = BeautifulSoup(r.content, 'html.parser')

		calendario_web = soup.find(id="calendario_ida").find_all("div", class_="web")[0]
		dias_ida = calendario_web.find_all("div", class_="p-1")

		for d in dias_ida:
			lista_spans = d.find_all("span")

			estado = lista_spans[-1].text.lower()
			if estado == "no disponible":
				estado = "x"*5
			else:

				dia = lista_spans[0].text.split(" ")[0]
				if (dia == "VIE" or dia == "SAB" or dia == "DOM"):
					toaster = ToastNotifier()
					toaster.show_toast("HAY UN ESPACIO DISPONIBLE",lista_spans[0].text)
				
				tiene_resultado = True
				estado = lista_spans[2].text

			if lista_spans[0]['class'] == "dia_numero":
				print("*"*30)
				print("DISPONIBLE")
				print("*"*30)

			print(lista_spans[0].text + ": " + estado)
			print("-"*30)

		debug_output(i, r)

	if tiene_resultado:
		print("--- REVISAR RESULTADO ---")
	else:
		print("--- SIN NOVEDAD ---")

def debug_output(i, r):
	with open("{}_debug".format(i), 'w') as f:
			f.write(r.text)

while True:
	main()
	sleep(60*15)