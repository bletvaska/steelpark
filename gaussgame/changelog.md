# Changelog


## 2025.7.1

* rozsirenie dokumentacie o pokyny pre manazment projektu pomocou `uv`
* v modeli `Settings` bola nahradena konfiguracia pre MQTT pomocou `mqtt_uri`
    * vsetky parametre v jednom retazci
    * parsovanie je automaticke pomocou funkcie `urlparse()` z modulu ` urllib.parse`
* vo vystupe vysledkov pribudli data pre generovanie gaussovej krivky
    * pridana zavislost na modul `pandas`
    
