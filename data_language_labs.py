# -*- coding: utf-8 -*-
"""
Four Core CEFR A1 Language Labs Database (Hören, Lesen, Schreiben, Sprechen).
Pedagogically authentic, original materials aligned with Schritte Neu, Menschen & Netzwerk.
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
                "რეგიონალური ბიო-ვაშლი — 1,99 ევრო კილოგრამი",
                "ბანანი — 2,50 ევრო კილოგრამი",
                "ფორთოხალი — 0,99 ევრო კილოგრამი",
                "გერმანული ყველი — 3,99 ევრო"
            ],
            "answer": 0,
            "transcript_ka": "ძვირფასო მომხმარებლებო! დღეს ახალი მიღებულია: ბიო-ვაშლი ჩვენი რეგიონიდან, კილოგრამი მხოლოდ ერთ ევროდ და ოთხმოცდაცხრამეტ ცენტად. ისარგებლეთ შეთავაზებით!"
        },
        {
            "id": "h_lab_4",
            "title": "სატელეფონო შეთანხმება: ბინის დათვალიერება",
            "category": "ბინის ქირაობა და დრო",
            "audio_text": "Hallo Herr Beridze, hier ist Weber Immobilien. Die Wohnungsbesichtigung findet morgen, am Freitag um siebzehn Uhr dreißig statt. Die Adresse ist Goethestraße zwölf. Bitte bestätigen Sie kurz per SMS.",
            "question": "როდის და სად ტარდება ბინის დათვალიერება?",
            "options": [
                "პარასკევს, 17:30 საათზე, გოეთეს ქუჩა 12-ში",
                "შაბათს, 10:00 საათზე, ბაჰნჰოფის ქუჩა 5-ში",
                "კვირას, 14:00 საათზე, შილერის ქუჩა 8-ში",
                "ორშაბათს, 18:00 საათზე, ცენტრალურ მოედანზე"
            ],
            "answer": 0,
            "transcript_ka": "გამარჯობა ბატონო ბერიძე, აქ არის ვებერის უძრავი ქონება. ბინის დათვალიერება გაიმართება ხვალ, პარასკევს ჩვიდმეტ საათსა და ოცდაათ წუთზე. მისამართია გოეთეს ქუჩა თორმეტი. გთხოვთ მოკლედ დამიდასტუროთ SMS-ით."
        }
    ],

    "lesen": [
        {
            "id": "l_lab_1",
            "title": "მეგობრის წერილი: დაბადების დღეზე დაპატიჟება",
            "category": "პირადი მიმოწერა (E-Mail)",
            "text_de": """Liebe Freunde,

am nächsten Samstag habe ich Geburtstag! Ich werde 25 Jahre alt und möchte das gerne mit euch feiern.
Die Party beginnt um 19:00 Uhr bei mir zu Hause in der Kantstraße 15.
Es gibt leckeres Essen, Musik und Getränke. Wenn ihr möchtet, könnt ihr einen Nachtisch oder Salat mitbringen.

Bitte gebt mir bis Donnerstag Bescheid, ob ihr kommt.

Ich freue mich sehr auf euch!
Liebe Grüße,
Sara""",
            "text_ka_summary": "ზარას წერილი მეგობრებისადმი, სადაც ის მათ დაბადების დღის წვეულებაზე ეპატიჟება.",
            "questions": [
                {
                    "q": "როდის იწყება ზარას დაბადების დღის წვეულება?",
                    "options": [
                        "შაბათს, 19:00 საათზე",
                        "პარასკევს, 18:00 საათზე",
                        "ხუთშაბათს, 20:00 საათზე",
                        "კვირას დილით"
                    ],
                    "answer": 0,
                    "explanation": "'Die Party beginnt um 19:00 Uhr am nächsten Samstag'."
                },
                {
                    "q": "რა შეუძლიათ მოიტანონ სტუმრებმა სურვილის შემთხვევაში?",
                    "options": [
                        "დესერტი ან სალათი (Nachtisch oder Salat)",
                        "მხოლოდ მუსიკალური დისკები",
                        "ძვირფასი საჩუქრები",
                        "სასმელები და ჭურჭელი"
                    ],
                    "answer": 0,
                    "explanation": "'Wenn ihr möchtet, könnt ihr einen Nachtisch oder Salat mitbringen'."
                },
                {
                    "q": "როდისთვის უნდა აცნობონ ზარას მოსვლის შესახებ?",
                    "options": [
                        "ხუთშაბათამდე (bis Donnerstag)",
                        "პარასკევს საღამოს",
                        "შაბათს წვეულების წინ",
                        "დღესვე დაუყოვნებლივ"
                    ],
                    "answer": 0,
                    "explanation": "'Bitte gebt mir bis Donnerstag Bescheid'."
                }
            ]
        },
        {
            "id": "l_lab_2",
            "title": "განცხადება ენის სკოლის დაფაზე (Aushang Sprachschule)",
            "category": "ოფიციალური განცხადება",
            "text_de": """ACHTUNG KURSTEILNEHMER!

Wegen Renovierungsarbeiten findet der Deutschkurs A1.2 ab Montag, dem 15. November, im Raum 204 (2. Stock) statt.
Der Unterricht beginnt wie gewohnt um 09:00 Uhr und endet um 12:15 Uhr.

Die Cafeteria im Erdgeschoss ist von Montag bis Freitag von 08:30 bis 14:00 Uhr geöffnet.

Die Schulleitung""",
            "text_ka_summary": "განცხადება ენების სკოლის სტუდენტებისთვის აუდიტორიის შეცვლის შესახებ.",
            "questions": [
                {
                    "q": "სად ჩატარდება გაკვეთილები 15 ნოემბრიდან?",
                    "options": [
                        "204-ე აუდიტორიაში, მე-2 სართულზე",
                        "101-ე აუდიტორიაში, პირველ სართულზე",
                        "კაფეტერიაში",
                        "სკოლის ეზოში"
                    ],
                    "answer": 0,
                    "explanation": "'im Raum 204 (2. Stock) statt'."
                },
                {
                    "q": "შეიცვალა თუ არა გაკვეთილების დაწყების დრო?",
                    "options": [
                        "არა, იწყება ჩვეულებრივად 09:00 საათზე ('wie gewohnt um 09:00 Uhr')",
                        "დიახ, იწყება 08:30 საათზე",
                        "დიახ, იწყება 10:00 საათზე",
                        "გაკვეთილები გადაიდო საღამოსთვის"
                    ],
                    "answer": 0,
                    "explanation": "'wie gewohnt um 09:00 Uhr' ნიშნავს: ჩვეულებრივად 09:00 საათზე."
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
        },
        {
            "id": "l_lab_4",
            "title": "შეტყობინება ექიმისგან: ანალიზების პასუხი და ვიზიტი",
            "category": "ჯანმრთელობა და პირადი შეტყობინება",
            "text_de": """Praxis Dr. Weber
Internist & Allgemeinmedizin
Hauptstraße 14, 80331 München

Lieber Herr Beridze,

Ihre Laborergebnisse sind da. Alle Werte sind weitgehend in Ordnung, aber Dr. Weber möchte die Blutwerte kurz persönlich mit Ihnen besprechen.

Bitte vereinbaren Sie online oder telefonisch einen Termin für nächsten Dienstag oder Mittwoch zwischen 14:00 und 17:00 Uhr.

Bringen Sie bitte Ihre Versichertenkarte mit.

Mit freundlichen Grüßen,
Praxisteam Dr. Weber
Tel: 089 2345678""",
            "text_ka_summary": "ექიმის შეტყობინება პაციენტისადმი ანალიზების პასუხისა და შეხვედრის დანიშვნის შესახებ.",
            "questions": [
                {
                    "q": "რატომ უნდა მივიდეს პაციენტი ექიმთან?",
                    "options": [
                        "ექიმს სურს ანალიზების პასუხების პირადად განხილვა",
                        "პაციენტი სასწრაფოდ საავადმყოფოში უნდა დაწვეს",
                        "ანალიზები დაიკარგა და თავიდანაა ჩასაბარებელი",
                        "ექიმი შვებულებაში გადის"
                    ],
                    "answer": 0,
                    "explanation": "'Dr. Weber möchte die Blutwerte kurz persönlich mit Ihnen besprechen' - ექიმს სურს ანალიზების პირადად განხილვა."
                },
                {
                    "q": "რომელ დღეებში და საათებშია შესაძლებელი ვიზიტის დანიშვნა?",
                    "options": [
                        "სამშაბათს ან ოთხშაბათს, 14:00-დან 17:00 საათამდე",
                        "ორშაბათს დილით 09:00 საათზე",
                        "მხოლოდ პარასკევს საღამოს",
                        "შაბათ-კვირას ნებისმიერ დროს"
                    ],
                    "answer": 0,
                    "explanation": "'nächsten Dienstag oder Mittwoch zwischen 14:00 und 17:00 Uhr'."
                },
                {
                    "q": "რა დოკუმენტი უნდა წაიღოს პაციენტმა თან?",
                    "options": [
                        "სადაზღვევო ბარათი (Versichertenkarte)",
                        "პასპორტი და დაბადების მოწმობა",
                        "მართვის მოწმობა",
                        "არაფერი არ არის საჭირო"
                    ],
                    "answer": 0,
                    "explanation": "'Bringen Sie bitte Ihre Versichertenkarte mit' - სადაზღვევო ბარათი."
                }
            ]
        }
    ],

    "schreiben": [
        {
            "id": "s_lab_1",
            "title": "ფორმა: სასტუმროს რეგისტრაციის ბარათი (Hotel-Anmeldeformular)",
            "type": "form",
            "instructions_ka": "შეავსეთ სასტუმროს სარეგისტრაციო ბარათი თქვენი რეალური ან სავარჯიშო მონაცემებით გერმანულად. ყველა ველი სავალდებულოა:",
            "fields": [
                {"id": "fn", "label_de": "Vorname", "label_ka": "სახელი", "placeholder": "z.B. Giorgi", "example": "Giorgi", "required": True},
                {"id": "ln", "label_de": "Familienname / Nachname", "label_ka": "გვარი", "placeholder": "z.B. Beridze", "example": "Beridze", "required": True},
                {"id": "bd", "label_de": "Geburtsdatum (TT.MM.JJJJ)", "label_ka": "დაბადების თარიღი", "placeholder": "15.05.1998", "example": "15.05.1998", "required": True},
                {"id": "nat", "label_de": "Staatsangehörigkeit", "label_ka": "მოქალაქეობა", "placeholder": "georgisch", "example": "georgisch", "required": True},
                {"id": "addr", "label_de": "Straße & Hausnummer", "label_ka": "ქუჩა და სახლის ნომერი", "placeholder": "Rustaveli Ave. 10", "example": "Rustaveli Ave. 10", "required": True},
                {"id": "city", "label_de": "PLZ & Wohnort", "label_ka": "საფოსტო ინდექსი და ქალაქი", "placeholder": "0108 Tiflis", "example": "0108 Tiflis", "required": True}
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
            "suggested_length": "20-30 სიტყვა (მინიმუმ 15 სიტყვა)",
            "min_words": 15,
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
            "suggested_length": "25-35 სიტყვა (მინიმუმ 15 სიტყვა)",
            "min_words": 15,
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
        },
        {
            "id": "s_lab_4",
            "title": "ბინის განცხადებაზე გამოხმაურება (Wohnungsanfrage)",
            "type": "free_text",
            "instructions_ka": """გაზეთში ნახეთ განცხადება 2-ოთახიან ბინაზე მიუნხენში. მისწერეთ მეპატრონეს (Frau Schneider) მოკლე მეილი (დაახლოებით 25-35 სიტყვა):
1. თავაზიანი მიმართვა (Sehr geehrte Frau Schneider,).
2. აუხსენით, რომ დაინტერესებული ხართ ბინით.
3. იკითხეთ, როდის არის შესაძლებელი ბინის დათვალიერება (Besichtigungstermin).
4. მიუთითეთ თქვენი საკონტაქტო ტელეფონის ნომერი.
5. ოფიციალური დამშვიდობება (Mit freundlichen Grüßen,).""",
            "suggested_length": "25-35 სიტყვა (მინიმუმ 15 სიტყვა)",
            "min_words": 15,
            "model_solution": """Sehr geehrte Frau Schneider,

ich habe Ihre Anzeige für die 2-Zimmer-Wohnung gelesen und habe großes Interesse.
Wann ist eine Wohnungsbesichtigung möglich?
Sie erreichen mich telefonisch unter 0176 1234567.

Mit freundlichen Grüßen,
[Vorname Nachname]""",
            "rubrics": [
                "თავაზიანი მიმართვა გვარით (Sehr geehrte Frau Schneider,)",
                "ინტერესის გამოხატვა ბინის მიმართ (Ich habe großes Interesse)",
                "დათვალიერების თარიღის კითხვა (Wann ist eine Besichtigung möglich?)",
                "საკონტაქტო ნომრის მითითება (Sie erreichen mich unter...)",
                "ოფიციალური დამშვიდობება (Mit freundlichen Grüßen, [სახელი გვარი])"
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
    ],

    "roleplay": [
        {
            "id": "rp_cafe",
            "title": "კაფეში შეკვეთა და გადახდა (Im Café bestellen)",
            "partner_name": "Markus",
            "partner_role": "ოფიციანტი (Kellner im Café Einstein)",
            "avatar": "🤵‍♂️",
            "situation_ka": "თქვენ ზიხართ ბერლინის კაფეში და გსურთ ყავის, ნამცხვრის შეკვეთა და ანგარიშის გასწორება.",
            "cultural_tip": "გერმანიაში კაფეებსა და რესტორნებში ოფიციანტს თითქმის ყოველთვის უტოვებენ ჩაის (Trinkgeld) დაახლოებით 5-10%-ს. თანხის გადაცემისას ამბობენ 'Stimmt so!' (ხურდა დაიტოვეთ).",
            "steps": [
                {
                    "step": 1,
                    "partner_de": "Guten Tag! Willkommen im Café Einstein. Was darf ich Ihnen bringen?",
                    "partner_ka": "გამარჯობა! კეთილი იყოს თქვენი მობრძანება კაფე აინშტაინში. რა მოგართვათ?",
                    "options": [
                        {
                            "text_de": "Guten Tag! Ich möchte bitte einen Kaffee und ein Stück Apfelkuchen.",
                            "text_ka": "გამარჯობა! ერთი ყავა და ერთი ნაჭერი ვაშლის ნამცხვარი მინდა, გეთაყვა.",
                            "points": 10,
                            "feedback_ka": "იდეალური, თავაზიანი და გრამატიკულად ზუსტი შეკვეთა Akkusativ-ში."
                        },
                        {
                            "text_de": "Hallo! Bringen Sie mir einen Kaffee, bitte.",
                            "text_ka": "გამარჯობა! ყავა მომიტანეთ, გეთაყვა.",
                            "points": 7,
                            "feedback_ka": "გასაგებია, თუმცა გერმანიაში უფრო თავაზიანია 'Ich möchte bitte...' ფორმა."
                        },
                        {
                            "text_de": "Ich esse ein Kaffee und trinke Kuchen.",
                            "text_ka": "ყავას ვჭამ და ნამცხვარს ვსვამ.",
                            "points": 2,
                            "feedback_ka": "ყურადღება მიაქციეთ ზმნებს: ყავას ვსვამთ (trinken), ნამცხვარს ვჭამთ (essen)!"
                        }
                    ]
                },
                {
                    "step": 2,
                    "partner_de": "Sehr gerne! Möchten Sie den Kaffee mit Milch und Zucker?",
                    "partner_ka": "დიდი სიამოვნებით! ყავა რძითა და შაქრით გნებავთ?",
                    "options": [
                        {
                            "text_de": "Nur mit Milch, bitte. Ohne Zucker.",
                            "text_ka": "მხოლოდ რძით, გეთაყვა. შაქრის გარეშე.",
                            "points": 10,
                            "feedback_ka": "ზუსტი და ბუნებრივი პასუხი 'mit' და 'ohne' წინდებულებით."
                        },
                        {
                            "text_de": "Ja, mit beidem, bitte.",
                            "text_ka": "დიახ, ორივეთი, გეთაყვა.",
                            "points": 9,
                            "feedback_ka": "მოკლე, სწორი და ეკონომიური გერმანული პასუხი."
                        },
                        {
                            "text_de": "Nein, ich nicht Zucker Milch.",
                            "text_ka": "არა, მე არა შაქარი რძე.",
                            "points": 2,
                            "feedback_ka": "უარყოფისთვის გამოიყენეთ 'ohne' (გარეშე) ან 'kein'."
                        }
                    ]
                },
                {
                    "step": 3,
                    "partner_de": "Kommt sofort! ... Bitteschön, Ihr Kaffee und der Apfelkuchen. Guten Appetit!",
                    "partner_ka": "ახლავე მოგართმევთ! ... ინებეთ, თქვენი ყავა და ვაშლის ნამცხვარი. გემრიელად მიირთვით!",
                    "options": [
                        {
                            "text_de": "Vielen Dank! Das sieht sehr lecker aus.",
                            "text_ka": "დიდი მადლობა! ძალიან გემრიელად გამოიყურება.",
                            "points": 10,
                            "feedback_ka": "ძალიან ზრდილობიანი და სასიამოვნო რეპლიკა."
                        },
                        {
                            "text_de": "Danke schön!",
                            "text_ka": "დიდი მადლობა!",
                            "points": 8,
                            "feedback_ka": "სწორი და სტანდარტული მადლობა."
                        },
                        {
                            "text_de": "Bitte schön.",
                            "text_ka": "არაფრის.",
                            "points": 3,
                            "feedback_ka": "როდესაც რამეს მოგართმევენ, პასუხობთ 'Danke'-თი და არა 'Bitte'-თი!"
                        }
                    ]
                },
                {
                    "step": 4,
                    "partner_de": "Hat es Ihnen geschmeckt? Möchten Sie bezahlen?",
                    "partner_ka": "მოგეწონათ? გადახდა გსურთ?",
                    "options": [
                        {
                            "text_de": "Ja, es war sehr lecker. Wir möchten bitte zahlen. Zusammen, bitte.",
                            "text_ka": "დიახ, ძალიან გემრიელი იყო. გადახდა გვსურს, ერთად გეთაყვა.",
                            "points": 10,
                            "feedback_ka": "იდეალური ფრაზა. გერმანიაში ყოველთვის აზუსტებენ: 'zusammen oder getrennt' (ერთად თუ ცალ-ცალკე)."
                        },
                        {
                            "text_de": "Die Rechnung, bitte.",
                            "text_ka": "ანგარიში, გეთაყვა.",
                            "points": 8,
                            "feedback_ka": "მოკლე და გასაგები."
                        },
                        {
                            "text_de": "Geld nehmen jetzt.",
                            "text_ka": "ფული აიღეთ ახლა.",
                            "points": 1,
                            "feedback_ka": "უხეში და გრამატიკულად გაუმართავია."
                        }
                    ]
                },
                {
                    "step": 5,
                    "partner_de": "Das macht zusammen 6 Euro 50, bitte.",
                    "partner_ka": "სულ 6 ევრო და 50 ცენტია, გეთაყვა.",
                    "options": [
                        {
                            "text_de": "Hier sind 8 Euro. Stimmt so, vielen Dank!",
                            "text_ka": "აი 8 ევრო. ხურდა დაიტოვეთ, დიდი მადლობა!",
                            "points": 10,
                            "feedback_ka": "გერმანული ეტიკეტის უმნიშვნელოვანესი ფრაზა 'Stimmt so!' (ხურდა დაიტოვეთ)."
                        },
                        {
                            "text_de": "Hier sind genau 6 Euro 50.",
                            "text_ka": "აი ზუსტად 6 ევრო და 50 ცენტი.",
                            "points": 8,
                            "feedback_ka": "სწორია და თავაზიანი."
                        },
                        {
                            "text_de": "Nein, das ist zu teuer, ich zahle nicht.",
                            "text_ka": "არა, ძალიან ძვირია, არ გადავიხდი.",
                            "points": 0,
                            "feedback_ka": "დაუშვებელი რეპლიკა შეკვეთის შემდეგ!"
                        }
                    ]
                }
            ]
        },
        {
            "id": "rp_hotel",
            "title": "სასტუმროში რეგისტრაცია და ნომრის მიღება (Einchecken im Hotel)",
            "partner_name": "Frau Weber",
            "partner_role": "ადმინისტრატორი (Rezeptionistin im Hotel Schiller)",
            "avatar": "👩‍💼",
            "situation_ka": "თქვენ მიხვედით სასტუმროში ფრანკფურტში და გსურთ ოთახის მიღება, საუზმისა და Wi-Fi-ის გარკვევა.",
            "cultural_tip": "გერმანიის სასტუმროებში სავალდებულოა სარეგისტრაციო ბარათის (Meldeschein) შევსება. სართულების დათვლა იწყება Erdgeschoss-ით (0 სართული / პირველი სართული).",
            "steps": [
                {
                    "step": 1,
                    "partner_de": "Guten Abend! Herzlich willkommen im Hotel Schiller. Wie kann ich Ihnen helfen?",
                    "partner_ka": "საღამო მშვიდობისა! კეთილი იყოს თქვენი მობრძანება სასტუმრო შილერში. რით შემიძლია დაგეხმაროთ?",
                    "options": [
                        {
                            "text_de": "Guten Abend! Ich habe ein Einzelzimmer auf den Namen Beridze reserviert.",
                            "text_ka": "საღამო მშვიდობისა! მე დაჯავშნილი მაქვს ერთადგილიანი ოთახი ბერიძის სახელზე.",
                            "points": 10,
                            "feedback_ka": "სრულყოფილი, ზუსტი და თავაზიანი მიმართვა."
                        },
                        {
                            "text_de": "Hallo! Mein Name ist Beridze, Zimmer bitte.",
                            "text_ka": "გამარჯობა! ჩემი გვარია ბერიძე, ოთახი მომეცით.",
                            "points": 6,
                            "feedback_ka": "ზედმეტად მოკლეა, თუმცა შინაარსი გასაგებია."
                        },
                        {
                            "text_de": "Ich schlafe hier kostenlos.",
                            "text_ka": "აქ უფასოდ მძინავს.",
                            "points": 1,
                            "feedback_ka": "გრამატიკულად და შინაარსობრივად შეუსაბამოა."
                        }
                    ]
                },
                {
                    "step": 2,
                    "partner_de": "Ah ja, Herr Beridze. Ein Einzelzimmer für drei Nächte. Könnten Sie bitte dieses Formular ausfüllen und unterschreiben?",
                    "partner_ka": "დიახ, ბატონო ბერიძე. ერთადგილიანი ოთახი სამი ღამით. ხომ ვერ შეავსებდით და ხელს მოაწერდით ამ ფორმას?",
                    "options": [
                        {
                            "text_de": "Natürlich, sehr gerne. Haben Sie einen Kugelschreiber für mich?",
                            "text_ka": "რა თქმა უნდა, დიდი სიამოვნებით. ხომ არ გაქვთ კალამი ჩემთვის?",
                            "points": 10,
                            "feedback_ka": "იდეალური რეპლიკა 'Kugelschreiber'-ის (კალამი) გამოყენებით."
                        },
                        {
                            "text_de": "Ja, ich mache das.",
                            "text_ka": "დიახ, გავაკეთებ.",
                            "points": 8,
                            "feedback_ka": "სწორია, თუმცა მარტივი."
                        },
                        {
                            "text_de": "Nein, keine Lust schreiben.",
                            "text_ka": "არა, წერის ხალისი არ მაქვს.",
                            "points": 0,
                            "feedback_ka": "უხეში და დაუშვებელი პასუხია."
                        }
                    ]
                },
                {
                    "step": 3,
                    "partner_de": "Hier ist ein Stift. Vielen Dank! Hier ist Ihre Schlüsselkarte: Zimmer 304 im dritten Stock.",
                    "partner_ka": "აი კალამი. დიდი მადლობა! აი თქვენი ბარათი: ოთახი 304, მესამე სართულზე.",
                    "options": [
                        {
                            "text_de": "Vielen Dank! Ab wann gibt es morgens Frühstück und wo?",
                            "text_ka": "დიდი მადლობა! რომელ საათიდან არის დილით საუზმე და სად?",
                            "points": 10,
                            "feedback_ka": "პრაქტიკული და გრამატიკულად უზადო შეკითხვა A1 დონეზე."
                        },
                        {
                            "text_de": "Danke. Wann Essen?",
                            "text_ka": "მადლობა. როდის ჭამა?",
                            "points": 5,
                            "feedback_ka": "პრიმიტიული სტრუქტურაა, გამოიყენეთ 'Wann gibt es Frühstück?'."
                        },
                        {
                            "text_de": "Ich mag kein Frühstück.",
                            "text_ka": "საუზმე არ მიყვარს.",
                            "points": 2,
                            "feedback_ka": "სასტუმროში ჩასვლისას უმჯობესია დააზუსტოთ საუზმის დრო ან თავაზიანად გადაუხადოთ მადლობა."
                        }
                    ]
                },
                {
                    "step": 4,
                    "partner_de": "Das Frühstücksbuffet ist von sieben bis zehn Uhr im Erdgeschoss. Das WLAN-Passwort steht auf der Karte.",
                    "partner_ka": "საუზმე შვედური მაგიდით არის 7-დან 10 საათამდე პირველ სართულზე (Erdgeschoss). Wi-Fi-ს პაროლი წერია ბარათზე.",
                    "options": [
                        {
                            "text_de": "Wunderbar, vielen herzlichen Dank! Einen schönen Abend noch.",
                            "text_ka": "შესანიშნავია, ძალიან დიდი მადლობა! სასიამოვნო საღამოს გისურვებთ.",
                            "points": 10,
                            "feedback_ka": "საუკეთესო, მაღალი კულტურის მქონე დამშვიდობება."
                        },
                        {
                            "text_de": "Danke, gute Nacht!",
                            "text_ka": "მადლობა, ღამე მშვიდობისა!",
                            "points": 8,
                            "feedback_ka": "კარგი და მოკლე პასუხი."
                        },
                        {
                            "text_de": "Tschüss.",
                            "text_ka": "ნახვამდის (არაფორმალური).",
                            "points": 3,
                            "feedback_ka": "სასტუმროს ადმინისტრატორთან ოფიციალურ გარემოში 'Tschüss' უხეშია; გამოიყენეთ 'Auf Wiedersehen'."
                        }
                    ]
                }
            ]
        },
        {
            "id": "rp_supermarkt",
            "title": "სუპერმარკეტში შოპინგი და წონა (Im Supermarkt einkaufen)",
            "partner_name": "Frau Schmidt",
            "partner_role": "გამყიდველი (Verkäuferin an der Frischetheke)",
            "avatar": "👩‍🌾",
            "situation_ka": "თქვენ ხართ მიუნხენის სუპერმარკეტში და გსურთ ყველის, ხილისა და პურის შეძენა და სალაროში გადახდა.",
            "cultural_tip": "გერმანიაში წონითი ერთეულია 'Pfund' (500 გრამი) და 'Kilo' (1000 გრამი). სალაროში პარკები (Tüte) ფასიანია.",
            "steps": [
                {
                    "step": 1,
                    "partner_de": "Guten Tag! Der Nächste bitte! Was darf es für Sie sein?",
                    "partner_ka": "გამარჯობა! შემდეგი მობრძანდით! რა გნებავთ?",
                    "options": [
                        {
                            "text_de": "Guten Tag! Ich hätte gerne zweihundert Gramm Gouda-Käse, bitte.",
                            "text_ka": "გამარჯობა! ორასი გრამი გაუდას ყველი მინდა, გეთაყვა.",
                            "points": 10,
                            "feedback_ka": "ფრაზა 'Ich hätte gerne...' არის გერმანული თავაზიანობის ეტალონი."
                        },
                        {
                            "text_de": "Ich will Käse.",
                            "text_ka": "მე მინდა ყველი.",
                            "points": 2,
                            "feedback_ka": "'Ich will' გერმანიაში უხეშად და გაუზრდელად ჟღერს, უმჯობესია 'Ich möchte' ან 'Ich hätte gern'."
                        },
                        {
                            "text_de": "Käse haben Sie?",
                            "text_ka": "ყველი გაქვთ?",
                            "points": 7,
                            "feedback_ka": "გასაგებია, თუმცა უმჯობესია შეკვეთის პირდაპირ გაცხადება."
                        }
                    ]
                },
                {
                    "step": 2,
                    "partner_de": "Am Stück oder geschnitten?",
                    "partner_ka": "მთლიან ნაჭრად თუ დაჭრილი?",
                    "options": [
                        {
                            "text_de": "Geschnitten, bitte. Schön dünn.",
                            "text_ka": "დაჭრილი, გეთაყვა. თხელ ნაჭრებად.",
                            "points": 10,
                            "feedback_ka": "ძალიან ბუნებრივი და პრაქტიკული გერმანული რეპლიკა."
                        },
                        {
                            "text_de": "Am Stück, bitte.",
                            "text_ka": "მთლიან ნაჭრად, გეთაყვა.",
                            "points": 9,
                            "feedback_ka": "ზუსტი და მკაფიო პასუხი."
                        },
                        {
                            "text_de": "Ich weiß nicht was das ist.",
                            "text_ka": "არ ვიცი რა არის ეს.",
                            "points": 3,
                            "feedback_ka": "გაიხსენეთ: 'geschnitten' = დაჭრილი."
                        }
                    ]
                },
                {
                    "step": 3,
                    "partner_de": "Kommt sofort. Darf es sonst noch etwas sein?",
                    "partner_ka": "ახლავე. კიდევ ხომ არაფერი გნებავთ?",
                    "options": [
                        {
                            "text_de": "Ja, haben Sie auch frische Brötchen?",
                            "text_ka": "დიახ, ახალი ფუნთუშებიც გაქვთ?",
                            "points": 10,
                            "feedback_ka": "სწორი კითხვა 'Brötchen' (ფუნთუშები) არსებითი სახელით."
                        },
                        {
                            "text_de": "Nein danke, das ist alles.",
                            "text_ka": "არა გმადლობთ, სულ ეს არის.",
                            "points": 10,
                            "feedback_ka": "იდეალური ფრაზა საყიდლების დასასრულებლად."
                        },
                        {
                            "text_de": "Nein, fertig.",
                            "text_ka": "არა, მორჩა.",
                            "points": 2,
                            "feedback_ka": "ზედმეტად მშრალი და უხეშია. გამოიყენეთ 'Das ist alles, danke'."
                        }
                    ]
                },
                {
                    "step": 4,
                    "partner_de": "Das macht zusammen 7 Euro 40. Brauchen Sie eine Tüte?",
                    "partner_ka": "სულ 7 ევრო და 40 ცენტია. პარკი გჭირდებათ?",
                    "options": [
                        {
                            "text_de": "Nein danke, ich habe eine Tasche dabei. Ich zahle mit Karte, bitte.",
                            "text_ka": "არა გმადლობთ, ჩანთა თან მაქვს. ბარათით გადავიხდი, გეთაყვა.",
                            "points": 10,
                            "feedback_ka": "უმაღლესი დონის გერმანული პასუხი ეკოლოგიური და გადახდის კულტურით."
                        },
                        {
                            "text_de": "Ja bitte, eine Tüte. Hier ist Geld.",
                            "text_ka": "დიახ გეთაყვა, ერთი პარკი. აი ფული.",
                            "points": 8,
                            "feedback_ka": "სწორი და გასაგები პასუხი."
                        },
                        {
                            "text_de": "Kein Geld haben.",
                            "text_ka": "ფული არ მაქვს.",
                            "points": 0,
                            "feedback_ka": "სალაროსთან ასეთი რეპლიკა დაუშვებელია."
                        }
                    ]
                }
            ]
        },
        {
            "id": "rp_weg",
            "title": "ქუჩაში გზის გაგება და ორიენტაცია (Nach dem Weg fragen)",
            "partner_name": "Thomas",
            "partner_role": "გამვლელი ქუჩაში (Passant in München)",
            "avatar": "🚶‍♂️",
            "situation_ka": "თქვენ ხართ მიუნხენის ცენტრში და ეძებთ ცენტრალურ ვაგზალს (Hauptbahnhof).",
            "cultural_tip": "გზის კითხვისას ყოველთვის იწყებენ თავაზიანი სიტყვით: 'Entschuldigung, wissen Sie wo...'. დამშვიდობებისას პასუხობენ: 'Danke gleichfalls!' (მადლობა, თქვენც ასევე).",
            "steps": [
                {
                    "step": 1,
                    "partner_de": "Hallo! Suchen Sie etwas? Sie sehen ein bisschen verloren aus.",
                    "partner_ka": "გამარჯობა! რამეს ეძებთ? ცოტა დაბნეული ჩანხართ.",
                    "options": [
                        {
                            "text_de": "Entschuldigung, können Sie mir bitte helfen? Ich suche den Hauptbahnhof.",
                            "text_ka": "უკაცრავად, ხომ ვერ დამეხმარებოდით? ცენტრალურ ვაგზალს ვეძებ.",
                            "points": 10,
                            "feedback_ka": "იდეალური, ბუნებრივი და თავაზიანი გზის კითხვა Akkusativ-ში (den Hauptbahnhof)."
                        },
                        {
                            "text_de": "Wo ist Bahnhof?",
                            "text_ka": "სად არის ვაგზალი?",
                            "points": 5,
                            "feedback_ka": "პრიმიტიულია. გამოიყენეთ 'Wo ist der Bahnhof bitte?'."
                        },
                        {
                            "text_de": "Ich verloren, hilf mir.",
                            "text_ka": "მე დაკარგული, მიშველე.",
                            "points": 3,
                            "feedback_ka": "გრამატიკულად გაუმართავია."
                        }
                    ]
                },
                {
                    "step": 2,
                    "partner_de": "Kein Problem! Gehen Sie hier geradeaus bis zur Kreuzung und dann biegen Sie nach links ab.",
                    "partner_ka": "პრობლემა არ არის! აქ პირდაპირ იარეთ გზაჯვარედინამდე და შემდეგ მარცხნივ შეუხვიეთ.",
                    "options": [
                        {
                            "text_de": "Geradeaus und dann links? Ist es weit von hier zu Fuß?",
                            "text_ka": "პირდაპირ და მერე მარცხნივ? შორია აქედან ფეხით?",
                            "points": 10,
                            "feedback_ka": "შესანიშნავი დაზუსტება 'zu Fuß' (ფეხით) ფრაზის გამოყენებით."
                        },
                        {
                            "text_de": "Ich verstehe nicht links rechts.",
                            "text_ka": "არ მესმის მარცხნივ მარჯვნივ.",
                            "points": 2,
                            "feedback_ka": "გაუმართავია. გაიხსენეთ: geradeaus = პირდაპირ, links = მარცხნივ, rechts = მარჯვნივ."
                        },
                        {
                            "text_de": "Gut, danke.",
                            "text_ka": "კარგი, მადლობა.",
                            "points": 7,
                            "feedback_ka": "მოკლეა, თუმცა გასაგები."
                        }
                    ]
                },
                {
                    "step": 3,
                    "partner_de": "Nein, gar nicht weit. Nur etwa fünf Minuten zu Fuß. Sie sehen das große Gebäude direkt vor sich.",
                    "partner_ka": "არა, სულაც არ არის შორს. მხოლოდ ხუთი წუთი ფეხით. დიდ შენობას პირდაპირ თქვენ წინ დაინახავთ.",
                    "options": [
                        {
                            "text_de": "Super, vielen herzlichen Dank für Ihre Hilfe! Einen schönen Tag noch.",
                            "text_ka": "სუპერ, ძალიან დიდი მადლობა დახმარებისთვის! სასიამოვნო დღეს გისურვებთ.",
                            "points": 10,
                            "feedback_ka": "უმაღლესი დონის მადლიერების გამოხატვა."
                        },
                        {
                            "text_de": "Danke schön, tschüss!",
                            "text_ka": "დიდი მადლობა, ნახვამდის!",
                            "points": 8,
                            "feedback_ka": "სწორი და მეგობრული."
                        },
                        {
                            "text_de": "Okay.",
                            "text_ka": "კარგი.",
                            "points": 3,
                            "feedback_ka": "გერმანიაში მხოლოდ 'Okay' მადლობის გარეშე უხეშად ჟღერს."
                        }
                    ]
                }
            ]
        },
        {
            "id": "rp_arzt",
            "title": "ექიმთან მიღებაზე და სიმპტომების აღწერა (Beim Arzt)",
            "partner_name": "Dr. Hoffmann",
            "partner_role": "ოჯახის ექიმი (Allgemeinarzt)",
            "avatar": "👨‍⚕️",
            "situation_ka": "თქვენ გაცივდით, გაქვთ ყელის ტკივილი და ტემპერატურა. მიხვედით ექიმთან მიღებაზე.",
            "cultural_tip": "გერმანიაში ექიმი გაძლევთ რეცეპტს (Rezept) აფთიაქისთვის და ავადმყოფობის ცნობას (Krankmeldung) სამსახურისთვის/უნივერსიტეტისთვის. ექიმის კეთილი სურვილია: 'Gute Besserung!' (გამოჯანმრთელებას გისურვებთ).",
            "steps": [
                {
                    "step": 1,
                    "partner_de": "Guten Tag! Nehmen Sie bitte Platz. Was fehlt Ihnen denn? Wo tut es weh?",
                    "partner_ka": "გამარჯობა! დაბრძანდით, გეთაყვა. რა გაწუხებთ? სად გტკივათ?",
                    "options": [
                        {
                            "text_de": "Guten Tag, Herr Doktor. Ich fühle mich nicht wohl. Ich habe seit zwei Tagen Halsschmerzen und Fieber.",
                            "text_ka": "გამარჯობა, ბატონო ექიმო. თავს კარგად არ ვგრძნობ. ორი დღეა ყელის ტკივილი და სიცხე მაქვს.",
                            "points": 10,
                            "feedback_ka": "სრულფასოვანი სამედიცინო ჩივილის ფორმულირება A1 დონეზე."
                        },
                        {
                            "text_de": "Mein Kopf tut weh und ich bin krank.",
                            "text_ka": "თავი მტკივა და ავად ვარ.",
                            "points": 8,
                            "feedback_ka": "სწორი და მარტივი აღწერა."
                        },
                        {
                            "text_de": "Ich sterbe vor Schmerzen.",
                            "text_ka": "ტკივილისგან ვკვდები.",
                            "points": 2,
                            "feedback_ka": "ზედმეტად დრამატულია ყოველდღიური გაციებისთვის."
                        }
                    ]
                },
                {
                    "step": 2,
                    "partner_de": "Ich verstehe. Haben Sie auch Husten oder Schnupfen?",
                    "partner_ka": "მესმის. ხველა ან სურდოც გაქვთ?",
                    "options": [
                        {
                            "text_de": "Ja, Husten habe ich auch, besonders nachts.",
                            "text_ka": "დიახ, ხველაც მაქვს, განსაკუთრებით ღამით.",
                            "points": 10,
                            "feedback_ka": "ზუსტი და მკაფიო დეტალიზაცია."
                        },
                        {
                            "text_de": "Nein, nur Hals und Fieber.",
                            "text_ka": "არა, მხოლოდ ყელი და სიცხე.",
                            "points": 8,
                            "feedback_ka": "გასაგები პასუხი."
                        },
                        {
                            "text_de": "Ich weiß nicht was Husten ist.",
                            "text_ka": "არ ვიცი რა არის ხველა.",
                            "points": 2,
                            "feedback_ka": "გაიხსენეთ: Husten = ხველა, Schnupfen = სურდო."
                        }
                    ]
                },
                {
                    "step": 3,
                    "partner_de": "Das ist eine Grippe. Ich verschreibe Ihnen Tabletten. Nehmen Sie eine Tablette dreimal täglich nach dem Essen.",
                    "partner_ka": "ეს გრიპია. წამლებს გამოგიწერთ. მიიღეთ თითო აბი დღეში სამჯერ ჭამის შემდეგ.",
                    "options": [
                        {
                            "text_de": "Verstanden, dreimal täglich nach dem Essen. Brauche ich eine Krankschreibung für die Arbeit?",
                            "text_ka": "გასაგებია, დღეში სამჯერ ჭამის შემდეგ. დამჭირდება ავადმყოფობის ფურცელი (Krankmeldung) სამსახურისთვის?",
                            "points": 10,
                            "feedback_ka": "გერმანიის შრომის კულტურის მნიშვნელოვანი ფრაზა 'Krankschreibung'."
                        },
                        {
                            "text_de": "Danke Herr Doktor, ich mache das so.",
                            "text_ka": "მადლობა ბატონო ექიმო, ასე გავაკეთებ.",
                            "points": 8,
                            "feedback_ka": "სწორი და თავაზიანი."
                        },
                        {
                            "text_de": "Ich trinke keine Tabletten.",
                            "text_ka": "აბებს არ ვსვამ.",
                            "points": 3,
                            "feedback_ka": "გერმანულად წამალს იღებენ (nehmen) და არა სვამენ (trinken)."
                        }
                    ]
                },
                {
                    "step": 4,
                    "partner_de": "Ja, hier ist das Rezept und Ihre Krankschreibung für drei Tage. Ruhen Sie sich aus. Gute Besserung!",
                    "partner_ka": "დიახ, აი რეცეპტი და თქვენი საავადმყოფო ფურცელი სამი დღით. დაისვენეთ. მალე გამოჯანმრთელებას გისურვებთ!",
                    "options": [
                        {
                            "text_de": "Vielen herzlichen Dank, Herr Doktor! Auf Wiedersehen.",
                            "text_ka": "ძალიან დიდი მადლობა, ბატონო ექიმო! ნახვამდის.",
                            "points": 10,
                            "feedback_ka": "სრულყოფილი დამშვიდობება."
                        },
                        {
                            "text_de": "Danke gleichfalls!",
                            "text_ka": "მადლობა, თქვენც ასევე!",
                            "points": 5,
                            "feedback_ka": "ექიმი ჯანმრთელია, ამიტომ 'Gute Besserung'-ზე პასუხობენ 'Vielen Dank'-ით."
                        },
                        {
                            "text_de": "Tschüss Arzt.",
                            "text_ka": "ნახვამდის ექიმო (არაფორმალური).",
                            "points": 2,
                            "feedback_ka": "ექიმთან გამოიყენეთ 'Auf Wiedersehen, Herr Doktor'."
                        }
                    ]
                }
            ]
        },
        {
            "id": "rp_wohnung",
            "title": "ბინის დათვალიერება და მეზობლის გაცნობა (WG-Besichtigung)",
            "partner_name": "Laura",
            "partner_role": "სტუდენტი და ბინის მეზობელი (Mitbewohnerin)",
            "avatar": "👱‍♀️",
            "situation_ka": "თქვენ ეძებთ ოთახს საერთო ბინაში (WG - Wohngemeinschaft) და მიხვედით ბინის დასათვალიერებლად.",
            "cultural_tip": "გერმანიაში სტუდენტთა 60% ცხოვრობს WG-ში (Wohngemeinschaft). 'Warmmiete' ნიშნავს ქირას გათბობის, წყლისა და კომუნალურების ჩათვლით, 'Kaltmiete' კი კომუნალურების გარეშე.",
            "steps": [
                {
                    "step": 1,
                    "partner_de": "Hi! Schön, dass du da bist. Komm doch rein! Wie heißt du noch mal?",
                    "partner_ka": "სალამი! მიხარია, რომ მოხვედი. შემოდი! რა გქვია?",
                    "options": [
                        {
                            "text_de": "Hallo Laura! Ich heiße Giorgi. Freut mich sehr, dich kennenzulernen!",
                            "text_ka": "გამარჯობა ლაურა! მე გიორგი მქვია. ძალიან მიხარია შენი გაცნობა!",
                            "points": 10,
                            "feedback_ka": "მეგობრული, უშუალო და გრამატიკულად ზუსტი გაცნობა ახალგაზრდულ გარემოში."
                        },
                        {
                            "text_de": "Guten Tag Frau Laura, mein Name ist Giorgi.",
                            "text_ka": "გამარჯობა ქალბატონო ლაურა, ჩემი გვარია გიორგი.",
                            "points": 7,
                            "feedback_ka": "WG-ში ახალგაზრდები ერთმანეთს 'Du'-თი (შენობით) მიმართავენ, 'Frau Laura' ზედმეტად ოფიციალურია."
                        },
                        {
                            "text_de": "Wo ist mein Zimmer?",
                            "text_ka": "სად არის ჩემი ოთახი?",
                            "points": 2,
                            "feedback_ka": "ზედმეტად პირდაპირი და უხეშია გაცნობის გარეშე."
                        }
                    ]
                },
                {
                    "step": 2,
                    "partner_de": "Freut mich auch, Giorgi! Hier ist das freie Zimmer. Es ist circa 18 Quadratmeter groß, hell und hat einen Balkon.",
                    "partner_ka": "მეც მიხარია, გიორგი! აი თავისუფალი ოთახი. დაახლოებით 18 კვადრატული მეტრია, ნათელია და აქვს აივანი.",
                    "options": [
                        {
                            "text_de": "Das Zimmer ist wirklich sehr schön! Wie hoch ist die Warmmiete im Monat?",
                            "text_ka": "ოთახი მართლაც ძალიან ლამაზია! რა არის თვიური Warmmiete (სრული ქირა)?",
                            "points": 10,
                            "feedback_ka": "შესანიშნავი კითხვა გერმანული ტერმინით 'Warmmiete'."
                        },
                        {
                            "text_de": "Was kostet das?",
                            "text_ka": "რა ღირს ეს?",
                            "points": 8,
                            "feedback_ka": "სწორი და მარტივი."
                        },
                        {
                            "text_de": "Zu klein, ich brauche Palast.",
                            "text_ka": "ძალიან პატარაა, სასახლე მჭირდება.",
                            "points": 1,
                            "feedback_ka": "იუმორისტულია, მაგრამ შეუსაბამო."
                        }
                    ]
                },
                {
                    "step": 3,
                    "partner_de": "Die Warmmiete ist 420 Euro inklusive Heizung, Wasser und schnellem Internet.",
                    "partner_ka": "სრული ქირა (Warmmiete) არის 420 ევრო გათბობის, წყლისა და სწრაფი ინტერნეტის ჩათვლით.",
                    "options": [
                        {
                            "text_de": "Das passt sehr gut in mein Budget. Ab wann ist das Zimmer frei?",
                            "text_ka": "ეს ძალიან კარგად ჯდება ჩემს ბიუჯეტში. როდიდან თავისუფლდება ოთახი?",
                            "points": 10,
                            "feedback_ka": "პროფესიონალური და მიზანმიმართული შეკითხვა."
                        },
                        {
                            "text_de": "Wann kann ich einziehen?",
                            "text_ka": "როდის შემიძლია გადმოსვლა?",
                            "points": 9,
                            "feedback_ka": "კარგი გერმანული ზმნა 'einziehen' (გადმოსვლა/დასახლება)."
                        },
                        {
                            "text_de": "Zu teuer, mach 100 Euro.",
                            "text_ka": "ძვირია, 100 ევროდ მომეცი.",
                            "points": 2,
                            "feedback_ka": "გერმანიაში WG-ს ფასზე ვაჭრობა მიუღებელია."
                        }
                    ]
                },
                {
                    "step": 4,
                    "partner_de": "Ab dem ersten nächsten Monats. Wir kochen abends oft zusammen in der Küche. Passt das für dich?",
                    "partner_ka": "მომავალი თვის პირველი რიცხვიდან. საღამოობით ხშირად ერთად ვამზადებთ ხოლმე სამზარეულოში. გაწყობს?",
                    "options": [
                        {
                            "text_de": "Ja, absolut! Ich koche sehr gern und kann auch mal georgische Spezialitäten machen.",
                            "text_ka": "დიახ, რა თქმა უნდა! საჭმლის კეთება ძალიან მიყვარს და ქართულ კერძებსაც სიამოვნებით მოგიმზადებთ ხოლმე.",
                            "points": 10,
                            "feedback_ka": "საუკეთესო პასუხი, რომელიც გარანტირებულად მოგაგებინებთ მეზობლების სიმპათიას!"
                        },
                        {
                            "text_de": "Ja, das finde ich gut.",
                            "text_ka": "დიახ, მომწონს ეს.",
                            "points": 8,
                            "feedback_ka": "სწორი და დადებითი პასუხი."
                        },
                        {
                            "text_de": "Nein, ich mag keine Menschen.",
                            "text_ka": "არა, ადამიანები არ მიყვარს.",
                            "points": 1,
                            "feedback_ka": "WG-ში (საერთო ბინაში) ასეთი პასუხით ოთახს არავინ მოგცემთ."
                        }
                    ]
                },
                {
                    "step": 5,
                    "partner_de": "Klingt super! Wir besprechen das heute Abend und melden uns morgen bei dir. Tschüss Giorgi!",
                    "partner_ka": "სუპერად ჟღერს! ამ საღამოს განვიხილავთ და ხვალ შეგეხმიანებით. ნახვამდის გიორგი!",
                    "options": [
                        {
                            "text_de": "Vielen Dank für die Einladung, Laura! Ich freue mich auf eure Nachricht. Tschüss!",
                            "text_ka": "დიდი მადლობა მოწვევისთვის, ლაურა! მოუთმენლად ველი თქვენს შეტყობინებას. ნახვამდის!",
                            "points": 10,
                            "feedback_ka": "შესანიშნავი, თავაზიანი და თბილი დამშვიდობება."
                        },
                        {
                            "text_de": "Danke Laura, tschüss!",
                            "text_ka": "მადლობა ლაურა, ნახვამდის!",
                            "points": 8,
                            "feedback_ka": "კარგი და მეგობრული."
                        },
                        {
                            "text_de": "Ich warte nicht.",
                            "text_ka": "არ დაველოდები.",
                            "points": 2,
                            "feedback_ka": "უადგილო რეპლიკა."
                        }
                    ]
                }
            ]
        }
    ]
}
