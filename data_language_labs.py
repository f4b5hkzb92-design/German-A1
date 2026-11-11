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
    ]
}
