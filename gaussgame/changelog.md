# Changelog


## 2025.7.1

* zmeny len v gaussovi
* rozsirenie dokumentacie o pokyny pre manazment projektu pomocou `uv`
* v modeli `Settings` bola nahradena konfiguracia pre MQTT pomocou `mqtt_uri`
    * vsetky parametre v jednom retazci
    * parsovanie je automaticke pomocou funkcie `urlparse()` z modulu ` urllib.parse`
    * upraveny `context.py` ako aj `bridge.py`
* vo vystupe vysledkov pribudli data pre generovanie gaussovej krivky
    * pridana zavislost na modul `pandas`
* pridany `template.env` pre docker kompoziciu 
    