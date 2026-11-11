# -*- coding: utf-8 -*-
"""
Four Core CEFR A1 Language Labs Database (Hören, Lesen, Schreiben, Sprechen).
Pedagogically authentic, original materials aligned with Schritte Neu & Menschen.
"""

LANGUAGE_LABS_DATA = {
    "hoeren": [
        {
            "id": "h_lab_1",
            "title": "ვაგზლის განცხადება (Bahnhofsdurchsage)",
            "category": "სატრანსპორტო შეტყობინება",
            "audio_text": "Achtung an Gleis vier: Der Intercity-Express nach München über Nürnberg fährt heute mit circa zehn Minuten Verspätung ab. Bitte beachten Sie die Lautsprecherdurchsagen.",
            "question": "რომელ მატარებელს აქვს დაგვიანება და სად მიემგზავრება?",
            "options": [
                "მიუნხენისკენ მიმავალ ICE-ს მე-4 ლიანდაგზე (დაახლოებით 10 წთ)",
                "ჰამბურგისკენ მიმავალ რეგიონულ მატარებელს მე-2 ლიანდაგზე",
                "ბერლინისკენ მიმავალ მატარებელს, რომელიც გაუქმდა",
                "ფრანკფურტისკენ მიმავალ მატარებელს 30 წუთიანი დაგვიანებით"
            ],
            "answer": 0,
            "transcript_ka": "ყურადღება მე-4 ლიანდაგზე: სამგზავრო ექსპრესი მიუნხენისკენ ნიურნბერგის გავლით დღეს დაახლოებით ათი წუთის დაგვიანებით გავა. გთხოვთ ყურადღება მიაქციოთ ხმოვან განცხადებებს."
        },
        {
            "id": "h_lab_2",
            "title": "სატელეფონო ავტომოპასუხე: ექიმის პრაქტიკა (Arztpraxis)",
            "category": "სატელეფონო შეტყობინება",
            "audio_text": "Guten Tag, hier ist die Praxis Dr. Becker. Unsere Sprechzeiten sind von Montag bis Donnerstag von acht bis zwölf Uhr. In dringenden Notfällen rufen Sie bitte die Nummer 116 117 an.",
            "question": "რომელ საათებშია ექიმის პრაქტიკა ღია პაციენტებისთვის?",
            "options": [
                "ორშაბათიდან ხუთშაბათამდე, 08:00-დან 12:00 საათამდე",
                "ორშაბათიდან პარასკევამდე, 09:00-დან 18:00 საათამდე",
                "მხოლოდ შაბათ-კვირას",
                "ყოველდღე 24 საათის განმავლობაში"
            ],
            "answer": 0,
            "transcript_ka": "დღე მშვიდობისა, აქ არის დოქტორ ბეკერის პრაქტიკა. ჩვენი მიღების საათებია ორშაბათიდან ხუთშაბათამდე რვიდან თორმეტ საათამდე. გადაუდებელ შემთხვევებში დარეკეთ ნომერზე 116 117."
        },
        {
            "id": "h_lab_3",
            "title": "სუპერმარკეტის შეთავაზება (Supermarkt-Angebot)",
            "category": "საყიდლები და ფასები",
            "audio_text": "Liebe Kundinnen und Kunden! Heute frisch eingetroffen: Bio-Äpfel aus der Region, das Kilo für nur ein Euro neunundneunzig. Greifen Sie zu!",
            "question": "რა პროდუქტია დღეს განსაკუთრებულ ფასად და რა ღირს?",
            "options": [
                "ბიო-ვაშლი — 1,99 € / კილოგრამი",
                "ახალი ბანანი — 0,99 € / კილოგრამი",
                "გერმანული ყველი — 3,50 € / ცალი",
                "ახალი პური — 2,50 € / ცალი"
            ],
            "answer": 0,
            "transcript_ka": "ძვირფასო მომხმარებლებო! დღეს ახალი მიღებულია: რეგიონული ბიო-ვაშლი, კილოგრამი მხოლოდ ერთ ევროდ და ოთხმოცდაცხრამეტ ცენტად. ისარგებლეთ შეთავაზებით!"
        },
        {
            "id": "h_lab_4",
            "title": "სასტუმროს ადმინისტრატორი (Hotel-Rezeption)",
            "category": "სასტუმრო და მოგზაურობა",
            "audio_text": "Guten Abend! Ihr Zimmer ist die Nummer 304 im dritten Stock. Der Aufzug ist links. Das Frühstücksbüfett steht ab sieben Uhr im Erdgeschoss für Sie bereit.",
            "question": "სად მდებარეობს ოთახი და როდის იწყება საუზმე?",
            "options": [
                "ოთახი 304 მე-3 სართულზე, საუზმე იწყება 07:00 საათზე 1-ელ სართულზე",
                "ოთახი 204 მე-2 სართულზე, საუზმე იწყება 08:30 საათზე",
                "ოთახი 104 პირველ სართულზე, საუზმე არ შედის ფასში",
                "ოთახი 304 მე-4 სართულზე, საუზმე იწყება 09:00 საათზე"
            ],
            "answer": 0,
            "transcript_ka": "საღამო მშვიდობისა! თქვენი ოთახია N304 მესამე სართულზე. ლიფტი მარცხნივაა. შვედური საუზმე დილის შვიდი საათიდან პირველ სართულზე (Erdgeschoss) მზად იქნება თქვენთვის."
        }
    ],

    "lesen": [
        {
            "id": "l_lab_1",
            "title": "მეგობრის წერილი: დაბადების დღეზე დაპატიჟება",
            "category": "პირადი წერილი / E-Mail",
            "text_de": """Liebe Nino,

am nächsten Samstag feiere ich meinen Geburtstag! Die Party beginnt um 19 Uhr bei mir zu Hause in der Goethestraße 12.
Wir wollen grillen und Musik hören. Kannst du bitte einen Salat oder einen Kuchen mitbringen?
Gib mir bitte bis Donnerstag Bescheid, ob du kommen kannst.

Ich freue mich auf dich!
Liebe Grüße,
Sarah""",
            "text_ka_summary": "ზარას წერილი ნინოსადმი: დაბადების დღის წვეულება შაბათს, 19:00 საათზე, გოეთეს ქუჩაზე.",
            "questions": [
                {
                    "q": "როდის იწყება ზარას დაბადების დღის წვეულება?",
                    "options": ["შაბათს, 19:00 საათზე", "პარასკევს, 18:00 საათზე", "ხუთშაბათს, 20:00 საათზე", "კვირას დილით"],
                    "answer": 0,
                    "explanation": "'Die Party beginnt um 19 Uhr am nächsten Samstag'."
                },
                {
                    "q": "რა სთხოვა ზარამ ნინოს წვეულებისთვის?",
                    "options": [
                        "სალათის ან ნამცხვრის მოტანა",
                        "მუსიკალური დისკების მოტანა",
                        "ხორცის ყიდვა",
                        "არაფრის მოტანა არ არის საჭირო"
                    ],
                    "answer": 0,
                    "explanation": "'Kannst du bitte einen Salat oder einen Kuchen mitbringen?'"
                },
                {
                    "q": "როდემდე უნდა შეატყობინოს ნინომ პასუხი?",
                    "options": ["ხუთშაბათამდე (bis Donnerstag)", "შაბათამდე", "პარასკევ საღამომდე", "დაუყოვნებლივ"],
                    "answer": 0,
                    "explanation": "'Gib mir bitte bis Donnerstag Bescheid'."
                }
            ]
        },
        {
            "id": "l_lab_2",
            "title": "ენის სკოლის განცხადება (Aushang an der Sprachschule)",
            "category": "ოფიციალური განცხადება / აფიშა",
            "text_de": """WICHTIGE INFORMATION FÜR KURSTEILNEHMER!

Wegen Renovierungsarbeiten finden die Deutschkurse der Niveaustufe A1 ab Montag, den 15. November, nicht im Raum 102 statt.
Der neue Unterrichtsraum ist Raum 205 im zweiten Stock.
Die Unterrichtszeiten bleiben unverändert: Montag bis Donnerstag, jeweils von 9:00 bis 12:30 Uhr.

Das Schulsekretariat""",
            "text_ka_summary": "სკოლის ადმინისტრაციის განცხადება რემონტისა და აუდიტორიის შეცვლის შესახებ.",
            "questions": [
                {
                    "q": "რატომ იცვლება გაკვეთილების ჩატარების ადგილი?",
                    "options": [
                        "სარემონტო სამუშაოების გამო (Renovierungsarbeiten)",
                        "მასწავლებლის ავადმყოფობის გამო",
                        "სტუდენტების სიმრავლის გამო",
                        "სკოლის დაკეტვის გამო"
                    ],
                    "answer": 0,
                    "explanation": "'Wegen Renovierungsarbeiten...' - სარემონტო სამუშაოების გამო."
                },
                {
                    "q": "რომელ ოთახში ჩატარდება გაკვეთილები?",
                    "options": ["ოთახ 205-ში (მე-2 სართულზე)", "ოთახ 102-ში", "სარდაფში", "ბიბლიოთეკაში"],
                    "answer": 0,
                    "explanation": "'Der neue Unterrichtsraum ist Raum 205 im zweiten Stock'."
                },
                {
                    "q": "იცვლება თუ არა მეცადინეობის განრიგი და საათები?",
                    "options": [
                        "არა, საათები უცვლელია (09:00-12:30)",
                        "დიახ, საღამოს 18:00 საათზე გადადის",
                        "დიახ, მხოლოდ პარასკევს ჩატარდება",
                        "გაკვეთილები 2 კვირით გადაიდო"
                    ],
                    "answer": 0,
                    "explanation": "'Die Unterrichtszeiten bleiben unverändert' - დრო უცვლელი რჩება."
                }
            ]
        },
        {
            "id": "l_lab_3",
            "title": "რესტორნის მენიუ (Speisekarte im Restaurant)",
            "category": "მენიუ და ფასები",
            "text_de": """Gasthof 'Zur Linde' - Tagesempfehlungen:

• Tagessuppe: Frische Tomatensuppe mit Kräutern — 4,80 €
• Hauptgericht: Wiener Schnitzel vom Schwein mit Pommes frites und kleinem Salat — 13,50 €
• Vegetarisch: Käsespätzle mit Röstzwiebeln — 11,20 €
• Dessert: Apfelstrudel mit Vanillesoße — 4,90 €
• Getränke: Mineralwasser 0,5l — 2,90 € | Apfelschorle 0,4l — 3,20 €

Alle Preise verstehen sich inklusive Bedienung und Mehrwertsteuer.""",
            "text_ka_summary": "რესტორნის დღის მენიუ ფასებითა და კერძების შემადგენლობით.",
            "questions": [
                {
                    "q": "რა ღირს ვენური შნიცელი გარნირით?",
                    "options": ["13,50 €", "11,20 €", "4,80 €", "15,00 €"],
                    "answer": 0,
                    "explanation": "Wiener Schnitzel mit Pommes frites — 13,50 €."
                },
                {
                    "q": "რომელი კერძია ვეგეტარიანული მენიუში?",
                    "options": [
                        "Käsespätzle (ყველიანი შპეცლე ხახვით)",
                        "Wiener Schnitzel",
                        "Tomatensuppe mit Fleisch",
                        "Rostbratwurst"
                    ],
                    "answer": 0,
                    "explanation": "Käsespätzle მითითებულია როგორც 'Vegetarisch'."
                }
            ]
        }
    ],

    "schreiben": [
        {
            "id": "s_lab_1",
            "title": "ფორმა: სასტუმროს რეგისტრაციის ბარათი (Hotel-Anmeldeformular)",
            "type": "form",
            "instructions_ka": "შეავსეთ სასტუმროს სარეგისტრაციო ბარათი თქვენი რეალური ან სავარჯიშო მონაცემებით გერმანულად:",
            "fields": [
                {"id": "fn", "label_de": "Vorname", "label_ka": "სახელი", "placeholder": "z.B. Giorgi", "example": "Giorgi"},
                {"id": "ln", "label_de": "Familienname / Nachname", "label_ka": "გვარი", "placeholder": "z.B. Beridze", "example": "Beridze"},
                {"id": "bd", "label_de": "Geburtsdatum (TT.MM.JJJJ)", "label_ka": "დაბადების თარიღი", "placeholder": "15.05.1998", "example": "15.05.1998"},
                {"id": "nat", "label_de": "Staatsangehörigkeit", "label_ka": "მოქალაქეობა", "placeholder": "georgisch", "example": "georgisch"},
                {"id": "addr", "label_de": "Straße & Hausnummer", "label_ka": "ქუჩა და სახლის ნომერი", "placeholder": "Rustaveli Ave. 10", "example": "Rustaveli Ave. 10"},
                {"id": "city", "label_de": "PLZ & Wohnort", "label_ka": "საფოსტო ინდექსი და ქალაქი", "placeholder": "0108 Tiflis", "example": "0108 Tiflis"}
            ]
        },
        {
            "id": "s_lab_2",
            "title": "მეგობრული წერილი: კინოში დაპატიჟებაზე პასუხი",
            "type": "free_text",
            "instructions_ka": """თქვენმა მეგობარმა ლუკასმა მოგწერათ და გეპატიჟებათ კინოში შაბათ საღამოს.
მისწერეთ მას მოკლე წერილი (დაახლოებით 20-30 სიტყვა):
1. გადაუხადეთ მადლობა მიწვევისთვის.
2. აუხსენით, რომ შაბათს არ გცალიათ (მიზეზი: მუშაობთ ან გამოცდისთვის სწავლობთ).
3. შესთავაზეთ შეხვედრა კვირას.""",
            "suggested_length": "20-30 სიტყვა",
            "model_solution": """Lieber Lukas,

vielen Dank für deine Einladung!
Am Samstag kann ich leider nicht kommen, weil ich für eine Prüfung lernen muss.
Hast du vielleicht am Sonntag Zeit? Wir können am Sonntagabend ins Kino gehen.

Liebe Grüße,
[Dein Name]""",
            "rubrics": [
                "მისალმება მეგობრულად (Lieber Lukas, / Hallo Lukas,)",
                "მადლობა მიწვევისთვის (Vielen Dank für die Einladung)",
                "უარის თქმა და მიზეზის დასახელება (Ich kann leider nicht...)",
                "ალტერნატიული დროის შეთავაზება (Hast du am Sonntag Zeit?)",
                "მეგობრული დამშვიდობება (Liebe Grüße, / Bis bald,)"
            ]
        },
        {
            "id": "s_lab_3",
            "title": "ოფიციალური მეილი: ენის კურსზე ინფორმაციის მოთხოვნა",
            "type": "free_text",
            "instructions_ka": """გსურთ გერმანული ენის A1 კურსზე ჩაწერა ბერლინში. მისწერეთ ენების სკოლას ოფიციალური წერილი (დაახლოებით 25-35 სიტყვა):
1. ოფიციალური თავაზიანი მისალმება (Sehr geehrte Damen und Herren,).
2. მიუთითეთ, რომ გსურთ A1 კურსის გავლა ივლისში.
3. იკითხეთ ფასი და გაკვეთილების განრიგი.
4. ოფიციალური დამშვიდობება.""",
            "suggested_length": "25-35 სიტყვა",
            "model_solution": """Sehr geehrte Damen und Herren,

ich möchte im Juli einen Deutschkurs A1 an Ihrer Sprachschule besuchen.
Können Sie mir bitte Informationen über die Kurstermine und die Preise schicken?

Vielen Dank im Voraus für Ihre Hilfe.

Mit freundlichen Grüßen,
[Vorname Nachname]""",
            "rubrics": [
                "ოფიციალური მიმართვა (Sehr geehrte Damen und Herren,)",
                "კურსის სურვილისა და დონის მითითება (Deutschkurs A1 im Juli)",
                "კითხვა ფასსა და განრიგზე (Preise und Kurstermine)",
                "მადლობა წინასწარ (Vielen Dank im Voraus)",
                "ოფიციალური დამშვიდობება (Mit freundlichen Grüßen, [სრული სახელი და გვარი])"
            ]
        }
    ],

    "sprechen": [
        {
            "id": "sp_lab_1",
            "title": "საკუთარი თავის წარდგენა (Sich vorstellen)",
            "instructions_ka": "წარადგინეთ თქვენი თავი 6 ძირითადი პუნქტის მიხედვით. ჩაწერეთ თქვენი ხმა და შეადარეთ გერმანულ ეტალონურ გამოთქმას:",
            "prompts": [
                {"point": "სახელი და გვარი", "phrase_de": "Mein Name ist Giorgi Beridze. (Ich heiße Giorgi.)"},
                {"point": "ასაკი", "phrase_de": "Ich bin fünfundzwanzig Jahre alt."},
                {"point": "წარმოშობის ქვეყანა", "phrase_de": "Ich komme aus Georgien."},
                {"point": "საცხოვრებელი ადგილი", "phrase_de": "Ich wohne in Tiflis."},
                {"point": "ენები", "phrase_de": "Meine Muttersprache ist Georgisch und ich lerne Deutsch."},
                {"point": "პროფესია", "phrase_de": "Ich bin Student von Beruf. (Ich arbeite als Ingenieur.)"},
                {"point": "ჰობი", "phrase_de": "Mein Hobby ist Schwimmen und ich lese gern."}
            ],
            "full_sample_de": "Guten Tag! Mein Name ist Giorgi Beridze. Ich bin fünfundzwanzig Jahre alt und komme aus Georgien. Ich wohne in Tiflis. Meine Muttersprache ist Georgisch, ich spreche Englisch und lerne jetzt Deutsch. Von Beruf bin ich Student. In meiner Freizeit spiele ich sehr gern Fußball und höre Musik."
        },
        {
            "id": "sp_lab_2",
            "title": "სიტუაციური თხოვნა და კითხვა (Bitten & Fragen im Alltag)",
            "instructions_ka": "მოუსმინეთ და გაიმეორეთ ყოველდღიური სასაუბრო რეპლიკები. შემდეგ ჩაწერეთ თქვენი საკუთარი ხმა:",
            "situations": [
                {
                    "situation_ka": "კაფეში ჭიქა წყლის თხოვნა:",
                    "phrase_de": "Könnte ich bitte ein Glas Wasser haben?",
                    "phrase_ka": "ხომ ვერ მომიტანდით ერთ ჭიქა წყალს, გეთაყვა?"
                },
                {
                    "situation_ka": "მატარებლის გამგზავრების დროის კითხვა ვაგზალზე:",
                    "phrase_de": "Entschuldigung, wann fährt der Zug nach München ab?",
                    "phrase_ka": "უკაცრავად, როდის გადის მატარებელი მიუნხენისკენ?"
                },
                {
                    "situation_ka": "მაღაზიაში ფასის კითხვა:",
                    "phrase_de": "Wie viel kostet dieses Buch bitte?",
                    "phrase_ka": "რა ღირს ეს წიგნი, გეთაყვა?"
                },
                {
                    "situation_ka": "ოთახში ფანჯრის გაღების თავაზიანი თხოვნა:",
                    "phrase_de": "Darf ich bitte das Fenster öffnen?",
                    "phrase_ka": "შეიძლება ფანჯარა გავაღო, გეთაყვა?"
                }
            ]
        }
    ]
}
