Nume: Predescu Ioan-Alexandru
Grupă: 333CB

# Tema 1 TODO
#### Este recomandat să folosiți diacritice. Se poate opta și pentru realizarea în limba engleză. 

Organizare
-
1. Explicație pentru soluția aleasă:

  Mi-am creeat un ThreadPool in care am un vector de threaduri care asteapta sa primeasca taskuri. Cand un task este adaugat
  in ThreadPool, unul dintre threaduri va prelua taskul si il va executa. Dupa ce taskul este executat, threadul va astepta
  sa primeasca un alt task. Daca nu mai sunt taskuri de executat, threadul va astepta pana cand va fi adaugat un task in ThreadPool.
  Pentru parsarea csv-ului m-am folosit de pandas. Cred ca timpul de executie al programului este destul de mare din cauza asta,
  dar si pentru ca imi incarc tot csv-ul, dupa care il parsez in functie de taskul primit.
  Tema a fost destul de interesanta, pentru ca am lucrat cu un backend.



Implementare
-

1. `ThreadPool` - clasa care implementează un thread pool.
  Am ca si atribute un vector de threaduri, o coada de taskuri si un lock care ma ajuta sa sincronizez la adaugarea unui task intr-o
  lista in care am doar task-uri done. De asemenea mai am o lista in care am task-urile submise.

2. `TaskRunner` - clasa care implementează un thread care primește taskuri dintr-o coadă și le execută.
  Cat timp ThreadPool-ul este activ, TaskRunner-ul va astepta sa primeasca un task. Dupa ce primeste un task, il va executa.
  Cand acesta devine inactiv, va executa toate task-urile ramase in coada de task-uri si va iesi din bucla.

  Ce ar fi fost util, un mini tutorial de Postman pentru a testa API-ul.
  Chiar daca am mai lucrat cu el ar fi fost bine venit, ca nu s-a facut asta la facultate.



Resurse utilizate
- 
ocw, lab 4 

* Resurse utilizate - toate resursele publice de pe internet/cărți/code snippets, chiar dacă sunt laboratoare de ASC

Git
-
1. Link către repo-ul de git
https://github.com/alexandru2908/ASC-1

Ce să **NU**
-
* Detalii de implementare despre fiecare funcție/fișier în parte
* Fraze lungi care să ocolească subiectul în cauză
* Răspunsuri și idei neargumentate
* Comentarii (din cod) și *TODO*-uri


