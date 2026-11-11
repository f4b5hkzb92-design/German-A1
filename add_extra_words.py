# -*- coding: utf-8 -*-
import sys

extra_words = [
    # --- ფერები (Farben) ---
    {"id": "farbe_rot", "word": "rot", "article": "", "gender": "none", "plural": "", "pos": "ზედსართავი სახელი", "georgian": "წითელი", "example_de": "Die Tomate ist rot.", "example_ka": "პომიდორი წითელია.", "category": "ფერები"},
    {"id": "farbe_blau", "word": "blau", "article": "", "gender": "none", "plural": "", "pos": "ზედსართავი სახელი", "georgian": "ლურჯი", "example_de": "Der Himmel ist heute blau.", "example_ka": "ცა დღეს ლურჯია.", "category": "ფერები"},
    {"id": "farbe_grun", "word": "grün", "article": "", "gender": "none", "plural": "", "pos": "ზედსართავი სახელი", "georgian": "მწვანე", "example_de": "Der Apfel ist grün.", "example_ka": "ვაშლი მწვანეა.", "category": "ფერები"},
    {"id": "farbe_gelb", "word": "gelb", "article": "", "gender": "none", "plural": "", "pos": "ზედსართავი სახელი", "georgian": "ყვითელი", "example_de": "Die Sonne ist gelb.", "example_ka": "მზე ყვითელია.", "category": "ფერები"},
    {"id": "farbe_schwarz", "word": "schwarz", "article": "", "gender": "none", "plural": "", "pos": "ზედსართავი სახელი", "georgian": "შავი", "example_de": "Ich trage eine schwarze Hose.", "example_ka": "შავი შარვალი მაცვია.", "category": "ფერები"},
    {"id": "farbe_weiss", "word": "weiß", "article": "", "gender": "none", "plural": "", "pos": "ზედსართავი სახელი", "georgian": "თეთრი", "example_de": "Der Schnee ist weiß.", "example_ka": "თოვლი თეთრია.", "category": "ფერები"},
    {"id": "farbe_grau", "word": "grau", "article": "", "gender": "none", "plural": "", "pos": "ზედსართავი სახელი", "georgian": "ნაცრისფერი", "example_de": "Die Wolken sind grau.", "example_ka": "ღრუბლები ნაცრისფერია.", "category": "ფერები"},
    {"id": "farbe_braun", "word": "braun", "article": "", "gender": "none", "plural": "", "pos": "ზედსართავი სახელი", "georgian": "ყავისფერი", "example_de": "Er hat braune Augen.", "example_ka": "მას ყავისფერი თვალები აქვს.", "category": "ფერები"},

    # --- ტანსაცმელი (Kleidung) ---
    {"id": "kleidung", "word": "die Kleidung", "article": "die", "gender": "f", "plural": "-", "pos": "არსებითი სახელი", "georgian": "ტანსაცმელი", "example_de": "Ich kaufe warme Kleidung für den Winter.", "example_ka": "ზამთრისთვის თბილ ტანსაცმელს ვყიდულობ.", "category": "ტანსაცმელი"},
    {"id": "hose", "word": "die Hose", "article": "die", "gender": "f", "plural": "-n", "pos": "არსებითი სახელი", "georgian": "შარვალი", "example_de": "Diese Hose passt mir perfekt.", "example_ka": "ეს შარვალი ზედგამოჭრილია ჩემთვის.", "category": "ტანსაცმელი"},
    {"id": "hemd", "word": "das Hemd", "article": "das", "gender": "n", "plural": "-en", "pos": "არსებითი სახელი", "georgian": "პერანგი (მამაკაცის)", "example_de": "Er trägt ein weißes Hemd.", "example_ka": "მას თეთრი პერანგი აცვია.", "category": "ტანსაცმელი"},
    {"id": "bluse", "word": "die Bluse", "article": "die", "gender": "f", "plural": "-n", "pos": "არსებითი სახელი", "georgian": "ბლუზა (ქალის)", "example_de": "Die Bluse ist aus Seide.", "example_ka": "ბლუზა აბრეშუმისგანაა.", "category": "ტანსაცმელი"},
    {"id": "kleid", "word": "das Kleid", "article": "das", "gender": "n", "plural": "-er", "pos": "არსებითი სახელი", "georgian": "კაბა", "example_de": "Das rote Kleid sieht sehr hübsch aus.", "example_ka": "წითელი კაბა ძალიან ლამაზად გამოიყურება.", "category": "ტანსაცმელი"},
    {"id": "jacke", "word": "die Jacke", "article": "die", "gender": "f", "plural": "-n", "pos": "არსებითი სახელი", "georgian": "ქურთუკი / პიჯაკი", "example_de": "Zieh deine Jacke an, es ist kalt!", "example_ka": "ჩაიცვი ქურთუკი, ცივა!", "category": "ტანსაცმელი"},
    {"id": "mantel", "word": "der Mantel", "article": "der", "gender": "m", "plural": "-ä-", "pos": "არსებითი სახელი", "georgian": "პალტო", "example_de": "Der Mantel hält sehr warm.", "example_ka": "პალტო ძალიან კარგად ათბობს.", "category": "ტანსაცმელი"},
    {"id": "schuhe", "word": "die Schuhe", "article": "die", "gender": "pl", "plural": "(მრავლობითი)", "pos": "არსებითი სახელი", "georgian": "ფეხსაცმელი", "example_de": "Meine neuen Schuhe sind bequem.", "example_ka": "ჩემი ახალი ფეხსაცმელი მოხერხებულია.", "category": "ტანსაცმელი"},
    {"id": "mutze", "word": "die Mütze", "article": "die", "gender": "f", "plural": "-n", "pos": "არსებითი სახელი", "georgian": "ქუდი (ნაქსოვი/თბილი)", "example_de": "Im Winter trage ich eine Mütze.", "example_ka": "ზამთარში ქუდს ვატარებ.", "category": "ტანსაცმელი"},
    {"id": "brille", "word": "die Brille", "article": "die", "gender": "f", "plural": "-n", "pos": "არსებითი სახელი", "georgian": "სათვალე", "example_de": "Wo ist meine Brille? Ich kann nicht lesen.", "example_ka": "სად არის ჩემი სათვალე? ვერ ვკითხულობ.", "category": "ტანსაცმელი"},
    {"id": "tasche", "word": "die Tasche", "article": "die", "gender": "f", "plural": "-n", "pos": "არსებითი სახელი", "georgian": "ჩანთა", "example_de": "Die Tasche ist sehr schwer.", "example_ka": "ჩანთა ძალიან მძიმეა.", "category": "ტანსაცმელი"},

    # --- სწავლა და ენა (Lernen & Sprache) ---
    {"id": "sprache", "word": "die Sprache", "article": "die", "gender": "f", "plural": "-n", "pos": "არსებითი სახელი", "georgian": "ენა", "example_de": "Welche Sprachen sprichst du?", "example_ka": "რომელ ენებზე ლაპარაკობ?", "category": "სწავლა & ენა"},
    {"id": "wort", "word": "das Wort", "article": "das", "gender": "n", "plural": "-ö-er", "pos": "არსებითი სახელი", "georgian": "სიტყვა", "example_de": "Was bedeutet dieses Wort auf Georgisch?", "example_ka": "რას ნიშნავს ეს სიტყვა ქართულად?", "category": "სწავლა & ენა"},
    {"id": "satz", "word": "der Satz", "article": "der", "gender": "m", "plural": "-ä-e", "pos": "არსებითი სახელი", "georgian": "წინადადება", "example_de": "Bilde bitte einen vollständigen Satz!", "example_ka": "შეადგინე სრული წინადადება, გეთაყვა!", "category": "სწავლა & ენა"},
    {"id": "grammatik", "word": "die Grammatik", "article": "die", "gender": "f", "plural": "-", "pos": "არსებითი სახელი", "georgian": "გრამატიკა", "example_de": "Die deutsche Grammatik ist logisch.", "example_ka": "გერმანული გრამატიკა ლოგიკურია.", "category": "სწავლა & ენა"},
    {"id": "ubung", "word": "die Übung", "article": "die", "gender": "f", "plural": "-en", "pos": "არსებითი სახელი", "georgian": "სავარჯიშო", "example_de": "Wir machen eine Grammatikübung.", "example_ka": "გრამატიკულ სავარჯიშოს ვაკეთებთ.", "category": "სწავლა & ენა"},
    {"id": "test", "word": "der Test", "article": "der", "gender": "m", "plural": "-s", "pos": "არსებითი სახელი", "georgian": "ტესტი", "example_de": "Ich habe den Test mit 100% bestanden!", "example_ka": "ტესტი 100%-ით ჩავაბარე!", "category": "სწავლა & ენა"},
    {"id": "prufung", "word": "die Prüfung", "article": "die", "gender": "f", "plural": "-en", "pos": "არსებითი სახელი", "georgian": "გამოცდა", "example_de": "Die A1-Prüfung findet nächste Woche statt.", "example_ka": "A1 გამოცდა მომავალ კვირას გაიმართება.", "category": "სწავლა & ენა"},
    {"id": "frage", "word": "die Frage", "article": "die", "gender": "f", "plural": "-n", "pos": "არსებითი სახელი", "georgian": "შეკითხვა", "example_de": "Darf ich eine Frage stellen?", "example_ka": "შეიძლება შეკითხვა დავსვა?", "category": "სწავლა & ენა"},
    {"id": "antwort", "word": "die Antwort", "article": "die", "gender": "f", "plural": "-en", "pos": "არსებითი სახელი", "georgian": "პასუხი", "example_de": "Das ist die richtige Antwort.", "example_ka": "ეს სწორი პასუხია.", "category": "სწავლა & ენა"},
    {"id": "beispiel", "word": "das Beispiel", "article": "das", "gender": "n", "plural": "-e", "pos": "არსებითი სახელი", "georgian": "მაგალითი (zum Beispiel = მაგალითად)", "example_de": "Geben Sie bitte ein Beispiel!", "example_ka": "მოიყვანეთ მაგალითი, გეთაყვა!", "category": "სწავლა & ენა"},
    {"id": "worterbuch", "word": "das Wörterbuch", "article": "das", "gender": "n", "plural": "-ü-er", "pos": "არსებითი სახელი", "georgian": "ლექსიკონი", "example_de": "Ich schlage das Wort im Wörterbuch nach.", "example_ka": "სიტყვას ლექსიკონში ვამოწმებ.", "category": "სწავლა & ენა"},
    {"id": "buch", "word": "das Buch", "article": "das", "gender": "n", "plural": "-ü-er", "pos": "არსებითი სახელი", "georgian": "წიგნი", "example_de": "Das Buch ist sehr interessant.", "example_ka": "წიგნი ძალიან საინტერესოა.", "category": "სწავლა & ენა"},
    {"id": "heft", "word": "das Heft", "article": "das", "gender": "n", "plural": "-e", "pos": "არსებითი სახელი", "georgian": "რვეული", "example_de": "Schreibe die Wörter in dein Heft!", "example_ka": "ჩაწერე სიტყვები შენს რვეულში!", "category": "სწავლა & ენა"},
    {"id": "bleistift", "word": "der Bleistift", "article": "der", "gender": "m", "plural": "-e", "pos": "არსებითი სახელი", "georgian": "ფანქარი", "example_de": "Ich schreibe Notizen mit dem Bleistift.", "example_ka": "ჩანაწერებს ფანქრით ვაკეთებ.", "category": "სწავლა & ენა"},
    {"id": "kugelschreiber", "word": "der Kugelschreiber", "article": "der", "gender": "m", "plural": "-", "pos": "არსებითი სახელი", "georgian": "კალამი (Kuli)", "example_de": "Hast du einen Kugelschreiber für mich?", "example_ka": "გაქვს კალამი ჩემთვის?", "category": "სწავლა & ენა"},

    # --- მოგზაურობა, დოკუმენტები და ყოველდღიურობა (Reisen & Alltag) ---
    {"id": "urlaub", "word": "der Urlaub", "article": "der", "gender": "m", "plural": "-e", "pos": "არსებითი სახელი", "georgian": "შვებულება / არდადეგები", "example_de": "Ich fahre im August in den Urlaub.", "example_ka": "აგვისტოში მივდივარ შვებულებაში.", "category": "მოგზაურობა & დოკუმენტები"},
    {"id": "reise", "word": "die Reise", "article": "die", "gender": "f", "plural": "-n", "pos": "არსებითი სახელი", "georgian": "მოგზაურობა / მგზავრობა", "example_de": "Gute Reise!", "example_ka": "ბედნიერ მგზავრობას გისურვებთ!", "category": "მოგზაურობა & დოკუმენტები"},
    {"id": "meer", "word": "das Meer", "article": "das", "gender": "n", "plural": "-e", "pos": "არსებითი სახელი", "georgian": "ზღვა", "example_de": "Wir schwimmen im Meer.", "example_ka": "ზღვაში ვცურავთ.", "category": "მოგზაურობა & დოკუმენტები"},
    {"id": "strand", "word": "der Strand", "article": "der", "gender": "m", "plural": "-ä-e", "pos": "არსებითი სახელი", "georgian": "პლაჟი / სანაპირო", "example_de": "Wir liegen am Strand in Batumi.", "example_ka": "ბათუმში პლაჟზე ვწევართ.", "category": "მოგზაურობა & დოკუმენტები"},
    {"id": "berge", "word": "die Berge", "article": "die", "gender": "pl", "plural": "(მრავლობითი)", "pos": "არსებითი სახელი", "georgian": "მთები", "example_de": "In Georgien gibt es wunderschöne Berge.", "example_ka": "საქართველოში ულამაზესი მთებია.", "category": "მოგზაურობა & დოკუმენტები"},
    {"id": "koffer", "word": "der Koffer", "article": "der", "gender": "m", "plural": "-", "pos": "არსებითი სახელი", "georgian": "ჩემოდანი", "example_de": "Ich packe meinen Koffer.", "example_ka": "ჩემოდანს ვალაგებ.", "category": "მოგზაურობა & დოკუმენტები"},
    {"id": "pass", "word": "der Pass", "article": "der", "gender": "m", "plural": "-ä-e", "pos": "არსებითი სახელი", "georgian": "პასპორტი", "example_de": "Zeigen Sie bitte Ihren Pass!", "example_ka": "მაჩვენეთ თქვენი პასპორტი, გეთაყვა!", "category": "მოგზაურობა & დოკუმენტები"},
    {"id": "ausweis", "word": "der Ausweis", "article": "der", "gender": "m", "plural": "-e", "pos": "არსებითი სახელი", "georgian": "პირადობის მოწმობა", "example_de": "Hier ist mein Personalausweis.", "example_ka": "აი ჩემი პირადობის მოწმობა.", "category": "მოგზაურობა & დოკუმენტები"},
    {"id": "flugzeug", "word": "das Flugzeug", "article": "das", "gender": "n", "plural": "-e", "pos": "არსებითი სახელი", "georgian": "თვითმფრინავი", "example_de": "Das Flugzeug startet pünktlich.", "example_ka": "თვითმფრინავი დროულად ფრინდება.", "category": "მოგზაურობა & დოკუმენტები"},
    {"id": "ticket", "word": "das Ticket", "article": "das", "gender": "n", "plural": "-s", "pos": "არსებითი სახელი", "georgian": "ბილეთი", "example_de": "Ich habe ein Flugticket nach Berlin.", "example_ka": "ბერლინის ავიაბილეთი მაქვს.", "category": "მოგზაურობა & დოკუმენტები"},
    {"id": "schlussel", "word": "der Schlüssel", "article": "der", "gender": "m", "plural": "-", "pos": "არსებითი სახელი", "georgian": "გასაღები", "example_de": "Ich finde meinen Schlüssel nicht.", "example_ka": "ჩემს გასაღებს ვერ ვპოულობ.", "category": "მოგზაურობა & დოკუმენტები"},
    {"id": "handy", "word": "das Handy", "article": "das", "gender": "n", "plural": "-s", "pos": "არსებითი სახელი", "georgian": "მობილური ტელეფონი", "example_de": "Meine Handynummer ist 0176...", "example_ka": "ჩემი მობილურის ნომერია 0176...", "category": "მოგზაურობა & დოკუმენტები"},
    {"id": "computer", "word": "der Computer", "article": "der", "gender": "m", "plural": "-", "pos": "არსებითი სახელი", "georgian": "კომპიუტერი", "example_de": "Ich arbeite am Computer.", "example_ka": "კომპიუტერთან ვმუშაობ.", "category": "მოგზაურობა & დოკუმენტები"},
    {"id": "rechnung", "word": "die Rechnung", "article": "die", "gender": "f", "plural": "-en", "pos": "არსებითი სახელი", "georgian": "ანგარიში / ჩეკი", "example_de": "Die Rechnung, bitte!", "example_ka": "ანგარიში, გეთაყვა!", "category": "მოგზაურობა & დოკუმენტები"},

    # --- კალენდარი და სეზონები (Monate & Jahreszeiten) ---
    {"id": "fruhling", "word": "der Frühling", "article": "der", "gender": "m", "plural": "-", "pos": "არსებითი სახელი", "georgian": "გაზაფხული", "example_de": "Im Frühling blühen die Blumen.", "example_ka": "გაზაფხულზე ყვავილები ყვავის.", "category": "კალენდარი & სეზონები"},
    {"id": "sommer", "word": "der Sommer", "article": "der", "gender": "m", "plural": "-", "pos": "არსებითი სახელი", "georgian": "ზაფხული", "example_de": "Im Sommer ist es sehr warm.", "example_ka": "ზაფხულში ძალიან თბილა.", "category": "კალენდარი & სეზონები"},
    {"id": "herbst", "word": "der Herbst", "article": "der", "gender": "m", "plural": "-", "pos": "არსებითი სახელი", "georgian": "შემოდგომა", "example_de": "Im Herbst fallen die Blätter.", "example_ka": "შემოდგომაზე ფოთლები ცვივა.", "category": "კალენდარი & სეზონები"},
    {"id": "winter", "word": "der Winter", "article": "der", "gender": "m", "plural": "-", "pos": "არსებითი სახელი", "georgian": "ზამთარი", "example_de": "Im Winter schneit es oft.", "example_ka": "ზამთარში ხშირად თოვს.", "category": "კალენდარი & სეზონები"},

    # --- კიდევ მნიშვნელოვანი ზმნები და წინდებულები ---
    {"id": "beginnen", "word": "beginnen", "article": "", "gender": "none", "plural": "", "pos": "ზმნა", "georgian": "დაწყება", "example_de": "Der Film beginnt um 20 Uhr.", "example_ka": "ფილმი 20 საათზე იწყება.", "category": "ზმნები"},
    {"id": "enden", "word": "enden", "article": "", "gender": "none", "plural": "", "pos": "ზმნა", "georgian": "დასრულება / დამთავრება", "example_de": "Die Party endet um Mitternacht.", "example_ka": "წვეულება შუაღამეს მთავრდება.", "category": "ზმნები"},
    {"id": "fragen", "word": "fragen", "article": "", "gender": "none", "plural": "", "pos": "ზმნა", "georgian": "კითხვა / შეკითხვის დასმა", "example_de": "Ich frage den Lehrer.", "example_ka": "მასწავლებელს ვეკითხები.", "category": "ზმნები"},
    {"id": "antworten", "word": "antworten", "article": "", "gender": "none", "plural": "", "pos": "ზმნა", "georgian": "პასუხის გაცემა (+ Dativ)", "example_de": "Bitte antworten Sie mir!", "example_ka": "გეთაყვა, მიპასუხეთ!", "category": "ზმნები"},
    {"id": "bezahlen", "word": "bezahlen", "article": "", "gender": "none", "plural": "", "pos": "ზმნა", "georgian": "გადახდა (ფულის)", "example_de": "Kann ich mit Karte bezahlen?", "example_ka": "ბარათით შემიძლია გადავიხადო?", "category": "ზმნები"},
    {"id": "kosten", "word": "kosten", "article": "", "gender": "none", "plural": "", "pos": "ზმნა", "georgian": "ღირებულება (ღირს)", "example_de": "Wie viel kostet dieser Pullover?", "example_ka": "რამდენი ღირს ეს სვიტერი?", "category": "ზმნები"},
    {"id": "erklaren", "word": "erklären", "article": "", "gender": "none", "plural": "", "pos": "ზმნა", "georgian": "ახსნა / განმარტება", "example_de": "Können Sie die Regel noch einmal erklären?", "example_ka": "შეგიძლიათ წესი კიდევ ერთხელ ამიხსნათ?", "category": "ზმნები"},
    {"id": "wiederholen", "word": "wiederholen", "article": "", "gender": "none", "plural": "", "pos": "ზმნა", "georgian": "გამეორება", "example_de": "Wiederholen Sie bitte den Satz!", "example_ka": "გაიმეორეთ წინადადება, გეთაყვა!", "category": "ზმნები"},
    {"id": "vergessen", "word": "vergessen", "article": "", "gender": "none", "plural": "", "pos": "ზმნა", "georgian": "დავიწყება (du vergisst)", "example_de": "Vergiss deinen Pass nicht!", "example_ka": "პასპორტი არ დაგავიწყდეს!", "category": "ზმნები"},
    {"id": "mitbringen", "word": "mitbringen", "article": "", "gender": "none", "plural": "", "pos": "ზმნა", "georgian": "თან მოტანა", "example_de": "Bring bitte Kuchen mit!", "example_ka": "ნამცხვარი წამოიღე თან, გეთაყვა!", "category": "ზმნები"},
    {"id": "einladen", "word": "einladen", "article": "", "gender": "none", "plural": "", "pos": "ზმნა", "georgian": "დაპატიჟება / მოწვევა", "example_de": "Ich lade dich zu meiner Geburtstagsfeier ein.", "example_ka": "გეპატიჟები ჩემი დაბადების დღის წვეულებაზე.", "category": "ზმნები"},
    {"id": "gratulieren", "word": "gratulieren", "article": "", "gender": "none", "plural": "", "pos": "ზმნა", "georgian": "მილოცვა (+ Dativ)", "example_de": "Ich gratuliere dir zum Geburtstag!", "example_ka": "გილოცავ დაბადების დღეს!", "category": "ზმნები"}
]

# Update data.js
import json

with open("/Users/shotachitaishvili/Documents/German A1/js/data.js", "r", encoding="utf-8") as f:
    raw = f.read()

# Strip "window.GERMAN_A1_DATA = " and trailing semicolon
prefix = "window.GERMAN_A1_DATA = "
if raw.startswith(prefix):
    json_str = raw[len(prefix):].rstrip().rstrip(";")
    data = json.loads(json_str)
    # Add extra words
    existing_ids = {w["id"] for w in data["dictionary"]}
    added = 0
    for w in extra_words:
        if w["id"] not in existing_ids:
            data["dictionary"].append(w)
            existing_ids.add(w["id"])
            added += 1

    # Also add extra words to article trainer if they have der/die/das
    existing_trainer = {x["word"] for x in data["article_trainer_words"]}
    for w in extra_words:
        if w["article"] in ["der", "die", "das"] and w["word"] not in existing_trainer:
            data["article_trainer_words"].append({
                "word": w["word"].replace("der ", "").replace("die ", "").replace("das ", ""),
                "article": w["article"],
                "georgian": w["georgian"],
                "gender": w["gender"]
            })

    output_content = prefix + json.dumps(data, ensure_ascii=False, indent=2) + ";\n"
    with open("/Users/shotachitaishvili/Documents/German A1/js/data.js", "w", encoding="utf-8") as f_out:
        f_out.write(output_content)
    print(f"Added {added} extra words! Total dictionary now: {len(data['dictionary'])}")
    print(f"Article trainer now: {len(data['article_trainer_words'])}")
