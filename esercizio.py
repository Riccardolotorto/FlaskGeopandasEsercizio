#realizzare un sito web che permetta all'utente di avere una mappa di un quartiere con le fontanelle. L'utente seleziona da un menù a tendina il nome del quartiere, clicca
#su un bottone e ottiene la mappa del quartiere scelto con le fontanelle. 


from flask import Flask, render_template, request, Response
app = Flask(__name__)

import geopandas as gpd
Quartieri = gpd.read_file('Quartieri/NIL_WM.shp')
Fontanelle = gpd.read_file('Fontanelle/Fontanelle_OSM_ODbL.shp')


@app.route('/', methods=['GET'])
def elenco_quartieri():
    nomi=Quartieri['NIL'].to_list()
    nomi.sort()
    return render_template('quartiere.html', nomi=nomi)


@app.route('/mappa', methods=['GET'])
def mappa():
    nomeQuartiere = request.args.get("quartiere")
    return render_template('mappa.html', nome = nomeQuartiere)

import io
import contextily
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib
import matplotlib.pyplot as plt


@app.route('/immagine', methods=['GET'])
def immagine():
    nome = request.args.get("q")
    quartiereScelto = Quartieri[Quartieri['NIL']== nome]
    fontaneIntersezione = Fontanelle[Fontanelle.intersects(quartiereScelto.geometry.item())]
    #creo il grafico
    fig, ax = plt.subplots(figsize = (12,8))
    quartiereScelto.to_crs(epsg=3857).plot(ax=ax, alpha=0.5)
    fontaneIntersezione.to_crs(3857).plot(ax = ax, markersize = 20, color = "Red")
    contextily.add_basemap(ax=ax)
    #converto il grafico in un'immagine
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png') #minetype: tipo del file che vogliamo
    #Respose: restituisce un numero, un oggetto o altro (non pagine html)

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)

