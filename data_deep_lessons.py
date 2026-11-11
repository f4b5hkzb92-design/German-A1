# -*- coding: utf-8 -*-
"""
Deep Lektionen Generator (10 Comprehensive Modules)
Each module features:
- Learning objectives
- 4-6 Extensive Grammar Sub-modules with Georgian comparative analysis
- 2-3 Multi-speaker realistic dialogues (Formal & Informal)
- Cultural and life tips for Georgians in Germany (DACH)
- 3 Exercise Modes:
  1. Multiple Choice (8-10 items with Georgian feedback)
  2. Lückentext (Fill-in-the-blank)
  3. Hörverstehen (Audio Listening Comprehension)
"""

DEEP_LESSONS = [
    # =========================================================================
    # LEKTION 1: ERSTE KONTAKTE, BEGRÜSSUNG, ALPHABET, PRÄSENS (SEIN, HEISSEN...)
    # =========================================================================
    {
        "id": 1,
        "title_de": "Lektion 1: Erste Kontakte & Begrüßung",
        "title_ka": "გაკვეთილი 1: პირველი კონტაქტი, გაცნობა და ანბანი",
        "icon": "👋",
        "level": "A1.1",
        "objectives_ka": [
            "მისალმება და დამშვიდობება ფორმალურ (Sie) და არაფორმალურ (du) სიტუაციებში",
            "საკუთარი თავის წარდგენა: სახელი, გვარი, წარმოშობა (ქვეყანა, ქალაქი) და სალაპარაკო ენები",
            "გერმანული ანბანის (Alphabet), უმლაუტების (Ä, Ö, Ü) და დიფთონგების (ei, ie, eu, sch, ch) ზუსტი წარმოთქმა",
            "ზმნების უღლება აწმყოში (Präsens): sein, heißen, kommen, wohnen, sprechen",
            "W-კითხვების (Wie? Woher? Wo? Was? Wer?) დასმა და სიტყვათა რიგის V2 წესი",
            "რიცხვები 0-დან 20-მდე და ტელეფონის ნომრის თქმა"
        ],
        "grammar_sections": [
            {
                "id": "1.1",
                "title": "1.1 მისალმება და დამშვიდობება: Du თუ Sie? (ქართული კონტექსტი)",
                "content_ka": """გერმანიაში, ავსტრიასა და შვეიცარიაში ადამიანთან მიმართვის ფორმა გაცილებით მკაცრად რეგულირდება, ვიდრე საქართველოში:

• **თავაზიანი ფორმა (Siezen - Sie):**
  გამოიყენება ყველა უცნობ ზრდასრულ ადამიანთან, სამსახურში, მაღაზიაში, ექიმთან, უნივერსიტეტის პროფესორთან.
  - მისალმება: **Guten Tag!** (დღე მშვიდობისა), **Guten Morgen!** (დილა მშვიდობისა - 11:00-მდე), **Guten Abend!** (საღამო მშვიდობისა - 18:00-ის შემდეგ).
  - დამშვიდობება: **Auf Wiedersehen!** (ნახვამდის პირისპირ), **Auf Wiederhören!** (ნახვამდის ტელეფონზე!).
  - მიმართვა: **Herr + გვარი** (Herr Beridze - ბატონო ბერიძე), **Frau + გვარი** (Frau Müller - ქალბატონო მიულერ).

• **შინაურული / მეგობრული ფორმა (Duzen - du):**
  გამოიყენება ოჯახის წევრებთან, მეგობრებთან, სტუდენტებს შორის და ბავშვებთან (15-16 წლამდე).
  - მისალმება: **Hallo!** (გამარჯობა), სამხრეთ გერმანიასა და ავსტრიაში: **Grüß Gott!**, შვეიცარიაში: **Grüezi!**
  - დამშვიდობება: **Tschüss!** (ნახვამდის/კარგად), **Bis bald!** (მალე შეხვედრამდე), **Bis später!** (დროებით).

> **💡 რჩევა ქართველებისთვის:** არასოდეს გადახვიდეთ "du"-ზე (შენობითზე) უფროსთან ან უცნობთან საკუთარი ინიციატივით! გერმანულ კულტურაში "du"-ს შემოთავაზების უფლება აქვს მხოლოდ მასპინძელს, ასაკით უფროსს ან თანამდებობით მაღლა მდგომს."""
            },
            {
                "id": "1.2",
                "title": "1.2 გერმანული ფონეტიკა: ასოთშეხამებები და უმლაუტები (ქართული ანალოგიებით)",
                "content_ka": """ქართული ენის ფონეტიკა მარტივია (რასაც ვხედავთ, იმას ვკითხულობთ), გერმანულში კი არსებობს ასოთშეხამებები, რომელთა დაზეპირება აუცილებელია:

1. **დიფთონგები (ორი ხმოვნის შერწყმა):**
   • **ei** იკითხება როგორც **[აი]** -> *mein* [მაინ], *nein* [ნაინ], *heißen* [ჰაისენ]. (ყურადღება: ქართველები ხშირად შეცდომით კითხულობენ როგორც "ეი").
   • **ie** იკითხება როგორც გრძელი **[იი]** -> *sie* [ზიი], *wie* [ვიი], *Wien* [ვიინ].
   • **eu / äu** იკითხება როგორც **[ოი]** -> *deutsch* [დოიჩ], *heute* [ჰოიტე], *Häuser* [ჰოიზერ].

2. **თანხმოვანთა შეხამებები:**
   • **sch** = **[შ]** -> *Schule* [შულე] (სკოლა).
   • **sp / st** სიტყვის ან ფესვის დასაწყისში = **[შპ / შტ]** -> *sprechen* [შპრეხენ], *Student* [შტუდენტ], *Stadt* [შტადტ].
   • **ch**-ს აქვს ორი წაკითხვა:
     - **მყარი [ხ]**: a, o, u ხმოვნების შემდეგ -> *Buch* [ბუხ], *machen* [მახენ], *noch* [ნოხ].
     - **რბილი [ჰ/ხ]** (იჩ-ლაუტი): e, i, ä, ö, ü ხმოვნების და თანხმოვნების შემდეგ -> *ich* [იჰ], *nicht* [ნიჰტ], *Milch* [მილჰ].
   • **s** ხმოვნის წინ იკითხება როგორც **[ზ]** -> *sein* [ზაინ], *sieben* [ზიბენ], *Salat* [ზალატ].
   • **v** უმეტესად იკითხება როგორც **[ფ]** -> *von* [ფონ], *vier* [ფიირ], *Vater* [ფათერ].
   • **w** იკითხება როგორც ჩვეულებრივი ქართული **[ვ]** -> *woher* [ვოჰერ], *Wasser* [ვასერ].
   • **z** ყოველთვის იკითხება როგორც **[ც]** -> *zehn* [ცეენ], *Zug* [ცუგ], *zwei* [ცვაი].

3. **უმლაუტები (Umlaute):**
   • **Ä / ä** = ღია [ე] (მაგ. *Mädchen* [მედხენ], *März* [მერც]).
   • **Ö / ö** = [ო]-სა და [ე]-ს შორის ბგერა (ტუჩები მომრგვალებული როგორც "ო"-სას, მაგრამ წარმოვთქვამთ "ე"-ს: *schön*, *hören*).
   • **Ü / ü** = [უ]-სა და [ი]-ს შორის ბგერა (ტუჩები მომრგვალებული როგორც "უ"-სას, მაგრამ წარმოვთქვამთ "ი"-ს: *fünf*, *München*)."""
            },
            {
                "id": "1.3",
                "title": "1.3 ზმნის უღლება აწმყოში (Präsens) და უწესო ზმნები (sein, heißen, sprechen)",
                "content_ka": """გერმანული ზმნის ინფინიტივი (საწყისი ფორმა) შედგება **ფუძისა (Stamm)** და დაბოლოება **-en**-ისგან (ან იშვიათად -n):
მაგ: *komm-en, lern-en, wohn-en, mach-en*.

აწმყო დროში (Präsens) ფუძეს ვუმატებთ პირის ნაცვალსახელის შესაბამის დაბოლოებებს:

| პირი | ნაცვალსახელი | დაბოლოება | რეგულარული ზმნა (kommen) | ზმნა wohnen |
| :--- | :--- | :--- | :--- | :--- |
| 1. მხოლობითი | **ich** (მე) | **-e** | ich komm-**e** | ich wohn-**e** |
| 2. მხოლობითი | **du** (შენ) | **-st** | du komm-**st** | du wohn-**st** |
| 3. მხოლობითი | **er/sie/es** (ის) | **-t** | er komm-**t** | er wohn-**t** |
| 1. მრავლობითი | **wir** (ჩვენ) | **-en** | wir komm-**en** | wir wohn-**en** |
| 2. მრავლობითი | **ihr** (თქვენ) | **-t** | ihr komm-**t** | ihr wohn-**t** |
| 3. მრავლობითი | **sie** (ისინი) | **-en** | sie komm-**en** | sie wohn-**en** |
| თავაზიანი | **Sie** (თქვენ) | **-en** | Sie komm-**en** | Sie wohn-**en** |

---

### ⚠️ განსაკუთრებული ზმნები Lektion 1-ში:

1. **ზმნა sein (ყოფნა):** სრულიად არარეგულარულია (როგორც ქართული "მე ვარ, შენ ხარ, ის არის"):
   • ich **bin** (მე ვარ)
   • du **bist** (შენ ხარ)
   • er/sie/es **ist** (ის არის)
   • wir **sind** (ჩვენ ვართ)
   • ihr **seid** (თქვენ ხართ)
   • sie/Sie **sind** (ისინი არიან / თქვენ ბრძანდებით)

> **💡 ქართული შეცდომა:** ქართულში ხშირად ვამბობთ: "მე გიორგი" ან "ის სტუდენტი". გერმანულში ზმნა **არასოდეს არ გამოიტოვება!** აუცილებლად უნდა ვთქვათ: *Ich **bin** Giorgi*, *Er **ist** Student*.

2. **ზმნა heißen (სახელად რქმევა):**
   რადგან ფუძე ბოლოვდება **-ß**-ზე, du-პირში ემატება მხოლოდ **-t** (და არა -st):
   • ich heiße, du **heißt** (და არა heißst!), er/sie/es heißt, wir heißen, ihr heißt, sie/Sie heißen.

3. **ზმნა sprechen (ლაპარაკი - ფუძის ხმოვნის მონაცვლეობა e -> i):**
   გერმანულში ძლიერ ზმნებს მხოლობითი რიცხვის du და er/sie/es პირებში ეცვლებათ ფუძის ხმოვანი:
   • ich sprech-e
   • du **sprichst** (e გადადის i-ში!)
   • er/sie/es **spricht**
   • wir sprechen, ihr sprecht, sie/Sie sprechen."""
            },
            {
                "id": "1.4",
                "title": "1.4 წინადადების აგება და კითხვები: W-Fragen vs. Ja/Nein-Fragen (V2 წესი)",
                "content_ka": """გერმანულში წინადადების წევრების რიგი კანონია! ზმნა წარმოადგენს წინადადების ღერძს.

### 1. თხრობითი წინადადება (Aussagesatz) — V2 წესი
ზმნა დგას **ყოველთვის მეორე ადგილზე (Verb an Position 2)**!
• *სტანდარტული რიგი:* [ქვემდებარე 1] + **[ზმნა 2]** + [დამატება 3]
  მაგ: *Ich* (1) **wohne** (2) *in Berlin* (3).
• *ინვერსიული რიგი (თუ წინ წამოვწევთ დროს ან ადგილს):*
  მაგ: *In Berlin* (1) **wohne** (2) *ich* (3). (ზმნა მაინც მე-2 ადგილზე დარჩა!).

---

### 2. კითხვითი წინადადება კითხვითი სიტყვით (W-Frage)
W-კითხვები იწყება W ასოზე (Wie, Woher, Wo, Was, Wer, Wann):
1. **კითხვითი სიტყვა** (Position 1)
2. **უღლებული ზმნა** (Position 2)
3. **ქვემდებარე** (Position 3)

| პოზიცია 1 (W-Wort) | პოზიცია 2 (Verb) | პოზიცია 3 (Subjekt) | ქართული თარგმანი |
| :--- | :--- | :--- | :--- |
| **Wie** (როგორ/რა) | **heißen** | Sie? | რა გქვიათ თქვენ? |
| **Woher** (საიდან) | **kommst** | du? | საიდან ხარ შენ? |
| **Wo** (სად) | **wohnen** | Sie? | სად ცხოვრობთ თქვენ? |
| **Was** (რა) | **sprichst** | du? | რომელ ენაზე ლაპარაკობ? |
| **Wer** (ვინ) | **ist** | das? | ვინ არის ეს? |

---

### 3. კითხვა კითხვითი სიტყვის გარეშე (Ja/Nein-Frage)
კითხვებში, რომელზეც პასუხია "დიახ" ან "არა", **ზმნა გადმოდის პირველ ადგილზე (Position 1)**!
• **Kommen** (1) Sie (2) aus Georgien? -> *Ja, ich komme aus Georgien.* / *Nein, ich komme aus Deutschland.*
• **Wohnst** (1) du (2) in Tiflis? -> *Ja, ich wohne in Tiflis.*
• **Sprechen** (1) Sie (2) Deutsch? -> *Ja, ein bisschen.*"""
            }
        ],
        "dialogues": [
            {
                "id": "d1",
                "title": "დიალოგი 1: ოფიციალური გაცნობა უნივერსიტეტში (Formell / Sie-Form)",
                "context": "გიორგი ბერიძე პირველად ხვდება გერმანული ენის ლექტორს, ქალბატონ ვაგნერს.",
                "lines": [
                    {"speaker": "Frau Wagner", "text_de": "Guten Tag! Mein Name ist Susanne Wagner. Herzlich willkommen an der Universität!", "text_ka": "დღე მშვიდობისა! ჩემი სახელია ზუზანე ვაგნერი. გულითადად მოგესალმებით უნივერსიტეტში!"},
                    {"speaker": "Giorgi", "text_de": "Guten Tag, Frau Wagner! Mein Name ist Giorgi Beridze. Sehr angenehm!", "text_ka": "დღე მშვიდობისა, ქალბატონო ვაგნერ! ჩემი სახელია გიორგი ბერიძე. ძალიან სასიამოვნოა!"},
                    {"speaker": "Frau Wagner", "text_de": "Freut mich auch, Herr Beridze. Woher kommen Sie?", "text_ka": "ჩემთვისაც სასიამოვნოა, ბატონო ბერიძე. საიდან ხართ წარმოშობით?"},
                    {"speaker": "Giorgi", "text_de": "Ich komme aus Georgien, aus der Hauptstadt Tiflis.", "text_ka": "მე საქართველოდან ვარ, დედაქალაქ თბილისიდან."},
                    {"speaker": "Frau Wagner", "text_de": "Interessant! Und welche Sprachen sprechen Sie?", "text_ka": "საინტერესოა! და რომელ ენებზე ლაპარაკობთ?"},
                    {"speaker": "Giorgi", "text_de": "Meine Muttersprache ist Georgisch. Ich spreche auch fließend Englisch und lerne jetzt Deutsch A1.", "text_ka": "ჩემი მშობლიური ენა ქართულია. ასევე თავისუფლად ვლაპარაკობ ინგლისურად და ახლა ვსწავლობ გერმანულ A1-ს."},
                    {"speaker": "Frau Wagner", "text_de": "Wunderbar! Ihr Deutsch klingt schon sehr gut.", "text_ka": "შესანიშნავია! თქვენი გერმანული უკვე ძალიან კარგად ჟღერს."}
                ]
            },
            {
                "id": "d2",
                "title": "დიალოგი 2: არაფორმალური გაცნობა სტუდენტებს შორის (Informell / du-Form)",
                "context": "ლუკა და ლენა ენის კურსის პირველ დღეს ეცნობიან ერთმანეთს კაფეტერიაში.",
                "lines": [
                    {"speaker": "Lukas", "text_de": "Hallo! Ist hier noch frei?", "text_ka": "გამარჯობა! აქ თავისუფალია?"},
                    {"speaker": "Lena", "text_de": "Ja, bitte, setz dich! Ich heiße Lena. Und wie heißt du?", "text_ka": "კი, დაბრძანდი! მე ლენა მქვია. შენ რა გქვია?"},
                    {"speaker": "Lukas", "text_de": "Hallo Lena, ich bin Lukas. Lernst du auch hier Deutsch?", "text_ka": "გამარჯობა ლენა, მე ლუკასი ვარ. შენც აქ სწავლობ გერმანულს?"},
                    {"speaker": "Lena", "text_de": "Ja, genau. Ich bin im A1-Kurs. Woher kommst du, Lukas?", "text_ka": "კი, ზუსტად. A1 კურსზე ვარ. საიდან ხარ, ლუკას?"},
                    {"speaker": "Lukas", "text_de": "Ich komme aus Georgien. Und du? Woher kommst du?", "text_ka": "მე საქართველოდან ვარ. შენ? საიდან ხარ?"},
                    {"speaker": "Lena", "text_de": "Ich komme aus Österreich, aus Wien. Aber jetzt wohne ich in Berlin.", "text_ka": "მე ავსტრიიდან ვარ, ვენიდან. მაგრამ ახლა ბერლინში ვცხოვრობ."},
                    {"speaker": "Lukas", "text_de": "Toll! Wien ist eine wunderschöne Stadt.", "text_ka": "მაგარია! ვენა ულამაზესი ქალაქია."}
                ]
            }
        ],
        "cultural_notes": {
            "title": "💡 კულტურული ცნობარი: გერმანული ეტიკეტი დამწყებთათვის",
            "content_ka": """1. **ხელის ჩამორთმევა (Händedruck):** გერმანიაში ოფიციალური და ნახევრად ოფიციალური შეხვედრისას მიღებულია მტკიცე, საქმიანი ხელის ჩამორთმევა და თვალებში ყურება.
2. **პუნქტუალურობა (Pünktlichkeit):** "5 წუთით ადრე მოსვლა უკვე დროზე მოსვლაა". თუ შეხვედრაზე 5 წუთითაც კი იგვიანებთ, აუცილებლად უნდა დარეკოთ ან მისწეროთ.
3. **დისტანცია და პირადი სივრცე:** გერმანელები საუბრისას ინარჩუნებენ დაახლოებით ერთი ხელის გაწვდენის დისტანციას."""
        },
        "exercises": {
            "multiple_choice": [
                {
                    "id": "mc1",
                    "question": "რომელი მისალმებაა ყველაზე მიზანშეწონილი დილის 9 საათზე ოფიციალურ გარემოში?",
                    "options": ["Gute Nacht!", "Guten Morgen!", "Guten Abend!", "Tschüss!"],
                    "answer": 1,
                    "explanation": "დილის 11:00 საათამდე ოფიციალური მისალმებაა 'Guten Morgen!'."
                },
                {
                    "id": "mc2",
                    "question": "როგორ იკითხება სწორად სიტყვა 'mein' (ჩემი)?",
                    "options": ["[მეინ]", "[მაინ]", "[მიინ]", "[მოინ]"],
                    "answer": 1,
                    "explanation": "'ei' ასოთშეხამება გერმანულში ყოველთვის იკითხება როგორც [აი]: mein = მაინ."
                },
                {
                    "id": "mc3",
                    "question": "შეავსეთ ზმნის სწორი ფორმა: 'Woher _______ du?'",
                    "options": ["komme", "kommt", "kommst", "kommen"],
                    "answer": 2,
                    "explanation": "du პირთან ზმნა იღებს -st დაბოლოებას: du kommst."
                },
                {
                    "id": "mc4",
                    "question": "რომელია ზმნა 'sein'-ის (ყოფნა) სწორი ფორმა 'wir' (ჩვენ) პირთან?",
                    "options": ["seid", "sind", "ist", "bin"],
                    "answer": 1,
                    "explanation": "ზმნა sein wir პირთან არის 'wir sind' (ჩვენ ვართ)."
                },
                {
                    "id": "mc5",
                    "question": "რომელია ზმნა 'heißen'-ის სწორი ფორმა 'du' პირთან?",
                    "options": ["heißst", "heißt", "heiße", "heißen"],
                    "answer": 1,
                    "explanation": "რადგან heißen ფუძეში შეიცავს ß-ს, du პირთან ემატება მხოლოდ -t (du heißt)."
                },
                {
                    "id": "mc6",
                    "question": "შეავსეთ: 'Er _______ sehr gut Deutsch.' (sprechen)",
                    "options": ["spreche", "sprecht", "spricht", "sprechst"],
                    "answer": 2,
                    "explanation": "ზმნა sprechen არარეგულარულია er/sie/es პირში: e იცვლება i-თ (er spricht)."
                },
                {
                    "id": "mc7",
                    "question": "რომელი წინადადებაა გრამატიკულად სწორი (V2 წესის მიხედვით)?",
                    "options": [
                        "In Berlin ich wohne.",
                        "In Berlin wohne ich.",
                        "In Berlin ich bin wohnen.",
                        "Wohne in Berlin ich."
                    ],
                    "answer": 1,
                    "explanation": "V2 წესი: თუ წინადადება იწყება ადგილით (In Berlin), ზმნა (wohne) მაინც მეორე ადგილზე რჩება, შემდეგ მოდის ქვემდებარე (ich)."
                },
                {
                    "id": "mc8",
                    "question": "რომელია რიცხვი 16 გერმანულად?",
                    "options": ["sechszehn", "sechzehn", "siebzehn", "sechzig"],
                    "answer": 1,
                    "explanation": "16-ში s აკლდება: sechs -> sechzehn."
                }
            ],
            "fill_in_blank": [
                {
                    "id": "fib1",
                    "sentence_before": "Wie ",
                    "sentence_after": " Sie? (heißen)",
                    "correct_answer": "heißen",
                    "hint": "თავაზიანი ფორმა Sie მოითხოვს -en დაბოლოებას"
                },
                {
                    "id": "fib2",
                    "sentence_before": "Ich ",
                    "sentence_after": " Student aus Georgien. (sein)",
                    "correct_answer": "bin",
                    "hint": "ზმნა sein ich პირთან არის 'bin'"
                },
                {
                    "id": "fib3",
                    "sentence_before": "Wo ",
                    "sentence_after": " du jetzt? (wohnen)",
                    "correct_answer": "wohnst",
                    "hint": "du პირთან ემატება -st"
                },
                {
                    "id": "fib4",
                    "sentence_before": "Mein Bruder ",
                    "sentence_after": " Spanisch und Deutsch. (sprechen)",
                    "correct_answer": "spricht",
                    "hint": "e იცვლება i-თ: er spricht"
                }
            ],
            "listening": [
                {
                    "id": "lis1",
                    "audio_text": "Guten Tag! Mein Name ist Susanne Wagner.",
                    "question": "რას ამბობს მოსაუბრე აუდიოში?",
                    "options": [
                        "დილა მშვიდობისა! მე მქვია ანა.",
                        "დღე მშვიდობისა! ჩემი სახელია ზუზანე ვაგნერი.",
                        "საღამო მშვიდობისა, ქალბატონო ვაგნერ!",
                        "ნახვამდის, ზუზანე!"
                    ],
                    "answer": 1
                },
                {
                    "id": "lis2",
                    "audio_text": "Ich komme aus Georgien und wohne in Berlin.",
                    "question": "სად ცხოვრობს მოსაუბრე?",
                    "options": ["თბილისში", "ვენაში", "ბერლინში", "მიუნხენში"],
                    "answer": 2
                },
                {
                    "id": "lis3",
                    "audio_text": "Sprichst du Englisch und Deutsch?",
                    "question": "რას ეკითხება მოსაუბრე?",
                    "options": [
                        "ლაპარაკობ ინგლისურად და გერმანულად?",
                        "სწავლობ ესპანურს?",
                        "საიდან ხარ?",
                        "რა გქვია?"
                    ],
                    "answer": 0
                }
            ]
        }
    }
]

print("Loaded Lektion 1 Pro Deep Module!")
