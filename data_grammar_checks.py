# -*- coding: utf-8 -*-
"""
Concept Check Questions (CCQs) for Deutsch A1 Pro Grammar Modules
Provides measurable comprehension verification for each grammar section of all 10 lessons.
"""

GRAMMAR_CHECKS = {
    # LEKTION 1
    "1.1": {
        "question": "როგორ მიმართავთ ოფიციალურ გარემოში უცნობ ზრდასრულ ადამიანს?",
        "options": ["Du (შენ)", "Sie (თქვენ - ოფიციალური)", "Ihr (თქვენ - არაფორმალური)"],
        "answer": 1,
        "explanation": "გერმანულში ოფიციალური თავაზიანი მიმართვაა 'Sie' (დიდი ასოთი). 'Du' გამოიყენება მხოლოდ მეგობრებთან და ოჯახში."
    },
    "1.2": {
        "question": "როგორ გამოითქმის ასოთშეხამება 'ei' გერმანულ სიტყვებში (მაგ. mein, heißen)?",
        "options": ["როგორც [ეი]", "როგორც [აი]", "როგორც [იი]"],
        "answer": 1,
        "explanation": "'ei' ყოველთვის გამოითქმის როგორც [აი], ხოლო 'ie' — როგორც გრძელი [ი:]."
    },
    "1.3": {
        "question": "რომელია ზმნის სწორი დაბოლოება 'du' პირისთვის (du kommst)?",
        "options": ["-e", "-st", "-t"],
        "answer": 1,
        "explanation": "მე-2 პირში (du) აწმყო დროში ზმნის ფუძეს ყოველთვის ემატება დაბოლოება '-st' (du kommst, du wohnst)."
    },
    "1.4": {
        "question": "რომელ პოზიციაზე დგას უღლებადი ზმნა Hauptsatz-ში (მთავარ წინადადებაში)?",
        "options": ["პირველ ადგილზე", "მე-2 ადგილზე (V2 წესი)", "წინადადების ბოლოში"],
        "answer": 1,
        "explanation": "გერმანულ მთავარ მტკიცებით წინადადებაში უღლებადი ზმნა მკაცრად მე-2 პოზიციაზე დგას (Verb-Second)."
    },

    # LEKTION 2
    "2.1": {
        "question": "რამდენი გრამატიკული სქესი არსებობს გერმანულ ენაში?",
        "options": ["ორი (მამრობითი და მდედრობითი)", "სამი (der, die, das)", "არცერთი, როგორც ქართულში"],
        "answer": 1,
        "explanation": "გერმანულში არის სამი სქესი: der (მამრობითი), die (მდედრობითი) და das (საშუალო)."
    },
    "2.2": {
        "question": "რა განსაზღვრული არტიკლი აქვთ არსებით სახელებს მრავლობით რიცხვში (Nominativ)?",
        "options": ["der", "die (ყველა სქესისთვის)", "das"],
        "answer": 1,
        "explanation": "მრავლობით რიცხვში განსაზღვრული არტიკლი ყველა სქესისთვის არის 'die'."
    },
    "2.3": {
        "question": "როგორ იტყვით: 'ეს ჩემი დაა' (die Schwester)?",
        "options": ["Das ist mein Schwester.", "Das ist meine Schwester.", "Das ist meinen Schwester."],
        "answer": 1,
        "explanation": "მდედრობით სქესთან კუთვნილებითი ნაცვალსახელი იღებს '-e' დაბოლოებას: meine Schwester."
    },

    # LEKTION 3
    "3.1": {
        "question": "რა განსხვავებაა 'kein'-სა და 'nicht'-ს შორის?",
        "options": [
            "kein უარყოფს არსებით სახელს, nicht — ზმნასა და ზედსართავს",
            "kein და nicht სრული სინონიმებია",
            "nicht გამოიყენება მხოლოდ კითხვებში"
        ],
        "answer": 0,
        "explanation": "'kein' უარყოფს განუსაზღვრელი არტიკლის მქონე ან უარტიკლო არსებით სახელს, 'nicht' კი ზმნას, ზედსართავს ან წინადადებას."
    },
    "3.2": {
        "question": "რას ნიშნავს შეკითხვა 'Was kostet das?'?",
        "options": ["სად არის ეს?", "რა ღირს ეს?", "გემრიელია ეს?"],
        "answer": 1,
        "explanation": "'Was kostet das?' ნიშნავს 'რა ღირს ეს?' ფასის გასაგებად."
    },
    "3.3": {
        "question": "რომელ პოზიციაზე დგება ძირითადი ინფინიტივი ზმნასთან 'möchten'?",
        "options": ["მე-2 ადგილზე", "უშუალოდ möchten-ის შემდეგ", "წინადადების ბოლოში (Satzklammer)"],
        "answer": 2,
        "explanation": "მოდალურ ზმნასთან ძირითადი ზმნა ინფინიტივის სახით წინადადების სულ ბოლოში გადადის (Ich möchte einen Kaffee trinken)."
    },

    # LEKTION 4
    "4.1": {
        "question": "რომელი არტიკლი იცვლის ფორმას Akkusativ-ში (ბრალდებითში)?",
        "options": ["მხოლოდ der -> den (მამრობითი)", "ყველა არტიკლი იცვლება", "მხოლოდ das -> des"],
        "answer": 0,
        "explanation": "Akkusativ-ში ფორმას იცვლის მხოლოდ მამრობითი სქესი: der -> den (einen/keinen). die და das უცვლელია."
    },
    "4.2": {
        "question": "როგორ ითქმის გერმანულად: 'ბინა არის ნათელი და მყუდრო'?",
        "options": ["Die Wohnung ist hell und gemütlich.", "Das Zimmer ist teuer.", "Die Küche ist dunkel."],
        "answer": 0,
        "explanation": "'hell' ნიშნავს ნათელს, ხოლო 'gemütlich' — მყუდროს."
    },
    "4.3": {
        "question": "რომელ ბრუნვას მოითხოვს გამოთქმა 'Es gibt...' (არის / არსებობს)?",
        "options": ["Nominativ (სახელობითი)", "Akkusativ (ბრალდებითი)", "Dativ (მიცემითი)"],
        "answer": 1,
        "explanation": "'Es gibt' ყოველთვის მოითხოვს Akkusativ-ს: Es gibt einen Balkon, es gibt eine Küche."
    },

    # LEKTION 5
    "5.1": {
        "question": "როგორ ითქმის გერმანულად 'ნახევარი სამი' (02:30)?",
        "options": ["halb zwei", "halb drei (ნახევარი აკლია სამს)", "zwei Uhr dreißig"],
        "answer": 1,
        "explanation": "გერმანულ სასაუბრო ენაში 'halb drei' ნიშნავს 02:30-ს (ნახევარი საათი მიდის სამისკენ)."
    },
    "5.2": {
        "question": "სად გადადის ზმნის განცალკევებადი წინსართი აწმყო დროში (მაგ. aufstehen)?",
        "options": ["ზმნის წინ რჩება", "წინადადების ბოლოში გადადის", "სრულად იკარგება"],
        "answer": 1,
        "explanation": "განცალკევებადი წინსართი (auf, ein, mit) აწმყოში გადადის წინადადების სულ ბოლოში: Ich stehe um 7 Uhr auf."
    },
    "5.3": {
        "question": "რომელი წინდებული გამოიყენება კვირის დღეებთან (მაგ. Montag)?",
        "options": ["im Montag", "am Montag", "um Montag"],
        "answer": 1,
        "explanation": "კვირის დღეებთან და დღის მონაკვეთებთან გამოიყენება 'am' (am Montag, am Morgen). საათებთან გამოიყენება 'um'."
    },

    # LEKTION 6
    "6.1": {
        "question": "როგორია მოდალური ზმნების (können, wollen) უღლება 'ich' და 'er/sie/es' პირებში?",
        "options": [
            "ერთმანეთისგან განსხვავდება",
            "იდენტურია და პირადი დაბოლოება არ ერთვის (ich kann = er kann)",
            "ორივეს ემატება -st"
        ],
        "answer": 1,
        "explanation": "მოდალურ ზმნებს 1-ლ და მე-3 პირში (ich და er/sie/es) იდენტური ფორმა აქვთ პირადი დაბოლოების გარეშე."
    },
    "6.2": {
        "question": "სად დგას 'gern' წინადადებაში მოქმედების სიამოვნებით შესრულების საჩვენებლად?",
        "options": ["წინადადების დასაწყისში", "უშუალოდ უღლებადი ზმნის შემდეგ", "წინადადების ბოლოში"],
        "answer": 1,
        "explanation": "'gern' დგება უშუალოდ უღლებადი ზმნის შემდეგ: Ich schwimme gern."
    },
    "6.3": {
        "question": "რომელია სწორი ფორმა: 'მე ვკითხულობ წიგნს' (lesen ზმნის ფუძის ცვლილება e->ie)?",
        "options": ["Ich lese ein Buch / du liest", "Ich lese kein Buch", "Du lest ein Buch"],
        "answer": 0,
        "explanation": "ზმნა 'lesen' მე-2 და მე-3 პირში იცვლის ფუძის ხმოვანს: ich lese, du liest, er liest."
    },

    # LEKTION 7
    "7.1": {
        "question": "როგორ იცვლება განსაზღვრული არტიკლები Dativ-ში (მიცემითში)?",
        "options": [
            "der/das -> dem, die -> der, Plural -> den (+n)",
            "არტიკლები არ იცვლება",
            "მხოლოდ der -> den"
        ],
        "answer": 0,
        "explanation": "Dativ-ში: der და das ხდება dem, die ხდება der, ხოლო მრავლობითში den (+n დაბოლოებით არსებითზე)."
    },
    "7.2": {
        "question": "რომელ ბრუნვას მოითხოვს წინდებულები: aus, bei, mit, nach, von, zu?",
        "options": ["მხოლოდ Akkusativ-ს", "მხოლოდ Dativ-ს", "Nominativ-ს"],
        "answer": 1,
        "explanation": "ეს წინდებულები (aus, bei, mit, nach, seit, von, zu) ყოველთვის უპირობოდ მოითხოვენ Dativ-ს."
    },
    "7.3": {
        "question": "როგორ ვკითხულობთ ქალაქში გზას თავაზიანად?",
        "options": ["Wo ist hier der Bahnhof, bitte?", "Fahr weg!", "Ich will Bahnhof."],
        "answer": 0,
        "explanation": "'Entschuldigung, wo ist hier..., bitte?' არის სწორი და თავაზიანი გერმანული მიმართვა."
    },

    # LEKTION 8
    "8.1": {
        "question": "რა სუფიქსი ერთვის ქალის პროფესიებს გერმანულში (მაგ. der Lehrer -> die ...)?",
        "options": ["-in (die Lehrerin)", "-heit", "-ung"],
        "answer": 0,
        "explanation": "მდედრობითი სქესის პროფესიებს ემატება სუფიქსი '-in' (die Ärztin, die Lehrerin, die Verkäuferin)."
    },
    "8.2": {
        "question": "როგორ იტყვით: 'მე ვმუშაობ ექიმად Siemens-ში'?",
        "options": ["Ich arbeite als Arzt bei Siemens.", "Ich arbeite wie Arzt in Siemens.", "Ich bin Arzt zu Siemens."],
        "answer": 0,
        "explanation": "პროფესიასთან გამოიყენება 'als', ხოლო კომპანიასთან — 'bei': als Arzt bei Siemens."
    },
    "8.3": {
        "question": "რას ნიშნავს 'Ich hatte gestern keine Zeit'?",
        "options": ["გუშინ დრო მქონდა", "გუშინ დრო არ მქონდა", "დღეს არ მცალია"],
        "answer": 1,
        "explanation": "'hatte' არის haben-ის ნამყო დრო (Präteritum): 'Ich hatte keine Zeit' = დრო არ მქონდა."
    },

    # LEKTION 9
    "9.1": {
        "question": "როგორ იქმნება თავაზიანი ბრძანებითი ფორმა (Imperativ) 'Sie'-სთვის?",
        "options": ["Trinken Sie bitte! (ინფინიტივი + Sie + bitte)", "Trink!", "Trinkt!"],
        "answer": 0,
        "explanation": "თავაზიანი იმპერატივი იქმნება ინფინიტივით და ნაცვალსახელით 'Sie': Kommen Sie bitte! Trinken Sie!"
    },
    "9.2": {
        "question": "როდის ვიყენებთ მოდალურ ზმნას 'sollen' ჯანმრთელობისა და რჩევის კონტექსტში?",
        "options": ["როცა ექიმი ან სხვა პირი გვაძლევს დავალებას/რჩევას", "მხოლოდ პირადი სურვილისას", "მხოლოდ აკრძალვისას"],
        "answer": 0,
        "explanation": "'sollen' გამოხატავს გარედან მიღებულ რჩევას ან მითითებას: Der Arzt sagt, ich soll im Bett bleiben."
    },
    "9.3": {
        "question": "როგორ ითქმის გერმანულად: 'ყელი მტკივა'?",
        "options": ["Mein Hals tut weh.", "Ich habe Hals weh.", "Der Hals ist krank."],
        "answer": 0,
        "explanation": "'wehtun' ნიშნავს ტკივილს: 'Mein Hals tut weh' (მხოლობითი) ან 'Meine Augen tun weh' (მრავლობითი)."
    },

    # LEKTION 10
    "10.1": {
        "question": "რომელი დამხმარე ზმნით იწარმოება Perfekt გადაადგილების ზმნებთან (gehen, fahren, fliegen)?",
        "options": ["haben", "sein", "werden"],
        "answer": 1,
        "explanation": "გადაადგილების (fahren, gehen, fliegen, kommen) და მდგომარეობის შეცვლის ზმნებთან Perfekt იწარმოება 'sein' დამხმარე ზმნით: Ich bin gefahren."
    },
    "10.2": {
        "question": "როგორ იწარმოება რეგულარული (სუსტი) ზმნების Partizip II?",
        "options": ["ge- + ფუძე + -t (gekauft, gemacht)", "მხოლოდ -en დაბოლოებით", "ge- პრეფიქსის გარეშე"],
        "answer": 0,
        "explanation": "სტანდარტული რეგულარული ზმნების Partizip II იწარმოება ფორმულით: ge- + ფუძე + -t (ge-mach-t, ge-kauf-t)."
    },
    "10.3": {
        "question": "სად დგას Partizip II (მაგ. gemacht) მთავარ წინადადებაში?",
        "options": ["მე-2 ადგილზე", "დამხმარე ზმნის წინ", "წინადადების სულ ბოლოში (Satzklammer)"],
        "answer": 2,
        "explanation": "Perfekt-ში დამხმარე ზმნა (haben/sein) დგას მე-2 ადგილზე, ხოლო Partizip II წინადადების სულ ბოლოში: Ich habe Deutsch gelernt."
    }
}
