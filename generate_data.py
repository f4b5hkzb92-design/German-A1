# -*- coding: utf-8 -*-
"""
Script to generate the complete dictionary, quizzes, exercises, and grammar tables.
Outputs js/data.js.
"""
import json
import os

OUTPUT_FILE = "/Users/shotachitaishvili/Documents/German A1/js/data.js"

# Import lessons from build_data
from build_data import lessons

dictionary = [
    # --- 1. მისალმება და ზრდილობა (Begrüßung & Höflichkeit) ---
    {"id": "hallo", "word": "Hallo", "article": "", "gender": "none", "plural": "", "pos": "შორისდებული", "georgian": "გამარჯობა (არაფორმალური)", "example_de": "Hallo! Wie geht es dir?", "example_ka": "გამარჯობა! როგორ ხარ?", "category": "მისალმება & ზრდილობა"},
    {"id": "guten_tag", "word": "Guten Tag", "article": "", "gender": "none", "plural": "", "pos": "ფრაზა", "georgian": "გამარჯობა / დღე მშვიდობისა", "example_de": "Guten Tag, Frau Müller!", "example_ka": "დღე მშვიდობისა, ქალბატონო მიულერ!", "category": "მისალმება & ზრდილობა"},
    {"id": "guten_morgen", "word": "Guten Morgen", "article": "", "gender": "none", "plural": "", "pos": "ფრაზა", "georgian": "დილა მშვიდობისა", "example_de": "Guten Morgen! Hast du gut geschlafen?", "example_ka": "დილა მშვიდობისა! კარგად გეძინა?", "category": "მისალმება & ზრდილობა"},
    {"id": "guten_abend", "word": "Guten Abend", "article": "", "gender": "none", "plural": "", "pos": "ფრაზა", "georgian": "საღამო მშვიდობისა", "example_de": "Guten Abend, meine Damen und Herren!", "example_ka": "საღამო მშვიდობისა, ქალბატონებო და ბატონებო!", "category": "მისალმება & ზრდილობა"},
    {"id": "gute_nacht", "word": "Gute Nacht", "article": "", "gender": "none", "plural": "", "pos": "ფრაზა", "georgian": "ღამე მშვიდობისა", "example_de": "Gute Nacht, schlaf gut!", "example_ka": "ღამე მშვიდობისა, ტკბილად დაიძინე!", "category": "მისალმება & ზრდილობა"},
    {"id": "auf_wiedersehen", "word": "Auf Wiedersehen", "article": "", "gender": "none", "plural": "", "pos": "ფრაზა", "georgian": "ნახვამდის (ოფიციალური)", "example_de": "Auf Wiedersehen, bis morgen!", "example_ka": "ნახვამდის, ხვალამდე!", "category": "მისალმება & ზრდილობა"},
    {"id": "tschuss", "word": "Tschüss", "article": "", "gender": "none", "plural": "", "pos": "ფრაზა", "georgian": "ნახვამდის / კარგად (მეგობრული)", "example_de": "Tschüss, bis bald!", "example_ka": "ნახვამდის, მალე შეხვედრამდე!", "category": "მისალმება & ზრდილობა"},
    {"id": "danke", "word": "Danke", "article": "", "gender": "none", "plural": "", "pos": "შორისდებული", "georgian": "მადლობა", "example_de": "Danke schön für das Geschenk!", "example_ka": "დიდი მადლობა საჩუქრისთვის!", "category": "მისალმება & ზრდილობა"},
    {"id": "bitte", "word": "Bitte", "article": "", "gender": "none", "plural": "", "pos": "შორისდებული", "georgian": "გეთაყვა / არაფრის", "example_de": "Ein Kaffee, bitte!", "example_ka": "ერთი ყავა, გეთაყვა!", "category": "მისალმება & ზრდილობა"},
    {"id": "entschuldigung", "word": "die Entschuldigung", "article": "die", "gender": "f", "plural": "-en", "pos": "არსებითი სახელი", "georgian": "ბოდიში / უკაცრავად", "example_de": "Entschuldigung, wo ist der Bahnhof?", "example_ka": "უკაცრავად, სად არის სადგური?", "category": "მისალმება & ზრდილობა"},
    {"id": "es_tut_mir_leid", "word": "Es tut mir leid", "article": "", "gender": "none", "plural": "", "pos": "ფრაზა", "georgian": "ვწუხვარ / მაპატიეთ", "example_de": "Es tut mir leid, ich habe keine Zeit.", "example_ka": "ვწუხვარ, დრო არ მაქვს.", "category": "მისალმება & ზრდილობა"},
    {"id": "ja", "word": "Ja", "article": "", "gender": "none", "plural": "", "pos": "ნაწილაკი", "georgian": "დიახ / კი", "example_de": "Ja, ich komme aus Georgien.", "example_ka": "დიახ, საქართველოდან ვარ.", "category": "მისალმება & ზრდილობა"},
    {"id": "nein", "word": "Nein", "article": "", "gender": "none", "plural": "", "pos": "ნაწილაკი", "georgian": "არა", "example_de": "Nein, das ist nicht mein Buch.", "example_ka": "არა, ეს ჩემი წიგნი არ არის.", "category": "მისალმება & ზრდილობა"},
    {"id": "vielleicht", "word": "vielleicht", "article": "", "gender": "none", "plural": "", "pos": "ზმნიზედა", "georgian": "შესაძლოა / იქნებ", "example_de": "Vielleicht kommt er morgen.", "example_ka": "იქნებ ის ხვალ მოვიდეს.", "category": "მისალმება & ზრდილობა"},
    {"id": "willkommen", "word": "Willkommen", "article": "", "gender": "none", "plural": "", "pos": "შორისდებული", "georgian": "კეთილი იყოს თქვენი მობრძანება", "example_de": "Herzlich willkommen in Deutschland!", "example_ka": "გულითადად მოგესალმებით გერმანიაში!", "category": "მისალმება & ზრდილობა"},

    # --- 2. ადამიანები და ოჯახი (Personen & Familie) ---
    {"id": "familie", "word": "die Familie", "article": "die", "gender": "f", "plural": "-n", "pos": "არსებითი სახელი", "georgian": "ოჯახი", "example_de": "Meine Familie lebt in Tiflis.", "example_ka": "ჩემი ოჯახი თბილისში ცხოვრობს.", "category": "ადამიანები & ოჯახი"},
    {"id": "vater", "word": "der Vater", "article": "der", "gender": "m", "plural": "-ä-", "pos": "არსებითი სახელი", "georgian": "მამა", "example_de": "Mein Vater ist Ingenieur.", "example_ka": "მამაჩემი ინჟინერია.", "category": "ადამიანები & ოჯახი"},
    {"id": "mutter", "word": "die Mutter", "article": "die", "gender": "f", "plural": "-ü-", "pos": "არსებითი სახელი", "georgian": "დედა", "example_de": "Meine Mutter kocht sehr gut.", "example_ka": "დედაჩემი ძალიან კარგად ამზადებს.", "category": "ადამიანები & ოჯახი"},
    {"id": "eltern", "word": "die Eltern", "article": "die", "gender": "pl", "plural": "(მხოლოდ მრავლობითი)", "pos": "არსებითი სახელი", "georgian": "მშობლები", "example_de": "Meine Eltern sind sehr nett.", "example_ka": "ჩემი მშობლები ძალიან საყვარლები არიან.", "category": "ადამიანები & ოჯახი"},
    {"id": "sohn", "word": "der Sohn", "article": "der", "gender": "m", "plural": "-ö-e", "pos": "არსებითი სახელი", "georgian": "ვაჟი / შვილი", "example_de": "Er hat einen Sohn.", "example_ka": "მას ერთი ვაჟი ჰყავს.", "category": "ადამიანები & ოჯახი"},
    {"id": "tochter", "word": "die Tochter", "article": "die", "gender": "f", "plural": "-ö-", "pos": "არსებითი სახელი", "georgian": "ქალიშვილი / შვილი", "example_de": "Ihre Tochter geht in die Schule.", "example_ka": "მისი ქალიშვილი სკოლაში დადის.", "category": "ადამიანები & ოჯახი"},
    {"id": "bruder", "word": "der Bruder", "article": "der", "gender": "m", "plural": "-ü-", "pos": "არსებითი სახელი", "georgian": "ძმა", "example_de": "Mein Bruder studiert Medizin.", "example_ka": "ჩემი ძმა მედიცინას სწავლობს.", "category": "ადამიანები & ოჯახი"},
    {"id": "schwester", "word": "die Schwester", "article": "die", "gender": "f", "plural": "-n", "pos": "არსებითი სახელი", "georgian": "და", "example_de": "Ich habe eine jüngere Schwester.", "example_ka": "მყავს უმცროსი და.", "category": "ადამიანები & ოჯახი"},
    {"id": "geschwister", "word": "die Geschwister", "article": "die", "gender": "pl", "plural": "(მხოლოდ მრავლობითი)", "pos": "არსებითი სახელი", "georgian": "დედმამიშვილები", "example_de": "Hast du Geschwister?", "example_ka": "გყავს დედმამიშვილები?", "category": "ადამიანები & ოჯახი"},
    {"id": "grossvater", "word": "der Großvater", "article": "der", "gender": "m", "plural": "-ä-", "pos": "არსებითი სახელი", "georgian": "ბაბუა (Opa)", "example_de": "Mein Großvater liest gern Zeitung.", "example_ka": "ბაბუაჩემს უყვარს გაზეთის კითხვა.", "category": "ადამიანები & ოჯახი"},
    {"id": "grossmutter", "word": "die Großmutter", "article": "die", "gender": "f", "plural": "-ü-", "pos": "არსებითი სახელი", "georgian": "ბებია (Oma)", "example_de": "Meine Oma bäckt leckeren Kuchen.", "example_ka": "ბებიაჩემი გემრიელ ნამცხვარს აცხობს.", "category": "ადამიანები & ოჯახი"},
    {"id": "grosseltern", "word": "die Großeltern", "article": "die", "gender": "pl", "plural": "(მხოლოდ მრავლობითი)", "pos": "არსებითი სახელი", "georgian": "ბებია და ბაბუა", "example_de": "Ich besuche oft meine Großeltern.", "example_ka": "ხშირად ვსტუმრობ ბებიას და ბაბუას.", "category": "ადამიანები & ოჯახი"},
    {"id": "kind", "word": "das Kind", "article": "das", "gender": "n", "plural": "-er", "pos": "არსებითი სახელი", "georgian": "ბავშვი", "example_de": "Das Kind spielt im Garten.", "example_ka": "ბავშვი ბაღში თამაშობს.", "category": "ადამიანები & ოჯახი"},
    {"id": "baby", "word": "das Baby", "article": "das", "gender": "n", "plural": "-s", "pos": "არსებითი სახელი", "georgian": "ჩვილი / პატარა ბავშვი", "example_de": "Das Baby schläft ruhig.", "example_ka": "პატარას მშვიდად სძინავს.", "category": "ადამიანები & ოჯახი"},
    {"id": "mann", "word": "der Mann", "article": "der", "gender": "m", "plural": "-ä-er", "pos": "არსებითი სახელი", "georgian": "კაცი / ქმარი", "example_de": "Ihr Mann arbeitet als Arzt.", "example_ka": "მისი ქმარი ექიმად მუშაობს.", "category": "ადამიანები & ოჯახი"},
    {"id": "frau", "word": "die Frau", "article": "die", "gender": "f", "plural": "-en", "pos": "არსებითი სახელი", "georgian": "ქალი / ცოლი / ქალბატონი", "example_de": "Frau Beridze spricht Deutsch.", "example_ka": "ქალბატონი ბერიძე გერმანულად ლაპარაკობს.", "category": "ადამიანები & ოჯახი"},
    {"id": "freund", "word": "der Freund", "article": "der", "gender": "m", "plural": "-e", "pos": "არსებითი სახელი", "georgian": "მეგობარი (ბიჭი) / შეყვარებული", "example_de": "Das ist mein bester Freund.", "example_ka": "ეს ჩემი საუკეთესო მეგობარია.", "category": "ადამიანები & ოჯახი"},
    {"id": "freundin", "word": "die Freundin", "article": "die", "gender": "f", "plural": "-nen", "pos": "არსებითი სახელი", "georgian": "მეგობარი (გოგო) / შეყვარებული", "example_de": "Ich treffe heute meine Freundin.", "example_ka": "დღეს ჩემს მეგობარ გოგოს ვხვდები.", "category": "ადამიანები & ოჯახი"},
    {"id": "mensch", "word": "der Mensch", "article": "der", "gender": "m", "plural": "-en", "pos": "არსებითი სახელი", "georgian": "ადამიანი", "example_de": "In Berlin leben viele Menschen.", "example_ka": "ბერლინში ბევრი ადამიანი ცხოვრობს.", "category": "ადამიანები & ოჯახი"},
    {"id": "leute", "word": "die Leute", "article": "die", "gender": "pl", "plural": "(მხოლოდ მრავლობითი)", "pos": "არსებითი სახელი", "georgian": "ხალხი", "example_de": "Die Leute sind sehr freundlich.", "example_ka": "ხალხი ძალიან მეგობრულია.", "category": "ადამიანები & ოჯახი"},
    {"id": "name", "word": "der Name", "article": "der", "gender": "m", "plural": "-n", "pos": "არსებითი სახელი", "georgian": "სახელი", "example_de": "Wie ist Ihr Name?", "example_ka": "როგორია თქვენი სახელი?", "category": "ადამიანები & ოჯახი"},
    {"id": "vorname", "word": "der Vorname", "article": "der", "gender": "m", "plural": "-n", "pos": "არსებითი სახელი", "georgian": "საკუთარი სახელი", "example_de": "Mein Vorname ist Giorgi.", "example_ka": "ჩემი სახელია გიორგი.", "category": "ადამიანები & ოჯახი"},
    {"id": "nachname", "word": "der Nachname", "article": "der", "gender": "m", "plural": "-n", "pos": "არსებითი სახელი", "georgian": "გვარი (Familienname)", "example_de": "Mein Nachname ist Beridze.", "example_ka": "ჩემი გვარია ბერიძე.", "category": "ადამიანები & ოჯახი"},
    {"id": "alter", "word": "das Alter", "article": "das", "gender": "n", "plural": "-", "pos": "არსებითი სახელი", "georgian": "ასაკი", "example_de": "Wie alt bist du?", "example_ka": "რამდენი წლის ხარ?", "category": "ადამიანები & ოჯახი"},
    {"id": "jahr", "word": "das Jahr", "article": "das", "gender": "n", "plural": "-e", "pos": "არსებითი სახელი", "georgian": "წელი", "example_de": "Ich bin 22 Jahre alt.", "example_ka": "მე 22 წლის ვარ.", "category": "ადამიანები & ოჯახი"},
    {"id": "ledig", "word": "ledig", "article": "", "gender": "none", "plural": "", "pos": "ზედსართავი სახელი", "georgian": "დასაოჯახებელი / უცოლო / გაუთხოვარი", "example_de": "Bist du verheiratet oder ledig?", "example_ka": "დაოჯახებული ხარ თუ დასაოჯახებელი?", "category": "ადამიანები & ოჯახი"},
    {"id": "verheiratet", "word": "verheiratet", "article": "", "gender": "none", "plural": "", "pos": "ზედსართავი სახელი", "georgian": "დაოჯახებული", "example_de": "Wir sind seit drei Jahren verheiratet.", "example_ka": "სამი წელია დაქორწინებულები ვართ.", "category": "ადამიანები & ოჯახი"},

    # --- 3. სახლი, ბინა და ავეჯი (Wohnen & Möbel) ---
    {"id": "wohnung", "word": "die Wohnung", "article": "die", "gender": "f", "plural": "-en", "pos": "არსებითი სახელი", "georgian": "ბინა", "example_de": "Die Wohnung hat drei Zimmer.", "example_ka": "ბინას აქვს სამი ოთახი.", "category": "სახლი & ავეჯი"},
    {"id": "haus", "word": "das Haus", "article": "das", "gender": "n", "plural": "-ä-er", "pos": "არსებითი სახელი", "georgian": "სახლი", "example_de": "Das Haus ist neu und modern.", "example_ka": "სახლი ახალი და თანამედროვეა.", "category": "სახლი & ავეჯი"},
    {"id": "zimmer", "word": "das Zimmer", "article": "das", "gender": "n", "plural": "-", "pos": "არსებითი სახელი", "georgian": "ოთახი", "example_de": "Mein Zimmer ist gemütlich.", "example_ka": "ჩემი ოთახი მყუდროა.", "category": "სახლი & ავეჯი"},
    {"id": "kuche", "word": "die Küche", "article": "die", "gender": "f", "plural": "-n", "pos": "არსებითი სახელი", "georgian": "სამზარეულო", "example_de": "In der Küche kochen wir Kaffee.", "example_ka": "სამზარეულოში ყავას ვადუღებთ.", "category": "სახლი & ავეჯი"},
    {"id": "bad", "word": "das Bad", "article": "das", "gender": "n", "plural": "-ä-er", "pos": "არსებითი სახელი", "georgian": "სააბაზანო (Badezimmer)", "example_de": "Das Bad hat eine Dusche.", "example_ka": "სააბაზანოს აქვს შხაპი.", "category": "სახლი & ავეჯი"},
    {"id": "wohnzimmer", "word": "das Wohnzimmer", "article": "das", "gender": "n", "plural": "-", "pos": "არსებითი სახელი", "georgian": "მისაღები ოთახი (ზალა)", "example_de": "Im Wohnzimmer steht ein großes Sofa.", "example_ka": "მისაღებ ოთახში დიდი დივანი დგას.", "category": "სახლი & ავეჯი"},
    {"id": "schlafzimmer", "word": "das Schlafzimmer", "article": "das", "gender": "n", "plural": "-", "pos": "არსებითი სახელი", "georgian": "საძინებელი ოთახი", "example_de": "Das Schlafzimmer ist ruhig.", "example_ka": "საძინებელი მშვიდია.", "category": "სახლი & ავეჯი"},
    {"id": "balkon", "word": "der Balkon", "article": "der", "gender": "m", "plural": "-e", "pos": "არსებითი სახელი", "georgian": "აივანი", "example_de": "Im Sommer sitzen wir auf dem Balkon.", "example_ka": "ზაფხულში აივანზე ვსხედვართ.", "category": "სახლი & ავეჯი"},
    {"id": "garten", "word": "der Garten", "article": "der", "gender": "m", "plural": "-ä-", "pos": "არსებითი სახელი", "georgian": "ბაღი / ეზო", "example_de": "Die Kinder spielen im Garten.", "example_ka": "ბავშვები ბაღში თამაშობენ.", "category": "სახლი & ავეჯი"},
    {"id": "flur", "word": "der Flur", "article": "der", "gender": "m", "plural": "-e", "pos": "არსებითი სახელი", "georgian": "დერეფანი / ჰოლი", "example_de": "Die Schuhe stehen im Flur.", "example_ka": "ფეხსაცმელი დერეფანში დევს.", "category": "სახლი & ავეჯი"},
    {"id": "tisch", "word": "der Tisch", "article": "der", "gender": "m", "plural": "-e", "pos": "არსებითი სახელი", "georgian": "მაგიდა", "example_de": "Das Buch liegt auf dem Tisch.", "example_ka": "წიგნი მაგიდაზე დევს.", "category": "სახლი & ავეჯი"},
    {"id": "stuhl", "word": "der Stuhl", "article": "der", "gender": "m", "plural": "-ü-e", "pos": "არსებითი სახელი", "georgian": "სკამი", "example_de": "Nimm bitte Platz auf dem Stuhl!", "example_ka": "დაჯექი სკამზე, გეთაყვა!", "category": "სახლი & ავეჯი"},
    {"id": "bett", "word": "das Bett", "article": "das", "gender": "n", "plural": "-en", "pos": "არსებითი სახელი", "georgian": "საწოლი / ლოგინი", "example_de": "Das Bett ist sehr bequem.", "example_ka": "საწოლი ძალიან მოხერხებულია.", "category": "სახლი & ავეჯი"},
    {"id": "sofa", "word": "das Sofa", "article": "das", "gender": "n", "plural": "-s", "pos": "არსებითი სახელი", "georgian": "დივანი", "example_de": "Wir sitzen auf dem Sofa.", "example_ka": "ჩვენ დივანზე ვსხედვართ.", "category": "სახლი & ავეჯი"},
    {"id": "schrank", "word": "der Schrank", "article": "der", "gender": "m", "plural": "-ä-e", "pos": "არსებითი სახელი", "georgian": "კარადა", "example_de": "Meine Kleidung hängt im Schrank.", "example_ka": "ჩემი ტანსაცმელი კარადაში კიდია.", "category": "სახლი & ავეჯი"},
    {"id": "kuhlschrank", "word": "der Kühlschrank", "article": "der", "gender": "m", "plural": "-ä-e", "pos": "არსებითი სახელი", "georgian": "მაცივარი", "example_de": "Die Milch steht im Kühlschrank.", "example_ka": "რძე მაცივარში დგას.", "category": "სახლი & ავეჯი"},
    {"id": "lampe", "word": "die Lampe", "article": "die", "gender": "f", "plural": "-n", "pos": "არსებითი სახელი", "georgian": "ნათურა / ლამპა", "example_de": "Die Lampe ist sehr hell.", "example_ka": "ლამპა ძალიან ნათელია.", "category": "სახლი & ავეჯი"},
    {"id": "teppich", "word": "der Teppich", "article": "der", "gender": "m", "plural": "-e", "pos": "არსებითი სახელი", "georgian": "ხალიჩა", "example_de": "Der Teppich ist blau.", "example_ka": "ხალიჩა ლურჯია.", "category": "სახლი & ავეჯი"},
    {"id": "bild", "word": "das Bild", "article": "das", "gender": "n", "plural": "-er", "pos": "არსებითი სახელი", "georgian": "სურათი / ნახატი", "example_de": "An der Wand hängt ein Bild.", "example_ka": "კედელზე ნახატი კიდია.", "category": "სახლი & ავეჯი"},
    {"id": "fenster", "word": "das Fenster", "article": "das", "gender": "n", "plural": "-", "pos": "არსებითი სახელი", "georgian": "ფანჯარა", "example_de": "Mach bitte das Fenster auf!", "example_ka": "გააღე ფანჯარა, გეთაყვა!", "category": "სახლი & ავეჯი"},
    {"id": "tur", "word": "die Tür", "article": "die", "gender": "f", "plural": "-en", "pos": "არსებითი სახელი", "georgian": "კარი", "example_de": "Schließe bitte die Tür!", "example_ka": "დაკეტე კარი, გეთაყვა!", "category": "სახლი & ავეჯი"},
    {"id": "miete", "word": "die Miete", "article": "die", "gender": "f", "plural": "-n", "pos": "არსებითი სახელი", "georgian": "ქირა", "example_de": "Wie viel kostet die Miete?", "example_ka": "რამდენია ქირა?", "category": "სახლი & ავეჯი"},

    # --- 4. საკვები და სასმელი (Essen & Trinken) ---
    {"id": "essen", "word": "das Essen", "article": "das", "gender": "n", "plural": "-", "pos": "არსებითი სახელი", "georgian": "საჭმელი / კვება", "example_de": "Das Essen schmeckt lecker.", "example_ka": "საჭმელი გემრიელია.", "category": "საჭმელი & სასმელი"},
    {"id": "trinken_verb", "word": "trinken", "article": "", "gender": "none", "plural": "", "pos": "ზმნა", "georgian": "დალევა / სმა", "example_de": "Ich trinke gern Mineralwasser.", "example_ka": "სიამოვნებით ვსვამ მინერალურ წყალს.", "category": "საჭმელი & სასმელი"},
    {"id": "brot", "word": "das Brot", "article": "das", "gender": "n", "plural": "-e", "pos": "არსებითი სახელი", "georgian": "პური", "example_de": "Ich kaufe frisches Brot.", "example_ka": "ახალ პურს ვყიდულობ.", "category": "საჭმელი & სასმელი"},
    {"id": "brotchen", "word": "das Brötchen", "article": "das", "gender": "n", "plural": "-", "pos": "არსებითი სახელი", "georgian": "ფუნთუშა (პატარა პური)", "example_de": "Zum Frühstück esse ich zwei Brötchen.", "example_ka": "საუზმეზე ორ ფუნთუშას ვჭამ.", "category": "საჭმელი & სასმელი"},
    {"id": "apfel", "word": "der Apfel", "article": "der", "gender": "m", "plural": "-ä-", "pos": "არსებითი სახელი", "georgian": "ვაშლი", "example_de": "Ein Apfel am Tag hält gesund.", "example_ka": "დღეში ერთი ვაშლი ჯანმრთელობას ინარჩუნებს.", "category": "საჭმელი & სასმელი"},
    {"id": "banane", "word": "die Banane", "article": "die", "gender": "f", "plural": "-n", "pos": "არსებითი სახელი", "georgian": "ბანანი", "example_de": "Ich mag gelbe Bananen.", "example_ka": "მიყვარს ყვითელი ბანანები.", "category": "საჭმელი & სასმელი"},
    {"id": "kartoffel", "word": "die Kartoffel", "article": "die", "gender": "f", "plural": "-n", "pos": "არსებითი სახელი", "georgian": "კარტოფილი", "example_de": "Die Deutschen essen viele Kartoffeln.", "example_ka": "გერმანელები ბევრ კარტოფილს ჭამენ.", "category": "საჭმელი & სასმელი"},
    {"id": "tomate", "word": "die Tomate", "article": "die", "gender": "f", "plural": "-n", "pos": "არსებითი სახელი", "georgian": "პომიდორი", "example_de": "Für den Salat brauche ich drei Tomaten.", "example_ka": "სალათისთვის სამი პომიდორი მჭირდება.", "category": "საჭმელი & სასმელი"},
    {"id": "gemuse", "word": "das Gemüse", "article": "das", "gender": "n", "plural": "-", "pos": "არსებითი სახელი", "georgian": "ბოსტნეული", "example_de": "Frisches Gemüse ist sehr gesund.", "example_ka": "ახალი ბოსტნეული ძალიან ჯანსაღია.", "category": "საჭმელი & სასმელი"},
    {"id": "obst", "word": "das Obst", "article": "das", "gender": "n", "plural": "-", "pos": "არსებითი სახელი", "georgian": "ხილი", "example_de": "Ich esse jeden Tag Obst.", "example_ka": "ყოველდღე ვჭამ ხილს.", "category": "საჭმელი & სასმელი"},
    {"id": "fleisch", "word": "das Fleisch", "article": "das", "gender": "n", "plural": "-", "pos": "არსებითი სახელი", "georgian": "ხორცი", "example_de": "Er ist Vegetarier und isst kein Fleisch.", "example_ka": "ის ვეგეტარიანელია და ხორცს არ ჭამს.", "category": "საჭმელი & სასმელი"},
    {"id": "fisch", "word": "der Fisch", "article": "der", "gender": "m", "plural": "-e", "pos": "არსებითი სახელი", "georgian": "თევზი", "example_de": "Am Freitag kochen wir Fisch.", "example_ka": "პარასკევს თევზს ვამზადებთ.", "category": "საჭმელი & სასმელი"},
    {"id": "kase", "word": "der Käse", "article": "der", "gender": "m", "plural": "-", "pos": "არსებითი სახელი", "georgian": "ყველი", "example_de": "Schweizer Käse schmeckt wunderbar.", "example_ka": "შვეიცარიული ყველი საოცრად გემრიელია.", "category": "საჭმელი & სასმელი"},
    {"id": "milch", "word": "die Milch", "article": "die", "gender": "f", "plural": "-", "pos": "არსებითი სახელი", "georgian": "რძე", "example_de": "Trinkst du Kaffee mit Milch?", "example_ka": "ყავას რძით სვამ?", "category": "საჭმელი & სასმელი"},
    {"id": "wasser", "word": "das Wasser", "article": "das", "gender": "n", "plural": "-", "pos": "არსებითი სახელი", "georgian": "წყალი", "example_de": "Ein Glas Wasser, bitte!", "example_ka": "ერთი ჭიქა წყალი, გეთაყვა!", "category": "საჭმელი & სასმელი"},
    {"id": "kaffee", "word": "der Kaffee", "article": "der", "gender": "m", "plural": "-", "pos": "არსებითი სახელი", "georgian": "ყავა", "example_de": "Ich brauche am Morgen einen heißen Kaffee.", "example_ka": "დილით ცხელი ყავა მჭირდება.", "category": "საჭმელი & სასმელი"},
    {"id": "tee", "word": "der Tee", "article": "der", "gender": "m", "plural": "-", "pos": "არსებითი სახელი", "georgian": "ჩაი", "example_de": "Möchtest du schwarzen oder grünen Tee?", "example_ka": "შავი ჩაი გინდა თუ მწვანე?", "category": "საჭმელი & სასმელი"},
    {"id": "bier", "word": "das Bier", "article": "das", "gender": "n", "plural": "-e", "pos": "არსებითი სახელი", "georgian": "ლუდი", "example_de": "Deutsches Bier ist weltweit berühmt.", "example_ka": "გერმანული ლუდი მსოფლიოში განთქმულია.", "category": "საჭმელი & სასმელი"},
    {"id": "wein", "word": "der Wein", "article": "der", "gender": "m", "plural": "-e", "pos": "არსებითი სახელი", "georgian": "ღვინო", "example_de": "Georgischer Wein ist der beste Wein.", "example_ka": "ქართული ღვინო საუკეთესო ღვინოა.", "category": "საჭმელი & სასმელი"},
    {"id": "ei", "word": "das Ei", "article": "das", "gender": "n", "plural": "-er", "pos": "არსებითი სახელი", "georgian": "კვერცხი", "example_de": "Ich koche zwei Eier zum Frühstück.", "example_ka": "საუზმეზე ორ კვერცხს ვხარშავ.", "category": "საჭმელი & სასმელი"},
    {"id": "zucker", "word": "der Zucker", "article": "der", "gender": "m", "plural": "-", "pos": "არსებითი სახელი", "georgian": "შაქარი", "example_de": "Ich trinke Kaffee ohne Zucker.", "example_ka": "ყავას უშაქროდ ვსვამ.", "category": "საჭმელი & სასმელი"},
    {"id": "salz", "word": "das Salz", "article": "das", "gender": "n", "plural": "-", "pos": "არსებითი სახელი", "georgian": "მარილი", "example_de": "Reichst du mir bitte das Salz?", "example_ka": "მომაწვდი მარილს, გეთაყვა?", "category": "საჭმელი & სასმელი"},
    {"id": "fruhstuck", "word": "das Frühstück", "article": "das", "gender": "n", "plural": "-", "pos": "არსებითი სახელი", "georgian": "საუზმე", "example_de": "Das Frühstück ist um 8 Uhr.", "example_ka": "საუზმე რვა საათზეა.", "category": "საჭმელი & სასმელი"},
    {"id": "mittagessen", "word": "das Mittagessen", "article": "das", "gender": "n", "plural": "-", "pos": "არსებითი სახელი", "georgian": "სადილი", "example_de": "Was gibt es heute zum Mittagessen?", "example_ka": "რა გვაქვს დღეს სადილად?", "category": "საჭმელი & სასმელი"},
    {"id": "abendessen", "word": "das Abendessen", "article": "das", "gender": "n", "plural": "-", "pos": "არსებითი სახელი", "georgian": "ვახშამი", "example_de": "Wir essen um 19 Uhr Abendessen.", "example_ka": "შვიდ საათზე ვვახშმობთ.", "category": "საჭმელი & სასმელი"},
    {"id": "hunger", "word": "der Hunger", "article": "der", "gender": "m", "plural": "-", "pos": "არსებითი სახელი", "georgian": "შიმშილი (Ich habe Hunger = მშია)", "example_de": "Ich habe großen Hunger!", "example_ka": "ძალიან მშია!", "category": "საჭმელი & სასმელი"},
    {"id": "durst", "word": "der Durst", "article": "der", "gender": "m", "plural": "-", "pos": "არსებითი სახელი", "georgian": "წყურვილი (Ich habe Durst = მწყურია)", "example_de": "Hast du Durst?", "example_ka": "გწყურია?", "category": "საჭმელი & სასმელი"},

    # --- 5. ქალაქი, ორიენტაცია და ტრანსპორტი (Stadt & Verkehr) ---
    {"id": "stadt", "word": "die Stadt", "article": "die", "gender": "f", "plural": "-ä-e", "pos": "არსებითი სახელი", "georgian": "ქალაქი", "example_de": "Berlin ist eine große Stadt.", "example_ka": "ბერლინი დიდი ქალაქია.", "category": "ქალაქი & ტრანსპორტი"},
    {"id": "strasse", "word": "die Straße", "article": "die", "gender": "f", "plural": "-n", "pos": "არსებითი სახელი", "georgian": "ქუჩა", "example_de": "In welcher Straße wohnst du?", "example_ka": "რომელ ქუჩაზე ცხოვრობ?", "category": "ქალაქი & ტრანსპორტი"},
    {"id": "platz", "word": "der Platz", "article": "der", "gender": "m", "plural": "-ä-e", "pos": "არსებითი სახელი", "georgian": "მოედანი / ადგილი", "example_de": "Wir treffen uns auf dem Alexanderplatz.", "example_ka": "ალექსანდერპლაცზე შევხვდეთ.", "category": "ქალაქი & ტრანსპორტი"},
    {"id": "bahnhof", "word": "der Bahnhof", "article": "der", "gender": "m", "plural": "-ö-e", "pos": "არსებითი სახელი", "georgian": "რკინიგზის სადგური", "example_de": "Der Zug fährt vom Hauptbahnhof ab.", "example_ka": "მატარებელი ცენტრალური სადგურიდან გადის.", "category": "ქალაქი & ტრანსპორტი"},
    {"id": "flughafen", "word": "der Flughafen", "article": "der", "gender": "m", "plural": "-ä-", "pos": "არსებითი სახელი", "georgian": "აეროპორტი", "example_de": "Wir fahren mit dem Taxi zum Flughafen.", "example_ka": "ტაქსით მივდივართ აეროპორტში.", "category": "ქალაქი & ტრანსპორტი"},
    {"id": "hotel", "word": "das Hotel", "article": "das", "gender": "n", "plural": "-s", "pos": "არსებითი სახელი", "georgian": "სასტუმრო", "example_de": "Das Hotel liegt im Zentrum.", "example_ka": "სასტუმრო ცენტრში მდებარეობს.", "category": "ქალაქი & ტრანსპორტი"},
    {"id": "bank", "word": "die Bank", "article": "die", "gender": "f", "plural": "-en", "pos": "არსებითი სახელი", "georgian": "ბანკი", "example_de": "Ich muss Geld auf der Bank wechseln.", "example_ka": "ბანკში ფული უნდა გადავცვალო.", "category": "ქალაქი & ტრანსპორტი"},
    {"id": "post", "word": "die Post", "article": "die", "gender": "f", "plural": "-", "pos": "არსებითი სახელი", "georgian": "ფოსტა", "example_de": "Wo kann ich diesen Brief aufgeben? - Bei der Post.", "example_ka": "სად შემიძლია ამ წერილის გაგზავნა? - ფოსტაში.", "category": "ქალაქი & ტრანსპორტი"},
    {"id": "apotheke", "word": "die Apotheke", "article": "die", "gender": "f", "plural": "-n", "pos": "არსებითი სახელი", "georgian": "აფთიაქი", "example_de": "Die Apotheke hat 24 Stunden geöffnet.", "example_ka": "აფთიაქი 24 საათია ღია.", "category": "ქალაქი & ტრანსპორტი"},
    {"id": "krankenhaus", "word": "das Krankenhaus", "article": "das", "gender": "n", "plural": "-ä-er", "pos": "არსებითი სახელი", "georgian": "საავადმყოფო", "example_de": "Der Krankenwagen bringt ihn ins Krankenhaus.", "example_ka": "სასწრაფო დახმარებას ის საავადმყოფოში მიჰყავს.", "category": "ქალაქი & ტრანსპორტი"},
    {"id": "museum", "word": "das Museum", "article": "das", "gender": "n", "plural": "Museen", "pos": "არსებითი სახელი", "georgian": "მუზეუმი", "example_de": "Das Pergamonmuseum ist weltbekannt.", "example_ka": "პერგამონის მუზეუმი მსოფლიოში ცნობილია.", "category": "ქალაქი & ტრანსპორტი"},
    {"id": "supermarkt", "word": "der Supermarkt", "article": "der", "gender": "m", "plural": "-ä-e", "pos": "არსებითი სახელი", "georgian": "სუპერმარკეტი", "example_de": "Ich kaufe im Supermarkt ein.", "example_ka": "სუპერმარკეტში ვაკეთებ საყიდლებს.", "category": "ქალაქი & ტრანსპორტი"},
    {"id": "bus", "word": "der Bus", "article": "der", "gender": "m", "plural": "-se", "pos": "არსებითი სახელი", "georgian": "ავტობუსი", "example_de": "Der Bus kommt um zehn Uhr.", "example_ka": "ავტობუსი ათ საათზე მოდის.", "category": "ქალაქი & ტრანსპორტი"},
    {"id": "zug", "word": "der Zug", "article": "der", "gender": "m", "plural": "-ü-e", "pos": "არსებითი სახელი", "georgian": "მატარებელი", "example_de": "Wir reisen mit dem Zug.", "example_ka": "ჩვენ მატარებლით ვმოგზაურობთ.", "category": "ქალაქი & ტრანსპორტი"},
    {"id": "u_bahn", "word": "die U-Bahn", "article": "die", "gender": "f", "plural": "-en", "pos": "არსებითი სახელი", "georgian": "მეტრო (მიწისქვეშა)", "example_de": "Die U-Bahn ist sehr schnell.", "example_ka": "მეტრო ძალიან სწრაფია.", "category": "ქალაქი & ტრანსპორტი"},
    {"id": "strassenbahn", "word": "die Straßenbahn", "article": "die", "gender": "f", "plural": "-en", "pos": "არსებითი სახელი", "georgian": "ტრამვაი", "example_de": "Nehmen Sie die Straßenbahn Linie 4!", "example_ka": "ჩაჯექით ტრამვაი N4-ში!", "category": "ქალაქი & ტრანსპორტი"},
    {"id": "taxi", "word": "das Taxi", "article": "das", "gender": "n", "plural": "-s", "pos": "არსებითი სახელი", "georgian": "ტაქსი", "example_de": "Rufen wir ein Taxi!", "example_ka": "ტაქსი გამოვიძახოთ!", "category": "ქალაქი & ტრანსპორტი"},
    {"id": "auto", "word": "das Auto", "article": "das", "gender": "n", "plural": "-s", "pos": "არსებითი სახელი", "georgian": "მანქანა / ავტომობილი", "example_de": "Er fährt jeden Tag mit dem Auto zur Arbeit.", "example_ka": "ის ყოველდღე მანქანით დადის სამსახურში.", "category": "ქალაქი & ტრანსპორტი"},
    {"id": "fahrrad", "word": "das Fahrrad", "article": "das", "gender": "n", "plural": "-ä-er", "pos": "არსებითი სახელი", "georgian": "ველოსიპედი", "example_de": "In Berlin fahren viele Leute Fahrrad.", "example_ka": "ბერლინში ბევრი ხალხი დადის ველოსიპედით.", "category": "ქალაქი & ტრანსპორტი"},
    {"id": "fahrkarte", "word": "die Fahrkarte", "article": "die", "gender": "f", "plural": "-n", "pos": "არსებითი სახელი", "georgian": "სამგზავრო ბილეთი", "example_de": "Eine Fahrkarte nach München, bitte!", "example_ka": "ერთი სამგზავრო ბილეთი მიუნხენამდე, გეთაყვა!", "category": "ქალაქი & ტრანსპორტი"},
    {"id": "haltestelle", "word": "die Haltestelle", "article": "die", "gender": "f", "plural": "-n", "pos": "არსებითი სახელი", "georgian": "გაჩერება", "example_de": "Die Haltestelle ist gleich um die Ecke.", "example_ka": "გაჩერება იქვე კუთხეშია.", "category": "ქალაქი & ტრანსპორტი"},

    # --- 6. დრო, კალენდარი და ამინდი (Zeit, Kalender & Wetter) ---
    {"id": "uhr", "word": "die Uhr", "article": "die", "gender": "f", "plural": "-en", "pos": "არსებითი სახელი", "georgian": "საათი (ხელსაწყო / დროის ერთეული)", "example_de": "Es ist genau zwei Uhr.", "example_ka": "ზუსტად ორი საათია.", "category": "დრო & ამინდი"},
    {"id": "stunde", "word": "die Stunde", "article": "die", "gender": "f", "plural": "-n", "pos": "არსებითი სახელი", "georgian": "საათი (ხანგრძლივობა: 60 წუთი)", "example_de": "Der Unterricht dauert zwei Stunden.", "example_ka": "გაკვეთილი ორ საათს გრძელდება.", "category": "დრო & ამინდი"},
    {"id": "minute", "word": "die Minute", "article": "die", "gender": "f", "plural": "-n", "pos": "არსებითი სახელი", "georgian": "წუთი", "example_de": "Warte bitte fünf Minuten!", "example_ka": "მოიცადე ხუთი წუთი, გეთაყვა!", "category": "დრო & ამინდი"},
    {"id": "tag", "word": "der Tag", "article": "der", "gender": "m", "plural": "-e", "pos": "არსებითი სახელი", "georgian": "დღე", "example_de": "Ich wünsche dir einen schönen Tag!", "example_ka": "ლამაზ დღეს გისურვებ!", "category": "დრო & ამინდი"},
    {"id": "woche", "word": "die Woche", "article": "die", "gender": "f", "plural": "-n", "pos": "არსებითი სახელი", "georgian": "კვირა (7 დღე)", "example_de": "Die Woche hat sieben Tage.", "example_ka": "კვირას შვიდი დღე აქვს.", "category": "დრო & ამინდი"},
    {"id": "wochenende", "word": "das Wochenende", "article": "das", "gender": "n", "plural": "-n", "pos": "არსებითი სახელი", "georgian": "შაბათ-კვირა / უქმეები", "example_de": "Schönes Wochenende!", "example_ka": "კარგ შაბათ-კვირას გისურვებ!", "category": "დრო & ამინდი"},
    {"id": "monat", "word": "der Monat", "article": "der", "gender": "m", "plural": "-e", "pos": "არსებითი სახელი", "georgian": "თვე", "example_de": "Ein Jahr hat zwölf Monate.", "example_ka": "ერთ წელს თორმეტი თვე აქვს.", "category": "დრო & ამინდი"},
    {"id": "morgen_adv", "word": "morgen", "article": "", "gender": "none", "plural": "", "pos": "ზმნიზედა", "georgian": "ხვალ", "example_de": "Morgen habe ich einen Test.", "example_ka": "ხვალ ტესტი მაქვს.", "category": "დრო & ამინდი"},
    {"id": "gestern", "word": "gestern", "article": "", "gender": "none", "plural": "", "pos": "ზმნიზედა", "georgian": "გუშინ", "example_de": "Gestern war ich zu Hause.", "example_ka": "გუშინ სახლში ვიყავი.", "category": "დრო & ამინდი"},
    {"id": "heute", "word": "heute", "article": "", "gender": "none", "plural": "", "pos": "ზმნიზედა", "georgian": "დღეს", "example_de": "Heute lerne ich Deutsch.", "example_ka": "დღეს გერმანულს ვსწავლობ.", "category": "დრო & ამინდი"},
    {"id": "jetzt", "word": "jetzt", "article": "", "gender": "none", "plural": "", "pos": "ზმნიზედა", "georgian": "ახლა", "example_de": "Jetzt ist es Zeit zu schlafen.", "example_ka": "ახლა ძილის დროა.", "category": "დრო & ამინდი"},
    {"id": "wetter", "word": "das Wetter", "article": "das", "gender": "n", "plural": "-", "pos": "არსებითი სახელი", "georgian": "ამინდი", "example_de": "Das Wetter ist heute herrlich.", "example_ka": "დღეს შესანიშნავი ამინდია.", "category": "დრო & ამინდი"},
    {"id": "sonne", "word": "die Sonne", "article": "die", "gender": "f", "plural": "-", "pos": "არსებითი სახელი", "georgian": "მზე", "example_de": "Die Sonne scheint den ganzen Tag.", "example_ka": "მზე მთელი დღე ანათებს.", "category": "დრო & ამინდი"},
    {"id": "regen", "word": "der Regen", "article": "der", "gender": "m", "plural": "-", "pos": "არსებითი სახელი", "georgian": "წვიმა", "example_de": "Es regnet stark.", "example_ka": "ძლიერად წვიმს.", "category": "დრო & ამინდი"},
    {"id": "schnee", "word": "der Schnee", "article": "der", "gender": "m", "plural": "-", "pos": "არსებითი სახელი", "georgian": "თოვლი", "example_de": "Im Winter liegt viel Schnee in den Bergen.", "example_ka": "ზამთარში მთებში ბევრი თოვლი დევს.", "category": "დრო & ამინდი"},

    # --- 7. პროფესიები და სამუშაო (Beruf & Arbeit) ---
    {"id": "beruf", "word": "der Beruf", "article": "der", "gender": "m", "plural": "-e", "pos": "არსებითი სახელი", "georgian": "პროფესია", "example_de": "Was bist du von Beruf?", "example_ka": "რა პროფესიის ხარ?", "category": "პროფესია & სამუშაო"},
    {"id": "arbeit", "word": "die Arbeit", "article": "die", "gender": "f", "plural": "-en", "pos": "არსებითი სახელი", "georgian": "სამუშაო / სამსახური", "example_de": "Ich gehe um 8 Uhr zur Arbeit.", "example_ka": "რვა საათზე სამსახურში მივდივარ.", "category": "პროფესია & სამუშაო"},
    {"id": "arzt", "word": "der Arzt", "article": "der", "gender": "m", "plural": "-ä-e", "pos": "არსებითი სახელი", "georgian": "ექიმი (კაცი)", "example_de": "Der Arzt untersucht den Patienten.", "example_ka": "ექიმი პაციენტს სინჯავს.", "category": "პროფესია & სამუშაო"},
    {"id": "arztin", "word": "die Ärztin", "article": "die", "gender": "f", "plural": "-nen", "pos": "არსებითი სახელი", "georgian": "ექიმი (ქალი)", "example_de": "Frau Dr. Schmidt ist eine erfahrene Ärztin.", "example_ka": "ქალბატონი დოქტორი შმიდტი გამოცდილი ექიმია.", "category": "პროფესია & სამუშაო"},
    {"id": "lehrer", "word": "der Lehrer", "article": "der", "gender": "m", "plural": "-", "pos": "არსებითი სახელი", "georgian": "მასწავლებელი (კაცი)", "example_de": "Unser Deutschlehrer erklärt die Grammatik gut.", "example_ka": "ჩვენი გერმანულის მასწავლებელი კარგად ხსნის გრამატიკას.", "category": "პროფესია & სამუშაო"},
    {"id": "lehrerin", "word": "die Lehrerin", "article": "die", "gender": "f", "plural": "-nen", "pos": "არსებითი სახელი", "georgian": "მასწავლებელი (ქალი)", "example_de": "Die Lehrerin korrigiert die Hausaufgaben.", "example_ka": "მასწავლებელი ასწორებს საშინაო დავალებებს.", "category": "პროფესია & სამუშაო"},
    {"id": "student", "word": "der Student", "article": "der", "gender": "m", "plural": "-en", "pos": "არსებითი სახელი", "georgian": "სტუდენტი (ბიჭი)", "example_de": "Er ist Student an der Universität.", "example_ka": "ის უნივერსიტეტის სტუდენტია.", "category": "პროფესია & სამუშაო"},
    {"id": "studentin", "word": "die Studentin", "article": "die", "gender": "f", "plural": "-nen", "pos": "არსებითი სახელი", "georgian": "სტუდენტი (გოგო)", "example_de": "Sie ist eine fleißige Studentin.", "example_ka": "ის ბეჯითი სტუდენტია.", "category": "პროფესია & სამუშაო"},
    {"id": "informatiker", "word": "der Informatiker", "article": "der", "gender": "m", "plural": "-", "pos": "არსებითი სახელი", "georgian": "ინფორმატიკოსი / IT სპეციალისტი", "example_de": "Als Informatiker programmiert er Apps.", "example_ka": "როგორც IT სპეციალისტი, ის აპლიკაციებს წერს.", "category": "პროფესია & სამუშაო"},
    {"id": "kellner", "word": "der Kellner", "article": "der", "gender": "m", "plural": "-", "pos": "არსებითი სახელი", "georgian": "მიმტანი (კაცი)", "example_de": "Herr Ober! Ein Glas Wasser, bitte!", "example_ka": "მიმტანო! ერთი ჭიქა წყალი, გეთაყვა!", "category": "პროფესია & სამუშაო"},
    {"id": "chef", "word": "der Chef", "article": "der", "gender": "m", "plural": "-s", "pos": "არსებითი სახელი", "georgian": "უფროსი / შეფი", "example_de": "Mein Chef ist sehr verständnisvoll.", "example_ka": "ჩემი უფროსი ძალიან გაგებული კაცია.", "category": "პროფესია & სამუშაო"},
    {"id": "kollege", "word": "der Kollege", "article": "der", "gender": "m", "plural": "-n", "pos": "არსებითი სახელი", "georgian": "კოლეგა (კაცი)", "example_de": "Ich trinke mit meinen Kollegen Kaffee.", "example_ka": "კოლეგებთან ერთად ყავას ვსვამ.", "category": "პროფესია & სამუშაო"},
    {"id": "geld", "word": "das Geld", "article": "das", "gender": "n", "plural": "-", "pos": "არსებითი სახელი", "georgian": "ფული", "example_de": "Er verdient gutes Geld.", "example_ka": "ის კარგ ფულს გამოიმუშავებს.", "category": "პროფესია & სამუშაო"},

    # --- 8. სხეული და ჯანმრთელობა (Körper & Gesundheit) ---
    {"id": "korper", "word": "der Körper", "article": "der", "gender": "m", "plural": "-", "pos": "არსებითი სახელი", "georgian": "სხეული", "example_de": "Sport ist gut für den Körper.", "example_ka": "სპორტი კარგია სხეულისთვის.", "category": "სხეული & ჯანმრთელობა"},
    {"id": "kopf", "word": "der Kopf", "article": "der", "gender": "m", "plural": "-ö-e", "pos": "არსებითი სახელი", "georgian": "თავი", "example_de": "Mein Kopf tut weh.", "example_ka": "თავი მტკივა.", "category": "სხეული & ჯანმრთელობა"},
    {"id": "auge", "word": "das Auge", "article": "das", "gender": "n", "plural": "-n", "pos": "არსებითი სახელი", "georgian": "თვალი", "example_de": "Sie hat blaue Augen.", "example_ka": "მას ლურჯი თვალები აქვს.", "category": "სხეული & ჯანმრთელობა"},
    {"id": "ohr", "word": "das Ohr", "article": "das", "gender": "n", "plural": "-en", "pos": "არსებითი სახელი", "georgian": "ყური", "example_de": "Mein linkes Ohr tut weh.", "example_ka": "მარცხენა ყური მტკივა.", "category": "სხეული & ჯანმრთელობა"},
    {"id": "nase", "word": "die Nase", "article": "die", "gender": "f", "plural": "-n", "pos": "არსებითი სახელი", "georgian": "ცხვირი", "example_de": "Meine Nase läuft.", "example_ka": "ცხვირიდან მდის.", "category": "სხეული & ჯანმრთელობა"},
    {"id": "mund", "word": "der Mund", "article": "der", "gender": "m", "plural": "-ü-er", "pos": "არსებითი სახელი", "georgian": "პირი", "example_de": "Öffnen Sie bitte den Mund!", "example_ka": "გააღეთ პირი, გეთაყვა!", "category": "სხეული & ჯანმრთელობა"},
    {"id": "hals", "word": "der Hals", "article": "der", "gender": "m", "plural": "-ä-e", "pos": "არსებითი სახელი", "georgian": "ყელი / კისერი", "example_de": "Ich habe Halsschmerzen.", "example_ka": "ყელის ტკივილი მაქვს.", "category": "სხეული & ჯანმრთელობა"},
    {"id": "arm", "word": "der Arm", "article": "der", "gender": "m", "plural": "-e", "pos": "არსებითი სახელი", "georgian": "მკლავი / ხელი", "example_de": "Mein Arm tut weh.", "example_ka": "მკლავი მტკივა.", "category": "სხეული & ჯანმრთელობა"},
    {"id": "hand", "word": "die Hand", "article": "die", "gender": "f", "plural": "-ä-e", "pos": "არსებითი სახელი", "georgian": "მტევანი / ხელი", "example_de": "Wasch dir bitte die Hände!", "example_ka": "დაიბანე ხელები, გეთაყვა!", "category": "სხეული & ჯანმრთელობა"},
    {"id": "bauch", "word": "der Bauch", "article": "der", "gender": "m", "plural": "-ä-e", "pos": "არსებითი სახელი", "georgian": "მუცელი", "example_de": "Das Kind hat Bauchschmerzen.", "example_ka": "ბავშვს მუცელი სტკივა.", "category": "სხეული & ჯანმრთელობა"},
    {"id": "bein", "word": "das Bein", "article": "das", "gender": "n", "plural": "-e", "pos": "არსებითი სახელი", "georgian": "ფეხი (მთლიანი ფეხი)", "example_de": "Er hat ein langes Bein.", "example_ka": "მას გრძელი ფეხი აქვს.", "category": "სხეული & ჯანმრთელობა"},
    {"id": "fuss", "word": "der Fuß", "article": "der", "gender": "m", "plural": "-ü-e", "pos": "არსებითი სახელი", "georgian": "ტერფი (Ich gehe zu Fuß = ფეხით მივდივარ)", "example_de": "Ich gehe zu Fuß zur Schule.", "example_ka": "სკოლაში ფეხით მივდივარ.", "category": "სხეული & ჯანმრთელობა"},
    {"id": "schmerz", "word": "der Schmerz", "article": "der", "gender": "m", "plural": "-en", "pos": "არსებითი სახელი", "georgian": "ტკივილი", "example_de": "Haben Sie Schmerzen?", "example_ka": "ტკივილი გაქვთ?", "category": "სხეული & ჯანმრთელობა"},
    {"id": "fieber", "word": "das Fieber", "article": "das", "gender": "n", "plural": "-", "pos": "არსებითი სახელი", "georgian": "სიცხე", "example_de": "Er hat hohes Fieber.", "example_ka": "მას მაღალი სიცხე აქვს.", "category": "სხეული & ჯანმრთელობა"},
    {"id": "husten", "word": "der Husten", "article": "der", "gender": "m", "plural": "-", "pos": "არსებითი სახელი", "georgian": "ხველა", "example_de": "Ich trinke Hustensaft.", "example_ka": "ხველის სიროფს ვსვამ.", "category": "სხეული & ჯანმრთელობა"},
    {"id": "medikament", "word": "das Medikament", "article": "das", "gender": "n", "plural": "-e", "pos": "არსებითი სახელი", "georgian": "მედიკამენტი / წამალი", "example_de": "Nehmen Sie dieses Medikament nach dem Essen!", "example_ka": "მიიღეთ ეს წამალი ჭამის შემდეგ!", "category": "სხეული & ჯანმრთელობა"},
    {"id": "tablette", "word": "die Tablette", "article": "die", "gender": "f", "plural": "-n", "pos": "არსებითი სახელი", "georgian": "აბი / ტაბლეტი", "example_de": "Ich nehme eine Tablette gegen Kopfschmerzen.", "example_ka": "თავის ტკივილის საწინააღმდეგო აბს ვიღებ.", "category": "სხეული & ჯანმრთელობა"},
    {"id": "krank", "word": "krank", "article": "", "gender": "none", "plural": "", "pos": "ზედსართავი სახელი", "georgian": "ავად", "example_de": "Ich kann nicht kommen, ich bin krank.", "example_ka": "ვერ მოვალ, ავად ვარ.", "category": "სხეული & ჯანმრთელობა"},
    {"id": "gesund", "word": "gesund", "article": "", "gender": "none", "plural": "", "pos": "ზედსართავი სახელი", "georgian": "ჯანმრთელი", "example_de": "Bleiben Sie gesund!", "example_ka": "ჯანმრთელობას გისურვებთ!", "category": "სხეული & ჯანმრთელობა"},

    # --- 9. ძირითადი A1 ზმნები (Wichtige A1 Verben) ---
    {"id": "sein", "word": "sein", "article": "", "gender": "none", "plural": "", "pos": "ზმნა", "georgian": "ყოფნა (ich bin, du bist, er ist...)", "example_de": "Ich bin Student.", "example_ka": "მე სტუდენტი ვარ.", "category": "ზმნები"},
    {"id": "haben", "word": "haben", "article": "", "gender": "none", "plural": "", "pos": "ზმნა", "georgian": "ქონა / ყოლა (ich habe, du hast, er hat...)", "example_de": "Ich habe eine Frage.", "example_ka": "მე შეკითხვა მაქვს.", "category": "ზმნები"},
    {"id": "kommen", "word": "kommen", "article": "", "gender": "none", "plural": "", "pos": "ზმნა", "georgian": "მოსვლა", "example_de": "Woher kommst du?", "example_ka": "საიდან მოდიხარ (ხარ)?", "category": "ზმნები"},
    {"id": "heissen", "word": "heißen", "article": "", "gender": "none", "plural": "", "pos": "ზმნა", "georgian": "სახელად წოდება (რქმევა)", "example_de": "Wie heißt du?", "example_ka": "რა გქვია?", "category": "ზმნები"},
    {"id": "wohnen", "word": "wohnen", "article": "", "gender": "none", "plural": "", "pos": "ზმნა", "georgian": "ცხოვრება", "example_de": "Ich wohne in Tiflis.", "example_ka": "მე თბილისში ვცხოვრობ.", "category": "ზმნები"},
    {"id": "lernen", "word": "lernen", "article": "", "gender": "none", "plural": "", "pos": "ზმნა", "georgian": "სწავლა", "example_de": "Wir lernen Deutsch A1.", "example_ka": "ჩვენ ვსწავლობთ გერმანულ A1-ს.", "category": "ზმნები"},
    {"id": "sprechen", "word": "sprechen", "article": "", "gender": "none", "plural": "", "pos": "ზმნა", "georgian": "ლაპარაკი / საუბარი (du sprichst)", "example_de": "Sprichst du Georgisch und Deutsch?", "example_ka": "ლაპარაკობ ქართულად და გერმანულად?", "category": "ზმნები"},
    {"id": "verstehen", "word": "verstehen", "article": "", "gender": "none", "plural": "", "pos": "ზმნა", "georgian": "გაგება / გაგება მნიშვნელობის", "example_de": "Ich verstehe diesen Satz nicht.", "example_ka": "ეს წინადადება არ მესმის.", "category": "ზმნები"},
    {"id": "machen", "word": "machen", "article": "", "gender": "none", "plural": "", "pos": "ზმნა", "georgian": "კეთება", "example_de": "Was machst du heute?", "example_ka": "რას აკეთებ დღეს?", "category": "ზმნები"},
    {"id": "gehen", "word": "gehen", "article": "", "gender": "none", "plural": "", "pos": "ზმნა", "georgian": "წასვლა (ფეხით)", "example_de": "Wie geht es Ihnen?", "example_ka": "როგორ ბრძანდებით?", "category": "ზმნები"},
    {"id": "fahren", "word": "fahren", "article": "", "gender": "none", "plural": "", "pos": "ზმნა", "georgian": "მგზავრობა / ტარება (du fährst)", "example_de": "Wir fahren nach Deutschland.", "example_ka": "ჩვენ გერმანიაში მივემგზავრებით.", "category": "ზმნები"},
    {"id": "kaufen", "word": "kaufen", "article": "", "gender": "none", "plural": "", "pos": "ზმნა", "georgian": "ყიდვა", "example_de": "Ich kaufe ein neues Buch.", "example_ka": "ახალ წიგნს ვყიდულობ.", "category": "ზმნები"},
    {"id": "lesen", "word": "lesen", "article": "", "gender": "none", "plural": "", "pos": "ზმნა", "georgian": "კითხვა (du liest)", "example_de": "Liest du gern Bücher?", "example_ka": "გიყვარს წიგნების კითხვა?", "category": "ზმნები"},
    {"id": "schreiben", "word": "schreiben", "article": "", "gender": "none", "plural": "", "pos": "ზმნა", "georgian": "წერა", "example_de": "Ich schreibe eine E-Mail.", "example_ka": "მე იმეილს ვწერ.", "category": "ზმნები"},
    {"id": "horen", "word": "hören", "article": "", "gender": "none", "plural": "", "pos": "ზმნა", "georgian": "მოსმენა / გაგონება", "example_de": "Ich höre gern klassische Musik.", "example_ka": "სიამოვნებით ვუსმენ კლასიკურ მუსიკას.", "category": "ზმნები"},
    {"id": "sehen", "word": "sehen", "article": "", "gender": "none", "plural": "", "pos": "ზმნა", "georgian": "დანახვა / ყურება (du siehst)", "example_de": "Siehst du den Bahnhof dort drüben?", "example_ka": "ხედავ იქით სადგურს?", "category": "ზმნები"},
    {"id": "schlafen", "word": "schlafen", "article": "", "gender": "none", "plural": "", "pos": "ზმნა", "georgian": "ძილი (du schläfst)", "example_de": "Ich schlafe acht Stunden.", "example_ka": "რვა საათი მძინავს.", "category": "ზმნები"},
    {"id": "aufstehen", "word": "aufstehen", "article": "", "gender": "none", "plural": "", "pos": "ზმნა", "georgian": "ადგომა (განცალკევებადი)", "example_de": "Ich stehe um 7 Uhr auf.", "example_ka": "შვიდ საათზე ვდგები.", "category": "ზმნები"},
    {"id": "einkaufen", "word": "einkaufen", "article": "", "gender": "none", "plural": "", "pos": "ზმნა", "georgian": "საყიდლებზე წასვლა", "example_de": "Am Samstag kaufen wir im Supermarkt ein.", "example_ka": "შაბათს სუპერმარკეტში ვაკეთებთ საყიდლებს.", "category": "ზმნები"},
    {"id": "anrufen", "word": "anrufen", "article": "", "gender": "none", "plural": "", "pos": "ზმნა", "georgian": "ტელეფონით დარეკვა", "example_de": "Rufst du mich heute an?", "example_ka": "დამირეკავ დღეს?", "category": "ზმნები"},
    {"id": "arbeiten", "word": "arbeiten", "article": "", "gender": "none", "plural": "", "pos": "ზმნა", "georgian": "მუშაობა", "example_de": "Wo arbeiten Sie?", "example_ka": "სად მუშაობთ?", "category": "ზმნები"},
    {"id": "brauchen", "word": "brauchen", "article": "", "gender": "none", "plural": "", "pos": "ზმნა", "georgian": "საჭიროება (+ Akkusativ)", "example_de": "Ich brauche deine Hilfe.", "example_ka": "შენი დახმარება მჭირდება.", "category": "ზმნები"},
    {"id": "finden", "word": "finden", "article": "", "gender": "none", "plural": "", "pos": "ზმნა", "georgian": "პოვნა / მიჩნევა (აზრი)", "example_de": "Wie findest du die Stadt?", "example_ka": "როგორ მოგწონს ეს ქალაქი?", "category": "ზმნები"},
    {"id": "wissen", "word": "wissen", "article": "", "gender": "none", "plural": "", "pos": "ზმნა", "georgian": "ცოდნა (ich weiß, du weißt)", "example_de": "Ich weiß es nicht.", "example_ka": "არ ვიცი.", "category": "ზმნები"},
    {"id": "kennen", "word": "kennen", "article": "", "gender": "none", "plural": "", "pos": "ზმნა", "georgian": "ცნობა / გაცნობა", "example_de": "Kennst du Giorgi?", "example_ka": "იცნობ გიორგის?", "category": "ზმნები"},
    {"id": "bleiben", "word": "bleiben", "article": "", "gender": "none", "plural": "", "pos": "ზმნა", "georgian": "დარჩენა (ist geblieben)", "example_de": "Ich bleibe heute zu Hause.", "example_ka": "დღეს სახლში ვრჩები.", "category": "ზმნები"},

    # --- 10. ზედსართავები (Wichtige Adjektive) ---
    {"id": "gut", "word": "gut", "article": "", "gender": "none", "plural": "", "pos": "ზედსართავი სახელი", "georgian": "კარგი", "example_de": "Das ist eine gute Idee.", "example_ka": "ეს კარგი იდეაა.", "category": "ზედსართავები"},
    {"id": "schlecht", "word": "schlecht", "article": "", "gender": "none", "plural": "", "pos": "ზედსართავი სახელი", "georgian": "ცუდი", "example_de": "Das Wetter ist heute schlecht.", "example_ka": "ამინდი დღეს ცუდია.", "category": "ზედსართავები"},
    {"id": "gross", "word": "groß", "article": "", "gender": "none", "plural": "", "pos": "ზედსართავი სახელი", "georgian": "დიდი", "example_de": "Das Haus ist sehr groß.", "example_ka": "სახლი ძალიან დიდია.", "category": "ზედსართავები"},
    {"id": "klein", "word": "klein", "article": "", "gender": "none", "plural": "", "pos": "ზედსართავი სახელი", "georgian": "პატარა", "example_de": "Das Zimmer ist klein aber fein.", "example_ka": "ოთახი პატარაა, მაგრამ საყვარელი.", "category": "ზედსართავები"},
    {"id": "schon", "word": "schön", "article": "", "gender": "none", "plural": "", "pos": "ზედსართავი სახელი", "georgian": "ლამაზი", "example_de": "Tiflis ist eine sehr schöne Stadt.", "example_ka": "თბილისი ძალიან ლამაზი ქალაქია.", "category": "ზედსართავები"},
    {"id": "neu", "word": "neu", "article": "", "gender": "none", "plural": "", "pos": "ზედსართავი სახელი", "georgian": "ახალი", "example_de": "Ich habe ein neues Auto.", "example_ka": "ახალი მანქანა მყავს.", "category": "ზედსართავები"},
    {"id": "alt", "word": "alt", "article": "", "gender": "none", "plural": "", "pos": "ზედსართავი სახელი", "georgian": "ძველი / ხანდაზმული", "example_de": "Das Buch ist alt.", "example_ka": "წიგნი ძველია.", "category": "ზედსართავები"},
    {"id": "teuer", "word": "teuer", "article": "", "gender": "none", "plural": "", "pos": "ზედსართავი სახელი", "georgian": "ძვირი", "example_de": "Die Wohnung ist zu teuer.", "example_ka": "ბინა მეტისმეტად ძვირია.", "category": "ზედსართავები"},
    {"id": "billig", "word": "billig", "article": "", "gender": "none", "plural": "", "pos": "ზედსართავი სახელი", "georgian": "იაფი", "example_de": "Hier kann man billig einkaufen.", "example_ka": "აქ იაფად შეიძლება საყიდლების გაკეთება.", "category": "ზედსართავები"},
    {"id": "schnell", "word": "schnell", "article": "", "gender": "none", "plural": "", "pos": "ზედსართავი სახელი", "georgian": "სწრაფი", "example_de": "Der ICE-Zug ist sehr schnell.", "example_ka": "ICE მატარებელი ძალიან სწრაფია.", "category": "ზედსართავები"},
    {"id": "langsam", "word": "langsam", "article": "", "gender": "none", "plural": "", "pos": "ზედსართავი სახელი", "georgian": "ნელი / ნელა", "example_de": "Bitte sprechen Sie langsamer!", "example_ka": "გეთაყვა, უფრო ნელა ისაუბრეთ!", "category": "ზედსართავები"},
    {"id": "einfach", "word": "einfach", "article": "", "gender": "none", "plural": "", "pos": "ზედსართავი სახელი", "georgian": "მარტივი / უბრალო", "example_de": "Deutsch lernen ist gar nicht so schwer, es ist einfach!", "example_ka": "გერმანულის სწავლა სულაც არაა რთული, მარტივია!", "category": "ზედსართავები"},
    {"id": "schwer", "word": "schwer", "article": "", "gender": "none", "plural": "", "pos": "ზედსართავი სახელი", "georgian": "მძიმე / რთული", "example_de": "Der Koffer ist sehr schwer.", "example_ka": "ჩემოდანი ძალიან მძიმეა.", "category": "ზედსართავები"},
    {"id": "richtig", "word": "richtig", "article": "", "gender": "none", "plural": "", "pos": "ზედსართავი სახელი", "georgian": "სწორი", "example_de": "Deine Antwort ist absolut richtig!", "example_ka": "შენი პასუხი აბსოლუტურად სწორია!", "category": "ზედსართავები"},
    {"id": "falsch", "word": "falsch", "article": "", "gender": "none", "plural": "", "pos": "ზედსართავი სახელი", "georgian": "მცდარი / არასწორი", "example_de": "Das ist leider falsch.", "example_ka": "სამწუხაროდ ეს მცდარია.", "category": "ზედსართავები"},

    # --- 11. კითხვითი სიტყვები (Fragewörter) ---
    {"id": "wie", "word": "wie", "article": "", "gender": "none", "plural": "", "pos": "კითხვითი სიტყვა", "georgian": "როგორ / როგორი", "example_de": "Wie geht es dir?", "example_ka": "როგორ ხარ?", "category": "კითხვითი სიტყვები"},
    {"id": "wo", "word": "wo", "article": "", "gender": "none", "plural": "", "pos": "კითხვითი სიტყვა", "georgian": "სად", "example_de": "Wo wohnst du?", "example_ka": "სად ცხოვრობ?", "category": "კითხვითი სიტყვები"},
    {"id": "woher", "word": "woher", "article": "", "gender": "none", "plural": "", "pos": "კითხვითი სიტყვა", "georgian": "საიდან", "example_de": "Woher kommst du?", "example_ka": "საიდან ხარ?", "category": "კითხვითი სიტყვები"},
    {"id": "wohin", "word": "wohin", "article": "", "gender": "none", "plural": "", "pos": "კითხვითი სიტყვა", "georgian": "სითკენ / სად (მიმართულება)", "example_de": "Wohin fährst du am Wochenende?", "example_ka": "სად მიემგზავრები შაბათ-კვირას?", "category": "კითხვითი სიტყვები"},
    {"id": "was", "word": "was", "article": "", "gender": "none", "plural": "", "pos": "კითხვითი სიტყვა", "georgian": "რა", "example_de": "Was machst du da?", "example_ka": "რას აკეთებ მანდ?", "category": "კითხვითი სიტყვები"},
    {"id": "wer", "word": "wer", "article": "", "gender": "none", "plural": "", "pos": "კითხვითი სიტყვა", "georgian": "ვინ", "example_de": "Wer ist der Mann dort?", "example_ka": "ვინ არის ის კაცი იქ?", "category": "კითხვითი სიტყვები"},
    {"id": "wann", "word": "wann", "article": "", "gender": "none", "plural": "", "pos": "კითხვითი სიტყვა", "georgian": "როდის", "example_de": "Wann beginnt der Kurs?", "example_ka": "როდის იწყება კურსი?", "category": "კითხვითი სიტყვები"},
    {"id": "warum", "word": "warum", "article": "", "gender": "none", "plural": "", "pos": "კითხვითი სიტყვა", "georgian": "რატომ", "example_de": "Warum lernst du Deutsch?", "example_ka": "რატომ სწავლობ გერმანულს?", "category": "კითხვითი სიტყვები"},
    {"id": "wie_viel", "word": "wie viel", "article": "", "gender": "none", "plural": "", "pos": "კითხვითი სიტყვა", "georgian": "რამდენი", "example_de": "Wie viel kostet das?", "example_ka": "რამდენი ღირს ეს?", "category": "კითხვითი სიტყვები"}
]

# --- Practice Exercises for each Lektion ---
lesson_quizzes = {
    1: [
        {
            "question": "როგორ იკითხება სწორად ასოთშეხამება 'ei' სიტყვაში 'mein'?",
            "options": ["ეი", "აი", "იი", "ოი"],
            "answer": 1,
            "explanation": "გერმანულში 'ei' ყოველთვის იკითხება როგორც [აი] (mein = მაინ, nein = ნაინ)."
        },
        {
            "question": "რომელია ზმნა 'kommen'-ის სწორი ფორმა 'du' პირთან?",
            "options": ["komme", "kommt", "kommst", "kommen"],
            "answer": 2,
            "explanation": "du პირთან ზმნის ფუძეს ემატება დაბოლოება -st: du kommst."
        },
        {
            "question": "შეავსეთ გამოტოვებული ადგილი: 'Wie _______ Sie?' (რა გქვიათ თქვენ?)",
            "options": ["heiße", "heißt", "heißen", "heiß"],
            "answer": 2,
            "explanation": "თავაზიან ფორმაში (Sie) ზმნა ყოველთვის იღებს -en დაბოლოებას: Wie heißen Sie?"
        },
        {
            "question": "რომელია ზმნა 'sein' (ყოფნა)-ის სწორი ფორმა 'er' პირთან?",
            "options": ["bin", "bist", "ist", "sind"],
            "answer": 2,
            "explanation": "ზმნა sein: ich bin, du bist, er/sie/es ist, wir sind..."
        },
        {
            "question": "სად დგას ზმნა გერმანულ თხრობით წინადადებაში?",
            "options": ["ყოველთვის პირველ ადგილზე", "ყოველთვის მეორე ადგილზე", "სულ ბოლოში", "ადგილს მნიშვნელობა არ აქვს"],
            "answer": 1,
            "explanation": "გერმანულის მთავარი ოქროს წესია (V2): ზმნა მთავარ წინადადებაში ყოველთვის მე-2 ადგილზე დგას!"
        }
    ],
    2: [
        {
            "question": "რომელი არტიკლი ეკუთვნის არსებით სახელს 'Mutter' (დედა)?",
            "options": ["der", "die", "das", "den"],
            "answer": 1,
            "explanation": "'die Mutter' - მდედრობითი სქესის სახელია, ამიტომ მისი არტიკლია 'die'."
        },
        {
            "question": "რომელი ფორმაა სწორი: 'ჩემი მამა' გერმანულად?",
            "options": ["meine Vater", "mein Vater", "meinen Vater", "meines Vater"],
            "answer": 1,
            "explanation": "მამრობით სქესთან (der Vater) კუთვნილებითი ნაცვალსახელია 'mein' (დაბოლოების გარეშე)."
        },
        {
            "question": "როგორ იწერება რიცხვი '25' გერმანულად?",
            "options": ["zwanzigfünf", "fünfundzwanzig", "fünfzigzwei", "zwanzigundfünf"],
            "answer": 1,
            "explanation": "გერმანელები ჯერ ერთეულს ამბობენ, მერე 'und', მერე ათეულს: fünf-und-zwanzig."
        },
        {
            "question": "რომელი არტიკლი აქვს ყველა არსებით სახელს მრავლობით რიცხვში (Plural)?",
            "options": ["der", "das", "die", "den"],
            "answer": 2,
            "explanation": "მრავლობით რიცხვში ყველა სქესის არსებით სახელს აქვს არტიკლი 'die'!"
        },
        {
            "question": "შეავსეთ: 'Das ist Anna und das sind _______ Kinder.' (მისი ბავშვები)",
            "options": ["sein", "ihr", "ihre", "seine"],
            "answer": 2,
            "explanation": "ანა ქალია (მისი = ihr), ხოლო Kinder მრავლობითია, ამიტომ ემატება -e: ihre Kinder."
        }
    ],
    3: [
        {
            "question": "როგორ ვთქვათ სწორად: 'მე ვაშლი არ მაქვს'?",
            "options": ["Ich habe nicht Apfel.", "Ich habe kein Apfel.", "Ich habe keinen Apfel.", "Ich habe nicht einen Apfel."],
            "answer": 2,
            "explanation": "არსებითი სახელის უარყოფისას ვიყენებთ kein-ს. რადგან der Apfel დგას Akkusativ-ში (ობიექტად), der -> den, ამიტომ: keinen Apfel!"
        },
        {
            "question": "როდის ვიყენებთ 'nicht'-ს?",
            "options": ["მხოლოდ არსებით სახელებთან", "ზმნების, ზედსართავების და წინადადების უარსაყოფად", "მხოლოდ მრავლობით რიცხვში", "არასდროს"],
            "answer": 1,
            "explanation": "nicht გამოიყენება მოქმედების (ზმნის), თვისების (ზედსართავის) და მთლიანი ფრაზის უარსაყოფად."
        },
        {
            "question": "რომელია 'das Brot'-ის განუსაზღვრელი არტიკლი?",
            "options": ["der", "ein", "eine", "einen"],
            "answer": 1,
            "explanation": "საშუალო სქესის (das) განუსაზღვრელი არტიკლია 'ein' (ein Brot)."
        },
        {
            "question": "როგორ ითქმის გერმანულად 'გემრიელია'?",
            "options": ["Es ist teuer.", "Es schmeckt lecker.", "Es ist hungrig.", "Es trinkt gut."],
            "answer": 1,
            "explanation": "'Es schmeckt lecker' ნიშნავს 'გემრიელია' (საჭმელზე საუბრისას)."
        }
    ],
    4: [
        {
            "question": "რა ემართება მამრობით არტიკლს (der) ბრალდებით ბრუნვაში (Akkusativ)?",
            "options": ["რჩება der", "ხდება dem", "ხდება den", "ხდება des"],
            "answer": 2,
            "explanation": "Akkusativ-ში მხოლოდ მამრობითი სქესი იცვლება: der -> den (და ein -> einen, kein -> keinen)."
        },
        {
            "question": "შეავსეთ: 'Ich kaufe _______ Tisch (der Tisch).' (მე ვყიდულობ ერთ მაგიდას)",
            "options": ["ein", "eine", "einen", "einem"],
            "answer": 2,
            "explanation": "der Tisch მამრობითია. kaufen მოითხოვს Akkusativ-ს, ამიტომ ein ხდება 'einen'!"
        },
        {
            "question": "რომელი ოთახია 'das Badezimmer'?",
            "options": ["სამზარეულო", "სააბაზანო", "საძინებელი", "მისაღები ოთახი"],
            "answer": 1,
            "explanation": "das Badezimmer / das Bad არის სააბაზანო ოთახი."
        },
        {
            "question": "რომელია ზედსართავ 'teuer' (ძვირი)-ის ანტონიმი (საპირისპირო სიტყვა)?",
            "options": ["groß", "billig", "hell", "schön"],
            "answer": 1,
            "explanation": "teuer = ძვირი, ხოლო billig = იაფი."
        }
    ],
    5: [
        {
            "question": "რას ნიშნავს სასაუბრო გერმანულში 'halb acht'?",
            "options": ["8:30", "7:30", "8:15", "7:45"],
            "answer": 1,
            "explanation": "ყურადღება! გერმანულში 'halb acht' ნიშნავს 'რვის ნახევარს', ანუ 7:30-ს!"
        },
        {
            "question": "რომელი წინსართი სცილდება ზმნას 'aufstehen' წინადადებაში: 'Ich stehe um 7 Uhr ___'?",
            "options": ["an", "ein", "auf", "aus"],
            "answer": 2,
            "explanation": "ზმნა არის aufstehen, ამიტომ auf გადადის წინადადების ბოლოში: 'Ich stehe um 7 Uhr auf'."
        },
        {
            "question": "რომელი წინდებული გამოიყენება ზუსტ საათთან (მაგ. 8 საათზე)?",
            "options": ["am", "im", "um", "an"],
            "answer": 2,
            "explanation": "საათთან ყოველთვის გამოიყენება 'um': um 8 Uhr, um wie viel Uhr?"
        },
        {
            "question": "რომელი წინდებული გამოიყენება კვირის დღეებთან (მაგ. ორშაბათს)?",
            "options": ["am", "im", "um", "in"],
            "answer": 0,
            "explanation": "დღეებთან და დღის მონაკვეთებთან გამოიყენება 'am': am Montag, am Morgen."
        }
    ],
    6: [
        {
            "question": "რომელია ზმნა 'können'-ის სწორი ფორმა 'ich' პირთან?",
            "options": ["könne", "kann", "kannst", "könnt"],
            "answer": 1,
            "explanation": "მოდალურ ზმნებს ich და er პირებში დაბოლოება არ აქვთ: ich kann, er kann."
        },
        {
            "question": "სად მიდის მეორე (ძირითადი) ზმნა, როცა წინადადებაში მოდალური ზმნაა?",
            "options": ["მოდალური ზმნის გვერდით", "წინადადების პირველ ადგილზე", "წინადადების სულ ბოლოში ინფინიტივში", "არსებითი სახელის წინ"],
            "answer": 2,
            "explanation": "Satzklammer (ჩარჩო): მოდალური ზმნა დგას მე-2 ადგილზე, ძირითადი ზმნა კი ინფინიტივში წინადადების ბოლოში (Ich kann Deutsch sprechen)."
        },
        {
            "question": "რას გამოხატავს მოდალური ზმნა 'möchten'?",
            "options": ["მკაცრ ვალდებულებას", "ზრდილობიან სურვილს ('მსურს')", "აკრძალვას", "წარსულ მოქმედებას"],
            "answer": 1,
            "explanation": "'möchten' ნიშნავს ზრდილობიან სურვილს: 'Ich möchte einen Kaffee trinken'."
        }
    ],
    7: [
        {
            "question": "რა ხდება მდედრობითი არტიკლი (die) მიცემით ბრუნვაში (Dativ)?",
            "options": ["რჩება die", "ხდება der", "ხდება dem", "ხდება den"],
            "answer": 1,
            "explanation": "დატივში ქალის/მდედრობითი სქესის არტიკლი die ხდება 'der' (mit der U-Bahn, in der Stadt)!"
        },
        {
            "question": "რომელ ბრუნვას მოითხოვს წინდებული 'mit'?",
            "options": ["მხოლოდ Nominativ-ს", "მხოლოდ Akkusativ-ს", "მუდამ Dativ-ს", "არცერთ ბრუნვას"],
            "answer": 2,
            "explanation": "წინდებული 'mit' მუდამ დატივს მოითხოვს: Ich fahre mit dem Bus."
        },
        {
            "question": "რას ნიშნავს გერმანული სიტყვა 'geradeaus'?",
            "options": ["მარცხნივ", "მარჯვნივ", "პირდაპირ", "უკან"],
            "answer": 2,
            "explanation": "geradeaus = პირდაპირ (Gehen Sie geradeaus!)."
        }
    ],
    8: [
        {
            "question": "როგორ ვაწარმოებთ მდედრობითი სქესის პროფესიას (მაგ. მასწავლებელი ქალი)?",
            "options": ["ვემატებთ -ung", "ვემატებთ -in", "ვემატებთ -heit", "არაფერი ემატება"],
            "answer": 1,
            "explanation": "მდედრობით პროფესიებს ემატება სუფიქსი -in: der Lehrer -> die Lehrerin, der Arzt -> die Ärztin."
        },
        {
            "question": "რას ნიშნავს 'Hier darf man nicht parken'?",
            "options": ["აქ პარკირება უფასოა", "აქ პარკირება აკრძალულია", "აქ უნდა გააჩეროთ მანქანა", "აქ პარკირება რეკომენდებულია"],
            "answer": 1,
            "explanation": "'nicht dürfen' გამოხატავს მკაცრ აკრძალვას: 'აქ პარკირება აკრძალულია / არ შეიძლება'."
        },
        {
            "question": "რომელია ზმნა 'müssen'-ის სწორი ფორმა 'er' პირთან?",
            "options": ["müsst", "musst", "muss", "müsse"],
            "answer": 2,
            "explanation": "ich muss, du musst, er/sie/es muss."
        }
    ],
    9: [
        {
            "question": "როგორ ვთქვათ გერმანულად 'თავი მტკივა'?",
            "options": ["Mein Kopf ist krank.", "Mein Kopf tut weh.", "Ich mache Kopfschmerz.", "Mein Kopf hat Schmerz."],
            "answer": 1,
            "explanation": "'Mein Kopf tut weh' ან 'Ich habe Kopfschmerzen' არის ტკივილის გამოხატვის სწორი ფორმა."
        },
        {
            "question": "რომელია ზმნა 'kommen'-ის ბრძანებითი ფორმა შენობით (du)?",
            "options": ["Kommst!", "Kommen!", "Komm!", "Komme!"],
            "answer": 2,
            "explanation": "du-ფორმის ბრძანებითში აკლდება ნაცვალსახელი 'du' და დაბოლოება '-st': Komm!"
        },
        {
            "question": "რომელია ზმნა 'sein'-ის თავაზიანი (Sie) ბრძანებითი ფორმა?",
            "options": ["Sind Sie!", "Seien Sie!", "Seid!", "War Sie!"],
            "answer": 1,
            "explanation": "ზმნა sein თავაზიან ბრძანებითში იღებს ფორმას 'Seien Sie!' (მაგ. Seien Sie ruhig!)."
        }
    ],
    10: [
        {
            "question": "რომელ დამხმარე ზმნას იღებს 'gehen' (წასვლა) წარსულ დროში (Perfekt)?",
            "options": ["haben (hat gegangen)", "sein (ist gegangen)", "werden", "bleiben"],
            "answer": 1,
            "explanation": "რადგან gehen გამოხატავს გადაადგილებას სივრცეში A-დან B-ში, დამხმარე ზმნაა sein: 'Er ist gegangen'."
        },
        {
            "question": "რომელია ზმნა 'kaufen'-ის Partizip II (მე-3 ფორმა)?",
            "options": ["gekauft", "gekaufen", "kaufte", "gekauftet"],
            "answer": 0,
            "explanation": "სუსტი (რეგულარული) ზმნა: ge- + kauf + -t = gekauft."
        },
        {
            "question": "შეავსეთ: 'Ich _______ gestern ein Buch gekauft.'",
            "options": ["bin", "habe", "hat", "war"],
            "answer": 1,
            "explanation": "kaufen მოითხოვს haben-ს: 'Ich habe gekauft'."
        },
        {
            "question": "სად დგას Partizip II წინადადებაში პერფექტის დროს?",
            "options": ["დამხმარე ზმნისთანავე მე-3 ადგილზე", "წინადადების სულ ბოლოში", "პირველ ადგილზე", "შუაში"],
            "answer": 1,
            "explanation": "Perfekt-ის ჩარჩო: დამხმარე ზმნა დგას მე-2 ადგილზე, Partizip II კი წინადადების სულ ბოლოში!"
        }
    ]
}

# --- Article Master Trainer Words ---
article_trainer_words = [
    {"word": "Tisch", "article": "der", "georgian": "მაგიდა", "gender": "m"},
    {"word": "Stuhl", "article": "der", "georgian": "სკამი", "gender": "m"},
    {"word": "Schrank", "article": "der", "georgian": "კარადა", "gender": "m"},
    {"word": "Apfel", "article": "der", "georgian": "ვაშლი", "gender": "m"},
    {"word": "Käse", "article": "der", "georgian": "ყველი", "gender": "m"},
    {"word": "Kaffee", "article": "der", "georgian": "ყავა", "gender": "m"},
    {"word": "Tee", "article": "der", "georgian": "ჩაი", "gender": "m"},
    {"word": "Wein", "article": "der", "georgian": "ღვინო", "gender": "m"},
    {"word": "Bahnhof", "article": "der", "georgian": "რკინიგზის სადგური", "gender": "m"},
    {"word": "Flughafen", "article": "der", "georgian": "აეროპორტი", "gender": "m"},
    {"word": "Bus", "article": "der", "georgian": "ავტობუსი", "gender": "m"},
    {"word": "Zug", "article": "der", "georgian": "მატარებელი", "gender": "m"},
    {"word": "Tag", "article": "der", "georgian": "დღე", "gender": "m"},
    {"word": "Monat", "article": "der", "georgian": "თვე", "gender": "m"},
    {"word": "Kopf", "article": "der", "georgian": "თავი", "gender": "m"},
    {"word": "Arm", "article": "der", "georgian": "მკლავი", "gender": "m"},
    {"word": "Fuß", "article": "der", "georgian": "ტერფი", "gender": "m"},
    {"word": "Vater", "article": "der", "georgian": "მამა", "gender": "m"},
    {"word": "Bruder", "article": "der", "georgian": "ძმა", "gender": "m"},
    {"word": "Sohn", "article": "der", "georgian": "ვაჟი", "gender": "m"},
    {"word": "Arzt", "article": "der", "georgian": "ექიმი", "gender": "m"},
    {"word": "Lehrer", "article": "der", "georgian": "მასწავლებელი", "gender": "m"},
    {"word": "Student", "article": "der", "georgian": "სტუდენტი", "gender": "m"},
    {"word": "Lampe", "article": "die", "georgian": "ლამპა / სანათი", "gender": "f"},
    {"word": "Wohnung", "article": "die", "georgian": "ბინა", "gender": "f"},
    {"word": "Küche", "article": "die", "georgian": "სამზარეულო", "gender": "f"},
    {"word": "Tür", "article": "die", "georgian": "კარი", "gender": "f"},
    {"word": "Banane", "article": "die", "georgian": "ბანანი", "gender": "f"},
    {"word": "Tomate", "article": "die", "georgian": "პომიდორი", "gender": "f"},
    {"word": "Kartoffel", "article": "die", "georgian": "კარტოფილი", "gender": "f"},
    {"word": "Milch", "article": "die", "georgian": "რძე", "gender": "f"},
    {"word": "Stadt", "article": "die", "georgian": "ქალაქი", "gender": "f"},
    {"word": "Straße", "article": "die", "georgian": "ქუჩა", "gender": "f"},
    {"word": "Bank", "article": "die", "georgian": "ბანკი", "gender": "f"},
    {"word": "Post", "article": "die", "georgian": "ფოსტა", "gender": "f"},
    {"word": "Apotheke", "article": "die", "georgian": "აფთიაქი", "gender": "f"},
    {"word": "U-Bahn", "article": "die", "georgian": "მეტრო", "gender": "f"},
    {"word": "Uhr", "article": "die", "georgian": "საათი", "gender": "f"},
    {"word": "Woche", "article": "die", "georgian": "კვირა", "gender": "f"},
    {"word": "Minute", "article": "die", "georgian": "წუთი", "gender": "f"},
    {"word": "Nase", "article": "die", "georgian": "ცხვირი", "gender": "f"},
    {"word": "Hand", "article": "die", "georgian": "ხელი / მტევანი", "gender": "f"},
    {"word": "Mutter", "article": "die", "georgian": "დედა", "gender": "f"},
    {"word": "Schwester", "article": "die", "georgian": "და", "gender": "f"},
    {"word": "Tochter", "article": "die", "georgian": "ქალიშვილი", "gender": "f"},
    {"word": "Frau", "article": "die", "georgian": "ქალი / ცოლი", "gender": "f"},
    {"word": "Haus", "article": "das", "georgian": "სახლი", "gender": "n"},
    {"word": "Zimmer", "article": "das", "georgian": "ოთახი", "gender": "n"},
    {"word": "Bett", "article": "das", "georgian": "საწოლი", "gender": "n"},
    {"word": "Sofa", "article": "das", "georgian": "დივანი", "gender": "n"},
    {"word": "Bild", "article": "das", "georgian": "სურათი", "gender": "n"},
    {"word": "Fenster", "article": "das", "georgian": "ფანჯარა", "gender": "n"},
    {"word": "Bad", "article": "das", "georgian": "სააბაზანო", "gender": "n"},
    {"word": "Brot", "article": "das", "georgian": "პური", "gender": "n"},
    {"word": "Brötchen", "article": "das", "georgian": "ფუნთუშა", "gender": "n"},
    {"word": "Wasser", "article": "das", "georgian": "წყალი", "gender": "n"},
    {"word": "Bier", "article": "das", "georgian": "ლუდი", "gender": "n"},
    {"word": "Fleisch", "article": "das", "georgian": "ხორცი", "gender": "n"},
    {"word": "Ei", "article": "das", "georgian": "კვერცხი", "gender": "n"},
    {"word": "Hotel", "article": "das", "georgian": "სასტუმრო", "gender": "n"},
    {"word": "Krankenhaus", "article": "das", "georgian": "საავადმყოფო", "gender": "n"},
    {"word": "Museum", "article": "das", "georgian": "მუზეუმი", "gender": "n"},
    {"word": "Auto", "article": "das", "georgian": "მანქანა", "gender": "n"},
    {"word": "Fahrrad", "article": "das", "georgian": "ველოსიპედი", "gender": "n"},
    {"word": "Jahr", "article": "das", "georgian": "წელი", "gender": "n"},
    {"word": "Auge", "article": "das", "georgian": "თვალი", "gender": "n"},
    {"word": "Ohr", "article": "das", "georgian": "ყური", "gender": "n"},
    {"word": "Bein", "article": "das", "georgian": "ფეხი", "gender": "n"},
    {"word": "Kind", "article": "das", "georgian": "ბავშვი", "gender": "n"},
    {"word": "Baby", "article": "das", "georgian": "ჩვილი ბავშვი", "gender": "n"},
    {"word": "Buch", "article": "das", "georgian": "წიგნი", "gender": "n"}
]

# --- Sentence Builder (Satzbau) Challenges ---
sentence_builders = [
    {
        "id": 1,
        "words": ["Ich", "komme", "aus", "Georgien."],
        "translation_ka": "მე საქართველოდან მოვდივარ (ვარ).",
        "hint": "ქვემდებარე -> ზმნა (მე-2 ადგილზე) -> წინდებული -> ქვეყანა."
    },
    {
        "id": 2,
        "words": ["Wie", "heißen", "Sie", "bitte?"],
        "translation_ka": "რა გქვიათ თქვენ, გეთაყვა?",
        "hint": "კითხვითი სიტყვა -> ზმნა -> ქვემდებარე -> bitte."
    },
    {
        "id": 3,
        "words": ["Mein", "Bruder", "wohnt", "in", "Berlin."],
        "translation_ka": "ჩემი ძმა ბერლინში ცხოვრობს.",
        "hint": "ქვემდებარე (Mein Bruder) -> ზმნა (wohnt) -> ადგილი."
    },
    {
        "id": 4,
        "words": ["Wir", "trinken", "gerne", "heißen", "Kaffee."],
        "translation_ka": "ჩვენ სიამოვნებით ვსვამთ ცხელ ყავას.",
        "hint": "Wir -> ზმნა -> gerne -> ობიექტი."
    },
    {
        "id": 5,
        "words": ["Ich", "brauche", "einen", "neuen", "Schreibtisch."],
        "translation_ka": "მე მჭირდება ახალი საწერი მაგიდა.",
        "hint": "Akkusativ მამრობითი: einen neuen Schreibtisch."
    },
    {
        "id": 6,
        "words": ["Um", "sieben", "Uhr", "stehe", "ich", "auf."],
        "translation_ka": "შვიდ საათზე მე ვდგები.",
        "hint": "თუ დროით იწყება (Um sieben Uhr), ზმნა (stehe) დგას მე-2 ადგილზე, ხოლო auf სულ ბოლოში!"
    },
    {
        "id": 7,
        "words": ["Er", "kann", "sehr", "gut", "Deutsch", "sprechen."],
        "translation_ka": "მას შეუძლია ძალიან კარგად გერმანულად ლაპარაკი.",
        "hint": "მოდალური ზმნის წესი: kann მე-2 ადგილზე, ინფინიტივი (sprechen) სულ ბოლოში!"
    },
    {
        "id": 8,
        "words": ["Ich", "fahre", "mit", "dem", "Bus", "zur", "Arbeit."],
        "translation_ka": "მე ავტობუსით მივდივარ სამსახურში.",
        "hint": "mit + dem Bus (Dativ)."
    },
    {
        "id": 9,
        "words": ["Hier", "darf", "man", "nicht", "rauchen."],
        "translation_ka": "აქ მოწევა არ შეიძლება (აკრძალულია).",
        "hint": "darf man nicht + rauchen."
    },
    {
        "id": 10,
        "words": ["Gestern", "habe", "ich", "meine", "Freunde", "besucht."],
        "translation_ka": "გუშინ მე ჩემს მეგობრებს ვესტუმრე.",
        "hint": "Gestern -> habe -> ich -> Freunde -> besucht (Partizip II ბოლოში)."
    }
]

# --- Comprehensive Final A1 Diagnostic Exam (20 questions) ---
final_exam_questions = [
    {
        "id": 1,
        "question": "'Woher kommen Sie?' - რომელია სწორი პასუხი?",
        "options": ["Ich heiße David.", "Ich komme aus Georgien.", "Ich wohne in Tiflis.", "Ja, ich spreche Deutsch."],
        "answer": 1,
        "explanation": "Woher (საიდან) მოითხოვს პასუხს ქვეყნის ან ქალაქის წარმოშობაზე: aus + ქვეყანა."
    },
    {
        "id": 2,
        "question": "აირჩიეთ სწორი ფორმა: 'Er _______ sehr gut Deutsch.' (sprechen)",
        "options": ["spreche", "sprecht", "spricht", "sprechen"],
        "answer": 2,
        "explanation": "ზმნა sprechen არარეგულარულია er პირში (e -> i): er spricht."
    },
    {
        "id": 3,
        "question": "რომელია 'das Kind'-ის მრავლობითი რიცხვი?",
        "options": ["die Kinde", "die Kindes", "die Kinder", "die Kindern"],
        "answer": 2,
        "explanation": "das Kind -> die Kinder (დაბოლოება -er)."
    },
    {
        "id": 4,
        "question": "შეავსეთ: 'Ich habe _______ Schwester und _______ Bruder.'",
        "options": ["eine / einen", "ein / einen", "einen / eine", "einer / einem"],
        "answer": 0,
        "explanation": "haben მოითხოვს Akkusativ-ს: die Schwester -> eine Schwester, der Bruder -> einen Bruder."
    },
    {
        "id": 5,
        "question": "რომელია სწორი უარყოფა: 'Das ist _______ Buch, das ist ein Heft.'",
        "options": ["nicht", "keine", "kein", "keinen"],
        "answer": 2,
        "explanation": "das Buch საშუალო სქესია, ამიტომ არსებითი სახელის უარყოფაა 'kein Buch'."
    },
    {
        "id": 6,
        "question": "'Wie viel Uhr ist es?' (15:45) - როგორ ითქმის სასაუბროდ?",
        "options": ["Viertel nach drei", "Viertel vor vier", "halb vier", "halb fünf"],
        "answer": 1,
        "explanation": "15:45 ნიშნავს, რომ 4 საათს აკლია 15 წუთი (მეოთხედი) -> Viertel vor vier."
    },
    {
        "id": 7,
        "question": "შეავსეთ: 'Am Samstag _______ wir im Supermarkt _______.' (einkaufen)",
        "options": ["kaufen / ein", "einkaufen / -", "kaufe / ein", "eingekauft / haben"],
        "answer": 0,
        "explanation": "განცალკევებადი ზმნა: wir kaufen ... ein."
    },
    {
        "id": 8,
        "question": "შეავსეთ: 'Wir _______ heute leider nicht ins Kino gehen.' (können)",
        "options": ["kann", "könnt", "können", "kannst"],
        "answer": 2,
        "explanation": "wir პირთან: wir können."
    },
    {
        "id": 9,
        "question": "შეავსეთ დატივის არტიკლი: 'Ich fahre jeden Tag mit _______ U-Bahn (die U-Bahn).'",
        "options": ["die", "der", "dem", "den"],
        "answer": 1,
        "explanation": "mit მოითხოვს Dativ-ს. მდედრობითი სქესის (die) არტიკლი დატივში ხდება 'der'!"
    },
    {
        "id": 10,
        "question": "შეავსეთ: 'Entschuldigung, wo ist _______ Bahnhof (der Bahnhof)?'",
        "options": ["der", "den", "dem", "des"],
        "answer": 0,
        "explanation": "Wo ist ...? ითხოვს სახელობით ბრუნვას (Nominativ) - der Bahnhof."
    },
    {
        "id": 11,
        "question": "შეავსეთ: 'Mein Vater arbeitet _______ Arzt.'",
        "options": ["wie", "als", "bei", "für"],
        "answer": 1,
        "explanation": "პროფესიასთან ყოველთვის გამოიყენება 'als': arbeitet als Arzt."
    },
    {
        "id": 12,
        "question": "შეავსეთ: 'Du bist krank. Du _______ zum Arzt gehen.'",
        "options": ["willst", "sollst", "darfst", "kann"],
        "answer": 1,
        "explanation": "რჩევის მისაცემად გამოიყენება sollen: du sollst zum Arzt gehen."
    },
    {
        "id": 13,
        "question": "რომელია 'essen' (ჭამა)-ის სწორი Partizip II (მე-3 ფორმა)?",
        "options": ["geesst", "gegessen", "geisst", "gegesset"],
        "answer": 1,
        "explanation": "essen არარეგულარული ძლიერი ზმნაა: hat gegessen."
    },
    {
        "id": 14,
        "question": "შეავსეთ: 'Wir _______ letztes Jahr nach Deutschland geflogen.'",
        "options": ["haben", "sind", "hatten", "waren"],
        "answer": 1,
        "explanation": "fliegen (ფრენა) გამოხატავს გადაადგილებას სივრცეში, ამიტომ იღებს 'sein'-ს: wir sind geflogen."
    },
    {
        "id": 15,
        "question": "როგორ მივმართოთ თავაზიანად ადამიანს ბრძანებითში: 'გააღეთ ფანჯარა!'",
        "options": ["Öffne das Fenster!", "Öffnet das Fenster!", "Öffnen Sie bitte das Fenster!", "Sie öffnen das Fenster!"],
        "answer": 2,
        "explanation": "თავაზიანი ბრძანებითი (Sie): ზმნის ინფინიტივი + Sie + bitte: 'Öffnen Sie bitte das Fenster!'."
    },
    {
        "id": 16,
        "question": "რას ნიშნავს 'Ich habe Durst'?",
        "options": ["მშია", "მწყურია", "დავიღალე", "მეძინება"],
        "answer": 1,
        "explanation": "der Durst = წყურვილი -> Ich habe Durst = მწყურია."
    },
    {
        "id": 17,
        "question": "შეავსეთ: 'Der Unterricht beginnt _______ 9 Uhr morgens.'",
        "options": ["am", "im", "um", "an"],
        "answer": 2,
        "explanation": "ზუსტ დროსთან ყოველთვის გამოიყენება წინდებული 'um': um 9 Uhr."
    },
    {
        "id": 18,
        "question": "რომელი წინადადებაა გრამატიკულად სრულიად სწორი?",
        "options": [
            "Heute ich habe keine Zeit.",
            "Heute habe ich keine Zeit.",
            "Heute habe keine Zeit ich.",
            "Ich keine Zeit habe heute."
        ],
        "answer": 1,
        "explanation": "თუ წინადადება იწყება დროითი სიტყვით (Heute), ზმნა (habe) უნდა იდგეს მე-2 ადგილზე, შემდეგ ქვემდებარე: 'Heute habe ich keine Zeit'."
    },
    {
        "id": 19,
        "question": "შეავსეთ: 'Ich trinke den Tee _______ Zucker.' (უშაქროდ)",
        "options": ["mit", "ohne", "von", "aus"],
        "answer": 1,
        "explanation": "'ohne' ნიშნავს 'გარეშე / უ-': ohne Zucker (უშაქროდ)."
    },
    {
        "id": 20,
        "question": "რომელი არსებითი სახელია საშუალო სქესის (das)?",
        "options": ["Küche", "Tisch", "Buch", "Stuhl"],
        "answer": 2,
        "explanation": "die Küche (მდედრობითი), der Tisch (მამრობითი), der Stuhl (მამრობითი), das Buch (საშუალო სქესი!)."
    }
]

# --- Grammar Reference Tables ---
grammar_tables = {
    "articles": {
        "title": "არტიკლების სრული შემაჯამებელი ცხრილი (A1 დონე)",
        "cases": [
            {
                "case_de": "Nominativ (სახელობითი - Wer? Was?)",
                "maskulin": "der / ein / kein",
                "feminin": "die / eine / keine",
                "neutrum": "das / ein / kein",
                "plural": "die / - / keine"
            },
            {
                "case_de": "Akkusativ (ბრალდებითი - Wen? Was?)",
                "maskulin": "den / einen / keinen (იცვლება!)",
                "feminin": "die / eine / keine",
                "neutrum": "das / ein / kein",
                "plural": "die / - / keine"
            },
            {
                "case_de": "Dativ (მიცემითი - Wo? Wem?)",
                "maskulin": "dem / einem / keinem",
                "feminin": "der / einer / keiner (იცვლება der-ად!)",
                "neutrum": "dem / einem / keinem",
                "plural": "den ...n / - / keinen ...n"
            }
        ]
    },
    "pronouns": {
        "title": "პირის ნაცვალსახელები (Personalpronomen)",
        "list": [
            {"person": "1. მხოლობითი (მე)", "nom": "ich", "akk": "mich (ჩემ / მე)", "dat": "mir (ჩემთვის / მე)"},
            {"person": "2. მხოლობითი (შენ)", "nom": "du", "akk": "dich", "dat": "dir"},
            {"person": "3. მხოლობითი (ის - მამრობითი)", "nom": "er", "akk": "ihn", "dat": "ihm"},
            {"person": "3. მხოლობითი (ის - მდედრობითი)", "nom": "sie", "akk": "sie", "dat": "ihr"},
            {"person": "3. მხოლობითი (ის - საშუალო)", "nom": "es", "akk": "es", "dat": "ihm"},
            {"person": "1. მრავლობითი (ჩვენ)", "nom": "wir", "akk": "uns", "dat": "uns"},
            {"person": "2. მრავლობითი (თქვენ - მეგობრული)", "nom": "ihr", "akk": "euch", "dat": "euch"},
            {"person": "3. მრავლობითი (ისინი)", "nom": "sie", "akk": "sie", "dat": "ihnen"},
            {"person": "თავაზიანი ფორმა (თქვენ)", "nom": "Sie", "akk": "Sie", "dat": "Ihnen"}
        ]
    },
    "modal_verbs": {
        "title": "მოდალური ზმნების უღლება აწმყოში",
        "verbs": [
            {"verb": "können (შეძლება)", "ich": "kann", "du": "kannst", "er": "kann", "wir": "können", "ihr": "könnt", "sie": "können"},
            {"verb": "müssen (ვალდებულება)", "ich": "muss", "du": "musst", "er": "muss", "wir": "müssen", "ihr": "müsst", "sie": "müssen"},
            {"verb": "wollen (ნდომა)", "ich": "will", "du": "willst", "er": "will", "wir": "wollen", "ihr": "wollt", "sie": "wollen"},
            {"verb": "möchten (სურვილი)", "ich": "möchte", "du": "möchtest", "er": "möchte", "wir": "möchten", "ihr": "möchtet", "sie": "möchten"},
            {"verb": "dürfen (ნებართვა)", "ich": "darf", "du": "darfst", "er": "darf", "wir": "dürfen", "ihr": "dürft", "sie": "dürfen"},
            {"verb": "sollen (რჩევა/დავალება)", "ich": "soll", "du": "sollst", "er": "soll", "wir": "sollen", "ihr": "sollt", "sie": "sollen"}
        ]
    },
    "irregular_verbs": {
        "title": "A1 დონის 25 ყველაზე გავრცელებული უწესო ზმნა (Partizip II)",
        "list": [
            {"inf": "sein", "prasens": "ist", "perfekt": "ist gewesen", "georgian": "ყოფნა"},
            {"inf": "haben", "prasens": "hat", "perfekt": "hat gehabt", "georgian": "ქონა / ყოლა"},
            {"inf": "gehen", "prasens": "geht", "perfekt": "ist gegangen", "georgian": "წასვლა"},
            {"inf": "fahren", "prasens": "fährt", "perfekt": "ist gefahren", "georgian": "მგზავრობა"},
            {"inf": "kommen", "prasens": "kommt", "perfekt": "ist gekommen", "georgian": "მოსვლა"},
            {"inf": "bleiben", "prasens": "bleibt", "perfekt": "ist geblieben", "georgian": "დარჩენა"},
            {"inf": "fliegen", "prasens": "fliegt", "perfekt": "ist geflogen", "georgian": "ფრენა"},
            {"inf": "aufstehen", "prasens": "steht auf", "perfekt": "ist aufgestanden", "georgian": "ადგომა"},
            {"inf": "essen", "prasens": "isst", "perfekt": "hat gegessen", "georgian": "ჭამა"},
            {"inf": "trinken", "prasens": "trinkt", "perfekt": "hat getrunken", "georgian": "სმა"},
            {"inf": "sprechen", "prasens": "spricht", "perfekt": "hat gesprochen", "georgian": "ლაპარაკი"},
            {"inf": "lesen", "prasens": "liest", "perfekt": "hat gelesen", "georgian": "კითხვა"},
            {"inf": "schreiben", "prasens": "schreibt", "perfekt": "hat geschrieben", "georgian": "წერა"},
            {"inf": "sehen", "prasens": "sieht", "perfekt": "hat gesehen", "georgian": "დანახვა / ყურება"},
            {"inf": "schlafen", "prasens": "schläft", "perfekt": "hat geschlafen", "georgian": "ძილი"},
            {"inf": "treffen", "prasens": "trifft", "perfekt": "hat getroffen", "georgian": "შეხვედრა"},
            {"inf": "helfen", "prasens": "hilft", "perfekt": "hat geholfen", "georgian": "დახმარება"},
            {"inf": "nehmen", "prasens": "nimmt", "perfekt": "hat genommen", "georgian": "აღება"},
            {"inf": "geben", "prasens": "gibt", "perfekt": "hat gegeben", "georgian": "მიცემა"},
            {"inf": "finden", "prasens": "findet", "perfekt": "hat gefunden", "georgian": "პოვნა"},
            {"inf": "wissen", "prasens": "weiß", "perfekt": "hat gewusst", "georgian": "ცოდნა"}
        ]
    }
}

# Assemble final data object
full_data = {
    "lessons": lessons,
    "dictionary": dictionary,
    "lesson_quizzes": lesson_quizzes,
    "article_trainer_words": article_trainer_words,
    "sentence_builders": sentence_builders,
    "final_exam_questions": final_exam_questions,
    "grammar_tables": grammar_tables
}

js_content = "window.GERMAN_A1_DATA = " + json.dumps(full_data, ensure_ascii=False, indent=2) + ";\n"

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write(js_content)

print(f"Successfully generated {OUTPUT_FILE}")
print(f"Total dictionary entries: {len(dictionary)}")
print(f"Total lessons: {len(lessons)}")
print(f"Article trainer entries: {len(article_trainer_words)}")
print(f"Sentence builders: {len(sentence_builders)}")
print(f"Final exam questions: {len(final_exam_questions)}")
