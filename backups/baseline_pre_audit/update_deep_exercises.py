# -*- coding: utf-8 -*-
"""
Helper script to expand exercise questions (MC, FIB, Listening) for Lektionen 2 to 10.
"""

# Rich exercises database for Lektionen 2 to 10
EXERCISES_DATA = {
    2: {
        "multiple_choice": [
            {"id": "mc2_1", "question": "რომელია 'Mutter'-ის სწორი განსაზღვრული არტიკლი?", "options": ["der", "die", "das", "den"], "answer": 1, "explanation": "die Mutter — მდედრობითი სქესის სახელია."},
            {"id": "mc2_2", "question": "როგორ ვთქვათ: 'ჩემი შვილები'?", "options": ["mein Kinder", "meine Kinder", "meinen Kinder", "meines Kinder"], "answer": 1, "explanation": "მრავლობით რიცხვში კუთვნილებით ნაცვალსახელს ემატება -e: meine Kinder."},
            {"id": "mc2_3", "question": "როგორ იწერება რიცხვი 45 გერმანულად?", "options": ["vierzigfünf", "fünfundvierzig", "fünfzigvier", "vierundfünfzig"], "answer": 1, "explanation": "ჯერ ერთეული (fünf), მერე und, მერე ათეული (vierzig) = fünfundvierzig."},
            {"id": "mc2_4", "question": "რომელი არსებითი სახელია საშუალო სქესის (das)?", "options": ["Vater", "Frau", "Kind", "Mutter"], "answer": 2, "explanation": "das Kind (ბავშვი) საშუალო სქესისაა."},
            {"id": "mc2_5", "question": "შეავსეთ: 'Das ist mein Bruder. _______ Name ist Luka.'", "options": ["Mein", "Sein", "Ihr", "Dein"], "answer": 1, "explanation": "ძმა კაცია (er), მისი კუთვნილებითი ნაცვალსახელია 'sein'."},
            {"id": "mc2_6", "question": "რას ნიშნავს გერმანული სიტყვა 'ledig'?", "options": ["დაქორწინებული", "დასაოჯახებელი", "განქორწინებული", "დაქვრივებული"], "answer": 1, "explanation": "ledig ნიშნავს დასაოჯახებელს / უცოლოს / გაუთხოვარს."},
            {"id": "mc2_7", "question": "რომელია რიცხვი 87 გერმანულად?", "options": ["siebenundachtzig", "achtundsiebzig", "achtzigundsieben", "siebzigundacht"], "answer": 0, "explanation": "sieben + und + achtzig = siebenundachtzig."}
        ],
        "fill_in_blank": [
            {"id": "fib2_1", "sentence_before": "Das ist Anna und das ist ", "sentence_after": " Schwester. (მისი და)", "correct_answer": "ihre", "hint": "ქალის კუთვნილებითი მდედრობითში: ihre"},
            {"id": "fib2_2", "sentence_before": "Ich bin 20 ", "sentence_after": " alt.", "correct_answer": "Jahre", "hint": "Jahre alt (წლის)"},
            {"id": "fib2_3", "sentence_before": "Hast du ", "sentence_after": "? (Geschwister - დედმამიშვილები)", "correct_answer": "Geschwister", "hint": "Geschwister"}
        ],
        "listening": [
            {"id": "lis2_1", "audio_text": "Meine Schwester ist vierundzwanzig Jahre alt.", "question": "რამდენი წლისაა მოსაუბრის და?", "options": ["14 წლის", "24 წლის", "34 წლის", "42 წლის"], "answer": 1},
            {"id": "lis2_2", "audio_text": "Mein Vater lebt und arbeitet in Tiflis.", "question": "სად ცხოვრობს და მუშაობს მამა?", "options": ["ბერლინში", "თბილისში", "ბათუმში", "მიუნხენში"], "answer": 1}
        ]
    },
    3: {
        "multiple_choice": [
            {"id": "mc3_1", "question": "როგორ ვთქვათ სწორად: 'მე ვაშლი არ მაქვს'?", "options": ["Ich habe nicht Apfel.", "Ich habe keinen Apfel.", "Ich habe kein Apfel.", "Ich habe nicht einen Apfel."], "answer": 1, "explanation": "არსებითი სახელის უარყოფისას ვიყენებთ kein-ს. der Apfel -> keinen Apfel Akkusativ-ში."},
            {"id": "mc3_2", "question": "რომელია 'das Brötchen'-ის განუსაზღვრელი არტიკლი?", "options": ["ein", "eine", "einen", "einem"], "answer": 0, "explanation": "საშუალო სქესის (das) განუსაზღვრელი არტიკლია ein."},
            {"id": "mc3_3", "question": "შეავსეთ: 'Der Kaffee ist _______ süß.' (არ არის ტკბილი)", "options": ["kein", "keine", "nicht", "nichts"], "answer": 2, "explanation": "ზედსართავის უარყოფისას ვიყენებთ nicht-ს."},
            {"id": "mc3_4", "question": "როგორ იკითხება ფასი: '2,50 €'?", "options": ["zwei fünfzig Euro", "zwei Euro fünfzig", "fünfzig zwei Euro", "zwei Cent fünfzig"], "answer": 1, "explanation": "ჯერ ევრო, მერე ცენტები: zwei Euro fünfzig."},
            {"id": "mc3_5", "question": "რომელია არსებითი სახელი 'das Ei'-ს (კვერცხი) მრავლობითი ფორმა?", "options": ["die Eie", "die Eier", "die Eien", "die Eis"], "answer": 1, "explanation": "das Ei -> die Eier."},
            {"id": "mc3_6", "question": "რას ნიშნავს 'Ich habe Hunger'?", "options": ["მწყურია", "მშია", "დავიღალე", "ცივა"], "answer": 1, "explanation": "der Hunger = შიმშილი -> Ich habe Hunger = მშია."}
        ],
        "fill_in_blank": [
            {"id": "fib3_1", "sentence_before": "Ich trinke ", "sentence_after": " Bier. (ლუდს არ ვსვამ)", "correct_answer": "kein", "hint": "das Bier საშუალოა -> kein"},
            {"id": "fib3_2", "sentence_before": "Ein Kilo ", "sentence_after": ", bitte! (Äpfel - ვაშლი)", "correct_answer": "Äpfel", "hint": "Äpfel (მრავლობითი)"},
            {"id": "fib3_3", "sentence_before": "Was ", "sentence_after": " das? (რა ღირს ეს?)", "correct_answer": "kostet", "hint": "ზმნა kosten"}
        ],
        "listening": [
            {"id": "lis3_1", "audio_text": "Das macht zusammen acht Euro zwanzig.", "question": "რამდენია გადასახდელი თანხა?", "options": ["8,20 €", "18,20 €", "8,50 €", "2,80 €"], "answer": 0},
            {"id": "lis3_2", "audio_text": "Ich möchte einen Kaffee ohne Zucker und ein Glas Wasser.", "question": "რას უკვეთავს კლიენტი?", "options": ["ჩაის ლიმონით და ლუდს", "ყავას უშაქროდ და ჭიქა წყალს", "ყავას შაქრით და წვენს", "ორ ჭიქა წყალს"], "answer": 1}
        ]
    },
    4: {
        "multiple_choice": [
            {"id": "mc4_1", "question": "შეავსეთ: 'Ich suche _______ Wohnung (die Wohnung).'", "options": ["einen", "eine", "ein", "einem"], "answer": 1, "explanation": "die Wohnung მდედრობითია, Akkusativ-ში რჩება eine."},
            {"id": "mc4_2", "question": "შეავსეთ: 'Er kauft _______ Tisch (der Tisch).'", "options": ["ein", "einen", "eine", "einem"], "answer": 1, "explanation": "der Tisch მამრობითია. Akkusativ-ში der ხდება den / einen."},
            {"id": "mc4_3", "question": "რომელი ოთახია 'das Badezimmer'?", "options": ["სამზარეულო", "სააბაზანო", "მისაღები", "საძინებელი"], "answer": 1, "explanation": "das Badezimmer არის სააბაზანო."},
            {"id": "mc4_4", "question": "რომელია ზედსართავ 'teuer' (ძვირი)-ის ანტონიმი?", "options": ["groß", "billig", "hell", "schön"], "answer": 1, "explanation": "teuer = ძვირი, billig = იაფი."},
            {"id": "mc4_5", "question": "რას ნიშნავს 'Warmmiete' გერმანიაში?", "options": ["ქირა გათბობისა და კომუნალურების გარეშე", "სრული ქირა გათბობისა და კომუნალურების ჩათვლით", "დეპოზიტის თანხა", "სამაკლერო გადასახადი"], "answer": 1, "explanation": "Warmmiete მოიცავს გათბობასა და კომუნალურ ხარჯებს."}
        ],
        "fill_in_blank": [
            {"id": "fib4_1", "sentence_before": "Hast du ", "sentence_after": " Schrank? (der Schrank)", "correct_answer": "einen", "hint": "der -> einen Akkusativ-ში"},
            {"id": "fib4_2", "sentence_before": "Die Wohnung ist sehr ", "sentence_after": ". (hell - ნათელი)", "correct_answer": "hell", "hint": "hell"}
        ],
        "listening": [
            {"id": "lis4_1", "audio_text": "Die Wohnung hat drei Zimmer und einen Balkon.", "question": "რამდენი ოთახი აქვს ბინას?", "options": ["2 ოთახი", "3 ოთახი", "4 ოთახი", "1 ოთახი"], "answer": 1}
        ]
    },
    5: {
        "multiple_choice": [
            {"id": "mc5_1", "question": "რას ნიშნავს სასაუბროდ 'halb zehn'?", "options": ["10:30", "09:30", "10:15", "09:45"], "answer": 1, "explanation": "halb zehn ნიშნავს ათის ნახევარს, ანუ 09:30-ს."},
            {"id": "mc5_2", "question": "რომელი წინდებული გამოიყენება ზუსტ საათთან?", "options": ["am", "im", "um", "in"], "answer": 2, "explanation": "საათთან გამოიყენება um: um 8 Uhr."},
            {"id": "mc5_3", "question": "რომელი წინდებული გამოიყენება კვირის დღეებთან?", "options": ["am", "im", "um", "in"], "answer": 0, "explanation": "დღეებთან გამოიყენება am: am Montag."},
            {"id": "mc5_4", "question": "სად მიდის წინსართი 'auf' ზმნიდან 'aufstehen' წინადადებაში: 'Ich stehe um 7 Uhr ___'?", "options": ["პირველ ადგილზე", "ზმნის წინ", "სულ ბოლოში (auf)", "შუაში"], "answer": 2, "explanation": "განცალკევებადი წინსართი მიდის წინადადების სულ ბოლოში: auf."},
            {"id": "mc5_5", "question": "რას ნიშნავს 'Viertel nach acht'?", "options": ["08:15", "08:45", "07:45", "08:30"], "answer": 0, "explanation": "Viertel nach acht = 08:15 (რვის თხუთმეტი წუთი)."}
        ],
        "fill_in_blank": [
            {"id": "fib5_1", "sentence_before": "Ich stehe um 7 Uhr ", "sentence_after": ". (aufstehen)", "correct_answer": "auf", "hint": "წინსართი auf ბოლოში"},
            {"id": "fib5_2", "sentence_before": "Der Film fängt um 20 Uhr ", "sentence_after": ". (anfangen)", "correct_answer": "an", "hint": "anfangen -> an"}
        ],
        "listening": [
            {"id": "lis5_1", "audio_text": "Der Zug fährt um Viertel vor neun ab.", "question": "რომელ საათზე გადის მატარებელი?", "options": ["08:45", "09:15", "08:15", "09:45"], "answer": 0}
        ]
    },
    6: {
        "multiple_choice": [
            {"id": "mc6_1", "question": "რომელია ზმნა 'können'-ის ფორმა 'er' პირთან?", "options": ["könnt", "kannst", "kann", "könne"], "answer": 2, "explanation": "ich kann, du kannst, er kann (დაბოლოების გარეშე!)."},
            {"id": "mc6_2", "question": "სად დგას მეორე ზმნა წინადადებაში მოდალური ზმნისას?", "options": ["მოდალურის გვერდით", "წინადადების სულ ბოლოში ინფინიტივში", "პირველ ადგილზე", "არსებითის წინ"], "answer": 1, "explanation": "Satzklammer-ის წესით მეორე ზმნა ინფინიტივში მიდის სულ ბოლოში."},
            {"id": "mc6_3", "question": "რას გამოხატავს მოდალური ზმნა 'möchten'?", "options": ["მკაცრ ვალდებულებას", "ზრდილობიან სურვილს ('მსურს')", "აკრძალვას", "წარსულს"], "answer": 1, "explanation": "möchten ნიშნავს ზრდილობიან სურვილს: Ich möchte einen Kaffee."},
            {"id": "mc6_4", "question": "რომელი სეზონია 'der Frühling'?", "options": ["ზაფხული", "შემოდგომა", "გაზაფხული", "ზამთარი"], "answer": 2, "explanation": "der Frühling არის გაზაფხული."}
        ],
        "fill_in_blank": [
            {"id": "fib6_1", "sentence_before": "Wir ", "sentence_after": " Deutsch lernen. (wollen)", "correct_answer": "wollen", "hint": "wir wollen"},
            {"id": "fib6_2", "sentence_before": "Kannst du gut ", "sentence_after": "? (schwimmen - ცურვა)", "correct_answer": "schwimmen", "hint": "ინფინიტივი: schwimmen"}
        ],
        "listening": [
            {"id": "lis6_1", "audio_text": "Am Sonntag kann ich leider nicht kommen.", "question": "როდის ვერ ახერხებს მოსვლას?", "options": ["შაბათს", "კვირას", "ორშაბათს", "პარასკევს"], "answer": 1}
        ]
    },
    7: {
        "multiple_choice": [
            {"id": "mc7_1", "question": "რა ხდება მდედრობითი არტიკლი (die) დატივში (Dativ)?", "options": ["die", "der", "dem", "den"], "answer": 1, "explanation": "დატივში die ხდება der: mit der U-Bahn."},
            {"id": "mc7_2", "question": "შეავსეთ: 'Ich fahre mit _______ Bus (der Bus).'", "options": ["den", "dem", "der", "das"], "answer": 1, "explanation": "mit მოითხოვს Dativ-ს. der Bus ხდება dem Bus."},
            {"id": "mc7_3", "question": "რას ნიშნავს გერმანული სიტყვა 'geradeaus'?", "options": ["მარცხნივ", "მარჯვნივ", "პირდაპირ", "უკან"], "answer": 2, "explanation": "geradeaus ნიშნავს პირდაპირ."},
            {"id": "mc7_4", "question": "რომელ ბრუნვას მოითხოვს წინდებული 'nach'?", "options": ["Nominativ", "Akkusativ", "Dativ", "Genitiv"], "answer": 2, "explanation": "nach მუდამ დატივს მოითხოვს."}
        ],
        "fill_in_blank": [
            {"id": "fib7_1", "sentence_before": "Ich gehe zu ", "sentence_after": " Arzt. (zu + dem = zum)", "correct_answer": "dem", "hint": "der Arzt -> dem Arzt"},
            {"id": "fib7_2", "sentence_before": "Wir fahren mit ", "sentence_after": " U-Bahn. (die U-Bahn)", "correct_answer": "der", "hint": "die -> der Dativ-ში"}
        ],
        "listening": [
            {"id": "lis7_1", "audio_text": "Biegen Sie an der Ampel nach rechts ab!", "question": "საით უნდა შეუხვიოს?", "options": ["მარცხნივ", "მარჯვნივ", "პირდაპირ", "უკან"], "answer": 1}
        ]
    },
    8: {
        "multiple_choice": [
            {"id": "mc8_1", "question": "როგორ ითქმის: 'ის ექიმად მუშაობს'?", "options": ["Er arbeitet wie Arzt.", "Er arbeitet als Arzt.", "Er arbeitet bei Arzt.", "Er arbeitet für Arzt."], "answer": 1, "explanation": "პროფესიასთან გამოიყენება als: arbeitet als Arzt."},
            {"id": "mc8_2", "question": "რას ნიშნავს 'Hier darf man nicht rauchen'?", "options": ["აქ მოწევა ნებადართულია", "აქ მოწევა აკრძალულია", "აქ უნდა მოწიოთ", "აქ სიგარეტი იყიდება"], "answer": 1, "explanation": "nicht dürfen გამოხატავს მკაცრ აკრძალვას."},
            {"id": "mc8_3", "question": "როგორ ვაწარმოებთ მდედრობითი სქესის პროფესიას (მასწავლებელი ქალი)?", "options": ["-ung", "-in (Lehrerin)", "-heit", "-keit"], "answer": 1, "explanation": "ქალის პროფესიებს ემატება -in: die Lehrerin."},
            {"id": "mc8_4", "question": "რომელია ზმნა 'müssen'-ის ფორმა 'er' პირთან?", "options": ["müsst", "musst", "muss", "müsse"], "answer": 2, "explanation": "ich muss, du musst, er muss."}
        ],
        "fill_in_blank": [
            {"id": "fib8_1", "sentence_before": "Er ", "sentence_after": " heute viel arbeiten. (müssen)", "correct_answer": "muss", "hint": "er muss"},
            {"id": "fib8_2", "sentence_before": "Ich arbeite ", "sentence_after": " Programmierer. (როგორც)", "correct_answer": "als", "hint": "als"}
        ],
        "listening": [
            {"id": "lis8_1", "audio_text": "Ich arbeite seit zwei Jahren bei Siemens.", "question": "რამდენი ხანია რაც მუშაობს სიმენსში?", "options": ["1 წელია", "2 წელია", "3 წელია", "5 თვეა"], "answer": 1}
        ]
    },
    9: {
        "multiple_choice": [
            {"id": "mc9_1", "question": "რომელია ზმნა 'trinken'-ის ბრძანებითი ფორმა შენობით (du)?", "options": ["Trinkst!", "Trink!", "Trinken!", "Trinke du!"], "answer": 1, "explanation": "du-ფორმის ბრძანებითში აკლდება -st და du: Trink!"},
            {"id": "mc9_2", "question": "შეავსეთ: 'Meine Augen _______ weh.' (თვალები მტკივა)", "options": ["tut", "tun", "hat", "haben"], "answer": 1, "explanation": "Augen მრავლობითია, ამიტომ tun weh."},
            {"id": "mc9_3", "question": "რომელია ზმნა 'sein'-ის თავაზიანი (Sie) ბრძანებითი?", "options": ["Sind Sie!", "Seien Sie!", "Seid!", "War Sie!"], "answer": 1, "explanation": "Seien Sie bitte ruhig!"},
            {"id": "mc9_4", "question": "რას ნიშნავს 'Gute Besserung!'?", "options": ["დილა მშვიდობისა", "მალე გამოჯანმრთელებას გისურვებ", "გემრიელად მიირთვით", "ბედნიერ მგზავრობას გისურვებ"], "answer": 1, "explanation": "Gute Besserung გამოიყენება ავადმყოფისთვის გამოჯანმრთელების სასურვებლად."}
        ],
        "fill_in_blank": [
            {"id": "fib9_1", "sentence_before": "Der Arzt sagt, ich ", "sentence_after": " im Bett bleiben. (sollen)", "correct_answer": "soll", "hint": "ich soll"},
            {"id": "fib9_2", "sentence_before": "Mein Kopf ", "sentence_after": " weh. (tut/tun)", "correct_answer": "tut", "hint": "Kopf მხოლობითია -> tut"}
        ],
        "listening": [
            {"id": "lis9_1", "audio_text": "Bleiben Sie bitte drei Tage im Bett!", "question": "რამდენი დღე უნდა დარჩეს ლოგინში?", "options": ["1 დღე", "2 დღე", "3 დღე", "1 კვირა"], "answer": 2}
        ]
    },
    10: {
        "multiple_choice": [
            {"id": "mc10_1", "question": "რომელ დამხმარე ზმნას იღებს 'fahren' (მგზავრობა) პერფექტში?", "options": ["haben (hat gefahren)", "sein (ist gefahren)", "werden", "bleiben"], "answer": 1, "explanation": "fahren მოძრაობის ზმნაა, იღებს sein-ს: ist gefahren."},
            {"id": "mc10_2", "question": "რომელია ზმნა 'machen'-ის Partizip II?", "options": ["gemacht", "gemachen", "machte", "gemachten"], "answer": 0, "explanation": "რეგულარული ზმნა: ge- + mach + -t = gemacht."},
            {"id": "mc10_3", "question": "შეავსეთ: 'Ich habe gestern ein Buch _______.' (kaufen)", "options": ["gekauft", "gekaufen", "kaufte", "kaufen"], "answer": 0, "explanation": "kaufen -> gekauft (Partizip II წინადადების ბოლოში)."},
            {"id": "mc10_4", "question": "რომელია ზმნა 'bleiben'-ის (დარჩენა) პერფექტის დამხმარე ზმნა?", "options": ["haben (hat geblieben)", "sein (ist geblieben)", "werden", "tun"], "answer": 1, "explanation": "bleiben გამონაკლისია და იღებს sein-ს: ist geblieben."},
            {"id": "mc10_5", "question": "იღებს თუ არა 'ge-' პრეფიქსს ზმნა 'studieren' პერფექტში?", "options": ["დიახ (gestudiert)", "არა (studiert)", "ორივე სწორია", "მხოლოდ -en დაბოლოებით"], "answer": 1, "explanation": "-ieren დაბოლოების ზმნები არ იღებენ ge-ს: hat studiert."}
        ],
        "fill_in_blank": [
            {"id": "fib10_1", "sentence_before": "Wir ", "sentence_after": " nach Berlin geflogen. (sein/haben)", "correct_answer": "sind", "hint": "wir sind geflogen"},
            {"id": "fib10_2", "sentence_before": "Er hat eine Pizza ", "sentence_after": ". (essen -> gegessen)", "correct_answer": "gegessen", "hint": "gegessen"}
        ],
        "listening": [
            {"id": "lis10_1", "audio_text": "Gestern habe ich meine Freunde in Tiflis besucht.", "question": "რა გააკეთა მოსაუბრემ გუშინ?", "options": ["მეგობრები მოინახულა თბილისში", "წიგნი იყიდა", "ბერლინში გაფრინდა", "იმუშავა"], "answer": 0}
        ]
    }
}

