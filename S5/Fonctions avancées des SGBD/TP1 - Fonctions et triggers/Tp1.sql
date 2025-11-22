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
    IF a<2 THEN
        RETURN a;
    ELSE
        FOR i IN 2..a LOOP
            resultat := resultat * i;
        END LOOP;
        RETURN resultat;
    END IF;
END; $$ LANGUAGE plpgsql;

SELECT factorielle_iterative(5);