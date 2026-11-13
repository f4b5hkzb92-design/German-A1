# -*- coding: utf-8 -*-
"""
Master Builder for Deutsch A1 Pro Edition.
Compiles all 734 words, 10 deep comprehensive lessons with multi-mode tests,
tables, sentence builders, and final diagnostic exam into js/data.js.
"""

import json
import os
import sys

DIR = "/Users/shotachitaishvili/Documents/German A1"
os.chdir(DIR)

from data_lexicon_part1 import LEXICON as p1
from data_lexicon_part2 import L2_WORDS as p2
from data_lexicon_part3 import L3_WORDS as p3
from data_lexicon_part4 import L4_WORDS as p4
from data_lexicon_part5 import L5_TO_L10_WORDS as p5
from data_lexicon_part6 import L_EXTRA_WORDS as p6

from data_deep_lessons import DEEP_LESSONS as DL1
from data_deep_lessons_part2 import L2 as DL2

L1 = DL1[0]

all_words = p1 + p2 + p3 + p4 + p5 + p6

from data_curriculum_expanded import DL3, DL4, DL5, DL6, DL7, DL8, DL9, DL10
from update_deep_exercises import EXERCISES_DATA
from data_language_labs import LANGUAGE_LABS_DATA

ALL_DEEP_LESSONS = [L1, DL2, DL3, DL4, DL5, DL6, DL7, DL8, DL9, DL10]
for les in ALL_DEEP_LESSONS:
    lid = les.get('id')
    if lid in EXERCISES_DATA:
        les['exercises'] = EXERCISES_DATA[lid]


# --- Extract words for Article Trainer (nouns with der/die/das) ---
article_trainer_words = []
seen_trainer = set()
for w in all_words:
    if w.get("article") in ["der", "die", "das"] and w["word"] not in seen_trainer:
        clean_word = w["word"].replace("der ", "").replace("die ", "").replace("das ", "").strip()
        seen_trainer.add(clean_word)
        article_trainer_words.append({
            "word": clean_word,
            "article": w["article"],
            "georgian": w["georgian"],
            "gender": w["gender"]
        })

print(f"Total Article Trainer items: {len(article_trainer_words)}")

# --- Sentence Builders (15 rich syntax levels) ---
sentence_builders = [
    {
        "id": 1,
        "words": ["Ich", "komme", "aus", "Georgien."],
        "translation_ka": "მე საქართველოდან ვარ.",
        "hint": "ქვემდებარე -> ზმნა (მე-2 ადგილზე) -> aus -> ქვეყანა."
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
        "hint": "Mein Bruder -> ზმნა -> in Berlin."
    },
    {
        "id": 4,
        "words": ["Ich", "trinke", "gerne", "heißen", "Kaffee."],
        "translation_ka": "სიამოვნებით ვსვამ ცხელ ყავას.",
        "hint": "Ich -> trinke -> gerne -> ობიექტი."
    },
    {
        "id": 5,
        "words": ["Wir", "brauchen", "einen", "großen", "Tisch."],
        "translation_ka": "ჩვენ გვჭირდება დიდი მაგიდა.",
        "hint": "Akkusativ მამრობითი: einen großen Tisch."
    },
    {
        "id": 6,
        "words": ["Um", "sieben", "Uhr", "stehe", "ich", "auf."],
        "translation_ka": "შვიდ საათზე მე ვდგები.",
        "hint": "თუ დროით იწყება, ზმნა მე-2 ადგილზეა, auf კი სულ ბოლოში!"
    },
    {
        "id": 7,
        "words": ["Er", "kann", "sehr", "gut", "Deutsch", "sprechen."],
        "translation_ka": "მას შეუძლია ძალიან კარგად გერმანულად ლაპარაკი.",
        "hint": "მოდალური ზმნა (kann) მე-2 ადგილზე, ინფინიტივი (sprechen) სულ ბოლოში!"
    },
    {
        "id": 8,
        "words": ["Ich", "fahre", "jeden", "Tag", "mit", "dem", "Bus."],
        "translation_ka": "მე ყოველდღე ავტობუსით დავდივარ.",
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
    },
    {
        "id": 11,
        "words": ["Am", "Wochenende", "wollen", "wir", "nach", "Wien", "fahren."],
        "translation_ka": "შაბათ-კვირას ჩვენ ვენაში გვინდა გამგზავრება.",
        "hint": "Am Wochenende -> wollen -> wir -> nach Wien -> fahren."
    },
    {
        "id": 12,
        "words": ["Der", "Arzt", "sagt,", "du", "sollst", "im", "Bett", "bleiben."],
        "translation_ka": "ექიმი ამბობს, რომ შენ ლოგინში უნდა დარჩე.",
        "hint": "du sollst im Bett bleiben."
    }
]

# --- Final Comprehensive CEFR A1 Exam (Multi-Skill: Hören, Lesen, Satzbau, Schreiben - 26 items) ---
final_exam_questions = [
    # --- MODUL 1: HÖREN (მოსმენა - 7 დავალება) ---
    {
        "id": 1,
        "module": "hoeren",
        "scenario": "სადგურის დისპეტჩერის განცხადება (Bahnhof Durchsage)",
        "audio_text": "Achtung an Gleis 4. Der Intercity 523 nach München über Nürnberg hat heute circa zwanzig Minuten Verspätung. Grund dafür ist eine technische Störung. Bitte beachten Sie die Durchsagen.",
        "question": "მოსმენა (Hören): რამდენი წუთით აგვიანებს მატარებელი მიუნხენის მიმართულებით?",
        "options": ["10 წუთით", "20 წუთით", "30 წუთით", "არ აგვიანებს, დროულად გადის"],
        "answer": 1,
        "explanation": "დისპეტჩერის განცხადება: 'hat heute circa zwanzig Minuten Verspätung' (დაახლოებით 20 წუთით აგვიანებს)."
    },
    {
        "id": 2,
        "module": "hoeren",
        "scenario": "ექიმის სატელეფონო ავტომოპასუხე (Anrufbeantworter)",
        "audio_text": "Guten Tag. Hier ist die Praxis von Doktor Schneider. Unsere Praxis bleibt diese Woche wegen Urlaub geschlossen. In dringenden Notfällen wenden Sie sich bitte an den ärztlichen Notdienst unter der Telefonnummer 116 117. Ab Montag sind wir wieder für Sie da.",
        "question": "მოსმენა (Hören): რა უნდა ქნას პაციენტმა გადაუდებელ შემთხვევაში?",
        "options": ["ორშაბათამდე მოიცადოს", "დარეკოს გადაუდებელ ნომერზე 116 117", "პირდაპირ კლინიკაში მივიდეს", "ხმოვანი შეტყობინება დატოვოს"],
        "answer": 1,
        "explanation": "ექიმის ჩანაწერში ნათქვამია: 'In dringenden Notfällen wenden Sie sich bitte an den ärztlichen Notdienst unter der Telefonnummer 116 117'."
    },
    {
        "id": 3,
        "module": "hoeren",
        "scenario": "სუპერმარკეტის აქცია (Supermarkt Durchsage)",
        "audio_text": "Liebe Kundinnen und Kunden! Heute im Sonderangebot in unserer Obstabteilung: Süße spanische Orangen, das Kilo für nur zwei Euro neunundvierzig! Greifen Sie zu, das Angebot gilt nur heute!",
        "question": "მოსმენა (Hören): რა ღირს ერთი კილოგრამი ფორთოხალი?",
        "options": ["1,49 €", "2,49 €", "3,49 €", "2,99 €"],
        "answer": 1,
        "explanation": "ფასის გაგონება: 'zwei Euro neunundvierzig' = 2,49 ევრო."
    },
    {
        "id": 4,
        "module": "hoeren",
        "scenario": "სატელეფონო შეთანხმება (Verabredung am Telefon)",
        "audio_text": "Hallo Anna, hier ist Lukas. Treffen wir uns heute Abend um halb sieben vor dem Kino? - Hallo Lukas. Um halb sieben schaffe ich es leider nicht. Geht es vielleicht um Viertel nach sieben? - Ja, perfekt, sieben Uhr fünfzehn passt mir super!",
        "question": "მოსმენა (Hören): რომელ საათზე შეთანხმდნენ ანა და ლუკასი შეხვედრაზე?",
        "options": ["18:30 საათზე (halb sieben)", "19:00 საათზე (sieben Uhr)", "19:15 საათზე (Viertel nach sieben)", "20:00 საათზე (acht Uhr)"],
        "answer": 2,
        "explanation": "ლუკასმა შესთავაზა 18:30 (halb sieben), მაგრამ ანამ სთხოვა 19:15 (Viertel nach sieben / sieben Uhr fünfzehn), რაზეც ლუკასი დათანხმდა."
    },
    {
        "id": 5,
        "module": "hoeren",
        "scenario": "გზის ახსნა ქუჩაში (Wegbeschreibung)",
        "audio_text": "Entschuldigen Sie bitte, wie komme ich zur nächsten Apotheke? - Gehen Sie hier geradeaus bis zur Kreuzung. An der Ampel biegen Sie rechts ab. Nach zweihundert Metern sehen Sie die Apotheke auf der linken Seite, direkt neben der Bäckerei.",
        "question": "მოსმენა (Hören): სად მდებარეობს აფთიაქი?",
        "options": ["შუქნიშანთან მარცხნივ", "მარჯვნივ მოხვევის შემდეგ, მარცხენა მხარეს საცხობის გვერდით", "სადგურის მოპირდაპირედ", "სწორედ კუთხეში"],
        "answer": 1,
        "explanation": "მითითება: 'An der Ampel rechts... auf der linken Seite, direkt neben der Bäckerei'."
    },
    {
        "id": 6,
        "module": "hoeren",
        "scenario": "აეროპორტის გამოცხადება (Flughafen Aufruf)",
        "audio_text": "Letzter Aufruf für Fluggäste des Lufthansa-Fluges LH 430 nach New York. Bitte begeben Sie sich unverzüglich zum Flugsteig B 26. Das Boarding wird in wenigen Minuten beendet.",
        "question": "მოსმენა (Hören): რომელ გეითთან (Flugsteig) უნდა მივიდნენ მგზავრები?",
        "options": ["A 14", "B 26", "C 32", "B 16"],
        "answer": 1,
        "explanation": "გამოცხადება: 'Bitte begeben Sie sich unverzüglich zum Flugsteig B 26'."
    },
    {
        "id": 7,
        "module": "hoeren",
        "scenario": "სახელმწიფო უწყების შეტყობინება (Bürgeramt Termin)",
        "audio_text": "Guten Morgen, Bürgeramt Mitte. Sie haben einen Termin zur Wohnsitzanmeldung gebucht. Ihr Termin ist am Donnerstag, dem zwanzigsten Mai, um zehn Uhr dreißig bei Herrn Richter im Zimmer 104.",
        "question": "მოსმენა (Hören): როდის და რომელ ოთახშია დანიშნული მიღება?",
        "options": ["ოთხშაბათს 10:00-ზე, ოთახი 102", "ხუთშაბათს 10:30-ზე, ოთახი 104", "პარასკევს 11:30-ზე, ოთახი 204", "ხუთშაბათს 14:00-ზე, ოთახი 104"],
        "answer": 1,
        "explanation": "'am Donnerstag... um zehn Uhr dreißig bei Herrn Richter im Zimmer 104'."
    },

    # --- MODUL 2: LESEN & GRAMMATIK (კითხვა და გრამატიკა - 8 დავალება) ---
    {
        "id": 8,
        "module": "lesen",
        "scenario": "მოსაწვევი წერილი (Einladung zum Sommerfest)",
        "reading_text": "Liebe Freunde,\nam Samstag, den 15. Juli, feiere ich meinen Geburtstag im Stadtpark! Wir grillen ab 17:00 Uhr. Fleisch und Getränke kaufe ich. Bitte bringt einen Salat oder ein Dessert mit. Wenn es regnet, feiern wir bei mir zu Hause. Schreibt mir bitte bis Mittwoch, ob ihr kommt!\nLiebe Grüße, Markus",
        "question": "კითხვა (Lesen): რას სთხოვს მარკუსი მეგობრებს, რა უნდა მოიტანონ წვეულებაზე?",
        "options": ["ხორცი და სასმელები", "სალათი ან დესერტი", "საკუთარი გრილი", "ქოლგები და კარავი"],
        "answer": 1,
        "explanation": "ტექსტში ნათქვამია: 'Fleisch und Getränke kaufe ich. Bitte bringt einen Salat oder ein Dessert mit'."
    },
    {
        "id": 9,
        "module": "lesen",
        "scenario": "მაღაზიის სამუშაო საათების აბრა (Öffnungszeiten)",
        "reading_text": "Sehr geehrte Kunden,\nwährend der Feiertage gelten folgende Öffnungszeiten:\nMontag - Donnerstag: 09:00 - 20:00 Uhr\nFreitag (Feiertag): GESCHLOSSEN\nSamstag: 10:00 - 18:00 Uhr\nAm Sonntag bleibt unser Haus geschlossen.",
        "question": "კითხვა (Lesen): შეუძლია თუ არა მომხმარებელს პარასკევს მაღაზიაში შესვლა?",
        "options": ["დიახ, 09:00-დან 20:00-მდე", "არა, პარასკევს მაღაზია დაკეტილია (Feiertag - geschlossen)", "მხოლოდ 10:00-დან 18:00-მდე", "მხოლოდ წინასწარი შეთანხმებით"],
        "answer": 1,
        "explanation": "აბრაზე გარკვევით წერია: 'Freitag (Feiertag): GESCHLOSSEN'."
    },
    {
        "id": 10,
        "module": "lesen",
        "scenario": "ბინის გაქირავების განცხადება (Wohnungsanzeige)",
        "reading_text": "Helle 2-Zimmer-Wohnung in Berlin-Mitte ab 1. September zu vermieten. 58 qm, 3. Stock mit Aufzug, Balkon zur Südseite, Einbauküche vorhanden. Kaltmiete: 650 Euro, Nebenkosten: 150 Euro. Haustiere sind leider nicht erlaubt. Nichtraucher bevorzugt.",
        "question": "კითხვა (Lesen): რამდენია ბინის საერთო ქირა კომუნალურების ჩათვლით (Warmmiete) თვეში?",
        "options": ["650 ევრო", "580 ევრო", "800 ევრო (650 + 150)", "150 ევრო"],
        "answer": 2,
        "explanation": "Kaltmiete (650 €) + Nebenkosten (150 €) = 800 € მთლიანი გადასახადი თვეში."
    },
    {
        "id": 11,
        "module": "lesen",
        "scenario": "გრამატიკა: Akkusativ masculine",
        "question": "გრამატიკა (Grammatik): შეავსეთ სწორი არტიკლი: 'Herr Müller kauft _______ neuen Fernseher (der Fernseher) für das Wohnzimmer.'",
        "options": ["ein", "einen", "einem", "einer"],
        "answer": 1,
        "explanation": "ზმნა kaufen მოითხოვს Akkusativ-ს. მამრობითი სქესის (der Fernseher) განუსაზღვრელი არტიკლი აკუზატივში ხდება 'einen'."
    },
    {
        "id": 12,
        "module": "lesen",
        "scenario": "გრამატიკა: Dativ mit Präpositionen",
        "question": "გრამატიკა (Grammatik): შეავსეთ: 'Ich fahre jeden Morgen mit _______ U-Bahn (die U-Bahn) und nach der Arbeit gehe ich zu _______ Arzt (der Arzt).'",
        "options": ["die / den", "der / dem", "dem / der", "den / des"],
        "answer": 1,
        "explanation": "წინდებულები 'mit' და 'zu' ყოველთვის მოითხოვს Dativ-ს: die U-Bahn -> mit der U-Bahn; der Arzt -> zum (zu dem) Arzt."
    },
    {
        "id": 13,
        "module": "lesen",
        "scenario": "გრამატიკა: Modalverben",
        "question": "გრამატიკა (Grammatik): შეავსეთ: 'Hier im Museum _______ man leider keine Fotos machen.' (აკრძალვა)",
        "options": ["darf", "muss", "will", "soll"],
        "answer": 0,
        "explanation": "აკრძალვის გამოსახატად (nicht dürfen) გამოიყენება 'man darf nicht'."
    },
    {
        "id": 14,
        "module": "lesen",
        "scenario": "გრამატიკა: Perfekt mit sein / haben",
        "question": "გრამატიკა (Grammatik): შეავსეთ დამხმარე ზმნები: 'Gestern _______ Thomas um 7 Uhr aufgestanden und er _______ eine Tasse Kaffee getrunken.'",
        "options": ["hat / ist", "ist / hat", "hat / hat", "ist / ist"],
        "answer": 1,
        "explanation": "aufstehen (ადგომა) მდგომარეობის შეცვლაა -> ist aufgestanden; trinken (დალევა) გარდამავალია -> hat getrunken."
    },
    {
        "id": 15,
        "module": "lesen",
        "scenario": "გრამატიკა: Negation kein vs nicht",
        "question": "გრამატიკა (Grammatik): შეავსეთ: 'Ich habe heute _______ Geld dabei und ich kann _______ einkaufen gehen.'",
        "options": ["nicht / kein", "kein / nicht", "keine / kein", "nicht / keine"],
        "answer": 1,
        "explanation": "არსებითი სახელის (das Geld) უარყოფაა 'kein Geld', ხოლო ზმნის/მოქმედების (einkaufen gehen) უარყოფაა 'nicht'."
    },

    # --- MODUL 3: SATZBAU & SYNTAX (სინტაქსი - 7 დავალება) ---
    {
        "id": 16,
        "module": "satzbau",
        "syntax_rule": "Verbstellung: Position 2 im Hauptsatz (Inversion)",
        "question": "სინტაქსი (Satzbau): დაიწყეთ წინადადება დროის გარემოებით 'Am Sonntag'. რომელი სიტყვათწყობაა გერმანულად სწორი?",
        "options": [
            "Am Sonntag ich bleibe den ganzen Tag zu Hause.",
            "Am Sonntag bleibe ich den ganzen Tag zu Hause.",
            "Am Sonntag bleibe den ganzen Tag zu Hause ich.",
            "Ich am Sonntag bleibe den ganzen Tag zu Hause."
        ],
        "answer": 1,
        "explanation": "გერმანულ თხრობით წინადადებაში უღლებადი ზმნა (bleibe) მკაცრად მე-2 ადგილზე დგას. თუ 1-ლ ადგილზე დროის გარემოებაა (Am Sonntag), სუბიექტი (ich) ზმნის შემდეგ გადადის."
    },
    {
        "id": 17,
        "module": "satzbau",
        "syntax_rule": "Satzklammer: Modalverb (Pos 2) ... Infinitiv (Ende)",
        "question": "სინტაქსი (Satzbau): რომელი წინადადება იცავს მოდალური ზმნის ჩარჩოს (Satzklammer) წესს?",
        "options": [
            "Wir müssen morgen um 8 Uhr am Flughafen sein.",
            "Wir müssen sein morgen um 8 Uhr am Flughafen.",
            "Wir wollen am Flughafen sein müssen morgen.",
            "Morgen wir müssen am Flughafen sein um 8 Uhr."
        ],
        "answer": 0,
        "explanation": "მოდალური ზმნა (müssen) დგას მე-2 პოზიციაზე, ხოლო ძირითადი ზმნა ინფინიტივში (sein) წინადადების ბოლოში!"
    },
    {
        "id": 18,
        "module": "satzbau",
        "syntax_rule": "Trennbare Verben: Präfix am Satzende",
        "question": "სინტაქსი (Satzbau): როგორ დალაგდება სიტყვები ზმნით 'einkaufen' (Ich / im Supermarkt / jeden Samstag / einkaufen)?",
        "options": [
            "Ich einkaufe jeden Samstag im Supermarkt.",
            "Ich kaufe jeden Samstag im Supermarkt ein.",
            "Jeden Samstag ich kaufe im Supermarkt ein.",
            "Ich will jeden Samstag im Supermarkt einkaufen ab."
        ],
        "answer": 1,
        "explanation": "განცალკევებადი ზმნის ფუძე (kaufe) დგას მე-2 პოზიციაზე, ხოლო თავსართი (ein) წინადადების ბოლოში."
    },
    {
        "id": 19,
        "module": "satzbau",
        "syntax_rule": "Ja/Nein-Frage: Verb auf Position 1",
        "question": "სინტაქსი (Satzbau): რომელია გრამატიკულად სწორი კითხვითი წინადადება: 'გინდა დღეს საღამოს კინოში წამოსვლა?'",
        "options": [
            "Du möchtest heute Abend ins Kino mitkommen?",
            "Möchtest du heute Abend ins Kino mitkommen?",
            "Möchtest mitkommen du heute Abend ins Kino?",
            "Ins Kino möchtest du heute Abend mitkommen?"
        ],
        "answer": 1,
        "explanation": "ზოგად (დიახ/არა) კითხვაში უღლებადი ზმნა (Möchtest) ყოველთვის დგას 1-ლ ადგილზე: Möchtest du ... mitkommen?"
    },
    {
        "id": 20,
        "module": "satzbau",
        "syntax_rule": "W-Frage: W-Wort (Pos 1) + Verb (Pos 2) + Subjekt (Pos 3)",
        "question": "სინტაქსი (Satzbau): რომელი წინადადებაა სწორად აგებული: 'რატომ სწავლობ შენ გერმანულს?'",
        "options": [
            "Warum du lernst Deutsch?",
            "Warum lernst du Deutsch?",
            "Lernst du warum Deutsch?",
            "Warum Deutsch du lernst?"
        ],
        "answer": 1,
        "explanation": "W-კითხვაში: 1. W-სიტყვა (Warum) -> 2. ზმნა (lernst) -> 3. ქვემდებარე (du) -> 4. დამატება (Deutsch)."
    },
    {
        "id": 21,
        "module": "satzbau",
        "syntax_rule": "Wortstellung: Zeit vor Ort (TeKaMoLo)",
        "question": "სინტაქსი (Satzbau): შეარჩიეთ სწორი თანმიმდევრობა: დრო (morgen) და მიმართულება (nach Berlin).",
        "options": [
            "Ich fahre nach Berlin morgen mit dem Zug.",
            "Ich fahre morgen mit dem Zug nach Berlin.",
            "Morgen ich fahre nach Berlin mit dem Zug.",
            "Ich nach Berlin morgen fahre mit dem Zug."
        ],
        "answer": 1,
        "explanation": "გერმანულში დროის გარემოება (morgen) წინ უსწრებს ტრანსპორტს (mit dem Zug) და მიმართულების ადგილს (nach Berlin)."
    },
    {
        "id": 22,
        "module": "satzbau",
        "syntax_rule": "Perfekt Satzklammer: Hilfsverb (Pos 2) ... Partizip II (Ende)",
        "question": "სინტაქსი (Satzbau): რომელია პერფექტის სწორი წყობა: 'გუშინ ჩვენ მეგობრებთან ერთად პიცა შევჭამეთ'?",
        "options": [
            "Gestern haben wir mit Freunden eine leckere Pizza gegessen.",
            "Gestern wir haben gegessen eine leckere Pizza mit Freunden.",
            "Gestern haben gegessen wir eine leckere Pizza mit Freunden.",
            "Wir gestern haben eine leckere Pizza gegessen mit Freunden."
        ],
        "answer": 0,
        "explanation": "Gestern (1) + haben (2) + wir (3) + mit Freunden eine leckere Pizza ... gegessen (წინადადების ბოლოში!)."
    },

    # --- MODUL 4: SCHREIBEN (წერა & ფორმულარები - 4 დავალება) ---
    {
        "id": 23,
        "module": "schreiben",
        "scenario": "სარეგისტრაციო ფორმის შევსება (Formular Teil 1: Personalien)",
        "question": "წერა (Schreiben - Formular): ლუკას მაიერის (Lukas Meier, დაბადებული 1998 წლის 14 მაისს, ცხოვრობს ბერლინში) მონაცემებით, რომელია სწორი 'Familienname' (გვარი) და 'Vorname' (სახელი)?",
        "options": [
            "Familienname: Lukas / Vorname: Meier",
            "Familienname: Meier / Vorname: Lukas",
            "Familienname: Berlin / Vorname: Lukas",
            "Familienname: Programmierer / Vorname: Meier"
        ],
        "answer": 1,
        "explanation": "Familienname ნიშნავს გვარს (Meier), ხოლო Vorname - სახელს (Lukas)."
    },
    {
        "id": 24,
        "module": "schreiben",
        "scenario": "სარეგისტრაციო ფორმის შევსება (Formular Teil 2: Wohnort & PLZ)",
        "question": "წერა (Schreiben - Formular): ლუკასის მისამართია: Kantstraße 24, 10623 Berlin. რომელია სწორი ჩანაწერი ველებისთვის 'Wohnort' (ქალაქი) და 'Postleitzahl / PLZ'?",
        "options": [
            "Wohnort: Kantstraße 24 / PLZ: Berlin",
            "Wohnort: Berlin / PLZ: 10623",
            "Wohnort: 10623 / PLZ: Kantstraße",
            "Wohnort: Deutschland / PLZ: Berlin"
        ],
        "answer": 1,
        "explanation": "Wohnort არის ქალაქი (Berlin), ხოლო PLZ (Postleitzahl) არის 5-ნიშნა საფოსტო ინდექსი (10623)."
    },
    {
        "id": 25,
        "module": "schreiben",
        "scenario": "საქმიანი ელ-ფოსტა მასწავლებელს (E-Mail: Anrede & Grund)",
        "question": "წერა (Schreiben - E-Mail): ავადმყოფობის გამო ხვალ ვერ მიდიხართ გაკვეთილზე. რომელი დასაწყისია (მისალმება და მიზეზი) ყველაზე სწორი და თავაზიანი მასწავლებელთან (Frau Müller)?",
        "options": [
            "Hallo Frau Müller! Ich kein Bock auf Schule morgen.",
            "Sehr geehrte Frau Müller, leider kann ich morgen nicht zum Unterricht kommen, weil ich krank bin.",
            "Tschüss Frau Müller, morgen ich bin krank und komme nicht.",
            "Liebe Müller, ich nicht kommen morgen."
        ],
        "answer": 1,
        "explanation": "თავაზიანი ფორმალური მიმართვაა 'Sehr geehrte Frau Müller,' და გრამატიკულად სწორი მიზეზი: 'leider kann ich morgen nicht zum Unterricht kommen, weil ich krank bin'."
    },
    {
        "id": 26,
        "module": "schreiben",
        "scenario": "საქმიანი ელ-ფოსტა მასწავლებელს (E-Mail: Bitte & Grußformel)",
        "question": "წერა (Schreiben - E-Mail): ქალბატონ მიულერთან წერილის დასასრულებლად: გსურთ საშინაო დავალების გამოგზავნის თხოვნა და ოფიციალური დამშვიდობება. რომელია სწორი?",
        "options": [
            "Geben Sie mir die Hausaufgabe schnell! Tschau!",
            "Könnten Sie mir bitte die Hausaufgaben per E-Mail schicken? Vielen Dank und mit freundlichen Grüßen, David.",
            "Was soll ich machen? Tschüss David.",
            "Ich mache keine Hausaufgaben. Bis später!"
        ],
        "answer": 1,
        "explanation": "თავაზიანი თხოვნაა 'Könnten Sie mir bitte die Hausaufgaben per E-Mail schicken?' და ოფიციალური დამშვიდობება 'Mit freundlichen Grüßen'."
    }
]

# Grammar tables
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
        "title": "A1 დონის 35 ყველაზე გავრცელებული უწესო ზმნა (Partizip II)",
        "list": [
            {"inf": "sein", "prasens": "ist", "perfekt": "ist gewesen", "georgian": "ყოფნა"},
            {"inf": "haben", "prasens": "hat", "perfekt": "hat gehabt", "georgian": "ქონა / ყოლა"},
            {"inf": "gehen", "prasens": "geht", "perfekt": "ist gegangen", "georgian": "წასვლა"},
            {"inf": "fahren", "prasens": "fährt", "perfekt": "ist gefahren", "georgian": "მგზავრობა"},
            {"inf": "kommen", "prasens": "kommt", "perfekt": "ist gekommen", "georgian": "მოსვლა"},
            {"inf": "bleiben", "prasens": "bleibt", "perfekt": "ist geblieben", "georgian": "დარჩენა"},
            {"inf": "fliegen", "prasens": "fliegt", "perfekt": "ist geflogen", "georgian": "ფრენა"},
            {"inf": "aufstehen", "prasens": "steht auf", "perfekt": "ist aufgestanden", "georgian": "ადგომა"},
            {"inf": "einschlafen", "prasens": "schläft ein", "perfekt": "ist eingeschlafen", "georgian": "ჩაძინება"},
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
            {"inf": "wissen", "prasens": "weiß", "perfekt": "hat gewusst", "georgian": "ცოდნა"},
            {"inf": "bringen", "prasens": "bringt", "perfekt": "hat gebracht", "georgian": "მოტანა"},
            {"inf": "denken", "prasens": "denkt", "perfekt": "hat gedacht", "georgian": "ფიქრი"},
            {"inf": "kennen", "prasens": "kennt", "perfekt": "hat gekannt", "georgian": "ცნობა"},
            {"inf": "beginnen", "prasens": "beginnt", "perfekt": "hat begonnen", "georgian": "დაწყება"},
            {"inf": "gewinnen", "prasens": "gewinnt", "perfekt": "hat gewonnen", "georgian": "მოგება"},
            {"inf": "verlieren", "prasens": "verliert", "perfekt": "hat verloren", "georgian": "დაკარგვა / წაგება"},
            {"inf": "schließen", "prasens": "schließt", "perfekt": "hat geschlossen", "georgian": "დაკეტვა"},
            {"inf": "einladen", "prasens": "lädt ein", "perfekt": "hat eingeladen", "georgian": "დაპატიჟება"}
        ]
    }
}

from data_grammar_checks import GRAMMAR_CHECKS

for lesson in ALL_DEEP_LESSONS:
    for sec in lesson.get("grammar_sections", []):
        sec_id = str(sec.get("id"))
        if sec_id in GRAMMAR_CHECKS:
            sec["check"] = GRAMMAR_CHECKS[sec_id]

# Master compile
master_data = {
    "lessons": ALL_DEEP_LESSONS,
    "dictionary": all_words,
    "article_trainer_words": article_trainer_words,
    "sentence_builders": sentence_builders,
    "final_exam_questions": final_exam_questions,
    "grammar_tables": grammar_tables,
    "language_labs": LANGUAGE_LABS_DATA
}

output_path = "/Users/shotachitaishvili/Documents/German A1/js/data.js"
js_text = "window.GERMAN_A1_DATA = " + json.dumps(master_data, ensure_ascii=False, indent=2) + ";\n"

with open(output_path, "w", encoding="utf-8") as f:
    f.write(js_text)

print(f"Master compilation complete!")
print(f"Total vocabulary items: {len(all_words)}")
print(f"Total deep lessons: {len(ALL_DEEP_LESSONS)}")
print(f"Total article trainer items: {len(article_trainer_words)}")
print(f"Total sentence builders: {len(sentence_builders)}")
print(f"Total final exam questions: {len(final_exam_questions)}")
print(f"File size: {os.path.getsize(output_path)} bytes")
