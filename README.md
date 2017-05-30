Online trackovanie závodov
==========================
Autor: Richard Rožár
Bakalárska práca 2017



Postup bez inštalácie
=====================

WEBOVÁ APLIKÁCIA BUDE DOSTUPN8 NA rozar.eu DOMÉNE OD 31.5. 2017 DO 30.6. 2017

Prihlasovacie údaje:
admin
admin

Na stránke sú vopred pripravené údaje. Sú tam vytvorené všetky objekty, ktoré treba na vytvorenie pretekov a posielanie
údajov. Na stránke sú prístupné 2 preteky. Prvý je ukončený závod, ktorý sa dá pozrieť zo záznamu. Druhý
(má názov Prázdny) je pripravený na posielanie údajov.

V prípade ak chcete vyskúšať posielanie údajov v projekte pod /projekt/scripts/simulation môžete spustiť python script
, ktorý bude posielať údaje do pretekov.

Pre spustenie potrebujete mať nainštalovaný python 3.5 a balíček requests, ktorý nainštalujete príkazom:
pip install requests==2.13.0

Po nainštalovaní budete môcť spustiť skript na posielane údajov pomocou
python simulate.py 2 rozar.eu

Počas toho môžete navštíviť rozar.eu/race/2 , kde uvidíte posielané dáta. Pri skončení skriptu sa závod ukončí.

V prípade ak chcete skript simulate.py použiť aj na iný vami vytvorený závod potrebujete k tomu mať:
Presne 2 účastníkov v závode s číslami 1 a 2
Trať, ktorú nájdete na rozar.eu (Veľké Úľany)
Typ závodu, ktorý obsahuje jedine Tím a Čas (na rozar.eu pod admin užívateľom ako "Tajné")
Projekciu nastavenú na EPSG:3857
Musí ho vytvoriť účet admin a nesmie mať iné heslo ako "admin"

Zvyšné údaje závisia od vás. Skript potom zavoláte ako:
python simulate.py <id_pretekov> rozar.eu
Id pretekov viete získať z adresy aplikácie, rozar.eu/#/race/<id_pretekov>

V prípade ak vám chýba možnosť nejakého športu, typu závodu, alebo typu polí pre typ závodu, projekcie, tak ich môžete
pridať popr. zmeniť na rozar.eu/admin (prihlasovacie údaje sú admin/admin)



Ako posielať dáta manuálne?
===========================
Popísaná na <domena>/api resp. rozar.eu/api



Spustenie aplikácie na lokálnom počítači
========================================
Na spustenie aplikácie potrebujete docker a docker-compose (treba stiahnuť z https://www.docker.com/). V prípade ak
docker inštalujete na windows, tak zahŕňa v sebe aj docker-compose. Po nainštalovaní dockera potrebujete overiť:

Port 80 je voľný
Port 8000 je voľný
Port 5432 je voľný
Máte aspoň 2GB voľnej pamäte
Máte aspoň 5 GB voľného miesta na disku
Máte prístup na internet

Ak všetky požiadavky splňujete v adresári /projekt zavoláte príkaz
docker-compose build

Samotné buildovanie závisí na rýchlosti vášho internetu a rýchlosti počítača. Ukončenie buildovania by malo trvať
cca. 15 minút.

Potom následne treba zavolať príkaz:
docker-compose up

Po to ako príkaz skončí môžete prejsť do webového prehliadača a pristúpiť k webovej aplikácii cez domény:
localhost
127.0.0.1

Výsledok bude totožný s obsahom na rozar.eu. V prípade, ak chcete posielať údaje stačí zmeniť druhý parameter simulate.py
python simulate 2 "localhost:80"
