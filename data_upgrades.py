# -*- coding: utf-8 -*-
"""
DEUTSCH A1 PRO — Advanced Pedagogy Datasets:
1. Plural Trainer (60 A1 nouns across all 5 plural patterns + Umlaut)
2. Verb Conjugation Trainer (50 drills for irregular Präsens, Vokalwechsel, Modals, Auxiliaries)
3. A1 Graded Mini-Stories (4 authentic interactive stories with audio text and comprehension checks)
"""

# ==============================================================================
# 1. PLURAL TRAINER DATASET (60 A1 Nouns)
# Patterns:
# - "-er" (+/- Umlaut): Kind -> Kinder, Buch -> Bücher
# - "-e" (+/- Umlaut): Tag -> Tage, Stuhl -> Stühle
# - "-(e)n": Frau -> Frauen, Lampe -> Lampen, Herr -> Herren
# - "-s": Auto -> Autos, Hotel -> Hotels, Handy -> Handys
# - "-" (unverändert +/- Umlaut): Apfel -> Äpfel, Zimmer -> Zimmer
# ==============================================================================
PLURAL_TRAINER_WORDS = [
    # Pattern: -er / -¨er
    {
        "id": 1,
        "singular": "das Kind",
        "word": "Kind",
        "article": "das",
        "plural": "die Kinder",
        "plural_word": "Kinder",
        "pattern": "-er",
        "rule_explanation": "საშუალო სქესის ერთმარცვლიანი სიტყვები ხშირად იღებენ -er დაბოლოებას: das Kind -> die Kinder.",
        "translation_ka": "ბავშვი / ბავშვები",
        "options": ["die Kinde", "die Kinder", "die Kindes", "die Kind"]
    },
    {
        "id": 2,
        "singular": "das Buch",
        "word": "Buch",
        "article": "das",
        "plural": "die Bücher",
        "plural_word": "Bücher",
        "pattern": "-¨er",
        "rule_explanation": "ხმოვანი u გადადის ü-ში (Umlaut) და ემატება -er: das Buch -> die Bücher.",
        "translation_ka": "წიგნი / წიგნები",
        "options": ["die Buche", "die Büchern", "die Bücher", "die Buchs"]
    },
    {
        "id": 3,
        "singular": "das Bild",
        "word": "Bild",
        "article": "das",
        "plural": "die Bilder",
        "plural_word": "Bilder",
        "pattern": "-er",
        "rule_explanation": "das Bild იღებს -er დაბოლოებას მრავლობითში: die Bilder.",
        "translation_ka": "სურათი / სურათები",
        "options": ["die Bilde", "die Bilder", "die Bilden", "die Bilds"]
    },
    {
        "id": 4,
        "singular": "das Haus",
        "word": "Haus",
        "article": "das",
        "plural": "die Häuser",
        "plural_word": "Häuser",
        "pattern": "-¨er",
        "rule_explanation": "au გადადის äu-ში და ემატება -er: das Haus -> die Häuser.",
        "translation_ka": "სახლი / სახლები",
        "options": ["die Hause", "die Häuser", "die Hausen", "die Häusern"]
    },
    {
        "id": 5,
        "singular": "das Kleid",
        "word": "Kleid",
        "article": "das",
        "plural": "die Kleider",
        "plural_word": "Kleider",
        "pattern": "-er",
        "rule_explanation": "das Kleid იღებს -er დაბოლოებას: die Kleider.",
        "translation_ka": "კაბა / კაბები",
        "options": ["die Kleide", "die Kleider", "die Kleiden", "die Kleids"]
    },
    {
        "id": 6,
        "singular": "das Licht",
        "word": "Licht",
        "article": "das",
        "plural": "die Lichter",
        "plural_word": "Lichter",
        "pattern": "-er",
        "rule_explanation": "das Licht იღებს -er დაბოლოებას: die Lichter.",
        "translation_ka": "სინათლე / სინათლეები",
        "options": ["die Lichte", "die Lichter", "die Lichten", "die Lichts"]
    },
    {
        "id": 7,
        "singular": "das Ei",
        "word": "Ei",
        "article": "das",
        "plural": "die Eier",
        "plural_word": "Eier",
        "pattern": "-er",
        "rule_explanation": "das Ei იღებს -er დაბოლოებას: die Eier.",
        "translation_ka": "კვერცხი / კვერცხები",
        "options": ["die Eine", "die Eier", "die Eien", "die Eis"]
    },
    {
        "id": 8,
        "singular": "das Wort",
        "word": "Wort",
        "article": "das",
        "plural": "die Wörter",
        "plural_word": "Wörter",
        "pattern": "-¨er",
        "rule_explanation": "o იღებს უმლაუტს ö და ემატება -er: das Wort -> die Wörter (ცალკეული სიტყვები).",
        "translation_ka": "სიტყვა / სიტყვები",
        "options": ["die Worte", "die Wörtern", "die Wörter", "die Worten"]
    },
    {
        "id": 9,
        "singular": "das Fahrrad",
        "word": "Fahrrad",
        "article": "das",
        "plural": "die Fahrräder",
        "plural_word": "Fahrräder",
        "pattern": "-¨er",
        "rule_explanation": "Rad გადადის Räder-ში: das Fahrrad -> die Fahrräder.",
        "translation_ka": "ველოსიპედი / ველოსიპედები",
        "options": ["die Fahrrade", "die Fahrräder", "die Fahrrads", "die Fahrraden"]
    },
    {
        "id": 10,
        "singular": "der Mann",
        "word": "Mann",
        "article": "der",
        "plural": "die Männer",
        "plural_word": "Männer",
        "pattern": "-¨er",
        "rule_explanation": "მამრობითი სქესის გამონაკლისი: a იღებს უმლაუტს ä და ემატება -er: der Mann -> die Männer.",
        "translation_ka": "კაცი / კაცები",
        "options": ["die Manne", "die Männer", "die Mannen", "die Manns"]
    },

    # Pattern: -e / -¨e
    {
        "id": 11,
        "singular": "der Tag",
        "word": "Tag",
        "article": "der",
        "plural": "die Tage",
        "plural_word": "Tage",
        "pattern": "-e",
        "rule_explanation": "მამრობითი სქესის არსებითი სახელების უმრავლესობა მრავლობითში იღებს -e-ს: der Tag -> die Tage.",
        "translation_ka": "დღე / დღეები",
        "options": ["die Tagen", "die Tage", "die Täge", "die Tags"]
    },
    {
        "id": 12,
        "singular": "der Tisch",
        "word": "Tisch",
        "article": "der",
        "plural": "die Tische",
        "plural_word": "Tische",
        "pattern": "-e",
        "rule_explanation": "der Tisch იღებს -e დაბოლოებას: die Tische.",
        "translation_ka": "მაგიდა / მაგიდები",
        "options": ["die Tischen", "die Tische", "die Tischer", "die Tischs"]
    },
    {
        "id": 13,
        "singular": "der Stuhl",
        "word": "Stuhl",
        "article": "der",
        "plural": "die Stühle",
        "plural_word": "Stühle",
        "pattern": "-¨e",
        "rule_explanation": "ხმოვანი u იღებს უმლაუტს ü და ემატება -e: der Stuhl -> die Stühle.",
        "translation_ka": "სკამი / სკამები",
        "options": ["die Stuhle", "die Stühle", "die Stühlen", "die Stühler"]
    },
    {
        "id": 14,
        "singular": "der Arzt",
        "word": "Arzt",
        "article": "der",
        "plural": "die Ärzte",
        "plural_word": "Ärzte",
        "pattern": "-¨e",
        "rule_explanation": "a გადადის ä-ში და ემატება -e: der Arzt -> die Ärzte.",
        "translation_ka": "ექიმი / ექიმები",
        "options": ["die Arzte", "die Ärzte", "die Ärzten", "die Arzts"]
    },
    {
        "id": 15,
        "singular": "der Ball",
        "word": "Ball",
        "article": "der",
        "plural": "die Bälle",
        "plural_word": "Bälle",
        "pattern": "-¨e",
        "rule_explanation": "der Ball -> die Bälle (უმლაუტი + e).",
        "translation_ka": "ბურთი / ბურთები",
        "options": ["die Balle", "die Bälle", "die Ballen", "die Bäller"]
    },
    {
        "id": 16,
        "singular": "der Freund",
        "word": "Freund",
        "article": "der",
        "plural": "die Freunde",
        "plural_word": "Freunde",
        "pattern": "-e",
        "rule_explanation": "der Freund იღებს -e დაბოლოებას: die Freunde.",
        "translation_ka": "მეგობარი / მეგობრები",
        "options": ["die Freunden", "die Freunde", "die Freunder", "die Freunds"]
    },
    {
        "id": 17,
        "singular": "der Hund",
        "word": "Hund",
        "article": "der",
        "plural": "die Hunde",
        "plural_word": "Hunde",
        "pattern": "-e",
        "rule_explanation": "der Hund იღებს -e დაბოლოებას: die Hunde (არა უმლაუტი!).",
        "translation_ka": "ძაღლი / ძაღლები",
        "options": ["die Hünde", "die Hunde", "die Hunden", "die Hunds"]
    },
    {
        "id": 18,
        "singular": "der Schuh",
        "word": "Schuh",
        "article": "der",
        "plural": "die Schuhe",
        "plural_word": "Schuhe",
        "pattern": "-e",
        "rule_explanation": "der Schuh იღებს -e დაბოლოებას: die Schuhe.",
        "translation_ka": "ფეხსაცმელი / ფეხსაცმელები",
        "options": ["die Schuhen", "die Schuhe", "die Schühe", "die Schuhs"]
    },
    {
        "id": 19,
        "singular": "das Jahr",
        "word": "Jahr",
        "article": "das",
        "plural": "die Jahre",
        "plural_word": "Jahre",
        "pattern": "-e",
        "rule_explanation": "საშუალო სქესის სიტყვა das Jahr მრავლობითში იღებს -e-ს: die Jahre.",
        "translation_ka": "წელი / წლები",
        "options": ["die Jahren", "die Jahre", "die Jähre", "die Jahrs"]
    },
    {
        "id": 20,
        "singular": "der Brief",
        "word": "Brief",
        "article": "der",
        "plural": "die Briefe",
        "plural_word": "Briefe",
        "pattern": "-e",
        "rule_explanation": "der Brief იღებს -e დაბოლოებას: die Briefe.",
        "translation_ka": "წერილი / წერილები",
        "options": ["die Briefen", "die Briefe", "die Briefer", "die Briefs"]
    },
    {
        "id": 21,
        "singular": "der Monat",
        "word": "Monat",
        "article": "der",
        "plural": "die Monate",
        "plural_word": "Monate",
        "pattern": "-e",
        "rule_explanation": "der Monat იღებს -e დაბოლოებას: die Monate (არ იღებს უმლაუტს!).",
        "translation_ka": "თვე / თვეები",
        "options": ["die Monaten", "die Monate", "die Mönate", "die Monats"]
    },
    {
        "id": 22,
        "singular": "der Zug",
        "word": "Zug",
        "article": "der",
        "plural": "die Züge",
        "plural_word": "Züge",
        "pattern": "-¨e",
        "rule_explanation": "u გადადის ü-ში და ემატება -e: der Zug -> die Züge.",
        "translation_ka": "მატარებელი / მატარებლები",
        "options": ["die Zuge", "die Züge", "die Zügen", "die Züger"]
    },

    # Pattern: -(e)n
    {
        "id": 23,
        "singular": "die Frau",
        "word": "Frau",
        "article": "die",
        "plural": "die Frauen",
        "plural_word": "Frauen",
        "pattern": "-en",
        "rule_explanation": "მდედრობითი სქესის სახელთა თითქმის 95% მრავლობითში იღებს -(e)n-ს: die Frau -> die Frauen.",
        "translation_ka": "ქალი / ქალები",
        "options": ["die Fraue", "die Frauen", "die Fräuer", "die Fraus"]
    },
    {
        "id": 24,
        "singular": "die Lampe",
        "word": "Lampe",
        "article": "die",
        "plural": "die Lampen",
        "plural_word": "Lampen",
        "pattern": "-n",
        "rule_explanation": "თუ მდედრობითი სახელი მთავრდება -e-ზე, ემატება მხოლოდ -n: die Lampe -> die Lampen.",
        "translation_ka": "ნათურა / ნათურები",
        "options": ["die Lamper", "die Lampen", "die Lampe", "die Lampes"]
    },
    {
        "id": 25,
        "singular": "die Tasche",
        "word": "Tasche",
        "article": "die",
        "plural": "die Taschen",
        "plural_word": "Taschen",
        "pattern": "-n",
        "rule_explanation": "die Tasche -> die Taschen.",
        "translation_ka": "ჩანთა / ჩანთები",
        "options": ["die Tascher", "die Taschen", "die Täsche", "die Tasches"]
    },
    {
        "id": 26,
        "singular": "die Sprache",
        "word": "Sprache",
        "article": "die",
        "plural": "die Sprachen",
        "plural_word": "Sprachen",
        "pattern": "-n",
        "rule_explanation": "die Sprache -> die Sprachen.",
        "translation_ka": "ენა / ენები",
        "options": ["die Sprächer", "die Sprachen", "die Spräche", "die Sprachs"]
    },
    {
        "id": 27,
        "singular": "die Wohnung",
        "word": "Wohnung",
        "article": "die",
        "plural": "die Wohnungen",
        "plural_word": "Wohnungen",
        "pattern": "-en",
        "rule_explanation": "-ung დაბოლოებიანი სახელები ყოველთვის იღებენ -en-ს: die Wohnung -> die Wohnungen.",
        "translation_ka": "ბინა / ბინები",
        "options": ["die Wohnunge", "die Wohnungen", "die Wohnungs", "die Wöhnung"]
    },
    {
        "id": 28,
        "singular": "die Zeitung",
        "word": "Zeitung",
        "article": "die",
        "plural": "die Zeitungen",
        "plural_word": "Zeitungen",
        "pattern": "-en",
        "rule_explanation": "-ung ბოლოკიდური -> -en: die Zeitung -> die Zeitungen.",
        "translation_ka": "გაზეთი / გაზეთები",
        "options": ["die Zeitunge", "die Zeitungen", "die Zeitungs", "die Zeiter"]
    },
    {
        "id": 29,
        "singular": "die Blume",
        "word": "Blume",
        "article": "die",
        "plural": "die Blumen",
        "plural_word": "Blumen",
        "pattern": "-n",
        "rule_explanation": "die Blume -> die Blumen.",
        "translation_ka": "ყვავილი / ყვავილები",
        "options": ["die Blüme", "die Blumen", "die Blumer", "die Blumes"]
    },
    {
        "id": 30,
        "singular": "die Frage",
        "word": "Frage",
        "article": "die",
        "plural": "die Fragen",
        "plural_word": "Fragen",
        "pattern": "-n",
        "rule_explanation": "die Frage -> die Fragen.",
        "translation_ka": "კითხვა / კითხვები",
        "options": ["die Fräge", "die Fragen", "die Frager", "die Frages"]
    },
    {
        "id": 31,
        "singular": "die Karte",
        "word": "Karte",
        "article": "die",
        "plural": "die Karten",
        "plural_word": "Karten",
        "pattern": "-n",
        "rule_explanation": "die Karte -> die Karten.",
        "translation_ka": "ბარათი / ბარათები",
        "options": ["die Kärte", "die Karten", "die Karter", "die Kartes"]
    },
    {
        "id": 32,
        "singular": "die Flasche",
        "word": "Flasche",
        "article": "die",
        "plural": "die Flaschen",
        "plural_word": "Flaschen",
        "pattern": "-n",
        "rule_explanation": "die Flasche -> die Flaschen.",
        "translation_ka": "ბოთლი / ბოთლები",
        "options": ["die Fläsche", "die Flaschen", "die Flascher", "die Flasches"]
    },
    {
        "id": 33,
        "singular": "die Katze",
        "word": "Katze",
        "article": "die",
        "plural": "die Katzen",
        "plural_word": "Katzen",
        "pattern": "-n",
        "rule_explanation": "die Katze -> die Katzen.",
        "translation_ka": "კატა / კატები",
        "options": ["die Kätze", "die Katzen", "die Katzer", "die Katzes"]
    },
    {
        "id": 34,
        "singular": "die Schwester",
        "word": "Schwester",
        "article": "die",
        "plural": "die Schwestern",
        "plural_word": "Schwestern",
        "pattern": "-n",
        "rule_explanation": "-er-ზე დაბოლოებული მდედრობითი სახელი იღებს -n-ს: die Schwester -> die Schwestern.",
        "translation_ka": "და / დები",
        "options": ["die Schwäster", "die Schwestern", "die Schwestere", "die Schwesters"]
    },
    {
        "id": 35,
        "singular": "die Schule",
        "word": "Schule",
        "article": "die",
        "plural": "die Schulen",
        "plural_word": "Schulen",
        "pattern": "-n",
        "rule_explanation": "die Schule -> die Schulen.",
        "translation_ka": "სკოლა / სკოლები",
        "options": ["die Schüle", "die Schulen", "die Schuler", "die Schules"]
    },
    {
        "id": 36,
        "singular": "der Student",
        "word": "Student",
        "article": "der",
        "plural": "die Studenten",
        "plural_word": "Studenten",
        "pattern": "-en",
        "rule_explanation": "სუსტი ბრუნების მამრობითი სახელები იღებენ -en-ს: der Student -> die Studenten.",
        "translation_ka": "სტუდენტი / სტუდენტები",
        "options": ["die Studente", "die Studenten", "die Studenter", "die Students"]
    },
    {
        "id": 37,
        "singular": "der Herr",
        "word": "Herr",
        "article": "der",
        "plural": "die Herren",
        "plural_word": "Herren",
        "pattern": "-en",
        "rule_explanation": "der Herr -> die Herren.",
        "translation_ka": "ბატონი / ბატონები",
        "options": ["die Herre", "die Herren", "die Herrs", "die Herrer"]
    },

    # Pattern: -s
    {
        "id": 38,
        "singular": "das Auto",
        "word": "Auto",
        "article": "das",
        "plural": "die Autos",
        "plural_word": "Autos",
        "pattern": "-s",
        "rule_explanation": "ნასესხები სიტყვები და ხმოვანზე (a, o, u, i, y) დაბოლოებული სახელები იღებენ -s დაბოლოებას: das Auto -> die Autos.",
        "translation_ka": "მანქანა / მანქანები",
        "options": ["die Autoen", "die Autos", "die Autoe", "die Autoer"]
    },
    {
        "id": 39,
        "singular": "das Foto",
        "word": "Foto",
        "article": "das",
        "plural": "die Fotos",
        "plural_word": "Fotos",
        "pattern": "-s",
        "rule_explanation": "das Foto -> die Fotos.",
        "translation_ka": "ფოტო / ფოტოები",
        "options": ["die Fotoen", "die Fotos", "die Föter", "die Fotoe"]
    },
    {
        "id": 40,
        "singular": "das Hotel",
        "word": "Hotel",
        "article": "das",
        "plural": "die Hotels",
        "plural_word": "Hotels",
        "pattern": "-s",
        "rule_explanation": "das Hotel -> die Hotels.",
        "translation_ka": "სასტუმრო / სასტუმროები",
        "options": ["die Hoteler", "die Hotels", "die Hotelen", "die Hotele"]
    },
    {
        "id": 41,
        "singular": "das Handy",
        "word": "Handy",
        "article": "das",
        "plural": "die Handys",
        "plural_word": "Handys",
        "pattern": "-s",
        "rule_explanation": "-y-ზე დაბოლოებული ნასესხები სიტყვა -> -s: das Handy -> die Handys.",
        "translation_ka": "მობილური / მობილურები",
        "options": ["die Handyen", "die Handys", "die Handies", "die Handye"]
    },
    {
        "id": 42,
        "singular": "das Restaurant",
        "word": "Restaurant",
        "article": "das",
        "plural": "die Restaurants",
        "plural_word": "Restaurants",
        "pattern": "-s",
        "rule_explanation": "ფრანგულიდან ნასესხები სიტყვა -> -s: das Restaurant -> die Restaurants.",
        "translation_ka": "რესტორანი / რესტორნები",
        "options": ["die Restaurante", "die Restaurants", "die Restauranten", "die Restauranter"]
    },
    {
        "id": 43,
        "singular": "das Sofa",
        "word": "Sofa",
        "article": "das",
        "plural": "die Sofas",
        "plural_word": "Sofas",
        "pattern": "-s",
        "rule_explanation": "-a-ზე დაბოლოებული სიტყვა -> -s: das Sofa -> die Sofas.",
        "translation_ka": "დივანი / დივნები",
        "options": ["die Sofae", "die Sofas", "die Sofaen", "die Söfer"]
    },
    {
        "id": 44,
        "singular": "das Café",
        "word": "Café",
        "article": "das",
        "plural": "die Cafés",
        "plural_word": "Cafés",
        "pattern": "-s",
        "rule_explanation": "das Café -> die Cafés.",
        "translation_ka": "კაფე / კაფეები",
        "options": ["die Caféen", "die Cafés", "die Caféer", "die Cafée"]
    },
    {
        "id": 45,
        "singular": "der Park",
        "word": "Park",
        "article": "der",
        "plural": "die Parks",
        "plural_word": "Parks",
        "pattern": "-s",
        "rule_explanation": "der Park -> die Parks.",
        "translation_ka": "პარკი / პარკები",
        "options": ["die Parke", "die Parks", "die Pärke", "die Parken"]
    },
    {
        "id": 46,
        "singular": "das Taxi",
        "word": "Taxi",
        "article": "das",
        "plural": "die Taxis",
        "plural_word": "Taxis",
        "pattern": "-s",
        "rule_explanation": "-i-ზე დაბოლოებული სიტყვა -> -s: das Taxi -> die Taxis.",
        "translation_ka": "ტაქსი / ტაქსები",
        "options": ["die Taxien", "die Taxis", "die Taxie", "die Taxies"]
    },
    {
        "id": 47,
        "singular": "das Ticket",
        "word": "Ticket",
        "article": "das",
        "plural": "die Tickets",
        "plural_word": "Tickets",
        "pattern": "-s",
        "rule_explanation": "das Ticket -> die Tickets.",
        "translation_ka": "ბილეთი / ბილეთები",
        "options": ["die Tickete", "die Tickets", "die Ticketen", "die Ticketer"]
    },

    # Pattern: - / -¨ (Unverändert +/- Umlaut)
    {
        "id": 48,
        "singular": "der Apfel",
        "word": "Apfel",
        "article": "der",
        "plural": "die Äpfel",
        "plural_word": "Äpfel",
        "pattern": "-¨",
        "rule_explanation": "-el დაბოლოებიანი მამრობითი სიტყვები დაბოლოებას არ იღებენ, მხოლოდ უმლაუტი ემატებათ: der Apfel -> die Äpfel.",
        "translation_ka": "ვაშლი / ვაშლები",
        "options": ["die Apfeln", "die Äpfel", "die Apfele", "die Apfels"]
    },
    {
        "id": 49,
        "singular": "der Bruder",
        "word": "Bruder",
        "article": "der",
        "plural": "die Brüder",
        "plural_word": "Brüder",
        "pattern": "-¨",
        "rule_explanation": "u გადადის ü-ში, დაბოლოება არ ემატება: der Bruder -> die Brüder.",
        "translation_ka": "ძმა / ძმები",
        "options": ["die Brudere", "die Brüder", "die Brudern", "die Bruders"]
    },
    {
        "id": 50,
        "singular": "die Mutter",
        "word": "Mutter",
        "article": "die",
        "plural": "die Mütter",
        "plural_word": "Mütter",
        "pattern": "-¨",
        "rule_explanation": "u იღებს უმლაუტს ü: die Mutter -> die Mütter.",
        "translation_ka": "დედა / დედები",
        "options": ["die Muttern", "die Mütter", "die Muttere", "die Mutters"]
    },
    {
        "id": 51,
        "singular": "die Tochter",
        "word": "Tochter",
        "article": "die",
        "plural": "die Töchter",
        "plural_word": "Töchter",
        "pattern": "-¨",
        "rule_explanation": "o იღებს უმლაუტს ö: die Tochter -> die Töchter.",
        "translation_ka": "ქალიშვილი / ქალიშვილები",
        "options": ["die Tochtern", "die Töchter", "die Tochtere", "die Tochters"]
    },
    {
        "id": 52,
        "singular": "der Vater",
        "word": "Vater",
        "article": "der",
        "plural": "die Väter",
        "plural_word": "Väter",
        "pattern": "-¨",
        "rule_explanation": "a იღებს უმლაუტს ä: der Vater -> die Väter.",
        "translation_ka": "მამა / მამები",
        "options": ["die Vatern", "die Väter", "die Vatere", "die Vaters"]
    },
    {
        "id": 53,
        "singular": "das Fenster",
        "word": "Fenster",
        "article": "das",
        "plural": "die Fenster",
        "plural_word": "Fenster",
        "pattern": "-",
        "rule_explanation": "-er დაბოლოებიანი საშუალო სქესის სიტყვა მრავლობითში სრულიად უცვლელია: das Fenster -> die Fenster.",
        "translation_ka": "ფანჯარა / ფანჯრები",
        "options": ["die Fenstern", "die Fenster", "die Fenstere", "die Fensters"]
    },
    {
        "id": 54,
        "singular": "das Zimmer",
        "word": "Zimmer",
        "article": "das",
        "plural": "die Zimmer",
        "plural_word": "Zimmer",
        "pattern": "-",
        "rule_explanation": "das Zimmer -> die Zimmer (არ იცვლება).",
        "translation_ka": "ოთახი / ოთახები",
        "options": ["die Zimmern", "die Zimmer", "die Zimmere", "die Zimmers"]
    },
    {
        "id": 55,
        "singular": "der Lehrer",
        "word": "Lehrer",
        "article": "der",
        "plural": "die Lehrer",
        "plural_word": "Lehrer",
        "pattern": "-",
        "rule_explanation": "-er დაბოლოებიანი მამრობითი პროფესიები არ იცვლება: der Lehrer -> die Lehrer.",
        "translation_ka": "მასწავლებელი / მასწავლებლები",
        "options": ["die Lehrern", "die Lehrer", "die Lehrere", "die Lehrers"]
    },
    {
        "id": 56,
        "singular": "der Schüler",
        "word": "Schüler",
        "article": "der",
        "plural": "die Schüler",
        "plural_word": "Schüler",
        "pattern": "-",
        "rule_explanation": "der Schüler -> die Schüler.",
        "translation_ka": "მოსწავლე / მოსწავლეები",
        "options": ["die Schülern", "die Schüler", "die Schülere", "die Schülers"]
    },
    {
        "id": 57,
        "singular": "der Koffer",
        "word": "Koffer",
        "article": "der",
        "plural": "die Koffer",
        "plural_word": "Koffer",
        "pattern": "-",
        "rule_explanation": "der Koffer -> die Koffer.",
        "translation_ka": "ჩემოდანი / ჩემოდნები",
        "options": ["die Koffern", "die Koffer", "die Köffer", "die Koffere"]
    },
    {
        "id": 58,
        "singular": "der Teller",
        "word": "Teller",
        "article": "der",
        "plural": "die Teller",
        "plural_word": "Teller",
        "pattern": "-",
        "rule_explanation": "der Teller -> die Teller.",
        "translation_ka": "თეფში / თეფშები",
        "options": ["die Tellern", "die Teller", "die Tellere", "die Tellers"]
    },
    {
        "id": 59,
        "singular": "der Computer",
        "word": "Computer",
        "article": "der",
        "plural": "die Computer",
        "plural_word": "Computer",
        "pattern": "-",
        "rule_explanation": "-er დაბოლოებიანი ინგლისური სიტყვა გერმანულში მრავლობითში უცვლელია: der Computer -> die Computer.",
        "translation_ka": "კომპიუტერი / კომპიუტერები",
        "options": ["die Computern", "die Computer", "die Computers", "die Computere"]
    },
    {
        "id": 60,
        "singular": "der Schlüssel",
        "word": "Schlüssel",
        "article": "der",
        "plural": "die Schlüssel",
        "plural_word": "Schlüssel",
        "pattern": "-",
        "rule_explanation": "-el დაბოლოებიანი სიტყვა უცვლელია: der Schlüssel -> die Schlüssel.",
        "translation_ka": "გასაღები / გასაღებები",
        "options": ["die Schlüsseln", "die Schlüssel", "die Schlüssele", "die Schlüssels"]
    }
]


# ==============================================================================
# 2. VERB CONJUGATION TRAINER DATASET (50 Drills)
# Covers:
# - Vokalwechsel e -> i (sprechen, helfen, essen, geben, treffen, nehmen)
# - Vokalwechsel e -> ie (sehen, lesen)
# - Vokalwechsel a -> ä (fahren, schlafen, waschen, laufen, tragen)
# - Hilfsverben: sein, haben
# - Modalverben: können, müssen, wollen, dürfen, möchten
# - Regular verbs with -t/-d stem: arbeiten, finden
# ==============================================================================
VERB_CONJUGATIONS_DATA = [
    # --- VOKALWECHSEL e -> i ---
    {
        "id": 1,
        "infinitive": "sprechen",
        "pronoun": "er",
        "correct": "spricht",
        "shift": "e -> i (Vokalwechsel)",
        "sentence": "Er _______ sehr gut Deutsch.",
        "translation_ka": "ის (კაცი) ძალიან კარგად ლაპარაკობს გერმანულად.",
        "rule": "ზმნა sprechen არარეგულარულია er პირში (e -> i): er spricht.",
        "options": ["spreche", "spricht", "sprecht", "sprechen"]
    },
    {
        "id": 2,
        "infinitive": "sprechen",
        "pronoun": "du",
        "correct": "sprichst",
        "shift": "e -> i (Vokalwechsel)",
        "sentence": "_______ du auch Englisch?",
        "translation_ka": "შენ ინგლისურადაც ლაპარაკობ?",
        "rule": "du პირთან: du sprichst (e -> i).",
        "options": ["sprichst", "sprechst", "spricht", "sprechen"]
    },
    {
        "id": 3,
        "infinitive": "helfen",
        "pronoun": "sie (ის ქალი)",
        "correct": "hilft",
        "shift": "e -> i (Vokalwechsel)",
        "sentence": "Sie _______ ihrer Mutter in der Küche.",
        "translation_ka": "ის თავის დედას სამზარეულოში ეხმარება.",
        "rule": "helfen იცვლის ფუძის ხმოვანს e -> i: sie hilft.",
        "options": ["helft", "hilft", "helfe", "helfen"]
    },
    {
        "id": 4,
        "infinitive": "essen",
        "pronoun": "er",
        "correct": "isst",
        "shift": "e -> i (Vokalwechsel)",
        "sentence": "Am Morgen _______ er immer ein Ei.",
        "translation_ka": "დილით ის ყოველთვის კვერცხს ჭამს.",
        "rule": "essen -> er isst (ორმაგი s შენარჩუნებულია).",
        "options": ["esst", "isst", "esse", "geesst"]
    },
    {
        "id": 5,
        "infinitive": "geben",
        "pronoun": "es",
        "correct": "gibt",
        "shift": "e -> i (Vokalwechsel)",
        "sentence": "In der Stadt _______ es viele Museen.",
        "translation_ka": "ქალაქში ბევრი მუზეუმია (არსებობს).",
        "rule": "es gibt = არის, არსებობს (geben -> es gibt).",
        "options": ["gebt", "gibt", "gebe", "geben"]
    },
    {
        "id": 6,
        "infinitive": "treffen",
        "pronoun": "du",
        "correct": "triffst",
        "shift": "e -> i (Vokalwechsel)",
        "sentence": "Wen _______ du heute Abend?",
        "translation_ka": "ვის ხვდები დღეს საღამოს?",
        "rule": "treffen -> du triffst (e -> i + ორმაგი f).",
        "options": ["treffst", "triffst", "trifft", "treffen"]
    },
    {
        "id": 7,
        "infinitive": "nehmen",
        "pronoun": "ich",
        "correct": "nehme",
        "shift": "Regular in 1st person",
        "sentence": "Ich _______ einen Kaffee mit Milch.",
        "translation_ka": "მე ავიღებ ყავას რძით.",
        "rule": "ich პირთან ფუძის ხმოვანი არ იცვლება: ich nehme.",
        "options": ["nehme", "nimme", "nimmst", "nehmt"]
    },
    {
        "id": 8,
        "infinitive": "nehmen",
        "pronoun": "er",
        "correct": "nimmt",
        "shift": "e -> i (Vokalwechsel)",
        "sentence": "Er _______ den Bus zur Arbeit.",
        "translation_ka": "ის სამსახურში ავტობუსით მიდის (ავტობუსს იღებს).",
        "rule": "nehmen 3-ე პირში იღებს უწესო ფორმას: er nimmt (e -> i + ორმაგი m).",
        "options": ["nehmt", "nimmt", "nehme", "nehmen"]
    },

    # --- VOKALWECHSEL e -> ie ---
    {
        "id": 9,
        "infinitive": "sehen",
        "pronoun": "du",
        "correct": "siehst",
        "shift": "e -> ie (Vokalwechsel)",
        "sentence": "_______ du den großen Turm dort?",
        "translation_ka": "ხედავ იქ იმ დიდ კოშკს?",
        "rule": "sehen იღებს ie-ს du და er პირებთან: du siehst.",
        "options": ["sehst", "siehst", "sieht", "sehen"]
    },
    {
        "id": 10,
        "infinitive": "sehen",
        "pronoun": "er",
        "correct": "sieht",
        "shift": "e -> ie (Vokalwechsel)",
        "sentence": "Er _______ jeden Abend fern.",
        "translation_ka": "ის ყოველ საღამოს ტელევიზორს უყურებს.",
        "rule": "er პირთან: er sieht.",
        "options": ["seht", "sieht", "sehe", "sehen"]
    },
    {
        "id": 11,
        "infinitive": "lesen",
        "pronoun": "du",
        "correct": "liest",
        "shift": "e -> ie (Vokalwechsel)",
        "sentence": "Was _______ du am Wochenende?",
        "translation_ka": "რას კითხულობ შაბათ-კვირას?",
        "rule": "lesen -> du liest (რადგან ფუძე s-ზე მთავრდება, ემატება მხოლოდ -t).",
        "options": ["lesst", "liest", "liesst", "lesen"]
    },
    {
        "id": 12,
        "infinitive": "lesen",
        "pronoun": "sie (ის ქალი)",
        "correct": "liest",
        "shift": "e -> ie (Vokalwechsel)",
        "sentence": "Anna _______ ein deutsches Buch.",
        "translation_ka": "ანა გერმანულ წიგნს კითხულობს.",
        "rule": "sie liest.",
        "options": ["lest", "liest", "lese", "lesen"]
    },

    # --- VOKALWECHSEL a -> ä ---
    {
        "id": 13,
        "infinitive": "fahren",
        "pronoun": "du",
        "correct": "fährst",
        "shift": "a -> ä (Umlaut)",
        "sentence": "_______ du mit dem Zug oder mit dem Auto?",
        "translation_ka": "მატარებლით მიდიხარ თუ მანქანით?",
        "rule": "fahren იღებს უმლაუტს a -> ä: du fährst.",
        "options": ["fahrst", "fährst", "fährt", "fahren"]
    },
    {
        "id": 14,
        "infinitive": "fahren",
        "pronoun": "er",
        "correct": "fährt",
        "shift": "a -> ä (Umlaut)",
        "sentence": "Der Zug nach München _______ um 10 Uhr ab.",
        "translation_ka": "მიუნხენის მატარებელი 10 საათზე გადის.",
        "rule": "er fährt.",
        "options": ["fahrt", "fährt", "fahre", "fahren"]
    },
    {
        "id": 15,
        "infinitive": "schlafen",
        "pronoun": "du",
        "correct": "schläfst",
        "shift": "a -> ä (Umlaut)",
        "sentence": "Wie lange _______ du am Sonntag?",
        "translation_ka": "რამდენ ხანს გძინავს კვირას?",
        "rule": "schlafen -> du schläfst.",
        "options": ["schlafst", "schläfst", "schläft", "schlafen"]
    },
    {
        "id": 16,
        "infinitive": "schlafen",
        "pronoun": "das Kind",
        "correct": "schläft",
        "shift": "a -> ä (Umlaut)",
        "sentence": "Das Baby _______ schon seit zwei Stunden.",
        "translation_ka": "პატარას უკვე ორი საათია სძინავს.",
        "rule": "das Kind (es) schläft.",
        "options": ["schlaft", "schläft", "schlafe", "schlafen"]
    },
    {
        "id": 17,
        "infinitive": "tragen",
        "pronoun": "er",
        "correct": "trägt",
        "shift": "a -> ä (Umlaut)",
        "sentence": "Er _______ heute eine blaue Jacke.",
        "translation_ka": "მას დღეს ლურჯი ქურთუკი აცვია.",
        "rule": "tragen -> er trägt.",
        "options": ["tragt", "trägt", "trage", "tragen"]
    },
    {
        "id": 18,
        "infinitive": "waschen",
        "pronoun": "du",
        "correct": "wäschst",
        "shift": "a -> ä (Umlaut)",
        "sentence": "_______ du dein Auto am Wochenende?",
        "translation_ka": "რეცხავ შენს მანქანას შაბათ-კვირას?",
        "rule": "waschen -> du wäschst.",
        "options": ["waschst", "wäschst", "wäscht", "waschen"]
    },
    {
        "id": 19,
        "infinitive": "laufen",
        "pronoun": "er",
        "correct": "läuft",
        "shift": "au -> äu (Umlaut)",
        "sentence": "Er _______ jeden Morgen im Park.",
        "translation_ka": "ის ყოველ დილით პარკში დარბის.",
        "rule": "laufen -> er läuft (au ხდება äu).",
        "options": ["lauft", "läuft", "laufe", "laufen"]
    },

    # --- HILFSVERBEN: SEIN & HABEN ---
    {
        "id": 20,
        "infinitive": "sein",
        "pronoun": "ich",
        "correct": "bin",
        "shift": "Irregular",
        "sentence": "Ich _______ aus Georgien.",
        "translation_ka": "მე საქართველოდან ვარ.",
        "rule": "ich bin = მე ვარ.",
        "options": ["bin", "bist", "ist", "sind"]
    },
    {
        "id": 21,
        "infinitive": "sein",
        "pronoun": "du",
        "correct": "bist",
        "shift": "Irregular",
        "sentence": "Wo _______ du gerade?",
        "translation_ka": "სად ხარ ახლა?",
        "rule": "du bist = შენ ხარ.",
        "options": ["bin", "bist", "seid", "sind"]
    },
    {
        "id": 22,
        "infinitive": "sein",
        "pronoun": "ihr",
        "correct": "seid",
        "shift": "Irregular",
        "sentence": "_______ ihr heute zu Hause?",
        "translation_ka": "თქვენ (მეგობრები) დღეს სახლში ხართ?",
        "rule": "ihr seid = თქვენ ხართ.",
        "options": ["sind", "seid", "bist", "sein"]
    },
    {
        "id": 23,
        "infinitive": "sein",
        "pronoun": "Sie (თავაზიანი)",
        "correct": "sind",
        "shift": "Irregular",
        "sentence": "_______ Sie Herr Müller?",
        "translation_ka": "თქვენ ბატონი მიულერი ბრძანდებით?",
        "rule": "Sie sind = თქვენ ბრძანდებით.",
        "options": ["seid", "sind", "ist", "bin"]
    },
    {
        "id": 24,
        "infinitive": "haben",
        "pronoun": "du",
        "correct": "hast",
        "shift": "Irregular stem",
        "sentence": "_______ du heute Zeit für einen Kaffee?",
        "translation_ka": "გაქვს დღეს დრო ყავისთვის?",
        "rule": "haben კარგავს b-ს du და er პირებთან: du hast.",
        "options": ["habst", "hast", "hat", "haben"]
    },
    {
        "id": 25,
        "infinitive": "haben",
        "pronoun": "er",
        "correct": "hat",
        "shift": "Irregular stem",
        "sentence": "Er _______ zwei Brüder und eine Schwester.",
        "translation_ka": "მას ორი ძმა და ერთი და ჰყავს.",
        "rule": "er hat.",
        "options": ["habt", "hat", "habe", "haben"]
    },
    {
        "id": 26,
        "infinitive": "haben",
        "pronoun": "ihr",
        "correct": "habt",
        "shift": "Regular plural",
        "sentence": "_______ ihr Hunger?",
        "translation_ka": "გშიათ თქვენ?",
        "rule": "ihr პირთან b ბრუნდება: ihr habt.",
        "options": ["hast", "habt", "hat", "haben"]
    },

    # --- MODALVERBEN: KÖNNEN, MÜSSEN, WOLLEN, DÜRFEN, MÖCHTEN ---
    {
        "id": 27,
        "infinitive": "können",
        "pronoun": "ich",
        "correct": "kann",
        "shift": "Modalverb (ich = er)",
        "sentence": "Ich _______ sehr gut schwimmen.",
        "translation_ka": "მე ძალიან კარგად შემიძლია ცურვა.",
        "rule": "მოდალურ ზმნებს 1-ლ და მე-3 პირში არ აქვთ დაბოლოება: ich kann, er kann.",
        "options": ["könne", "kann", "kannst", "können"]
    },
    {
        "id": 28,
        "infinitive": "können",
        "pronoun": "du",
        "correct": "kannst",
        "shift": "Modalverb",
        "sentence": "_______ du mir bitte helfen?",
        "translation_ka": "შეგიძლია გთხოვ დამეხმარო?",
        "rule": "du kannst.",
        "options": ["könnst", "kannst", "kann", "können"]
    },
    {
        "id": 29,
        "infinitive": "können",
        "pronoun": "wir",
        "correct": "können",
        "shift": "Modalverb (plural)",
        "sentence": "Wir _______ morgen ins Kino gehen.",
        "translation_ka": "ჩვენ ხვალ შეგვიძლია კინოში წასვლა.",
        "rule": "wir können (მრავლობითში უმლაუტი ბრუნდება).",
        "options": ["kann", "könnt", "können", "könne"]
    },
    {
        "id": 30,
        "infinitive": "müssen",
        "pronoun": "ich",
        "correct": "muss",
        "shift": "Modalverb (ich = er)",
        "sentence": "Ich _______ heute lange arbeiten.",
        "translation_ka": "მე დღეს დიდხანს უნდა ვიმუშაო.",
        "rule": "ich muss (დაბოლოების გარეშე, ü გადადის u-ში).",
        "options": ["müsse", "muss", "musst", "müssen"]
    },
    {
        "id": 31,
        "infinitive": "müssen",
        "pronoun": "du",
        "correct": "musst",
        "shift": "Modalverb",
        "sentence": "Du _______ zum Arzt gehen, wenn du krank bist.",
        "translation_ka": "შენ ექიმთან უნდა წახვიდე, თუ ავად ხარ.",
        "rule": "du musst.",
        "options": ["müsst", "musst", "muss", "müssen"]
    },
    {
        "id": 32,
        "infinitive": "müssen",
        "pronoun": "er",
        "correct": "muss",
        "shift": "Modalverb (ich = er)",
        "sentence": "Er _______ früh aufstehen.",
        "translation_ka": "ის ადრე უნდა ადგეს.",
        "rule": "er muss.",
        "options": ["müsst", "muss", "musste", "müssen"]
    },
    {
        "id": 33,
        "infinitive": "wollen",
        "pronoun": "ich",
        "correct": "will",
        "shift": "Modalverb",
        "sentence": "Ich _______ Deutsch lernen.",
        "translation_ka": "მე მინდა გერმანული ვისწავლო.",
        "rule": "ich will.",
        "options": ["wolle", "will", "willst", "wollen"]
    },
    {
        "id": 34,
        "infinitive": "wollen",
        "pronoun": "du",
        "correct": "willst",
        "shift": "Modalverb",
        "sentence": "Was _______ du trinken?",
        "translation_ka": "რა გინდა დალიო?",
        "rule": "du willst.",
        "options": ["wollst", "willst", "will", "wollen"]
    },
    {
        "id": 35,
        "infinitive": "wollen",
        "pronoun": "wir",
        "correct": "wollen",
        "shift": "Modalverb (plural)",
        "sentence": "Wir _______ am Wochenende nach Wien reisen.",
        "translation_ka": "ჩვენ შაბათ-კვირას ვენაში გამგზავრება გვინდა.",
        "rule": "wir wollen.",
        "options": ["will", "wollt", "wollen", "wolle"]
    },
    {
        "id": 36,
        "infinitive": "dürfen",
        "pronoun": "man",
        "correct": "darf",
        "shift": "Modalverb (Verbot / Erlaubnis)",
        "sentence": "Hier _______ man nicht parken.",
        "translation_ka": "აქ პარკირება არ შეიძლება (აკრძალულია).",
        "rule": "man darf nicht = აკრძალულია (man = er/sie/es).",
        "options": ["dürft", "darf", "darfst", "dürfen"]
    },
    {
        "id": 37,
        "infinitive": "dürfen",
        "pronoun": "ich",
        "correct": "darf",
        "shift": "Modalverb",
        "sentence": "_______ ich Sie etwas fragen?",
        "translation_ka": "შეიძლება რაღაც გკითხოთ?",
        "rule": "darf ich = შეიძლება? ნებართვის თავაზიანი თხოვნა.",
        "options": ["Dürfe", "Darf", "Darfst", "Dürfen"]
    },
    {
        "id": 38,
        "infinitive": "möchten",
        "pronoun": "ich",
        "correct": "möchte",
        "shift": "Höflichkeitsform",
        "sentence": "Ich _______ ein Glas Wasser, bitte.",
        "translation_ka": "ერთი ჭიქა წყალი მსურს, გთხოვთ.",
        "rule": "ich möchte = მსურს, მინდა (თავაზიანი).",
        "options": ["möchte", "möchtest", "mag", "möchten"]
    },
    {
        "id": 39,
        "infinitive": "möchten",
        "pronoun": "du",
        "correct": "möchtest",
        "shift": "Höflichkeitsform",
        "sentence": "Was _______ du essen?",
        "translation_ka": "რა გსურს მიირთვა?",
        "rule": "du möchtest.",
        "options": ["möchtst", "möchtest", "möchte", "möchten"]
    },
    {
        "id": 40,
        "infinitive": "möchten",
        "pronoun": "er",
        "correct": "möchte",
        "shift": "Höflichkeitsform",
        "sentence": "Er _______ gern in Berlin wohnen.",
        "translation_ka": "მას სიამოვნებით სურს ბერლინში ცხოვრება.",
        "rule": "er möchte (ich და er ფორმები იდენტურია!).",
        "options": ["möchtet", "möchte", "möchten", "mag"]
    },

    # --- REGELMÄSSIGE VERBEN & STAMM AUF -t / -d ---
    {
        "id": 41,
        "infinitive": "arbeiten",
        "pronoun": "du",
        "correct": "arbeitest",
        "shift": "Stamm auf -t (e-Einschub)",
        "sentence": "Wo _______ du?",
        "translation_ka": "სად მუშაობ?",
        "rule": "თუ ფუძე -t-ზე მთავრდება, გამოთქმის გასაადვილებლად ემატება -e-: du arbeitest.",
        "options": ["arbeitst", "arbeitest", "arbeitet", "arbeiten"]
    },
    {
        "id": 42,
        "infinitive": "arbeiten",
        "pronoun": "er",
        "correct": "arbeitet",
        "shift": "Stamm auf -t (e-Einschub)",
        "sentence": "Mein Vater _______ als Ingenieur.",
        "translation_ka": "მამაჩემი ინჟინრად მუშაობს.",
        "rule": "er arbeitet.",
        "options": ["arbeitt", "arbeitet", "arbeite", "arbeiten"]
    },
    {
        "id": 43,
        "infinitive": "finden",
        "pronoun": "du",
        "correct": "findest",
        "shift": "Stamm auf -d (e-Einschub)",
        "sentence": "Wie _______ du diesen Film?",
        "translation_ka": "როგორ მოგწონს ეს ფილმი?",
        "rule": "ფუძე -d-ზე მთავრდება -> du findest.",
        "options": ["findst", "findest", "findet", "finden"]
    },
    {
        "id": 44,
        "infinitive": "wohnen",
        "pronoun": "wir",
        "correct": "wohnen",
        "shift": "Regular",
        "sentence": "Wir _______ seit fünf Jahren in Hamburg.",
        "translation_ka": "ჩვენ ხუთი წელია ჰამბურგში ვცხოვრობთ.",
        "rule": "wir wohnen.",
        "options": ["wohne", "wohnt", "wohnen", "gewohnt"]
    },
    {
        "id": 45,
        "infinitive": "lernen",
        "pronoun": "ihr",
        "correct": "lernt",
        "shift": "Regular",
        "sentence": "_______ ihr fleißig Deutsch?",
        "translation_ka": "ბეჯითად სწავლობთ გერმანულს?",
        "rule": "ihr lernt (დაბოლოება -t).",
        "options": ["lernen", "lernt", "lernst", "lerne"]
    },
    {
        "id": 46,
        "infinitive": "trinken",
        "pronoun": "er",
        "correct": "trinkt",
        "shift": "Regular",
        "sentence": "Er _______ morgens immer schwarzen Tee.",
        "translation_ka": "ის დილაობით ყოველთვის შავ ჩაის სვამს.",
        "rule": "er trinkt.",
        "options": ["trinke", "trinkt", "trinkst", "trinken"]
    },
    {
        "id": 47,
        "infinitive": "kaufen",
        "pronoun": "du",
        "correct": "kaufst",
        "shift": "Regular",
        "sentence": "Was _______ du im Supermarkt?",
        "translation_ka": "რას ყიდულობ სუპერმარკეტში?",
        "rule": "du kaufst.",
        "options": ["kauft", "kaufst", "kaufe", "kaufen"]
    },
    {
        "id": 48,
        "infinitive": "schreiben",
        "pronoun": "ich",
        "correct": "schreibe",
        "shift": "Regular",
        "sentence": "Ich _______ eine E-Mail an meine Lehrerin.",
        "translation_ka": "მე ელ-ფოსტას ვწერ ჩემს მასწავლებელს.",
        "rule": "ich schreibe.",
        "options": ["schreibe", "schreibst", "schreibt", "schreiben"]
    },
    {
        "id": 49,
        "infinitive": "kommen",
        "pronoun": "er",
        "correct": "kommt",
        "shift": "Regular",
        "sentence": "David _______ aus Georgien.",
        "translation_ka": "დავითი საქართველოდან მოდის (არის).",
        "rule": "er kommt.",
        "options": ["komme", "kommt", "kömmt", "kommen"]
    },
    {
        "id": 50,
        "infinitive": "heißen",
        "pronoun": "du",
        "correct": "heißt",
        "shift": "Stamm auf -ß",
        "sentence": "Wie _______ du mit Vornamen?",
        "translation_ka": "რა გქვია სახელი?",
        "rule": "რადგან ფუძე მთავრდება ß-ზე, du პირთან ემატება მხოლოდ -t (არა -st): du heißt.",
        "options": ["heißst", "heißt", "heiße", "heißen"]
    }
]


# ==============================================================================
# 3. A1 GRADED MINI-STORIES (Kurzgeschichten mit Audio & Vokabel-Popup)
# ==============================================================================
A1_MINI_STORIES = [
    {
        "id": "story_1",
        "title_de": "Nicos erste Schritte in Berlin",
        "title_ka": "ნიკოს პირველი ნაბიჯები ბერლინში",
        "level": "A1.1",
        "audio_text": "Nico kommt am Hauptbahnhof in Berlin an. Er hat einen großen Koffer und einen Rucksack. Es ist zehn Uhr morgens und das Wetter ist sonnig. Nico sucht die Sprachschule in der Kantstraße. Er geht zu einer Information und fragt höflich: Entschuldigung, wie komme ich zur Kantstraße? Die Dame lächelt und antwortet: Nehmen Sie die S-Bahn Linie 7 bis zum Bahnhof Savignyplatz. Von dort sind es nur drei Minuten zu Fuß. Nico bedankt sich herzlich. Im Zug trifft er ein nettes Mädchen namens Lisa. Sie lernen sich kennen und sprechen über ihre Hobbys. Berlin gefällt Nico schon am ersten Tag sehr gut!",
        "paragraphs": [
            {
                "de": "Nico kommt am Hauptbahnhof in Berlin an. Er hat einen großen Koffer und einen Rucksack. Es ist zehn Uhr morgens und das Wetter ist sonnig.",
                "ka": "ნიკო ბერლინის ცენტრალურ სადგურზე ჩადის. მას აქვს დიდი ჩემოდანი და ზურგჩანთა. დილის ათი საათია და მზიანი ამინდია.",
                "glossary": [
                    {"word": "Hauptbahnhof", "article": "der", "ka": "ცენტრალური რკინიგზის სადგური"},
                    {"word": "Koffer", "article": "der", "ka": "ჩემოდანი"},
                    {"word": "Rucksack", "article": "der", "ka": "ზურგჩანთა"},
                    {"word": "sonnig", "ka": "მზიანი"}
                ]
            },
            {
                "de": "Nico sucht die Sprachschule in der Kantstraße. Er geht zu einer Information und fragt höflich: „Entschuldigung, wie komme ich zur Kantstraße?“",
                "ka": "ნიკო ეძებს ენების სკოლას კანტის ქუჩაზე. ის მიდის საინფორმაციო ბიუროსთან და თავაზიანად ეკითხება: „უკაცრავად, როგორ მივიდე კანტის ქუჩამდე?“",
                "glossary": [
                    {"word": "Sprachschule", "article": "die", "ka": "ენების სკოლა"},
                    {"word": "höflich", "ka": "თავაზიანად"},
                    {"word": "Entschuldigung", "article": "die", "ka": "ბოდიში / უკაცრავად"}
                ]
            },
            {
                "de": "Die Dame lächelt und antwortet: „Nehmen Sie die S-Bahn Linie 7 bis zum Bahnhof Savignyplatz. Von dort sind es nur drei Minuten zu Fuß.“ Nico bedankt sich herzlich.",
                "ka": "ქალბატონი იღიმის და პასუხობს: „ჩაჯექით S-Bahn-ის მე-7 ხაზზე სადგურ სავინიპლაცამდე. იქიდან ფეხით მხოლოდ სამი წუთის სავალია.“ ნიკო გულწრფელ მადლობას უხდის.",
                "glossary": [
                    {"word": "lächeln", "ka": "ღიმილი"},
                    {"word": "zu Fuß", "ka": "ფეხით"},
                    {"word": "bedankt sich", "ka": "მადლობას უხდის"}
                ]
            },
            {
                "de": "Im Zug trifft er ein nettes Mädchen namens Lisa. Sie lernen sich kennen und sprechen über ihre Hobbys. Berlin gefällt Nico schon am ersten Tag sehr gut!",
                "ka": "მატარებელში ის ხვდება საყვარელ გოგონას, სახელად ლიზას. ისინი ერთმანეთს ეცნობიან და თავიანთ ჰობიზე საუბრობენ. ბერლინი ნიკოს უკვე პირველივე დღეს ძალიან მოსწონს!",
                "glossary": [
                    {"word": "kennenlernen", "ka": "გაცნობა"},
                    {"word": "gefällt", "ka": "მოსწონს"}
                ]
            }
        ],
        "quiz": [
            {
                "question": "რომელ საათზე ჩავიდა ნიკო ბერლინში?",
                "options": ["დილის 08:00 საათზე", "დილის 10:00 საათზე", "შუადღის 12:00 საათზე", "საღამოს 18:00 საათზე"],
                "answer": 1,
                "explanation": "ტექსტში ნათქვამია: „Es ist zehn Uhr morgens“ (დილის 10 საათია)."
            },
            {
                "question": "რომელი ტრანსპორტით ურჩია ქალბატონმა მგზავრობა?",
                "options": ["ტაქსით", "ავტობუსით", "S-Bahn-ის მე-7 ხაზით", "U-Bahn-ით"],
                "answer": 2,
                "explanation": "ქალბატონმა უთხრა: „Nehmen Sie die S-Bahn Linie 7...“"
            },
            {
                "question": "ვის შეხვდა ნიკო მატარებელში?",
                "options": ["ენების მასწავლებელს", "გოგონას, სახელად ლიზას", "თავის ძმას", "პოლიციელს"],
                "answer": 1,
                "explanation": "„Im Zug trifft er ein nettes Mädchen namens Lisa.“"
            }
        ]
    },
    {
        "id": "story_2",
        "title_de": "Ein chaotischer Einkauf im Supermarkt",
        "title_ka": "ქაოტური საყიდლები სუპერმარკეტში",
        "level": "A1.1",
        "audio_text": "Heute kocht David für seine Freunde. Er geht in den Supermarkt an der Ecke. Auf seinem Einkaufszettel stehen: Tomaten, Zwiebeln, Käse, Brot und Mineralwasser. Im Supermarkt sucht er zuerst das Gemüse. Die Tomaten kosten ein Euro neunundneunzig pro Kilo. Er nimmt auch ein Pfund Äpfel. Plötzlich merkt er, dass er sein Portemonnaie vergessen hat! Zum Glück hat er sein Handy dabei und kann kontaktlos mit dem Telefon bezahlen. Die Kassiererin sagt: Das macht zusammen zwölf Euro fünfzig. David bezahlt und packt alles schnell in seine Stofftasche. Das Abendessen ist gerettet!",
        "paragraphs": [
            {
                "de": "Heute kocht David für seine Freunde. Er geht in den Supermarkt an der Ecke. Auf seinem Einkaufszettel stehen: Tomaten, Zwiebeln, Käse, Brot und Mineralwasser.",
                "ka": "დღეს დავითი თავისი მეგობრებისთვის სადილს ამზადებს. ის კუთხეში მდებარე სუპერმარკეტში მიდის. მის საყიდლების სიაში წერია: პომიდორი, ხახვი, ყველი, პური და მინერალური წყალი.",
                "glossary": [
                    {"word": "kochen", "ka": "საჭმლის მომზადება"},
                    {"word": "Einkaufszettel", "article": "der", "ka": "საყიდლების სია"},
                    {"word": "Zwiebel", "article": "die", "ka": "ხახვი"}
                ]
            },
            {
                "de": "Im Supermarkt sucht er zuerst das Gemüse. Die Tomaten kosten ein Euro neunundneunzig pro Kilo. Er nimmt auch ein Pfund Äpfel.",
                "ka": "სუპერმარკეტში ის ჯერ ბოსტნეულს ეძებს. პომიდორი კილოგრამი ერთი ევრო და ოთხმოცდაცხრამეტი ცენტი ღირს. ის ასევე იღებს ერთ ფუნტ (500 გრ) ვაშლს.",
                "glossary": [
                    {"word": "Gemüse", "article": "das", "ka": "ბოსტნეული"},
                    {"word": "Pfund", "article": "das", "ka": "ფუნტი (500 გრამი)"}
                ]
            },
            {
                "de": "Plötzlich merkt er, dass er sein Portemonnaie vergessen hat! Zum Glück hat er sein Handy dabei und kann kontaktlos mit dem Telefon bezahlen.",
                "ka": "უცებ ის ამჩნევს, რომ საფულე სახლში დარჩა! საბედნიეროდ, მობილური თან აქვს და ტელეფონით უკონტაქტოდ გადახდა შეუძლია.",
                "glossary": [
                    {"word": "Portemonnaie", "article": "das", "ka": "საფულე"},
                    {"word": "vergessen", "ka": "დავიწყება"},
                    {"word": "bezahlen", "ka": "გადახდა"}
                ]
            },
            {
                "de": "Die Kassiererin sagt: „Das macht zusammen zwölf Euro fünfzig.“ David bezahlt und packt alles schnell in seine Stofftasche. Das Abendessen ist gerettet!",
                "ka": "მოლარე ეუბნება: „სულ თორმეტი ევრო და ორმოცდაათი ცენტია.“ დავითი იხდის და ყველაფერს სწრაფად ალაგებს ნაჭრის ჩანთაში. ვახშამი გადარჩენილია!",
                "glossary": [
                    {"word": "Kassiererin", "article": "die", "ka": "მოლარე ქალი"},
                    {"word": "Stofftasche", "article": "die", "ka": "ნაჭრის ჩანთა"}
                ]
            }
        ],
        "quiz": [
            {
                "question": "რა დაავიწყდა დავითს სახლში?",
                "options": ["საყიდლების სია", "საფულე (Portemonnaie)", "მობილური ტელეფონი", "გასაღები"],
                "answer": 1,
                "explanation": "„Plötzlich merkt er, dass er sein Portemonnaie vergessen hat!“"
            },
            {
                "question": "რამდენი გადაიხადა დავითმა სულ საყიდლებში?",
                "options": ["10,50 €", "12,50 €", "15,00 €", "1,99 €"],
                "answer": 1,
                "explanation": "მოლარემ უთხრა: „Das macht zusammen zwölf Euro fünfzig“ (12,50 €)."
            },
            {
                "question": "როგორ გადაიხადა დავითმა თანხა?",
                "options": ["ნაღდი ფულით", "საბანკო ქვითრით", "მობილური ტელეფონით უკონტაქტოდ", "მეგობარმა გადაუხადა"],
                "answer": 2,
                "explanation": "„...und kann kontaktlos mit dem Telefon bezahlen.“"
            }
        ]
    },
    {
        "id": "story_3",
        "title_de": "Einladung zum gemütlichen Abendessen",
        "title_ka": "დაპატიჟება მყუდრო სადილზე",
        "level": "A1.2",
        "audio_text": "Am Freitagabend ist David bei Familie Weber eingeladen. Herr und Frau Weber wohnen in einer schönen Altbauwohnung in München. David kauft unterwegs einen Blumenstrauß für Frau Weber und eine Flasche Saft. Um Punkt neunzehn Uhr klingelt er an der Tür. In Deutschland ist Pünktlichkeit sehr wichtig. Herr Weber öffnet die Tür und begrüßt ihn herzlich: Schön, dass du da bist! Sie setzen sich ins Wohnzimmer. Es gibt typisch bayerisches Essen: gebratenes Hähnchen mit Kartoffelsalat. Sie unterhalten sich über Reisen und das Leben in Deutschland. Um zweiundzwanzig Uhr verabschiedet sich David und sagt: Vielen Dank für den wunderschönen Abend!",
        "paragraphs": [
            {
                "de": "Am Freitagabend ist David bei Familie Weber eingeladen. Herr und Frau Weber wohnen in einer schönen Altbauwohnung in München. David kauft unterwegs einen Blumenstrauß für Frau Weber und eine Flasche Saft.",
                "ka": "პარასკევ საღამოს დავითი ვებერების ოჯახშია მიპატიჟებული. ბატონი და ქალბატონი ვებერები მიუნხენში მშვენიერ ძველებურ ბინაში ცხოვრობენ. დავითი გზად ყვავილების თაიგულს ყიდულობს ქალბატონი ვებერისთვის და ერთ ბოთლ წვენს.",
                "glossary": [
                    {"word": "eingeladen", "ka": "მიპატიჟებული"},
                    {"word": "Altbauwohnung", "article": "die", "ka": "ძველებური ტიპის ბინა (მაღალჭერიანი)"},
                    {"word": "Blumenstrauß", "article": "der", "ka": "ყვავილების თაიგული"}
                ]
            },
            {
                "de": "Um Punkt neunzehn Uhr klingelt er an der Tür. In Deutschland ist Pünktlichkeit sehr wichtig. Herr Weber öffnet die Tür und begrüßt ihn herzlich: „Schön, dass du da bist!“",
                "ka": "ზუსტად ცხრამეტ საათზე ის კარზე ზარს რეკავს. გერმანიაში პუნქტუალობა ძალიან მნიშვნელოვანია. ბატონი ვებერი კარს აღებს და გულითად მოკითხვას ეუბნება: „სასიამოვნოა, რომ მოხვედი!“",
                "glossary": [
                    {"word": "Pünktlichkeit", "article": "die", "ka": "პუნქტუალურობა (სიზუსტე)"},
                    {"word": "klingeln", "ka": "ზარის დარეკვა"},
                    {"word": "begrüßen", "ka": "მისალმება"}
                ]
            },
            {
                "de": "Sie setzen sich ins Wohnzimmer. Es gibt typisch bayerisches Essen: gebratenes Hähnchen mit Kartoffelsalat. Sie unterhalten sich über Reisen und das Leben in Deutschland.",
                "ka": "ისინი მისაღებ ოთახში სხდებიან. სუფრაზე ტიპური ბავარიული კერძია: შემწვარი ქათამი კარტოფილის სალათით. ისინი საუბრობენ მოგზაურობასა და გერმანიაში ცხოვრებაზე.",
                "glossary": [
                    {"word": "Kartoffelsalat", "article": "der", "ka": "კარტოფილის სალათი"},
                    {"word": "unterhalten sich", "ka": "საუბარი / დროსტარება"}
                ]
            },
            {
                "de": "Um zweiundzwanzig Uhr verabschiedet sich David und sagt: „Vielen Dank für den wunderschönen Abend!“",
                "ka": "ოცდაორ (22:00) საათზე დავითი ემშვიდობება მათ და ამბობს: „დიდი მადლობა მშვენიერი საღამოსთვის!“",
                "glossary": [
                    {"word": "verabschieden", "ka": "დამშვიდობება"},
                    {"word": "wunderschön", "ka": "საოცარი / ულამაზესი"}
                ]
            }
        ],
        "quiz": [
            {
                "question": "რა მიიტანა დავითმა საჩუქრად?",
                "options": ["შოკოლადი და ღვინო", "ყვავილების თაიგული და წვენი", "წიგნი და ტორტი", "არაფერი"],
                "answer": 1,
                "explanation": "„David kauft unterwegs einen Blumenstrauß für Frau Weber und eine Flasche Saft.“"
            },
            {
                "question": "რომელ საათზე მივიდა დავითი სტუმრად?",
                "options": ["18:30 საათზე", "ზუსტად 19:00 საათზე (Um Punkt 19 Uhr)", "20:00 საათზე", "დააგვიანა"],
                "answer": 1,
                "explanation": "„Um Punkt neunzehn Uhr klingelt er an der Tür.“"
            },
            {
                "question": "რა კერძი მიირთვეს მასპინძლებთან ერთად?",
                "options": ["პიცა და პასტა", "შემწვარი ქათამი კარტოფილის სალათით", "თევზი ბრინჯით", "მხოლოდ სუპი"],
                "answer": 1,
                "explanation": "„...gebratenes Hähnchen mit Kartoffelsalat.“"
            }
        ]
    },
    {
        "id": "story_4",
        "title_de": "Ein Besuch beim Arzt",
        "title_ka": "ვიზიტი ექიმთან და აფთიაქი",
        "level": "A1.2",
        "audio_text": "Anna fühlt sich heute gar nicht gut. Sie hat starke Kopfschmerzen und Husten. Ihr Hals tut auch weh. Sie ruft in der Praxis von Dr. Becker an: Guten Tag, ich brauche dringend einen Termin, ich bin krank. Die Sprechstundenhilfe sagt: Kommen Sie bitte heute um elf Uhr vorbei. In der Praxis untersucht der Arzt Anna gründlich. Er misst Fieber und schaut in ihren Hals. Er sagt: Sie haben eine Erkältung. Sie müssen drei Tage im Bett bleiben und viel Tee trinken. Der Arzt gibt ihr ein Rezept. In der Apotheke holt Anna Tabletten und Hustensaft. Nach zwei Tagen Ruhe fühlt sie sich schon viel besser.",
        "paragraphs": [
            {
                "de": "Anna fühlt sich heute gar nicht gut. Sie hat starke Kopfschmerzen und Husten. Ihr Hals tut auch weh.",
                "ka": "ანა დღეს საერთოდ არ გრძნობს თავს კარგად. მას ძლიერი თავის ტკივილი და ხველა აქვს. ყელიც სტკივა.",
                "glossary": [
                    {"word": "Kopfschmerzen", "article": "die", "ka": "თავის ტკივილი"},
                    {"word": "Husten", "article": "der", "ka": "ხველა"},
                    {"word": "wehtun", "ka": "ტკივილი (Hals tut weh = ყელი მტკივა)"}
                ]
            },
            {
                "de": "Sie ruft in der Praxis von Dr. Becker an: „Guten Tag, ich brauche dringend einen Termin, ich bin krank.“ Die Sprechstundenhilfe sagt: „Kommen Sie bitte heute um elf Uhr vorbei.“",
                "ka": "ის ექიმ ბეკერის პრაქტიკაში რეკავს: „გამარჯობა, სასწრაფოდ მჭირდება ვიზიტი, ავად ვარ.“ ექიმის ასისტენტი ეუბნება: „გთხოვთ მობრძანდეთ დღეს თერთმეტ საათზე.“",
                "glossary": [
                    {"word": "dringend", "ka": "გადაუდებელი / სასწრაფო"},
                    {"word": "Sprechstundenhilfe", "article": "die", "ka": "ექიმის მიმღები / ასისტენტი"}
                ]
            },
            {
                "de": "In der Praxis untersucht der Arzt Anna gründlich. Er misst Fieber und schaut in ihren Hals. Er sagt: „Sie haben eine Erkältung. Sie müssen drei Tage im Bett bleiben und viel Tee trinken.“",
                "ka": "კლინიკაში ექიმი ანას საფუძვლიანად სინჯავს. ის სიცხეს უზომავს და ყელში ჩახედავს. ეუბნება: „თქვენ გაციებული ხართ. სამი დღე ლოგინში უნდა დარჩეთ და ბევრი ჩაი დალიოთ.“",
                "glossary": [
                    {"word": "untersuchen", "ka": "გასინჯვა / გამოკვლევა"},
                    {"word": "Fieber", "article": "das", "ka": "სიცხე (ტემპერატურა)"},
                    {"word": "Erkältung", "article": "die", "ka": "გაციება"}
                ]
            },
            {
                "de": "Der Arzt gibt ihr ein Rezept. In der Apotheke holt Anna Tabletten und Hustensaft. Nach zwei Tagen Ruhe fühlt sie sich schon viel besser.",
                "ka": "ექიმი მას რეცეპტს აძლევს. აფთიაქში ანა ტაბლეტებსა და ხველის სიროფს იღებს. ორდღიანი დასვენების შემდეგ ის უკვე გაცილებით უკეთ გრძნობს თავს.",
                "glossary": [
                    {"word": "Rezept", "article": "das", "ka": "რეცეპტი"},
                    {"word": "Hustensaft", "article": "der", "ka": "ხველის სიროფი"},
                    {"word": "Ruhe", "article": "die", "ka": "სიმშვიდე / დასვენება"}
                ]
            }
        ],
        "quiz": [
            {
                "question": "რა სიმპტომები ჰქონდა ანას?",
                "options": ["მუცლის ტკივილი", "თავის ტკივილი, ხველა და ყელის ტკივილი", "კბილის ტკივილი", "ფეხის ტკივილი"],
                "answer": 1,
                "explanation": "„Sie hat starke Kopfschmerzen und Husten. Ihr Hals tut auch weh.“"
            },
            {
                "question": "რა რჩევა მისცა ექიმმა ანას?",
                "options": ["სამსახურში წასულიყო", "სამი დღე ლოგინში დარჩენილიყო და ბევრი ჩაი დაელია", "სპორტით დაკავებულიყო", "საავადმყოფოში დაწოლილიყო"],
                "answer": 1,
                "explanation": "„Sie müssen drei Tage im Bett bleiben und viel Tee trinken.“"
            },
            {
                "question": "რა იყიდა ანამ აფთიაქში რეცეპტით?",
                "options": ["ვიტამინები და კრემი", "ტაბლეტები და ხველის სიროფი (Tabletten und Hustensaft)", "მხოლოდ თერმომეტრი", "ჩაი და თაფლი"],
                "answer": 1,
                "explanation": "„In der Apotheke holt Anna Tabletten und Hustensaft.“"
            }
        ]
    }
]

# ==============================================================================
# 4. PREPOSITION & CASE TRAINER DATASET (40 A1 Drills)
# Topics:
# - Dativ Prepositions: mit, nach, aus, zu, bei, von, seit
# - Akkusativ Prepositions: für, ohne, durch, um, gegen
# - Wechselpräpositionen (in, auf, an, neben, unter, vor): Wo? (Dativ) vs. Wohin? (Akkusativ)
# ==============================================================================
PREPOSITION_CASES_DATA = [
    # --- 1. DATIV PREPOSITIONS (15 drills) ---
    {
        "id": 1,
        "type": "dativ",
        "preposition": "mit",
        "sentence": "Ich fahre jeden Morgen mit _______ zur Arbeit.",
        "correct": "dem Bus",
        "options": ["dem Bus", "den Bus", "der Bus", "des Busses"],
        "translation_ka": "ყოველ დილით ავტობუსით მივდივარ სამსახურში.",
        "rule_ka": "წინდებული „mit“ ყოველთვის მოითხოვს მიცემით ბრუნვას (Dativ): der Bus -> dem Bus.",
        "hint": "mit + Dativ (der -> dem)"
    },
    {
        "id": 2,
        "type": "dativ",
        "preposition": "mit",
        "sentence": "Er spricht am Telefon mit _______ .",
        "correct": "der Lehrerin",
        "options": ["die Lehrerin", "der Lehrerin", "den Lehrerin", "einer Lehrerin"],
        "translation_ka": "ის ტელეფონით ელაპარაკება მასწავლებელ ქალს.",
        "rule_ka": "„mit“ მოითხოვს Dativ-ს. მდედრობითი სქესის არტიკლი die Dativ-ში ხდება der: die Lehrerin -> der Lehrerin.",
        "hint": "mit + Dativ (die -> der)"
    },
    {
        "id": 3,
        "type": "dativ",
        "preposition": "mit",
        "sentence": "Wir fahren am Wochenende mit _______ ans Meer.",
        "correct": "dem Auto",
        "options": ["das Auto", "dem Auto", "den Auto", "des Autos"],
        "translation_ka": "შაბათ-კვირას მანქანით მივდივართ ზღვაზე.",
        "rule_ka": "საშუალო სქესის არტიკლი das Dativ-ში ხდება dem: das Auto -> dem Auto.",
        "hint": "mit + Dativ (das -> dem)"
    },
    {
        "id": 4,
        "type": "dativ",
        "preposition": "mit",
        "sentence": "Nico geht heute Abend mit _______ ins Kino.",
        "correct": "seinen Freunden",
        "options": ["seine Freunde", "seinen Freunden", "seiner Freunde", "seinem Freund"],
        "translation_ka": "ნიკო დღეს საღამოს მეგობრებთან ერთად მიდის კინოში.",
        "rule_ka": "მრავლობით რიცხვში Dativ იღებს -n დაბოლოებას როგორც არტიკლზე/ნაცვალსახელზე, ისე არსებით სახელზე: die Freunde -> seinen Freunden.",
        "hint": "mit + Dativ Plural (die -> den ...-n)"
    },
    {
        "id": 5,
        "type": "dativ",
        "preposition": "nach",
        "sentence": "Nach _______ gehe ich direkt nach Hause.",
        "correct": "dem Unterricht",
        "options": ["der Unterricht", "den Unterricht", "dem Unterricht", "des Unterrichts"],
        "translation_ka": "გაკვეთილის შემდეგ პირდაპირ სახლში მივდივარ.",
        "rule_ka": "წინდებული „nach“ (შემდეგ/კენ) მართავს Dativ-ს: der Unterricht -> dem Unterricht.",
        "hint": "nach + Dativ (der -> dem)"
    },
    {
        "id": 6,
        "type": "dativ",
        "preposition": "nach",
        "sentence": "Nach _______ kocht Lukas eine Suppe.",
        "correct": "der Arbeit",
        "options": ["die Arbeit", "der Arbeit", "den Arbeit", "einer Arbeit"],
        "translation_ka": "სამუშაოს შემდეგ ლუკასი სუპს ამზადებს.",
        "rule_ka": "„nach“ მოითხოვს Dativ-ს: die Arbeit -> der Arbeit.",
        "hint": "nach + Dativ (die -> der)"
    },
    {
        "id": 7,
        "type": "dativ",
        "preposition": "aus",
        "sentence": "Frau Meier kommt ursprünglich aus _______ .",
        "correct": "der Schweiz",
        "options": ["die Schweiz", "der Schweiz", "den Schweiz", "in die Schweiz"],
        "translation_ka": "ქალბატონი მაიერი წარმოშობით შვეიცარიიდან არის.",
        "rule_ka": "წინდებული „aus“ (დან) მართავს Dativ-ს: die Schweiz (მდედრ.) -> aus der Schweiz.",
        "hint": "aus + Dativ (die -> der)"
    },
    {
        "id": 8,
        "type": "dativ",
        "preposition": "aus",
        "sentence": "Der Chef kommt gerade aus _______ .",
        "correct": "dem Büro",
        "options": ["das Büro", "den Büro", "dem Büro", "des Büros"],
        "translation_ka": "უფროსი ახლახან გამოვიდა ოფისიდან.",
        "rule_ka": "„aus“ მოითხოვს Dativ-ს: das Büro -> aus dem Büro.",
        "hint": "aus + Dativ (das -> dem)"
    },
    {
        "id": 9,
        "type": "dativ",
        "preposition": "zu",
        "sentence": "Ich fühle mich nicht gut, ich gehe zum (zu _______ ) Arzt.",
        "correct": "dem",
        "options": ["dem", "den", "der", "des"],
        "translation_ka": "თავს კარგად ვერ ვგრძნობ, ექიმთან მივდივარ (zum = zu dem).",
        "rule_ka": "წინდებული „zu“ (კენ/თან) მართავს Dativ-ს: zu + dem = zum.",
        "hint": "zu + Dativ (der -> dem -> zum)"
    },
    {
        "id": 10,
        "type": "dativ",
        "preposition": "zu",
        "sentence": "Am Sonntag fahre ich zu _______ Mutter.",
        "correct": "meiner",
        "options": ["meine", "meiner", "meinen", "meinem"],
        "translation_ka": "კვირას დედაჩემთან მივდივარ.",
        "rule_ka": "„zu“ მოითხოვს Dativ-ს: die Mutter -> zu meiner Mutter.",
        "hint": "zu + Dativ (die -> meiner)"
    },
    {
        "id": 11,
        "type": "dativ",
        "preposition": "zu",
        "sentence": "Wie komme ich zu _______ Bahnhof?",
        "correct": "dem",
        "options": ["dem", "den", "der", "das"],
        "translation_ka": "როგორ მივიდე სადგურამდე? (zum Bahnhof)",
        "rule_ka": "der Bahnhof Dativ-ში ხდება dem Bahnhof (zu + dem = zum).",
        "hint": "zu + Dativ (der -> dem)"
    },
    {
        "id": 12,
        "type": "dativ",
        "preposition": "bei",
        "sentence": "Ich wohne seit zwei Monaten bei _______ Familie.",
        "correct": "einer",
        "options": ["eine", "einer", "einem", "einen"],
        "translation_ka": "უკვე ორი თვეა ერთ ოჯახთან ვცხოვრობ.",
        "rule_ka": "წინდებული „bei“ (თან/დროს) მართავს Dativ-ს: die Familie -> bei einer Familie.",
        "hint": "bei + Dativ (die -> einer)"
    },
    {
        "id": 13,
        "type": "dativ",
        "preposition": "bei",
        "sentence": "Mein Onkel arbeitet bei _______ Firma Siemens.",
        "correct": "der",
        "options": ["die", "der", "den", "dem"],
        "translation_ka": "ბიძაჩემი ფირმა Siemens-ში მუშაობს.",
        "rule_ka": "„bei“ მოითხოვს Dativ-ს: die Firma -> bei der Firma.",
        "hint": "bei + Dativ (die -> der)"
    },
    {
        "id": 14,
        "type": "dativ",
        "preposition": "von",
        "sentence": "Das ist das neue Fahrrad von _______ Bruder.",
        "correct": "meinem",
        "options": ["mein", "meinen", "meinem", "meiner"],
        "translation_ka": "ეს ჩემი ძმის ახალი ველოსიპედია.",
        "rule_ka": "წინდებული „von“ (-ის/დან) მართავს Dativ-ს: der Bruder -> von meinem Bruder.",
        "hint": "von + Dativ (der -> meinem)"
    },
    {
        "id": 15,
        "type": "dativ",
        "preposition": "seit",
        "sentence": "Wir lernen seit _______ Jahr fleißig Deutsch.",
        "correct": "einem",
        "options": ["ein", "einen", "einem", "einer"],
        "translation_ka": "უკვე ერთი წელია ბეჯითად ვსწავლობთ გერმანულს.",
        "rule_ka": "წინდებული „seit“ (დროიდან/უკვე) მართავს Dativ-ს: das Jahr -> seit einem Jahr.",
        "hint": "seit + Dativ (das -> einem)"
    },

    # --- 2. AKKUSATIV PREPOSITIONS (12 drills) ---
    {
        "id": 16,
        "type": "akkusativ",
        "preposition": "für",
        "sentence": "Dieses schöne Buch ist für _______ Vater.",
        "correct": "meinen",
        "options": ["mein", "meinen", "meinem", "meiner"],
        "translation_ka": "ეს ლამაზი წიგნი მამაჩემისთვისაა.",
        "rule_ka": "წინდებული „für“ (თვის) ყოველთვის მოითხოვს ბრალდებით ბრუნვას (Akkusativ): der Vater -> meinen Vater.",
        "hint": "für + Akkusativ (der -> meinen)"
    },
    {
        "id": 17,
        "type": "akkusativ",
        "preposition": "für",
        "sentence": "Ich habe Blumen für _______ Mutter gekauft.",
        "correct": "meine",
        "options": ["meine", "meiner", "meinen", "meinem"],
        "translation_ka": "ყვავილები დედაჩემისთვის ვიყიდე.",
        "rule_ka": "„für“ მოითხოვს Akkusativ-ს. მდედრობითი სქესი Akkusativ-ში უცვლელია: die Mutter -> meine Mutter.",
        "hint": "für + Akkusativ (die -> meine)"
    },
    {
        "id": 18,
        "type": "akkusativ",
        "preposition": "für",
        "sentence": "Das ist ein Geschenk für _______ Kind.",
        "correct": "das",
        "options": ["das", "dem", "den", "des"],
        "translation_ka": "ეს საჩუქარია ბავშვისთვის.",
        "rule_ka": "საშუალო სქესი Akkusativ-ში უცვლელია: das Kind -> für das Kind.",
        "hint": "für + Akkusativ (das -> das)"
    },
    {
        "id": 19,
        "type": "akkusativ",
        "preposition": "ohne",
        "sentence": "Ich trinke meinen Kaffee immer ohne _______ .",
        "correct": "Zucker",
        "options": ["Zucker", "dem Zucker", "einem Zucker", "Zuckers"],
        "translation_ka": "ყავას ყოველთვის უშაქროდ (შაქრის გარეშე) ვსვამ.",
        "rule_ka": "წინდებული „ohne“ (გარეშე) მართავს Akkusativ-ს (ხშირად გამოიყენება არტიკლის გარეშე).",
        "hint": "ohne + Akkusativ"
    },
    {
        "id": 20,
        "type": "akkusativ",
        "preposition": "ohne",
        "sentence": "Ohne _______ Pass darf man nicht reisen.",
        "correct": "einen",
        "options": ["ein", "einen", "einem", "einer"],
        "translation_ka": "პასპორტის გარეშე მოგზაურობა არ შეიძლება.",
        "rule_ka": "„ohne“ მოითხოვს Akkusativ-ს: der Pass (მამრ.) -> einen Pass.",
        "hint": "ohne + Akkusativ (der -> einen)"
    },
    {
        "id": 21,
        "type": "akkusativ",
        "preposition": "ohne",
        "sentence": "Er geht nie ohne _______ Brille aus dem Haus.",
        "correct": "seine",
        "options": ["seine", "seiner", "seinem", "seinen"],
        "translation_ka": "ის სახლიდან სათვალის გარეშე არასდროს გადის.",
        "rule_ka": "die Brille (მდედრ.) Akkusativ-ში: ohne seine Brille.",
        "hint": "ohne + Akkusativ (die -> seine)"
    },
    {
        "id": 22,
        "type": "akkusativ",
        "preposition": "durch",
        "sentence": "Wir gehen jeden Sonntag spazieren durch _______ Park.",
        "correct": "den",
        "options": ["der", "den", "dem", "des"],
        "translation_ka": "ყოველ კვირას პარკში (პარკის გავლით) ვსეირნობთ.",
        "rule_ka": "წინდებული „durch“ (გავლით/მეშვეობით) მართავს Akkusativ-ს: der Park -> durch den Park.",
        "hint": "durch + Akkusativ (der -> den)"
    },
    {
        "id": 23,
        "type": "akkusativ",
        "preposition": "durch",
        "sentence": "Der Zug fährt durch _______ Tunnel.",
        "correct": "einen langen",
        "options": ["ein langer", "einen langen", "einem langen", "eines langen"],
        "translation_ka": "მატარებელი გადის გრძელ გვირაბში.",
        "rule_ka": "„durch“ მოითხოვს Akkusativ-ს: der Tunnel -> einen langen Tunnel.",
        "hint": "durch + Akkusativ (der -> einen)"
    },
    {
        "id": 24,
        "type": "akkusativ",
        "preposition": "um",
        "sentence": "Die Familie sitzt gemütlich um _______ Tisch.",
        "correct": "den",
        "options": ["der", "den", "dem", "des"],
        "translation_ka": "ოჯახი მყუდროდ ზის მაგიდის ირგვლივ.",
        "rule_ka": "წინდებული „um“ (ირგვლივ) მართავს Akkusativ-ს: der Tisch -> um den Tisch.",
        "hint": "um + Akkusativ (der -> den)"
    },
    {
        "id": 25,
        "type": "akkusativ",
        "preposition": "um",
        "sentence": "Die Bäckerei ist gleich um _______ Ecke.",
        "correct": "die",
        "options": ["die", "der", "den", "dem"],
        "translation_ka": "საცხობი პირდაპირ კუთხეშია (კუთხეს რომ მოუხვევთ).",
        "rule_ka": "„um“ მოითხოვს Akkusativ-ს: die Ecke -> um die Ecke.",
        "hint": "um + Akkusativ (die -> die)"
    },
    {
        "id": 26,
        "type": "akkusativ",
        "preposition": "gegen",
        "sentence": "Bayern München spielt heute gegen _______ BVB Dortmund.",
        "correct": "den",
        "options": ["der", "den", "dem", "des"],
        "translation_ka": "ბაიერნი დღეს დორტმუნდის ბორუსიის წინააღმდეგ თამაშობს.",
        "rule_ka": "წინდებული „gegen“ (წინააღმდეგ) მართავს Akkusativ-ს: der BVB -> gegen den BVB.",
        "hint": "gegen + Akkusativ (der -> den)"
    },
    {
        "id": 27,
        "type": "akkusativ",
        "preposition": "gegen",
        "sentence": "Haben Sie ein Medikament gegen _______ Kopfschmerzen?",
        "correct": "die",
        "options": ["die", "der", "den", "dem"],
        "translation_ka": "გაქვთ წამალი თავის ტკივილის წინააღმდეგ?",
        "rule_ka": "„gegen“ მოითხოვს Akkusativ-ს: die Kopfschmerzen (მრავლ.) -> gegen die Kopfschmerzen.",
        "hint": "gegen + Akkusativ (Plural -> die)"
    },

    # --- 3. WECHSELPRAEPOSITIONEN (Wo? Dativ vs. Wohin? Akkusativ) (13 drills) ---
    {
        "id": 28,
        "type": "wechsel",
        "preposition": "in",
        "sentence": "Wo ist Peter? - Er ist im (in _______ ) Supermarkt.",
        "correct": "dem",
        "options": ["dem", "den", "der", "das"],
        "translation_ka": "სად არის პეტერი? - ის სუპერმარკეტშია (im = in dem).",
        "rule_ka": "შეკითხვაზე „Wo?“ (სად? სტატიკური მდებარეობა) Wechselpräposition მოითხოვს Dativ-ს: in + dem = im.",
        "hint": "Wo? -> Dativ (der -> dem -> im)"
    },
    {
        "id": 29,
        "type": "wechsel",
        "preposition": "in",
        "sentence": "Wohin geht Peter? - Er geht in _______ Supermarkt.",
        "correct": "den",
        "options": ["der", "den", "dem", "im"],
        "translation_ka": "სად (საით) მიდის პეტერი? - ის მიდის სუპერმარკეტში.",
        "rule_ka": "შეკითხვაზე „Wohin?“ (სად? მიმართულება/მოძრაობა) Wechselpräposition მოითხოვს Akkusativ-ს: in + den Supermarkt.",
        "hint": "Wohin? -> Akkusativ (der -> den)"
    },
    {
        "id": 30,
        "type": "wechsel",
        "preposition": "in",
        "sentence": "Wo wohnst du? - Ich wohne in _______ Stadtmitte.",
        "correct": "der",
        "options": ["die", "der", "den", "in die"],
        "translation_ka": "სად ცხოვრობ? - ქალაქის ცენტრში ვცხოვრობ.",
        "rule_ka": "Wo? (სად?) -> Dativ: die Stadtmitte (მდედრ.) Dativ-ში ხდება der: in der Stadtmitte.",
        "hint": "Wo? -> Dativ (die -> der)"
    },
    {
        "id": 31,
        "type": "wechsel",
        "preposition": "in",
        "sentence": "Wohin fährst du am Samstag? - Ich fahre in _______ Stadt.",
        "correct": "die",
        "options": ["die", "der", "den", "in der"],
        "translation_ka": "სად მიდიხარ შაბათს? - ქალაქში მივდივარ.",
        "rule_ka": "Wohin? (საით?) -> Akkusativ: die Stadt (მდედრ.) Akkusativ-ში უცვლელია: in die Stadt.",
        "hint": "Wohin? -> Akkusativ (die -> die)"
    },
    {
        "id": 32,
        "type": "wechsel",
        "preposition": "in",
        "sentence": "Die Dokumente liegen in _______ Regal.",
        "correct": "dem",
        "options": ["das", "dem", "den", "des"],
        "translation_ka": "დოკუმენტები თაროზე დევს (Wo? -> Regal-ში).",
        "rule_ka": "Wo? (სად დევს?) -> Dativ: das Regal -> in dem (im) Regal.",
        "hint": "Wo? -> Dativ (das -> dem)"
    },
    {
        "id": 33,
        "type": "wechsel",
        "preposition": "auf",
        "sentence": "Wo liegt die Zeitung? - Sie liegt auf _______ Tisch.",
        "correct": "dem",
        "options": ["der", "den", "dem", "das"],
        "translation_ka": "სად დევს გაზეთი? - ის მაგიდაზე დევს.",
        "rule_ka": "Wo? (სად? მაგიდაზე დევს) -> Dativ: der Tisch -> auf dem Tisch.",
        "hint": "Wo? -> Dativ (der -> dem)"
    },
    {
        "id": 34,
        "type": "wechsel",
        "preposition": "auf",
        "sentence": "Wohin legst du das Handy? - Ich lege es auf _______ Tisch.",
        "correct": "den",
        "options": ["der", "den", "dem", "das"],
        "translation_ka": "სად დებ ტელეფონს? - მაგიდაზე ვდებ.",
        "rule_ka": "Wohin? (საით? ვდებ) -> Akkusativ: der Tisch -> auf den Tisch.",
        "hint": "Wohin? -> Akkusativ (der -> den)"
    },
    {
        "id": 35,
        "type": "wechsel",
        "preposition": "auf",
        "sentence": "Wir kaufen am Samstag frisches Obst auf _______ Markt.",
        "correct": "dem",
        "options": ["der", "den", "dem", "das"],
        "translation_ka": "შაბათს ბაზარზე ვყიდულობთ ახალ ხილს.",
        "rule_ka": "Wo? (სად ვყიდულობთ? ბაზარზე) -> Dativ: der Markt -> auf dem Markt.",
        "hint": "Wo? -> Dativ (der -> dem)"
    },
    {
        "id": 36,
        "type": "wechsel",
        "preposition": "an",
        "sentence": "Der ICE-Zug steht schon an _______ Bahnsteig 4.",
        "correct": "dem",
        "options": ["der", "den", "dem", "das"],
        "translation_ka": "სწრაფი მატარებელი უკვე მე-4 ბაქანთან დგას.",
        "rule_ka": "Wo? (სად დგას? ბაქანთან) -> Dativ: der Bahnsteig -> an dem (am) Bahnsteig.",
        "hint": "Wo? -> Dativ (der -> dem -> am)"
    },
    {
        "id": 37,
        "type": "wechsel",
        "preposition": "an",
        "sentence": "Ich hänge das neue Foto an _______ Wand.",
        "correct": "die",
        "options": ["die", "der", "den", "dem"],
        "translation_ka": "ახალ ფოტოს კედელზე ვკიდებ.",
        "rule_ka": "Wohin? (საით ვკიდებ? მოქმედება) -> Akkusativ: die Wand -> an die Wand.",
        "hint": "Wohin? -> Akkusativ (die -> die)"
    },
    {
        "id": 38,
        "type": "wechsel",
        "preposition": "neben",
        "sentence": "Maria sitzt in der Schule neben _______ Freundin.",
        "correct": "ihrer",
        "options": ["ihre", "ihrer", "ihrem", "ihren"],
        "translation_ka": "მარია სკოლაში თავის მეგობარ გოგოს გვერდით ზის.",
        "rule_ka": "Wo? (სად ზის? გვერდით) -> Dativ: die Freundin (მდედრ.) -> neben ihrer Freundin.",
        "hint": "Wo? -> Dativ (die -> ihrer)"
    },
    {
        "id": 39,
        "type": "wechsel",
        "preposition": "unter",
        "sentence": "Die kleine Katze schläft unter _______ Bett.",
        "correct": "dem",
        "options": ["das", "dem", "den", "des"],
        "translation_ka": "პატარა კატას საწოლის ქვეშ სძინავს.",
        "rule_ka": "Wo? (სად სძინავს?) -> Dativ: das Bett -> unter dem Bett.",
        "hint": "Wo? -> Dativ (das -> dem)"
    },
    {
        "id": 40,
        "type": "wechsel",
        "preposition": "vor",
        "sentence": "Wir treffen uns um 19 Uhr vor _______ Kino.",
        "correct": "dem",
        "options": ["das", "dem", "den", "des"],
        "translation_ka": "19:00 საათზე კინოთეატრის წინ ვხვდებით.",
        "rule_ka": "Wo? (სად ვხვდებით?) -> Dativ: das Kino -> vor dem Kino.",
        "hint": "Wo? -> Dativ (das -> dem)"
    }
]

# ==============================================================================
# 5. HÖR-DIKTAT (A1 AUDIO DICTATION LAB DATASET - 15 TASKS)
# Categories:
# - Buchstabieren: Namen & Straßen (მართლწერა ასო-ასო)
# - Nummern: Handynummern, Zimmernummern, Postleitzahlen
# - Uhrzeiten: Digitale & umgangssprachliche Zeitangaben
# - Preise: Geldbeträge in Euro und Cent
# - Mustersätze: A1 Alltagskommunikation
# ==============================================================================
A1_HÖR_DIKTAT_DATA = [
    # 1. Buchstabieren (4 tasks)
    {
        "id": "dik_1",
        "category": "buchstabieren",
        "category_ka": "მართლწერა (Buchstabieren)",
        "title": "გვარის მართლწერა (Nachname buchstabieren)",
        "prompt_ka": "მოუსმინეთ აუდიოს და ჩაწერეთ მოქალაქის გვარი გერმანული მართლწერით:",
        "audio_text": "Mein Nachname ist Schneider. Ich buchstabiere: S - C - H - N - E - I - D - E - R. Schneider.",
        "expected": "Schneider",
        "accepted": ["schneider", "Schneider"],
        "hint": "S - C - H - N - E - I - D - E - R (ei = [აი])",
        "explanation": "გერმანულში გვარი იწერება დიდი ასოთი: Schneider. ასოთშეხამება SCH = [შ], ხოლო EI = [აი]."
    },
    {
        "id": "dik_2",
        "category": "buchstabieren",
        "category_ka": "მართლწერა (Buchstabieren)",
        "title": "ქალაქის სახელის მართლწერა",
        "prompt_ka": "მოუსმინეთ და ჩაწერეთ გერმანიის ქალაქის სახელი:",
        "audio_text": "Ich wohne in Leipzig. Buchstabiert: L - E - I - P - Z - I - G. Leipzig.",
        "expected": "Leipzig",
        "accepted": ["leipzig", "Leipzig"],
        "hint": "L - E - I - P - Z - I - G (Z = [ც])",
        "explanation": "Leipzig (ლაიფციგი): ასო Z გერმანულში ყოველთვის იკითხება როგორც [ც]."
    },
    {
        "id": "dik_3",
        "category": "buchstabieren",
        "category_ka": "მართლწერა (Buchstabieren)",
        "title": "ქუჩის სახელის მართლწერა (Straße)",
        "prompt_ka": "მოუსმინეთ და ჩაწერეთ ქუჩის დასახელება:",
        "audio_text": "Meine Adresse ist Blumenstraße. B - L - U - M - E - N - S - T - R - A - Doppel-S - E. Blumenstraße.",
        "expected": "Blumenstraße",
        "accepted": ["blumenstraße", "Blumenstraße", "blumenstrasse", "Blumenstrasse"],
        "hint": "B - L - U - M - E - N - S - T - R - A - ß - E (შეიძლება ჩაიწეროს როგორც ß, ისე ss)",
        "explanation": "Blumenstraße (ყვავილების ქუჩა). გერმანული ასო ß (Eszett) შეიძლება დაიწეროს როგორც ß ან ss."
    },
    {
        "id": "dik_4",
        "category": "buchstabieren",
        "category_ka": "მართლწერა (Buchstabieren)",
        "title": "გვარის მართლწერა უმლაუტით (Umlaut)",
        "prompt_ka": "მოუსმინეთ და ჩაწერეთ გერმანული გვარი:",
        "audio_text": "Frau Müller kommt heute. Ich buchstabiere: M - U-Umlaut - Doppel-L - E - R. Müller.",
        "expected": "Müller",
        "accepted": ["müller", "Müller", "mueller", "Mueller"],
        "hint": "M - ü - l - l - e - r (U-Umlaut = Ü / ue)",
        "explanation": "Müller: U-Umlaut (Ü) კლავიატურაზე თუ არ გაქვთ, სტანდარტულად ჩაიწერება როგორც ue."
    },

    # 2. Nummern & Telefon (4 tasks)
    {
        "id": "dik_5",
        "category": "nummern",
        "category_ka": "ნომრები & ტელეფონი",
        "title": "მობილურის ნომრის ჩაწერა (Handynummer)",
        "prompt_ka": "მოუსმინეთ და ჩაწერეთ მობილური ტელეფონის ნომერი (ციფრებით):",
        "audio_text": "Meine Handynummer ist: null - eins - sieben - sechs - vier - fünf - acht - neun - zwei - drei.",
        "expected": "0176458923",
        "accepted": ["0176458923", "0176 45 89 23", "0176-45-89-23", "0176/458923"],
        "hint": "null (0), eins (1), sieben (7), sechs (6), vier (4), fünf (5), acht (8), neun (9), zwei (2), drei (3)",
        "explanation": "გერმანული ციფრები: null (0), eins (1), sieben (7), sechs (6), vier (4), fünf (5), acht (8), neun (9), zwei (2), drei (3)."
    },
    {
        "id": "dik_6",
        "category": "nummern",
        "category_ka": "ნომრები & ტელეფონი",
        "title": "სასტუმროს ოთახის ნომერი (Zimmernummer)",
        "prompt_ka": "მოუსმინეთ და ჩაწერეთ სასტუმროს ოთახის ნომერი (ციფრებით):",
        "audio_text": "Ihr Zimmer ist die Nummer dreihundertvierzehn. Ich wiederhole: Zimmer drei - eins - vier.",
        "expected": "314",
        "accepted": ["314", "Zimmer 314", "zimmer 314"],
        "hint": "dreihundertvierzehn = 314",
        "explanation": "dreihundert (300) + vierzehn (14) = 314."
    },
    {
        "id": "dik_7",
        "category": "nummern",
        "category_ka": "ნომრები & ტელეფონი",
        "title": "საფოსტო ინდექსი (Postleitzahl - PLZ)",
        "prompt_ka": "მოუსმინეთ და ჩაწერეთ ბერლინის საფოსტო ინდექსი (5 ციფრი):",
        "audio_text": "Die Postleitzahl von Berlin-Mitte ist eins - null - eins - eins - sieben. Zehntausendeinhundertsiebzehn.",
        "expected": "10117",
        "accepted": ["10117"],
        "hint": "eins - null - eins - eins - sieben = 10117",
        "explanation": "გერმანიის საფოსტო ინდექსი (PLZ) ყოველთვის 5-ნიშნაა: 10117."
    },
    {
        "id": "dik_8",
        "category": "nummern",
        "category_ka": "ნომრები & ტელეფონი",
        "title": "გადაუდებელი დახმარების ნომერი (Notfallnummer)",
        "prompt_ka": "მოუსმინეთ და ჩაწერეთ ექიმის გადაუდებელი დახმარების ნომერი:",
        "audio_text": "Im Notfall wählen Sie bitte die Nummer: eins - eins - sechs - eins - eins - sieben.",
        "expected": "116117",
        "accepted": ["116117", "116 117", "116-117"],
        "hint": "eins-eins-sechs-eins-eins-sieben = 116117",
        "explanation": "116 117 არის გერმანიის ოფიციალური სამედიცინო სადისპეტჩერო სამსახურის ნომერი."
    },

    # 3. Uhrzeiten (3 tasks)
    {
        "id": "dik_9",
        "category": "uhrzeit",
        "category_ka": "საათი & განრიგი",
        "title": "მატარებლის გამგზავრების დრო (Uhrzeit)",
        "prompt_ka": "მოუსმინეთ და ჩაწერეთ მატარებლის გამგზავრების დრო (ფორმატში HH:MM):",
        "audio_text": "Der Zug nach München fährt um vierzehn Uhr dreißig ab. Vierzehn Uhr dreißig.",
        "expected": "14:30",
        "accepted": ["14:30", "14.30", "14:30 Uhr", "14:30 uhr"],
        "hint": "vierzehn Uhr dreißig = 14:30",
        "explanation": "vierzehn (14) Uhr dreißig (30) = 14:30."
    },
    {
        "id": "dik_10",
        "category": "uhrzeit",
        "category_ka": "საათი & განრიგი",
        "title": "ექიმთან შეხვედრის დრო (halb)",
        "prompt_ka": "მოუსმინეთ და ჩაწერეთ ექიმთან ვიზიტის დრო (ფორმატში HH:MM):",
        "audio_text": "Ihr Termin beim Arzt ist morgen früh um halb neun. Halb neun.",
        "expected": "08:30",
        "accepted": ["08:30", "8:30", "08.30", "8.30"],
        "hint": "halb neun = 08:30 (გერმანულში halb neun ნიშნავს 9-ის ნახევარს, ანუ 08:30-ს)",
        "explanation": "გერმანული წესი: „halb neun“ ნიშნავს, რომ ცხრამდე დარჩენილია ნახევარი საათი, ანუ 08:30."
    },
    {
        "id": "dik_11",
        "category": "uhrzeit",
        "category_ka": "საათი & განრიგი",
        "title": "შეხვედრის დრო (Viertel nach)",
        "prompt_ka": "მოუსმინეთ და ჩაწერეთ შეხვედრის დრო (ფორმატში HH:MM):",
        "audio_text": "Wir treffen uns um Viertel nach fünf am Nachmittag. Viertel nach fünf.",
        "expected": "17:15",
        "accepted": ["17:15", "5:15", "17.15", "5.15"],
        "hint": "Viertel nach fünf am Nachmittag = 17:15",
        "explanation": "Viertel nach fünf (5-ს გადაცილებული 15 წუთი) + am Nachmittag (ნაშუადღევს) = 17:15."
    },

    # 4. Preise & Beträge (2 tasks)
    {
        "id": "dik_12",
        "category": "preise",
        "category_ka": "ფასები & თანხები",
        "title": "პროდუქტის ფასის ჩაწერა (Preis)",
        "prompt_ka": "მოუსმინეთ და ჩაწერეთ წიგნის ფასი (მაგ. 14,99 ან 14.99):",
        "audio_text": "Das Buch kostet vierzehn Euro neunundneunzig. Vierzehn Euro neunundneunzig.",
        "expected": "14,99",
        "accepted": ["14,99", "14.99", "14,99 Euro", "14.99 Euro", "14,99 €", "14.99 €"],
        "hint": "vierzehn Euro neunundneunzig = 14,99",
        "explanation": "vierzehn (14) Euro + neunundneunzig (99) Cent = 14,99 €."
    },
    {
        "id": "dik_13",
        "category": "preise",
        "category_ka": "ფასები & თანხები",
        "title": "ბილეთის ფასის ჩაწერა",
        "prompt_ka": "მოუსმინეთ და ჩაწერეთ მატარებლის ბილეთის ფასი:",
        "audio_text": "Die Fahrkarte nach Hamburg kostet achtundzwanzig Euro fünfzig. Achtundzwanzig Euro fünfzig.",
        "expected": "28,50",
        "accepted": ["28,50", "28.50", "28,50 Euro", "28.50 Euro", "28,50 €", "28.50 €"],
        "hint": "achtundzwanzig Euro fünfzig = 28,50",
        "explanation": "achtundzwanzig (28) Euro + fünfzig (50) Cent = 28,50 €."
    },

    # 5. A1 Mustersätze (2 tasks)
    {
        "id": "dik_14",
        "category": "saetze",
        "category_ka": "A1 წინადადებები",
        "title": "მოკლე წინადადება: სასტუმროში რეგისტრაცია",
        "prompt_ka": "მოუსმინეთ და ჩაწერეთ მთლიანი წინადადება გერმანულად:",
        "audio_text": "Ich habe ein Zimmer reserviert.",
        "expected": "Ich habe ein Zimmer reserviert.",
        "accepted": ["Ich habe ein Zimmer reserviert.", "ich habe ein zimmer reserviert", "Ich habe ein Zimmer reserviert", "Ich habe ein zimmer reserviert."],
        "hint": "Ich habe ein Zimmer reserviert. (Perfect ფორმა)",
        "explanation": "Perfekt დროში: დამხმარე ზმნა habe მე-2 ადგილზე, ნამყო მიმღეობა reserviert ბოლოში. არსებითი სახელი Zimmer იწერება დიდი ასოთი."
    },
    {
        "id": "dik_15",
        "category": "saetze",
        "category_ka": "A1 წინადადებები",
        "title": "მოკლე წინადადება: თავაზიანი თხოვნა",
        "prompt_ka": "მოუსმინეთ და ჩაწერეთ კაფეში შეკვეთის ფრაზა:",
        "audio_text": "Ich möchte bitte einen Kaffee.",
        "expected": "Ich möchte bitte einen Kaffee.",
        "accepted": ["Ich möchte bitte einen Kaffee.", "ich möchte bitte einen kaffee", "Ich möchte bitte einen Kaffee", "ich moechte bitte einen kaffee"],
        "hint": "Ich möchte bitte einen Kaffee. (möchte + Akkusativ)",
        "explanation": "A1 თავაზიანი ფორმულა: Ich möchte bitte einen Kaffee (მამრ. Akkusativ: der -> einen)."
    }
]


