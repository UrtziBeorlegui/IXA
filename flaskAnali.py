from flask import Flask, render_template, request
from forms import bilatuForm
from flask_bootstrap import Bootstrap
import Analisis

Analisis.initializeAnalizador()
app = Flask(__name__)
app.config["SECRET_KEY"] = "5f3e0c21c011f36d8a789b2ba07dba47092c8983"
Bootstrap(app)


@app.route("/", methods = ["GET", "POST"])
def home():

    formhitza = bilatuForm()
    analisia = None
    sarrerak = []
    sarrerak2 = []

    if formhitza.validate_on_submit():
        textua = formhitza.hitza.data
        analisia = Analisis.analizarPalabra(textua)
        sarrerak = analisia.getinformation()
        print(f"sarerrak\n {sarrerak}")
        sarrerak2 = []
        sarrerak3 = []
        for n in sarrerak:
            aux = n.split(",")
            if aux[len(aux) - 1] == "" or aux[len(aux) - 1] == " ":
                sarrerak2.append(aux[:len(aux) - 1])
            else:
             sarrerak2.append(aux)
    return render_template("bilatu.html", title = "Anali", formhitza=formhitza, textua = sarrerak2, textua2 = sarrerak)


if __name__ == "__main__":
        app.run(debug=True)
