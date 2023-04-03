# Projet-programmation-HAI405I
Bibliothèque markdown: **showdown** convertir markdown syntaxe en html
- source :https://github.com/showdownjs/showdown

Bibliotheque latex:**mathJax** inclue des notions mathématiques sur la page
- source : https://docs.mathjax.org/en/latest/web/start.html
- source : src="https://www.tuhh.de/MathJax/MathJax.js?config=TeX-MML-AM_HTMLorMML">

Bibliothèque coloration de code : **Highlight** met en évidence les éléments clés d'un code source en utilisant des couleurs ou des styles différents
- Source:https://highlightjs.org/download/ 

Bibliothèque mermaid : **Mermaid API**
- Sources : https://mermaid.js.org/config/usage.html 
- https://github.com/mermaid-js/mermaid/issues/32 

## Installation

```bash
pip install flask
pip install flask-login
pip install email-validator
pip install pytz
pip install flask-sqlalchemy
pip install flask-socketio
pip install sqlite3
pip install wordcloud (il faut avoir une version de python inférieure à 3.7)
pip install indexer
pip install spellchecker

```

Run the program using 
```bash
python3 -m venv venv
source venv/bin/activate
#apres avoir instaler tout on pourra executer

python3 app.py 
```

Sources d'inspiration:
- Wikipedia
- Github
- ChatGPT
- W3schools: https://www.w3schools.com/html/
- Grafikart : https://grafikart.fr/tutoriels/javascript
- Mermaid: https://mermaid.js.org/config/usage.html
- codePen:https://codepen.io/eniotna/pen/
- MathJax https://docs.mathjax.org/
- Python :https://pythonbasics.org/


Liste de tout ce qu’on n'a pas fait :
- Fonction /coloration de code/ de manière dynamique
- les sequences de questions
- Connecter le markdown,mermaid et latex avec la saisie du texte pour la création des questions

Liens des sites web utilisés :
- SOCKET CONFIG : https://socket.io/docs/v4/client-installation/
- BOOTSTRAP : https://mdbootstrap.com/docs/standard/extended/textarea/
- BOOTSTRAP (barre de progrès) : https://www.w3schools.com/bootstrap/bootstrap_progressbars.asp
- JSON : https://developer.mozilla.org/fr/docs/Web/JavaScript/Reference/Global_Objects/JSON/stringify
- JINJA : https://jinja.palletsprojects.com/en/3.1.x/templates/
- JAVASCRIPT : https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch
- JAVASCRIPT : https://www.youtube.com/watch?v=pgWcJygAk4s
- FLASK : https://snyk.io/advisor/python/Flask/functions/flask.request.form.get
- NUAGES DE MOTS  :https://datascientest.com/wordcloud-python
- jsPDF : https://cdnjs.cloudflare.com/ajax/libs/jspdf/1.5.3/jspdf.debug.js
          https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.4.0/jspdf.umd.min.js

## Génération de contrôles

 ### Description

La génération de contrôle est une application web qui permet de générer deux types de contrôle, anonyme ou identifié en sélectionnant le nombre de question pour chaque étiquette dans le contrôle .
dans notre cas on a 4 étiquettes de question qui sont : JAVA ,compilation,PHP ,Python

Fonctionnalités

   - Ajouter/supprimer des étiquettes.
   - Sélectionner le type de copie soit anonyme  soit identifié .
   - Sélectionner le type de génération de question soit basique soit avancé .
   - Sélectionner l’affichage des questions dans des contrôles soit à l’ordre des étiquette c’est-à-dire les   questions avec étiquette JAVA puis celles avec étiquette compila-tion puis celles de PHP et en fin Python ,soit de manière aléatoire 
   - Imprimer des contrôles .


