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

# --- Final Diagnostic Exam (25 questions) ---
final_exam_questions = [
    {
        "id": 1,
        "question": "'Woher kommen Sie?' - რომელია სწორი პასუხი?",
        "options": ["Ich heiße David.", "Ich komme aus Georgien.", "Ich wohne in Tiflis.", "Ja, ich spreche Deutsch."],
        "answer": 1,
        "explanation": "Woher (საიდან) მოითხოვს პასუხს წარმოშობაზე: aus + ქვეყანა."
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
        "explanation": "haben მოითხოვს Akkusativ-ს: die Schwester -> eine, der Bruder -> einen."
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
        "explanation": "15:45 ნიშნავს, რომ 4 საათს აკლია 15 წუთი -> Viertel vor vier."
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
        "explanation": "mit მოითხოვს Dativ-ს. მდედრობითი (die) დატივში ხდება 'der'!"
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
        "explanation": "fliegen (ფრენა) გამოხატავს გადაადგილებას, ამიტომ იღებს sein-ს: wir sind geflogen."
    },
    {
        "id": 15,
        "question": "როგორ მივმართოთ თავაზიანად ადამიანს ბრძანებითში: 'გააღეთ ფანჯარა!'",
        "options": ["Öffne das Fenster!", "Öffnet das Fenster!", "Öffnen Sie bitte das Fenster!", "Sie öffnen das Fenster!"],
        "answer": 2,
        "explanation": "თავაზიანი ბრძანებითი (Sie): ზმნა ინფინიტივში + Sie + bitte."
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
        "explanation": "ზუსტ დროსთან გამოიყენება წინდებული 'um': um 9 Uhr."
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
        "explanation": "V2 წესი: თუ დროით იწყება (Heute), ზმნა (habe) დგას მე-2 ადგილზე: Heute habe ich keine Zeit."
    },
    {
        "id": 19,
        "question": "შეავსეთ: 'Ich trinke den Tee _______ Zucker.' (უშაქროდ)",
        "options": ["mit", "ohne", "von", "aus"],
        "answer": 1,
        "explanation": "ohne ნიშნავს 'გარეშე / უ-': ohne Zucker."
    },
    {
        "id": 20,
        "question": "რომელი არსებითი სახელია საშუალო სქესის (das)?",
        "options": ["Küche", "Tisch", "Buch", "Stuhl"],
        "answer": 2,
        "explanation": "die Küche (მდედრობითი), der Tisch (მამრობითი), das Buch (საშუალო სქესი!)."
    },
    {
        "id": 21,
        "question": "როგორ იწერება რიცხვი 73 გერმანულად?",
        "options": ["siebzigdrei", "dreiundsiebzig", "dreiundsechzig", "siebenunddreißig"],
        "answer": 1,
        "explanation": "drei + und + siebzig = dreiundsiebzig."
    },
    {
        "id": 22,
        "question": "რომელია ზმნა 'sein'-ის ფორმა 'ihr' (თქვენ - მეგობრები) პირთან?",
        "options": ["seid", "sind", "bist", "ist"],
        "answer": 0,
        "explanation": "ihr seid (თქვენ ხართ)."
    },
    {
        "id": 23,
        "question": "შეავსეთ: 'Das ist mein Vater. Er wohnt mit _______ Mutter in Tiflis.'",
        "options": ["meine", "meiner", "meinem", "meinen"],
        "answer": 1,
        "explanation": "mit მოითხოვს Dativ-ს. die Mutter დატივში ხდება meiner Mutter."
    },
    {
        "id": 24,
        "question": "რას ნიშნავს გერმანული სიტყვა 'gemütlich'?",
        "options": ["ძვირი", "მყუდრო / სასიამოვნო", "ბნელი", "ხმაურიანი"],
        "answer": 1,
        "explanation": "gemütlich ნიშნავს მყუდროს, კომფორტულს."
    },
    {
        "id": 25,
        "question": "რომელია 'gehen' (წასვლა)-ის სწორი პერფექტის ფორმა?",
        "options": ["hat gegeht", "ist gegangen", "hat gegangen", "ist gegeht"],
        "answer": 1,
        "explanation": "gehen მოძრაობის ზმნაა, იღებს sein-ს და უწესო ფორმას: ist gegangen."
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
