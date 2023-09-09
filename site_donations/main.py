from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Configuration de la base de données
db = mysql.connector.connect(
    host="localhost",
    port ="3307",
    user="root",
    password="example",
    database="donation",
)
cursor = db.cursor()

# Page d"accueil
@app.route("/")
def index():
    return render_template("index.html")

# Page du formulaire
@app.route("/donate", methods=["GET", "POST"])
def donate():
    if request.method == "POST":
        # Récupérer les données du formulaire
        nom = request.form["name"]
        email = request.form["email"]
        prix = request.form["amount"]
        # ... autres champs

        # Insérer les données dans la base de données
        query = "INSERT INTO donations (nom, email, prix) VALUES (%s, %s, %s)"
        valeur = (nom, email, prix)
        cursor.execute(query, valeur)
        db.commit()

        return redirect(url_for("donations"))

    return render_template("donate.html")

# Page des promesses de don
@app.route("/donations")
def donations():
    query = "SELECT nom, email, prix FROM donations"
    cursor.execute(query)
    donations = cursor.fetchall()
    total_query = "SELECT SUM(prix) FROM donations"
    cursor.execute(total_query)
    total_collected = cursor.fetchone()[0]
    return render_template("donations.html", donations=donations, total_collected=total_collected)

if __name__ == "__main__":
    app.run(debug=True)