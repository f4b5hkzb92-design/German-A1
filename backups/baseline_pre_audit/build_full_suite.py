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

# Lessons 3 to 10 detailed objects
DL3 = {
    "id": 3,
    "title_de": "Lektion 3: Essen, Trinken & Einkaufen",
    "title_ka": "გაკვეთილი 3: საჭმელი, სასმელი და საყიდლები",
    "icon": "🍎",
    "level": "A1.1",
    "objectives_ka": [
        "სურსათის, სასმელებისა და კერძების დასახელება",
        "განუსაზღვრელი არტიკლი (ein, eine, ein) და მისი გამოყენების წესები",
        "უარყოფა: kein vs. nicht (ქართველებისთვის უმნიშვნელოვანესი განსხვავება)",
        "არსებითი სახელების მრავლობითი ფორმები (Plural: -e, -er, -en, -s, Umlaut)",
        "სუპერმარკეტსა და ბაზარში საყიდლების გაკეთება, ფასების კითხვა და გადახდა",
        "რესტორანში შეკვეთა და მომსახურების მიღება"
    ],
    "grammar_sections": [
        {
            "id": "3.1",
            "title": "3.1 განუსაზღვრელი არტიკლი (Unbestimmter Artikel: ein, eine)",
            "content_ka": """განუსაზღვრელი არტიკლი გამოიყენება მაშინ, როდესაც საგანს პირველად ვახსენებთ ან ვგულისხმობთ ზოგადად ერთ რომელიმე საგანს (ქართულად: "ერთი / რომელიღაც"):
• **der** -> **ein** (*ein Apfel* = ერთი ვაშლი)
• **das** -> **ein** (*ein Brot* = ერთი პური)
• **die** -> **eine** (*eine Banane* = ერთი ბანანი)
• **ყურადღება:** მრავლობით რიცხვში განუსაზღვრელი არტიკლი **არ არსებობს**!
  - მხოლობითი: *Das ist ein Apfel.* (ეს ვაშლია.)
  - მრავლობითი: *Das sind Äpfel.* (ეს ვაშლებია - არტიკლის გარეშე!)."""
        },
        {
            "id": "3.2",
            "title": "3.2 უარყოფა: kein vs. nicht (ქართული ენის შეცდომების თავიდან აცილება)",
            "content_ka": """ქართულში ყველგან ვიყენებთ სიტყვას "არ" ან "არა". გერმანულში კი არსებობს მკაცრი წესი:

1. **kein / keine გამოიყენება მხოლოდ არსებითი სახელის უარსაყოფად**, რომელსაც ჩვეულებრივ ექნებოდა ein ან იქნებოდა არტიკლის გარეშე:
   • *Das ist ein Apfel.* -> *Das ist **kein** Apfel.* (ეს არ არის ვაშლი - მამრობითი/საშუალო)
   • *Das ist eine Tomate.* -> *Das ist **keine** Tomate.* (ეს არ არის პომიდორი - მდედრობითი)
   • *Ich habe Zeit.* -> *Ich habe **keine** Zeit.* (დრო არ მაქვს)
   • *Ich esse Fleisch.* -> *Ich esse **kein** Fleisch.* (ხორცს არ ვჭამ)

2. **nicht გამოიყენება ყველა სხვა შემთხვევაში**:
   • **ზმნის უარყოფისას:** *Ich trinke **nicht**.* (არ ვსვამ)
   • **ზედსართავი სახელის უარყოფისას:** *Der Kaffee ist **nicht** süß.* (ყავა არ არის ტკბილი)
   • **საკუთარ სახელებთან:** *Das ist **nicht** Giorgi.* (ეს არ არის გიორგი)
   • **განსაზღვრულ არტიკლთან:** *Das ist **nicht der** Apfel von Anna.* (ეს არ არის ანას ვაშლი)."""
        },
        {
            "id": "3.3",
            "title": "3.3 არსებითი სახელის მრავლობითი რიცხვი (Plural)",
            "content_ka": """გერმანულში მრავლობითი რიცხვი 5 ძირითადი გზით იწარმოება (და ყველა მრავლობითი იღებს არტიკლს **die**):
1. **დაბოლოება -e (ხშირად უმლაუტით):** *der Tisch -> die Tische*, *der Apfel -> die Äpfel*.
2. **დაბოლოება -(e)n:** *die Frau -> die Frauen*, *die Tomate -> die Tomaten*. (ყველაზე გავრცელებული მდედრობითებში).
3. **დაბოლოება -er (ხშირად უმლაუტით):** *das Kind -> die Kinder*, *das Buch -> die Bücher*.
4. **დაბოლოება -s (უცხო სიტყვებში):** *das Auto -> die Autos*, *das Hotel -> die Hotels*.
5. **დაბოლოების გარეშე (-):** *der Lehrer -> die Lehrer*, *das Zimmer -> die Zimmer*."""
        }
    ],
    "dialogues": [
        {
            "id": "d3_1",
            "title": "დიალოგი: საყიდლები სუპერმარკეტში",
            "context": "მყიდველი და გამყიდველი ბოსტნეულის განყოფილებაში.",
            "lines": [
                {"speaker": "Verkäufer", "text_de": "Guten Tag! Was darf es sein?", "text_ka": "დღე მშვიდობისა! რას ინებებთ?"},
                {"speaker": "Kunde", "text_de": "Guten Tag! Ich brauche ein Kilo Äpfel und zwei Kilo Kartoffeln.", "text_ka": "დღე მშვიდობისა! მჭირდება ერთი კილო ვაშლი და ორი კილო კარტოფილი."},
                {"speaker": "Verkäufer", "text_de": "Gerne. Möchten Sie auch Tomaten? Die Tomaten sind heute im Angebot.", "text_ka": "სიამოვნებით. პომიდორიც გნებავთ? პომიდორი დღეს ფასდაკლებითაა."},
                {"speaker": "Kunde", "text_de": "Ja, geben Sie mir bitte 500 Gramm Tomaten. Haben Sie auch frischen Käse?", "text_ka": "დიახ, მომეცით 500 გრამი პომიდორი. ახალი ყველიც გაქვთ?"},
                {"speaker": "Verkäufer", "text_de": "Nein, tut mir leid, Käse haben wir leider nicht.", "text_ka": "არა, მაპატიეთ, ყველი სამწუხაროდ არ გვაქვს."},
                {"speaker": "Kunde", "text_de": "Kein Problem. Was macht das zusammen?", "text_ka": "პრობლემა არ არის. სულ რამდენი იქნება?"},
                {"speaker": "Verkäufer", "text_de": "Das macht zusammen 5 Euro 80.", "text_ka": "სულ იქნება 5 ევრო და 80 ცენტი."}
            ]
        }
    ],
    "cultural_notes": {
        "title": "💡 კულტურული ცნობარი: გადახდა და ტარა გერმანიაში (Pfand)",
        "content_ka": "გერმანიაში პლასტმასისა და მინის ბოთლებზე მოქმედებს დეპოზიტის სისტემა (Pfand - 8-დან 25 ცენტამდე). ცარიელ ბოთლებს აბარებენ სუპერმარკეტის ავტომატში და იღებენ ჩეკს."
    },
    "exercises": {
        "multiple_choice": [
            {
                "id": "mc3_1",
                "question": "როგორ ვთქვათ სწორად: 'მე ვაშლი არ მაქვს'?",
                "options": ["Ich habe nicht Apfel.", "Ich habe keinen Apfel.", "Ich habe kein Apfel.", "Ich habe nicht einen Apfel."],
                "answer": 1,
                "explanation": "არსებითი სახელის უარყოფისას გამოიყენება kein. რადგან der Apfel დგას Akkusativ-ში, ხდება keinen Apfel."
            },
            {
                "id": "mc3_2",
                "question": "რომელია 'das Brötchen'-ის განუსაზღვრელი არტიკლი?",
                "options": ["ein", "eine", "einen", "einem"],
                "answer": 0,
                "explanation": "საშუალო სქესის (das) განუსაზღვრელი არტიკლია ein."
            },
            {
                "id": "mc3_3",
                "question": "შეავსეთ: 'Der Kaffee ist _______ süß.' (არ არის ტკბილი)",
                "options": ["kein", "keine", "nicht", "nichts"],
                "answer": 2,
                "explanation": "ზედსართავი სახელის (süß) უარყოფისას ვიყენებთ nicht-ს."
            }
        ],
        "fill_in_blank": [
            {
                "id": "fib3_1",
                "sentence_before": "Ich trinke ",
                "sentence_after": " Bier. (ლუდს არ ვსვამ)",
                "correct_answer": "kein",
                "hint": "das Bier საშუალო სქესია -> kein Bier"
            }
        ],
        "listening": [
            {
                "id": "lis3_1",
                "audio_text": "Das macht zusammen acht Euro zwanzig.",
                "question": "რამდენია გადასახდელი თანხა?",
                "options": ["8,20 €", "18,20 €", "8,50 €", "2,80 €"],
                "answer": 0
            }
        ]
    }
}

DL4 = {
    "id": 4,
    "title_de": "Lektion 4: Meine Wohnung & Der Akkusativ",
    "title_ka": "გაკვეთილი 4: ჩემი ბინა და ბრალდებითი ბრუნვა (Akkusativ)",
    "icon": "🏠",
    "level": "A1.1",
    "objectives_ka": [
        "ბინის, ოთახების, ავეჯისა და საყოფაცხოვრებო ნივთების აღწერა",
        "ბრალდებითი ბრუნვა (Akkusativ: den/die/das/die, einen/eine/ein, keinen/keine/kein)",
        "ზედსართავი სახელები ბინის დასახასიათებლად (hell, dunkel, groß, klein, teuer, billig)",
        "ბინის ქირაობის განცხადებების გაგება (Kaltmiete, Warmmiete, Nebenkosten, Kaution)"
    ],
    "grammar_sections": [
        {
            "id": "4.1",
            "title": "4.1 ბრალდებითი ბრუნვა (Der Akkusativ) — რა იცვლება?",
            "content_ka": """გერმანულში Akkusativ პასუხობს კითხვებზე: **Wen?** (ვის?) და **Was?** (რას?).
გამოიყენება პირდაპირი ობიექტისას ისეთ ზმნებთან, როგორიცაა: *haben* (ქონა), *brauchen* (საჭიროება), *kaufen* (ყიდვა), *suchen* (ძებნა), *finden* (მიჩნევა), *sehen* (დანახვა).

> **დიდი შვება ქართველებისთვის:**
> Akkusativ-ში ფორმას იცვლის **მხოლოდ მამრობითი სქესი (der)**!
> მდედრობითი (die), საშუალო (das) და მრავლობითი (die) უცვლელი რჩება!

| სქესი | Nominativ (სახელობითი) | Akkusativ (ბრალდებითი) | მაგალითი |
| :--- | :--- | :--- | :--- |
| მამრობითი (m) | **der** / ein / kein | **den / einen / keinen** (იცვლება!) | Ich habe **einen** Tisch. |
| მდედრობითი (f) | **die** / eine / keine | **die / eine / keine** (უცვლელია) | Ich habe **eine** Lampe. |
| საშუალო (n) | **das** / ein / kein | **das / ein / kein** (უცვლელია) | Ich habe **ein** Bett. |
| მრავლობითი (pl) | **die** / - / keine | **die / - / keine** (უცვლელია) | Ich habe Stühle. |"""
        }
    ],
    "dialogues": [
        {
            "id": "d4_1",
            "title": "დიალოგი: ბინის დათვალიერება",
            "context": "გიორგი და გამქირავებელი ათვალიერებენ ბინას.",
            "lines": [
                {"speaker": "Vermieter", "text_de": "Hier ist das Wohnzimmer. Es ist sehr groß und hell.", "text_ka": "აი მისაღები ოთახი. ის ძალიან დიდი და ნათელია."},
                {"speaker": "Giorgi", "text_de": "Ja, wunderbar! Hat die Wohnung auch einen Balkon?", "text_ka": "კი, შესანიშნავია! აქვს ბინას აივანიც?"},
                {"speaker": "Vermieter", "text_de": "Ja, die Tür dort führt direkt auf den Balkon.", "text_ka": "დიახ, ის კარი იქით პირდაპირ აივანზე გადის."},
                {"speaker": "Giorgi", "text_de": "Wie hoch ist die Warmmiete?", "text_ka": "რამდენია სრული ქირა?"},
                {"speaker": "Vermieter", "text_de": "Die Warmmiete beträgt 750 Euro inklusive Nebenkosten und Heizung.", "text_ka": "სრული ქირა 750 ევროა კომუნალურებისა და გათბობის ჩათვლით."}
            ]
        }
    ],
    "cultural_notes": {
        "title": "💡 კულტურული ცნობარი: ბინის ქირაობა გერმანიაში",
        "content_ka": "გერმანიაში ბინები უმეტესად ქირავდება სრულიად ცარიელი (ხშირად სამზარეულოს გარეშეც კი). ქირის გადახდა ხდება ყოველი თვის პირველ სამ სამუშაო დღეში."
    },
    "exercises": {
        "multiple_choice": [
            {
                "id": "mc4_1",
                "question": "შეავსეთ: 'Ich suche _______ Wohnung (die Wohnung).'",
                "options": ["einen", "eine", "ein", "einem"],
                "answer": 1,
                "explanation": "die Wohnung მდედრობითია, Akkusativ-ში რჩება eine Wohnung."
            },
            {
                "id": "mc4_2",
                "question": "შეავსეთ: 'Er kauft _______ Tisch (der Tisch).'",
                "options": ["ein", "einen", "eine", "einem"],
                "answer": 1,
                "explanation": "der Tisch მამრობითია. Akkusativ-ში der ხდება den / einen."
            }
        ],
        "fill_in_blank": [
            {
                "id": "fib4_1",
                "sentence_before": "Hast du ",
                "sentence_after": " Schrank? (der Schrank)",
                "correct_answer": "einen",
                "hint": "der -> einen Akkusativ-ში"
            }
        ],
        "listening": [
            {
                "id": "lis4_1",
                "audio_text": "Die Wohnung hat drei Zimmer und einen Balkon.",
                "question": "რამდენი ოთახი აქვს ბინას?",
                "options": ["2 ოთახი", "3 ოთახი", "4 ოთახი", "1 ოთახი"],
                "answer": 1
            }
        ]
    }
}

DL5 = {
    "id": 5,
    "title_de": "Lektion 5: Mein Tag, Uhrzeit & Trennbare Verben",
    "title_ka": "გაკვეთილი 5: დღის რეჟიმი, საათი და განცალკევებადი ზმნები",
    "icon": "⏰",
    "level": "A1.1",
    "objectives_ka": [
        "საათის თქმა როგორც ოფიციალურ (24h), ისე სასაუბრო (halb, viertel nach/vor) ფორმატში",
        "განცალკევებადი ზმნების მექანიზმის ათვისება (aufstehen, einkaufen, anrufen, fernsehen)",
        "დროის წინდებულების სწორი გამოყენება: um, am, im",
        "დღის განრიგისა და ყოველდღიური აქტივობების მოყოლა"
    ],
    "grammar_sections": [
        {
            "id": "5.1",
            "title": "5.1 საათის თქმა: ოფიციალური vs. სასაუბრო (გერმანული 'halb'-ის ხაფანგი)",
            "content_ka": """• **ოფიციალური დრო (24-საათიანი - რადიოში, მატარებელში):**
  - 14:15 = vierzehn Uhr fünfzehn
  - 08:30 = acht Uhr dreißig

• **არაფორმალური / სასაუბრო დრო:**
  - **nach** (გადაცილებული): 08:10 -> *zehn nach acht*
  - **vor** (აკლია): 07:50 -> *zehn vor acht*
  - **Viertel** (15 წუთი): 08:15 -> *Viertel nach acht*, 08:45 -> *Viertel vor neun*
  - **halb (ნახევარი - ყურადღება!):**
    გერმანულში "halb acht" ნიშნავს, რომ **რვას აკლია ნახევარი, ანუ 07:30-ია**!
    - 08:30 = *halb neun*
    - 12:30 = *halb eins*."""
        },
        {
            "id": "5.2",
            "title": "5.2 განცალკევებადი ზმნები (Trennbare Verben) — წინსართის გაგდება ბოლოში",
            "content_ka": """ზოგიერთ ზმნას აქვს წინსართი (ab-, an-, auf-, aus-, ein-, mit-, vor-, zu-), რომელიც უღლებისას სცილდება ზმნას და **გადადის წინადადების სულ ბოლოში**:
• **aufstehen** (ადგომა): Ich **stehe** jeden Tag um 7 Uhr **auf**.
• **einkaufen** (საყიდლებზე წასვლა): Wir **kaufen** am Samstag im Supermarkt **ein**.
• **anrufen** (დარეკვა): Er **ruft** seine Mutter **an**."""
        }
    ],
    "dialogues": [
        {
            "id": "d5_1",
            "title": "დიალოგი: შეხვედრის დანიშვნა",
            "context": "მარი და გიორგი თანხმდებიან შეხვედრის დროზე.",
            "lines": [
                {"speaker": "Marie", "text_de": "Wann treffen wir uns heute Abend?", "text_ka": "როდის შევხვდეთ ამ საღამოს?"},
                {"speaker": "Giorgi", "text_de": "Um wie viel Uhr beginnt der Deutschkurs?", "text_ka": "რომელ საათზე იწყება გერმანულის კურსი?"},
                {"speaker": "Marie", "text_de": "Der Kurs fängt um Viertel nach sechs an und hört um Viertel vor acht auf.", "text_ka": "კურსი იწყება ექვსის თხუთმეტზე და მთავრდება რვის თხუთმეტ წუთზე."},
                {"speaker": "Giorgi", "text_de": "Perfekt! Dann treffen wir uns um acht Uhr im Café.", "text_ka": "იდეალურია! მაშინ რვა საათზე შევხვდეთ კაფეში."}
            ]
        }
    ],
    "cultural_notes": {
        "title": "💡 კულტურული ცნობარი: Ruhezeiten (დასვენების საათები)",
        "content_ka": "გერმანიაში მოქმედებს მკაცრი კანონი სიმშვიდის შესახებ: საღამოს 22:00-დან დილის 06:00-მდე, ასევე კვირა დღეს და უქმეებზე ხმაური (მტვერსასრუტი, სარეცხი მანქანა, რემონტი) აკრძალულია."
    },
    "exercises": {
        "multiple_choice": [
            {
                "id": "mc5_1",
                "question": "რას ნიშნავს სასაუბროდ 'halb zehn'?",
                "options": ["10:30", "09:30", "10:15", "09:45"],
                "answer": 1,
                "explanation": "halb zehn ნიშნავს ათის ნახევარს, ანუ 09:30-ს."
            },
            {
                "id": "mc5_2",
                "question": "რომელი წინდებული გამოიყენება ზუსტ საათთან?",
                "options": ["am", "im", "um", "in"],
                "answer": 2,
                "explanation": "საათთან გამოიყენება um: um 8 Uhr."
            }
        ],
        "fill_in_blank": [
            {
                "id": "fib5_1",
                "sentence_before": "Ich stehe um 7 Uhr ",
                "sentence_after": ". (aufstehen)",
                "correct_answer": "auf",
                "hint": "წინსართი auf გადადის ბოლოში"
            }
        ],
        "listening": [
            {
                "id": "lis5_1",
                "audio_text": "Der Zug fährt um Viertel vor neun ab.",
                "question": "რომელ საათზე გადის მატარებელი?",
                "options": ["08:45", "09:15", "08:15", "09:45"],
                "answer": 0
            }
        ]
    }
}

DL6 = {
    "id": 6,
    "title_de": "Lektion 6: Freizeit, Hobbys & Modalverben",
    "title_ka": "გაკვეთილი 6: თავისუფალი დრო და მოდალური ზმნები",
    "icon": "⚽",
    "level": "A1.2",
    "objectives_ka": [
        "ჰობებზე, სპორტსა და თავისუფალ დროზე საუბარი",
        "მოდალური ზმნების (können, wollen, möchten) უღლება და წესები",
        "წინადადების ჩარჩო (Satzklammer): მოდალური ზმნა მე-2 ადგილზე, ინფინიტივი სულ ბოლოში!",
        "კვირის დღეები, თვეები, წელიწადის დროები და ამინდი"
    ],
    "grammar_sections": [
        {
            "id": "6.1",
            "title": "6.1 მოდალური ზმნები და წინადადების ჩარჩო (Satzklammer)",
            "content_ka": """მოდალური ზმნები გამოხატავენ მოქმედების შესაძლებლობას (können), სურვილს (wollen/möchten) ან აუცილებლობას.
მათ აქვთ ორი ოქროს წესი:
1. **ich და er/sie/es პირებში არ აქვთ დაბოლოება და ფორმა იდენტურია!** (ich kann = er kann).
2. **წინადადების ჩარჩო:** მოდალური ზმნა იუღლება და დგას **მე-2 ადგილზე**, ხოლო ძირითადი ზმნა უცვლელი ინფინიტივის სახით მიდის **წინადადების სულ ბოლოში**!
   - *Ich **kann** sehr gut Deutsch **sprechen**.* (მე შემიძლია გერმანულად ლაპარაკი).
   - *Wir **wollen** am Samstag ins Kino **gehen**.*"""
        }
    ],
    "dialogues": [
        {
            "id": "d6_1",
            "title": "დიალოგი: შაბათ-კვირის გეგმები",
            "context": "მეგობრები გეგმავენ დასვენებას.",
            "lines": [
                {"speaker": "Stefan", "text_de": "Was willst du am Wochenende machen?", "text_ka": "რისი გაკეთება გინდა შაბათ-კვირას?"},
                {"speaker": "Giorgi", "text_de": "Ich möchte am Samstag Fußball spielen und am Sonntag ein Buch lesen.", "text_ka": "შაბათს მინდა ფეხბურთი ვითამაშო და კვირას წიგნი წავიკითხო."},
                {"speaker": "Stefan", "text_de": "Kannst du gut schwimmen? Wir können ins Schwimmbad gehen.", "text_ka": "კარგად შეგიძლია ცურვა? შეგვიძლია აუზზე წავიდეთ."},
                {"speaker": "Giorgi", "text_de": "Tolle Idee! Am Sonntag habe ich Zeit.", "text_ka": "მაგარი იდეაა! კვირას მექნება დრო."}
            ]
        }
    ],
    "cultural_notes": {
        "title": "💡 კულტურული ცნობარი: Vereinsleben (კლუბური ცხოვრება)",
        "content_ka": "გერმანიაში უკიდურესად პოპულარულია გაერთიანებები (Vereine) - სპორტული კლუბები, საფეხბურთო გუნდები, მუსიკალური ან მოხალისეობრივი საზოგადოებები."
    },
    "exercises": {
        "multiple_choice": [
            {
                "id": "mc6_1",
                "question": "რომელია ზმნა 'können'-ის ფორმა 'er' პირთან?",
                "options": ["könnt", "kannst", "kann", "könne"],
                "answer": 2,
                "explanation": "ich kann, du kannst, er kann."
            },
            {
                "id": "mc6_2",
                "question": "სად დგას მეორე ზმნა წინადადებაში: 'Er will heute Fußball _______'?",
                "options": ["პირველ ადგილზე", "სულ ბოლოში ინფინიტივში (spielen)", "მოდალური ზმნის გვერდით", "არტიკლთან"],
                "answer": 1,
                "explanation": "Satzklammer-ის წესით ძირითადი ზმნა ინფინიტივში მიდის წინადადების სულ ბოლოში."
            }
        ],
        "fill_in_blank": [
            {
                "id": "fib6_1",
                "sentence_before": "Wir ",
                "sentence_after": " Deutsch lernen. (wollen)",
                "correct_answer": "wollen",
                "hint": "wir პირთან არის wollen"
            }
        ],
        "listening": [
            {
                "id": "lis6_1",
                "audio_text": "Am Sonntag kann ich leider nicht kommen.",
                "question": "როდის ვერ მოდის მოსაუბრე?",
                "options": ["შაბათს", "კვირას", "ორშაბათს", "პარასკევს"],
                "answer": 1
            }
        ]
    }
}

DL7 = {
    "id": 7,
    "title_de": "Lektion 7: Unterwegs in der Stadt & Der Dativ",
    "title_ka": "გაკვეთილი 7: ქალაქში ორიენტაცია და მიცემითი ბრუნვა (Dativ)",
    "icon": "🚇",
    "level": "A1.2",
    "objectives_ka": [
        "ქალაქში ორიენტაცია და გზის ახსნა (geradeaus, nach links, nach rechts)",
        "მიცემითი ბრუნვა (Der Dativ: dem, der, dem, den + n)",
        "წინდებულები, რომლებიც მუდამ Dativ-ს მოითხოვენ: mit, nach, aus, zu, bei, von, seit",
        "საზოგადოებრივი ტრანსპორტით სარგებლობა და ბილეთების შეძენა"
    ],
    "grammar_sections": [
        {
            "id": "7.1",
            "title": "7.1 მიცემითი ბრუნვა (Der Dativ) და არტიკლების ცვლილება",
            "content_ka": """დატივი პასუხობს კითხვებზე: **Wo?** (სად?) და **Wem?** (ვის?).
არტიკლები დატივში შემდეგნაირად იცვლება:
• **der -> dem** (*der Bus -> mit dem Bus*)
• **das -> dem** (*das Auto -> mit dem Auto*)
• **die -> der** (*die U-Bahn -> mit der U-Bahn* — ყურადღება! ქალის არტიკლი ხდება der!)
• **die Plural -> den (+ არსებითს ემატება -n)** (*die Freunde -> mit den Freunden*)."""
        },
        {
            "id": "7.2",
            "title": "7.2 დატივის 7 ოქროს წინდებული (immer mit Dativ!)",
            "content_ka": """დაიმახსოვრეთ ეს წინდებულები — მათ შემდეგ **მუდამ გამოიყენება Dativ**:
**aus, bei, mit, nach, seit, von, zu**
• *Ich fahre **mit dem** Zug.* (მატარებლით)
• *Ich gehe **zum** (zu + dem) Arzt.* (ექიმთან მივდივარ)
• *Ich gehe **zur** (zu + der) Bank.* (ბანკში მივდივარ)
• *Ich wohne **bei meinen** Eltern.* (მშობლებთან ვცხოვრობ)."""
        }
    ],
    "dialogues": [
        {
            "id": "d7_1",
            "title": "დიალოგი: გზის კითხვა ქუჩაში",
            "context": "ტურისტი ეკითხება გამვლელს გზას სადგურისკენ.",
            "lines": [
                {"speaker": "Tourist", "text_de": "Entschuldigung, wie komme ich zum Hauptbahnhof?", "text_ka": "უკაცრავად, როგორ მივიდე ცენტრალურ სადგურამდე?"},
                {"speaker": "Passant", "text_de": "Gehen Sie hier geradeaus bis zur Kreuzung und biegen Sie nach links ab.", "text_ka": "იარეთ აქ პირდაპირ გზაჯვარედინამდე და შეუხვიეთ მარცხნივ."},
                {"speaker": "Tourist", "text_de": "Kann ich auch mit dem Bus fahren?", "text_ka": "ავტობუსითაც შემიძლია წავიდე?"},
                {"speaker": "Passant", "text_de": "Ja, der Bus Linie 100 fährt direkt zum Bahnhof.", "text_ka": "დიახ, N100 ავტობუსი პირდაპირ სადგურამდე მიდის."}
            ]
        }
    ],
    "cultural_notes": {
        "title": "💡 კულტურული ცნობარი: ტრანსპორტი DACH ქვეყნებში",
        "content_ka": "გერმანიის მეტროსა და მატარებლებში არ არის ტურნიკეტები, მაგრამ მოქმედებს მკაცრი შემთხვევითი კონტროლი. ბილეთის დაუკომპოსტირებლად მგზავრობა 60 ევრო ჯარიმაა."
    },
    "exercises": {
        "multiple_choice": [
            {
                "id": "mc7_1",
                "question": "რა ხდება მდედრობითი არტიკლი (die) დატივში (Dativ)?",
                "options": ["die", "der", "dem", "den"],
                "answer": 1,
                "explanation": "დატივში die ხდება der: mit der U-Bahn."
            },
            {
                "id": "mc7_2",
                "question": "შეავსეთ: 'Ich fahre mit _______ Bus (der Bus).'",
                "options": ["den", "dem", "der", "das"],
                "answer": 1,
                "explanation": "mit მოითხოვს Dativ-ს. der Bus ხდება dem Bus."
            }
        ],
        "fill_in_blank": [
            {
                "id": "fib7_1",
                "sentence_before": "Ich gehe zu ",
                "sentence_after": " Arzt. (zu + dem = zum)",
                "correct_answer": "dem",
                "hint": "der Arzt -> dem Arzt"
            }
        ],
        "listening": [
            {
                "id": "lis7_1",
                "audio_text": "Biegen Sie an der Ampel nach rechts ab!",
                "question": "საით უნდა შეუხვიოს მძღოლმა?",
                "options": ["მარცხნივ", "მარჯვნივ", "პირდაპირ", "უკან"],
                "answer": 1
            }
        ]
    }
}

DL8 = {
    "id": 8,
    "title_de": "Lektion 8: Beruf, Arbeit & Alltag",
    "title_ka": "გაკვეთილი 8: პროფესია, სამუშაო და მოდალური ზმნები (müssen, dürfen)",
    "icon": "💼",
    "level": "A1.2",
    "objectives_ka": [
        "პროფესიების დასახელება და მდედრობითი ფორმის (-in) წარმოება",
        "მოდალური ზმნები: müssen (ვალდებულება) და dürfen (ნებართვა / nicht dürfen = აკრძალვა)",
        "წინდებულები სამსახურთან: als (როგორც), bei (+ Dativ - კომპანიაში), seit (+ Dativ - უკვე რამდენი ხანია)",
        "სამუშაო გრაფიკისა და მოვალეობების აღწერა"
    ],
    "grammar_sections": [
        {
            "id": "8.1",
            "title": "8.1 პროფესიები და მდედრობითი ფორმა -in",
            "content_ka": """გერმანულში ქალის პროფესიის გამოსახატავად მამრობით ფორმას ემატება სუფიქსი **-in**:
• *der Lehrer* -> *die Lehrer**in***
• *der Arzt* -> *die **Ärztin*** (უმლაუტით)
• *der Student* -> *die Student**in***
• მრავლობითში: *die Lehrerinnen, die Ärztinnen*.

წინდებულები:
• *Ich arbeite **als** Arzt.* (ვმუშაობ როგორც ექიმი)
• *Ich arbeite **bei** Siemens.* (ვმუშაობ სიმენსში)."""
        },
        {
            "id": "8.2",
            "title": "8.2 მოდალური ზმნები: müssen და dürfen",
            "content_ka": """• **müssen (აუცილებლობა):**
  - ich muss, du musst, er muss, wir müssen, ihr müsst, sie müssen.
  - *Ich **muss** heute lange **arbeiten**.* (დღეს დიდხანს უნდა ვიმუშაო).
• **dürfen (ნებართვა / nicht dürfen = მკაცრი აკრძალვა!):**
  - ich darf, du darfst, er darf, wir dürfen, ihr dürft, sie dürfen.
  - *Hier **darf** man **nicht** parken!* (აქ პარკირება აკრძალულია!)."""
        }
    ],
    "dialogues": [
        {
            "id": "d8_1",
            "title": "დიალოგი: გასაუბრება სამსახურზე",
            "context": "გიორგი საუბრობს თავის პროფესიაზე.",
            "lines": [
                {"speaker": "Klara", "text_de": "Was bist du von Beruf, Giorgi?", "text_ka": "რა პროფესიის ხარ, გიორგი?"},
                {"speaker": "Giorgi", "text_de": "Ich bin Informatiker. Ich arbeite als Softwareentwickler bei einer Firma.", "text_ka": "ინფორმატიკოსი ვარ. ვმუშაობ პროგრამულ დეველოპერად ერთ ფირმაში."},
                {"speaker": "Klara", "text_de": "Seit wann arbeitest du dort?", "text_ka": "რამდენი ხანია რაც იქ მუშაობ?"},
                {"speaker": "Giorgi", "text_de": "Seit einem Jahr. Die Arbeit macht mir viel Spaß.", "text_ka": "უკვე ერთი წელია. სამსახური ძალიან მსიამოვნებს."}
            ]
        }
    ],
    "cultural_notes": {
        "title": "💡 კულტურული ცნობარი: Feierabend და სამუშაო ეთიკა",
        "content_ka": "გერმანელები მკაცრად მიჯნავენ სამსახურსა და პირად ცხოვრებას (Work-Life-Balance). სამუშაო საათების დასრულების შემდეგ (Feierabend) თანამშრომლებს საქმიან საკითხებზე იშვიათად აწუხებენ."
    },
    "exercises": {
        "multiple_choice": [
            {
                "id": "mc8_1",
                "question": "როგორ ითქმის: 'ის ექიმად მუშაობს'?",
                "options": ["Er arbeitet wie Arzt.", "Er arbeitet als Arzt.", "Er arbeitet bei Arzt.", "Er arbeitet für Arzt."],
                "answer": 1,
                "explanation": "პროფესიასთან გამოიყენება als: arbeitet als Arzt."
            },
            {
                "id": "mc8_2",
                "question": "რას ნიშნავს 'Hier darf man nicht rauchen'?",
                "options": ["აქ მოწევა ნებადართულია", "აქ მოწევა აკრძალულია", "აქ უნდა მოწიოთ", "აქ სიგარეტი იყიდება"],
                "answer": 1,
                "explanation": "nicht dürfen გამოხატავს მკაცრ აკრძალვას."
            }
        ],
        "fill_in_blank": [
            {
                "id": "fib8_1",
                "sentence_before": "Er ",
                "sentence_after": " heute Überstunden machen. (müssen)",
                "correct_answer": "muss",
                "hint": "er პირთან ფორმაა muss"
            }
        ],
        "listening": [
            {
                "id": "lis8_1",
                "audio_text": "Ich arbeite seit zwei Jahren bei Siemens.",
                "question": "რამდენი ხანია რაც მოსაუბრე მუშაობს სიმენსში?",
                "options": ["1 წელია", "2 წელია", "3 წელია", "5 თვეა"],
                "answer": 1
            }
        ]
    }
}

DL9 = {
    "id": 9,
    "title_de": "Lektion 9: Körper, Gesundheit & Imperativ",
    "title_ka": "გაკვეთილი 9: სხეული, ჯანმრთელობა და ბრძანებითი კილო",
    "icon": "🩺",
    "level": "A1.2",
    "objectives_ka": [
        "სხეულის ნაწილების დასახელება და ტკივილის გამოხატვა (tut weh / tun weh)",
        "ბრძანებითი კილო (Der Imperativ): du-ფორმა (Komm!), ihr-ფორმა (Kommt!), Sie-ფორმა (Kommen Sie!)",
        "ექიმთან ვიზიტი, სიმპტომების აღწერა და აფთიაქში წამლის ყიდვა",
        "მოდალური ზმნა sollen (რჩევა და ექიმის დავალება)"
    ],
    "grammar_sections": [
        {
            "id": "9.1",
            "title": "9.1 ბრძანებითი კილო (Der Imperativ: du, ihr, Sie)",
            "content_ka": """ბრძანებითი კილო გამოიყენება თხოვნის, რჩევისა და ბრძანებისას:
1. **du-ფორმა (შენობით):**
   ზმნის du-ფორმას აკლდება **du** და დაბოლოება **-st**!
   - *du machst* -> **Mach!** (გააკეთე!)
   - *du trinkst* -> **Trink!** (დალიე!)
   - *du sprichst* -> **Sprich!** (e->i მონაცვლეობა რჩება, მაგრამ a->ä უმლაუტი ქრება: *du fährst* -> **Fahr!**).

2. **ihr-ფორმა (თქვენობით მეგობრებთან/ბავშვებთან):**
   ზუსტად ზმნის ihr-ფორმაა ნაცვალსახელის გარეშე:
   - *ihr macht* -> **Macht!** (გააკეთეთ!)
   - *ihr kommt* -> **Kommt!** (მოდით!)

3. **Sie-ფორმა (თავაზიანი ფორმა):**
   ინფინიტივს ემატება Sie (შებრუნებული თანმიმდევრობით):
   - **Trinken Sie bitte viel Tee!** (დალიეთ ბევრი ჩაი, გეთაყვა!).
   - გამონაკლისი: sein -> **Seien Sie bitte ruhig!**"""
        }
    ],
    "dialogues": [
        {
            "id": "d9_1",
            "title": "დიალოგი: ექიმის კაბინეტში",
            "context": "პაციენტი და ექიმი გასინჯვის დროს.",
            "lines": [
                {"speaker": "Arzt", "text_de": "Guten Tag! Was fehlt Ihnen denn?", "text_ka": "გამარჯობა! რა გაწუხებთ?"},
                {"speaker": "Patient", "text_de": "Mein Kopf tut sehr weh und ich habe Halsschmerzen und Fieber.", "text_ka": "თავი ძალიან მტკივა, ყელის ტკივილი და სიცხე მაქვს."},
                {"speaker": "Arzt", "text_de": "Öffnen Sie bitte den Mund! Ja, der Hals ist rot. Sie haben eine Grippe.", "text_ka": "გააღეთ პირი, გეთაყვა! დიახ, ყელი გაწითლებულია. გრიპი გაქვთ."},
                {"speaker": "Patient", "text_de": "Was soll ich tun, Herr Doktor?", "text_ka": "რა უნდა გავაკეთო, ექიმო?"},
                {"speaker": "Arzt", "text_de": "Bleiben Sie drei Tage im Bett und nehmen Sie diese Tabletten dreimal täglich!", "text_ka": "დარჩით სამი დღე ლოგინში და მიიღეთ ეს აბები დღეში სამჯერ!"}
            ]
        }
    ],
    "cultural_notes": {
        "title": "💡 კულტურული ცნობარი: ჯანდაცვის სისტემა და დაზღვევა (Krankenkasse)",
        "content_ka": "გერმანიაში სამედიცინო დაზღვევა სავალდებულოა ყველასთვის. ექიმთან ვიზიტისთვის საჭიროა წინასწარ ტერმინის (Termin) ჩანიშვნა და სადაზღვევო ბარათის (Gesundheitskarte) წარდგენა."
    },
    "exercises": {
        "multiple_choice": [
            {
                "id": "mc9_1",
                "question": "რომელია ზმნა 'trinken'-ის ბრძანებითი ფორმა შენობით (du)?",
                "options": ["Trinkst!", "Trink!", "Trinken!", "Trinke du!"],
                "answer": 1,
                "explanation": "du-ფორმის ბრძანებითში აკლდება -st და ნაცვალსახელი: Trink!"
            },
            {
                "id": "mc9_2",
                "question": "შეავსეთ: 'Meine Augen _______ weh.' (თვალები მტკივა)",
                "options": ["tut", "tun", "hat", "haben"],
                "answer": 1,
                "explanation": "Augen მრავლობითია, ამიტომ tun weh."
            }
        ],
        "fill_in_blank": [
            {
                "id": "fib9_1",
                "sentence_before": "Der Arzt sagt, ich ",
                "sentence_after": " viel schlafen. (sollen)",
                "correct_answer": "soll",
                "hint": "ich პირთან არის soll"
            }
        ],
        "listening": [
            {
                "id": "lis9_1",
                "audio_text": "Bleiben Sie bitte im Bett!",
                "question": "რას ავალებს ექიმი პაციენტს?",
                "options": ["გადით სასეირნოდ", "დარჩით ლოგინში", "მიიღეთ ცივი შხაპი", "წადით სამსახურში"],
                "answer": 1
            }
        ]
    }
}

DL10 = {
    "id": 10,
    "title_de": "Lektion 10: Im Urlaub & Das Perfekt",
    "title_ka": "გაკვეთილი 10: შვებულება და წარსული დრო (Das Perfekt)",
    "icon": "🏖️",
    "level": "A1.2",
    "objectives_ka": [
        "A1 დონის გვირგვინი: სასაუბრო წარსული დროის (Das Perfekt) სრული დაუფლება",
        "დამხმარე ზმნების არჩევა: haben vs. sein (გადაადგილება და მდგომარეობის შეცვლა)",
        "Partizip II-ის წარმოება: რეგულარული (ge...t), არარეგულარული (ge...en) და განცალკევებადი ზმნები",
        "მოგზაურობაზე, შვებულებასა და წარსულ ამბებზე თავისუფლად საუბარი"
    ],
    "grammar_sections": [
        {
            "id": "10.1",
            "title": "10.1 წარსული დროის (Perfekt) სტრუქტურა და Satzklammer",
            "content_ka": """გერმანულ სასაუბრო ენაში წარსული მოვლენების გადმოსაცემად ვიყენებთ **Perfekt**-ს.
მისი ფორმულაა:
**haben / sein** (უღლებული მე-2 ადგილზე) + ... + **Partizip II** (წინადადების სულ ბოლოს!).

• *Ich **habe** gestern ein Buch **gekauft**.* (გუშინ წიგნი ვიყიდე).
• *Wir **sind** nach Berlin **gefahren**.* (ბერლინში გავემგზავრეთ)."""
        },
        {
            "id": "10.2",
            "title": "10.2 როდის sein და როდის haben? (საკვანძო წესი)",
            "content_ka": """• **sein გამოიყენება მხოლოდ მაშინ, როდესაც ზმნა გამოხატავს:**
  1. **გადაადგილებას სივრცეში (A წერტილიდან B-ში):** *gehen, fahren, fliegen, kommen, reisen*.
  2. **მდგომარეობის შეცვლას:** *aufstehen, einschlafen*.
  3. **გამონაკლისები:** *bleiben* (დარჩენა -> ist geblieben), *sein* (ყოფნა -> ist gewesen).

• **haben გამოიყენება ყველა სხვა დანარჩენ შემთხვევაში (ზმნების 90%):**
  - *Ich habe gemacht, gearbeitet, gegessen, getrunken, gelernt, gelesen, geschlafen*."""
        },
        {
            "id": "10.3",
            "title": "10.3 Partizip II-ის წარმოება",
            "content_ka": """1. **სუსტი (რეგულარული) ზმნები:** **ge- + Stamm + -t**
   - *machen -> gemacht*, *kaufen -> gekauft*, *hören -> gehört*.
2. **ძლიერი (არარეგულარული) ზმნები:** **ge- + (შეცვლილი) Stamm + -en**
   - *trinken -> getrunken*, *essen -> gegessen*, *schreiben -> geschrieben*.
3. **განცალკევებადი ზმნები:** **ge-** ჯდება წინსართსა და ფუძეს შორის:
   - *aufstehen -> auf**ge**standen*, *einkaufen -> ein**ge**kauft*.
4. **ზმნები -ieren დაბოლოებით:** **არ იღებენ ge-ს!**
   - *studieren -> studiert*, *fotografieren -> fotografiert*."""
        }
    ],
    "dialogues": [
        {
            "id": "d10_1",
            "title": "დიალოგი: შვებულების ამბები",
            "context": "სოფი და გიორგი საუბრობენ არდადეგებზე.",
            "lines": [
                {"speaker": "Sophie", "text_de": "Hallo Giorgi! Wie war dein Urlaub?", "text_ka": "გამარჯობა გიორგი! როგორი იყო შენი შვებულება?"},
                {"speaker": "Giorgi", "text_de": "Es war fantastisch! Ich bin nach Österreich geflogen und habe Wien besichtigt.", "text_ka": "ფანტასტიკური იყო! ავსტრიაში გავფრინდი და ვენა დავათვალიერე."},
                {"speaker": "Sophie", "text_de": "Toll! Was hast du dort gegessen?", "text_ka": "მაგარია! რა ჭამე იქ?"},
                {"speaker": "Giorgi", "text_de": "Ich habe Sachertorte gegessen und echten Wiener Kaffee getrunken.", "text_ka": "ზახერტორტი ვჭამე და ნამდვილი ვენური ყავა დავლიე."},
                {"speaker": "Sophie", "text_de": "Hast du auch Souvenirs gekauft?", "text_ka": "სუვენირებიც იყიდე?"},
                {"speaker": "Giorgi", "text_de": "Ja, ich habe Schokolade für meine Familie in Georgien mitgebracht.", "text_ka": "კი, შოკოლადი ჩამოვუტანე ჩემს ოჯახს საქართველოში."}
            ]
        }
    ],
    "cultural_notes": {
        "title": "💡 კულტურული ცნობარი: Urlaubsweltmeister (მოგზაურობის ჩემპიონები)",
        "content_ka": "გერმანელებს ხშირად უწოდებენ მოგზაურობის მსოფლიო ჩემპიონებს (Reiseweltmeister). საშუალო სტატისტიკური გერმანელი წელიწადში 30 დღე შვებულებით სარგებლობს."
    },
    "exercises": {
        "multiple_choice": [
            {
                "id": "mc10_1",
                "question": "რომელ დამხმარე ზმნას იღებს 'fahren' (მგზავრობა) პერფექტში?",
                "options": ["haben (hat gefahren)", "sein (ist gefahren)", "werden", "bleiben"],
                "answer": 1,
                "explanation": "fahren გამოხატავს გადაადგილებას სივრცეში, ამიტომ დამხმარე ზმნაა sein."
            },
            {
                "id": "mc10_2",
                "question": "რომელია ზმნა 'machen'-ის Partizip II?",
                "options": ["gemacht", "gemachen", "machte", "gemachten"],
                "answer": 0,
                "explanation": "რეგულარული ზმნა: ge- + mach + -t = gemacht."
            },
            {
                "id": "mc10_3",
                "question": "შეავსეთ: 'Ich habe gestern ein Buch _______.' (kaufen)",
                "options": ["gekauft", "gekaufen", "kaufte", "kaufen"],
                "answer": 0,
                "explanation": "kaufen -> gekauft (Partizip II წინადადების ბოლოში)."
            }
        ],
        "fill_in_blank": [
            {
                "id": "fib10_1",
                "sentence_before": "Wir ",
                "sentence_after": " nach Berlin geflogen. (sein/haben)",
                "correct_answer": "sind",
                "hint": "fliegen მოითხოვს sein-ს: wir sind geflogen"
            }
        ],
        "listening": [
            {
                "id": "lis10_1",
                "audio_text": "Gestern habe ich meine Freunde in Tiflis besucht.",
                "question": "რა გააკეთა მოსაუბრემ გუშინ?",
                "options": [
                    "გუშინ მეგობრები მოინახულა თბილისში",
                    "გუშინ წიგნი იყიდა",
                    "გუშინ ბერლინში გაფრინდა",
                    "გუშინ იმუშავა"
                ],
                "answer": 0
            }
        ]
    }
}

ALL_DEEP_LESSONS = [L1, DL2, DL3, DL4, DL5, DL6, DL7, DL8, DL9, DL10]

# Enrich exercises for all lessons with multi-mode deep exercises (Multiple Choice, Lückentext, Hörverstehen)
from update_deep_exercises import EXERCISES_DATA
for les in ALL_DEEP_LESSONS:
    lid = les.get("id")
    if lid in EXERCISES_DATA:
        les["exercises"] = EXERCISES_DATA[lid]


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
    "grammar_tables": grammar_tables
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
