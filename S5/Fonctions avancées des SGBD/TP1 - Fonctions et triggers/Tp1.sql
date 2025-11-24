/*Exercice 1.*/
CREATE OR REPLACE FUNCTION plus_longue_chaine(chaine1 text, chaine2 text)
RETURNS TEXT AS $$
BEGIN
    IF LENGTH(chaine1) >= LENGTH(CHAINE2) THEN
        RETURN chaine1;
    ELSE
        RETURN chaine2;
    END IF;
END; $$ LANGUAGE plpgsql;

SELECT plus_longue_chaine('Bonjour', 'Saluttt');

/*Exercice 2.*/
CREATE OR REPLACE FUNCTION afficher_mots(texte TEXT) 
RETURNS VOID AS $$
DECLARE
    mot TEXT;
    mots TEXT[];
BEGIN
    mots := string_to_array(texte, ' ');
    FOREACH mot IN ARRAY mots LOOP
        RAISE NOTICE '%', mot;
    END LOOP;
END; $$ LANGUAGE plpgsql;

SELECT afficher_mots('Test de la focntion afficher_mots');

/*Exercice 3.*/
CREATE OR REPLACE FUNCTION factorielle_iterative(a INTEGER)
RETURNS INTEGER AS $$
DECLARE
    resultat INTEGER := 1;
    i INTEGER;
BEGIN
	IF a<0 THEN
        RETURN NULL;
    ELSIF a<2 THEN
        RETURN a;
    ELSE
        FOR i IN 2..a LOOP
            resultat := resultat * i;
        END LOOP;
        RETURN resultat;
    END IF;
END; $$ LANGUAGE plpgsql;

SELECT factorielle_iterative(-1);

/*Exercice 4.*/
/*a)*/
SELECT SUM(duree) FROM films;

/*b)*/
CREATE OR REPLACE FUNCTION somme_duree_films() 
RETURNS INTEGER AS $$
DECLARE
    total INTEGER := 0;      
    x RECORD;              
BEGIN
    FOR x IN SELECT * FROM films LOOP
        total := total + x.duree;
    END LOOP;
    RETURN total;
END; 
$$ LANGUAGE plpgsql;

SELECT somme_duree_films();

/*Exercice 5.*/
SELECT AVG(prixAchat) FROM dvds;

CREATE OR REPLACE FUNCTION prix_moyen_films()
RETURNS FLOAT AS $$
DECLARE
	curs CURSOR FOR SELECT prixAchat FROM dvds;
    prix_total FLOAT := 0;
    nb_dvds INTEGER := 0;
    dvd_record RECORD;
BEGIN
	OPEN curs;
    LOOP
        FETCH curs INTO dvd_record;
        EXIT WHEN NOT FOUND;
        prix_total := prix_total + dvd_record.prixAchat;
        nb_dvds := nb_dvds + 1;
    END LOOP;
    CLOSE curs;
    RETURN prix_total / nb_dvds;
END; $$ LANGUAGE plpgsql;

SELECT prix_moyen_films();
/*Exercice 1.*/
CREATE OR REPLACE FUNCTION plus_longue_chaine(chaine1 text, chaine2 text)
RETURNS TEXT AS $$
BEGIN
    IF LENGTH(chaine1) >= LENGTH(CHAINE2) THEN
        RETURN chaine1;
    ELSE
        RETURN chaine2;
    END IF;
END; $$ LANGUAGE plpgsql;

SELECT plus_longue_chaine('Bonjour', 'Saluttt');

/*Exercice 2.*/
CREATE OR REPLACE FUNCTION afficher_mots(texte TEXT) 
RETURNS VOID AS $$
DECLARE
    mot TEXT;
    mots TEXT[];
BEGIN
    mots := string_to_array(texte, ' ');
    FOREACH mot IN ARRAY mots LOOP
        RAISE NOTICE '%', mot;
    END LOOP;
END; $$ LANGUAGE plpgsql;

SELECT afficher_mots('Test de la focntion afficher_mots');

/*Exercice 3.*/
CREATE OR REPLACE FUNCTION factorielle_iterative(a INTEGER)
RETURNS INTEGER AS $$
DECLARE
    resultat INTEGER := 1;
    i INTEGER;
BEGIN
	IF a<0 THEN
        RETURN NULL;
    ELSIF a<2 THEN
        RETURN a;
    ELSE
        FOR i IN 2..a LOOP
            resultat := resultat * i;
        END LOOP;
        RETURN resultat;
    END IF;
END; $$ LANGUAGE plpgsql;

SELECT factorielle_iterative(-1);

/*Exercice 4.*/
/*a)*/
SELECT SUM(duree) FROM films;

/*b)*/
CREATE OR REPLACE FUNCTION somme_duree_films() 
RETURNS INTEGER AS $$
DECLARE
    total INTEGER := 0;      
    x RECORD;              
BEGIN
    FOR x IN SELECT * FROM films LOOP
        total := total + x.duree;
    END LOOP;
    RETURN total;
END; 
$$ LANGUAGE plpgsql;

SELECT somme_duree_films();

/*Exercice 5.*/
SELECT AVG(prixAchat) FROM dvds;

CREATE OR REPLACE FUNCTION prix_moyen_films()
RETURNS FLOAT AS $$
DECLARE
	curs CURSOR FOR SELECT prixAchat FROM dvds;
    prix_total FLOAT := 0;
    nb_dvds INTEGER := 0;
    dvd_record RECORD;
BEGIN
	OPEN curs;
    LOOP
        FETCH curs INTO dvd_record;
		EXIT WHEN NOT FOUND;
        prix_total := prix_total + dvd_record.prixAchat;
        nb_dvds := nb_dvds + 1;
    END LOOP;
    CLOSE curs;
	 IF nb_dvds = 0 THEN
        RAISE EXCEPTION no_data_found;
	END IF;
    RETURN prix_total / nb_dvds;
END; $$ LANGUAGE plpgsql;

SELECT prix_moyen_films();

TRUNCATE  TABLE dvds CASCADE

/*Exercice 6.*/
ALTER TABLE locations DROP CONSTRAINT IF EXISTS locations_nodvd_fkey;
ALTER TABLE locations ADD CONSTRAINT locations_nodvd_fkey FOREIGN KEY (NoDVD) REFERENCES dvds(NoDVD) ON UPDATE CASCADE;
CREATE OR REPLACE FUNCTION renumeroter_nodvd() 
RETURNS void AS $$
DECLARE
    rec RECORD;
    new_id INTEGER := 1;
    old_id INTEGER;
BEGIN
    FOR rec IN SELECT NoDVD FROM dvds ORDER BY NoDVD LOOP
        old_id := rec.NoDVD;
        IF old_id != new_id THEN
            UPDATE dvds SET NoDVD = new_id WHERE NoDVD = old_id;
        END IF;
        new_id := new_id + 1;
    END LOOP;
END;
$$ LANGUAGE plpgsql;


SELECT  renumeroter_nodvd();

select nodvd from dvds order by nodvd;;

/*Exercice 7.*/
CREATE OR REPLACE FUNCTION exception_insertion_film()

RETURNS TRIGGER AS $$
BEGIN
    IF NEW.AnneeSortie IS NOT NULL AND NEW.AnneeSortie < 1891 THEN
        RAISE EXCEPTION 'Année de sortie invalide : %', NEW.AnneeSortie;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_insertion_film
BEFORE INSERT OR UPDATE ON films
FOR EACH ROW EXECUTE FUNCTION exception_insertion_film();

INSERT INTO films(titre, duree, anneeSortie) VALUES('test', 1201, 2024);
INSERT INTO films(titre, duree, anneeSortie) VALUES('test2', 100, 1800);


/*Exercice 8*/
CREATE OR REPLACE FUNCTION remplir_prix_achat_moyen()
RETURNS TRIGGER AS $$
DECLARE
    avg_prix INTEGER;
BEGIN
    IF NEW.prixAchat IS NOT NULL THEN
        RETURN NEW;
    END IF;

    SELECT AVG(prixAchat) INTO avg_prix
    FROM dvds
    WHERE Titre = NEW.Titre AND prixAchat IS NOT NULL;

    IF avg_prix IS NOT NULL THEN
        NEW.prixAchat := avg_prix;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_dvd_prix
BEFORE INSERT ON dvds
FOR EACH ROW EXECUTE FUNCTION remplir_prix_achat_moyen();

INSERT INTO dvds (NoDVD, Titre) VALUES (1008, '8 mm')
SELECT * FROM dvds WHERE NoDVD = 1008;



/*EXO9*/

CREATE OR REPLACE FUNCTION verifier_pk_clients()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.NoClient IS NULL THEN
        RAISE EXCEPTION 'La clé primaire ne peut pas être NULL';
    END IF;

    IF NEW.NoClient != OLD.NoClient OR OLD IS NULL THEN
        IF EXISTS (SELECT 1 FROM clients WHERE NoClient = NEW.NoClient) THEN
            RAISE EXCEPTION 'Un client % existe déjà', NEW.NoClient;
        END IF;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_verifier_pk_clients
BEFORE INSERT OR UPDATE ON clients
FOR EACH ROW EXECUTE FUNCTION verifier_pk_clients();


INSERT INTO clients VALUES (101, 'Jean B', '123 Rue ');
SELECT * FROM clients WHERE NoClient = 101;
UPDATE clients SET NomClient = 'Jean A' WHERE NoClient = 101;
SELECT * FROM clients WHERE NoClient = 101;

INSERT INTO clients VALUES (101, 'Jean azdazd', '123 Rue ');

SELECT * FROM clients WHERE NoClient = 101;




