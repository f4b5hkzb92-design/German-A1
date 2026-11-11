# -*- coding: utf-8 -*-
"""
Builder script to generate comprehensive data.js for German A1 learning platform.
Based on Schritte International Neu / Menschen / Netzwerk A1 curriculum used in Georgian universities and schools.
"""
import json
import os

BASE_DIR = "/Users/shotachitaishvili/Documents/German A1"

# --- 10 Full Lektionen ---
lessons = [
    {
        "id": 1,
        "title_de": "Lektion 1: Erste Kontakte & Begrüßung",
        "title_ka": "გაკვეთილი 1: პირველი კონტაქტი და მისალმება",
        "icon": "👋",
        "description_ka": "ისწავლეთ მისალმება, საკუთარი თავის წარდგენა, გერმანული ანბანი და ძირითადი ზმნების უღლება აწმყოში.",
        "grammar_sections": [
            {
                "title": "1. გერმანული ანბანი და წარმოთქმის ძირითადი წესები (Alphabet & Aussprache)",
                "content_ka": """გერმანულ ანბანში 26 ლათინური ასოა + 3 უმლაუტი (Ä, Ö, Ü) და ესცეტი (ß).
ქართველებისთვის განსაკუთრებით მნიშვნელოვანია ასოთშეხამებების ცოდნა:
• **ei** იკითხება როგორც [აი] (მაგ: *mein* [მაინ] - ჩემი, *nein* [ნაინ] - არა)
• **ie** იკითხება როგორც გრძელი [იი] (მაგ: *sie* [ზიი] - ის, *wie* [ვიი] - როგორ)
• **eu / äu** იკითხება როგორც [ოი] (მაგ: *deutsch* [დოიჩ] - გერმანული, *Häuser* [ჰოიზერ] - სახლები)
• **sch** იკითხება როგორც [შ] (მაგ: *Schule* [შულე] - სკოლა)
• **ch** - a, o, u-ს შემდეგ იკითხება როგორც [ხ] (მაგ: *Buch* [ბუხ] - წიგნი, *machen* [მახენ] - კეთება); e, i, ä, ö, ü-ს შემდეგ იკითხება როგორც რბილი [ჰ/ხ] (მაგ: *ich* [იჰ] - მე, *nicht* [ნიჰტ] - არა)
• **sp / st** სიტყვის ან ფუძის დასაწყისში იკითხება როგორც [შპ / შტ] (მაგ: *sprechen* [შპრეხენ] - ლაპარაკი, *Student* [შტუდენტ] - სტუდენტი)
• **s** ხმოვნის წინ იკითხება როგორც [ზ] (მაგ: *sein* [ზაინ] - ყოფნა, *sieben* [ზიბენ] - შვიდი)
• **ß** (eszett) იკითხება როგორც ორმაგი [ს] (მაგ: *heißen* [ჰაისენ] - სახელად წოდება)
• **w** იკითხება როგორც [ვ] (მაგ: *wer* [ვერ] - ვინ, *wo* [ვო] - სად)
• **v** უმეტესად იკითხება როგორც [ფ] (მაგ: *von* [ფონ] - -დან/-გან, *Vater* [ფათერ] - მამა)"""
            },
            {
                "title": "2. პირის ნაცვალსახელები (Personalpronomen)",
                "content_ka": """გერმანულში პირის ნაცვალსახელები აუცილებლად გამოიყენება წინადადებაში:
• **ich** - მე
• **du** - შენ (შინაურული, მეგობრული)
• **er** - ის (მამრობითი სქესი)
• **sie** - ის (მდედრობითი სქესი)
• **es** - ის (საშუალო სქესი)
• **wir** - ჩვენ
• **ihr** - თქვენ (მეგობრებთან, ბავშვებთან მრავლობითში)
• **sie** - ისინი (მესამე პირი მრავლობითი)
• **Sie** - თქვენ (თავაზიანი ფორმა ერთ ან რამდენიმე უცხო ადამიანთან, იწერება დიდი ასოთი!)"""
            },
            {
                "title": "3. ზმნის უღლება აწმყოში (Präsens)",
                "content_ka": """გერმანული ზმნების უმეტესობა ინფინიტივში ბოლოვდება **-en**-ზე (მაგ: *komm-en, lern-en, wohn-en*).
ფუძეს (Stamm) ემატება შემდეგი პირის დაბოლოებები:
• ich -> **-e** (ich komme - მე მოვდივარ)
• du -> **-st** (du kommst - შენ მოდიხარ)
• er/sie/es -> **-t** (er kommt - ის მოდის)
• wir -> **-en** (wir kommen - ჩვენ მოვდივართ)
• ihr -> **-t** (ihr kommt - თქვენ მოდიხართ)
• sie/Sie -> **-en** (sie/Sie kommen - ისინი მოდიან / თქვენ მოდიხართ)

**განსაკუთრებული ზმნები:**
1. ზმნა **sein** (ყოფნა) - სრულიად უწესოა:
   ich bin, du bist, er/sie/es ist, wir sind, ihr seid, sie/Sie sind.
2. ზმნა **heißen** (სახელად წოდება):
   ich heiße, du heißt (არა heißst!), er/sie/es heißt, wir heißen, ihr heißt, sie/Sie heißen.
3. ზმნა **sprechen** (ლაპარაკი) - ფუძის ხმოვანი ეცვლება du და er/sie/es პირებში (e -> i):
   ich spreche, du sprichst, er spricht, wir sprechen, ihr sprecht, sie/Sie sprechen."""
            },
            {
                "title": "4. კითხვითი წინადადებები (W-Fragen) და სიტყვათა რიგი",
                "content_ka": """გერმანულში წესრიგი მკაცრია!
• **W-Frage (კითხვითი სიტყვით):**
  1. კითხვითი სიტყვა (Wie, Woher, Wo, Was, Wer)
  2. ზმნა (ყოველთვის მე-2 ადგილზე!)
  3. ქვემდებარე (სუბიექტი)
  *მაგალითად:* **Wie** (1) **heißen** (2) **Sie** (3)? (რა გქვიათ თქვენ?)
  **Woher** (1) **kommst** (2) **du** (3)? (საიდან ხარ?)

• **Ja/Nein-Frage (დიახ/არა კითხვა):**
  ზმნა გადმოდის პირველ ადგილზე!
  *მაგალითად:* **Kommen** (1) **Sie** (2) aus Georgien? (მოდიხართ თუ არა საქართველოდან?)
  პასუხი: *Ja, ich komme aus Georgien.* ან *Nein, ich komme aus Deutschland.*"""
            }
        ],
        "dialogues": [
            {
                "speaker": "Anna",
                "text_de": "Guten Tag! Mein Name ist Anna Meier. Wie heißen Sie?",
                "text_ka": "გამარჯობა! ჩემი სახელია ანა მაიერი. რა გქვიათ თქვენ?"
            },
            {
                "speaker": "Giorgi",
                "text_de": "Guten Tag, Frau Meier! Ich heiße Giorgi Beridze. Freut mich!",
                "text_ka": "გამარჯობა, ქალბატონო მაიერ! მე მქვია გიორგი ბერიძე. სასიამოვნოა!"
            },
            {
                "speaker": "Anna",
                "text_de": "Freut mich auch! Woher kommen Sie, Herr Beridze?",
                "text_ka": "ჩემთვისაც სასიამოვნოა! საიდან ხართ, ბატონო ბერიძე?"
            },
            {
                "speaker": "Giorgi",
                "text_de": "Ich komme aus Georgien, aus Tiflis. Und wo wohnen Sie?",
                "text_ka": "მე საქართველოდან ვარ, თბილისიდან. და თქვენ სად ცხოვრობთ?"
            },
            {
                "speaker": "Anna",
                "text_de": "Ich wohne in Berlin. Sprechen Sie Deutsch?",
                "text_ka": "მე ბერლინში ვცხოვრობ. ლაპარაკობთ გერმანულად?"
            },
            {
                "speaker": "Giorgi",
                "text_de": "Ja, ein bisschen. Ich lerne jetzt Deutsch A1 an der Universität.",
                "text_ka": "დიახ, ცოტას. ახლა ვსწავლობ გერმანულ A1-ს უნივერსიტეტში."
            }
        ],
        "vocabulary_ids": [
            "guten_tag", "hallo", "auf_wiedersehen", "tschuss", "danke", "bitte",
            "name", "land", "deutschland", "georgien", "kommen", "heissen",
            "sein", "sprechen", "wohnen", "lernen", "wie", "woher", "wo", "was", "wer"
        ]
    },
    {
        "id": 2,
        "title_de": "Lektion 2: Familie, Freunde & Zahlen",
        "title_ka": "გაკვეთილი 2: ოჯახი, მეგობრები და რიცხვები",
        "icon": "👨‍👩‍👧‍👦",
        "description_ka": "გაეცანით ოჯახის წევრებს, კუთვნილებით ნაცვალსახელებს, გერმანულ არტიკლებს და რიცხვებს 0-დან 100-მდე.",
        "grammar_sections": [
            {
                "title": "1. გრამატიკული სქესი და განსაზღვრული არტიკლები (der, die, das)",
                "content_ka": """ქართულ ენაში სქესი არ გვაქვს, მაგრამ გერმანულში ყველა არსებით სახელს გააჩნია სქესი და იწერება **დიდი ასოთი**!
არსებობს 3 სქესი:
• **der** - მამრობითი სქესი (Maskulinum) - [ლურჯი ფერი]
  მაგ: *der Vater* (მამა), *der Bruder* (ძმა), *der Mann* (კაცი), *der Tisch* (მაგიდა)
• **die** - მდედრობითი სქესი (Femininum) - [წითელი ფერი]
  მაგ: *die Mutter* (დედა), *die Schwester* (და), *die Frau* (ქალი), *die Lampe* (ნათურა)
• **das** - საშუალო სქესი (Neutrum) - [მწვანე ფერი]
  მაგ: *das Kind* (ბავშვი), *das Mädchen* (გოგონა), *das Buch* (წიგნი), *das Auto* (მანქანა)
• **die** - მრავლობითი რიცხვი (Plural) - [იისფერი ფერი]
  მრავლობით რიცხვში ყველა სქესის სახელი იღებს არტიკლს **die**!
  მაგ: *die Eltern* (მშობლები), *die Kinder* (ბავშვები).

> **ოქროს წესი ქართველი შემსწავლელებისთვის:** ყოველი ახალი სიტყვა ისწავლეთ მის არტიკლთან და მრავლობით ფორმასთან ერთად! მხოლოდ "Vater = მამა" არ კმარა, უნდა ისწავლოთ: "der Vater, die Väter"."""
            },
            {
                "title": "2. კუთვნილებითი ნაცვალსახელები (Possessivpronomen: mein, dein)",
                "content_ka": """კუთვნილებითი ნაცვალსახელი ეთანხმება იმ საგნის სქესს, რომელიც მას მოსდევს:
• მამრობითი (der) და საშუალო (das):
  - **mein** Vater (ჩემი მამა)
  - **mein** Kind (ჩემი შვილი)
  - **dein** Vater (შენი მამა), **dein** Kind (შენი შვილი)
• მდედრობითი (die) და მრავლობითი (die Plural) - ემატება **-e**:
  - **meine** Mutter (ჩემი დედა)
  - **meine** Eltern (ჩემი მშობლები)
  - **deine** Schwester (შენი და), **deine** Freunde (შენი მეგობრები)"""
            },
            {
                "title": "3. რიცხვები 0-დან 100-მდე (Zahlen von 0 bis 100)",
                "content_ka": """• 0-12: null, eins, zwei, drei, vier, fünf, sechs, sieben, acht, neun, zehn, elf, zwölf.
• 13-19: dreizehn, vierzehn, fünfzehn, sechzehn (s აკლდება), siebzehn (en აკლდება), achtzehn, neunzehn.
• ათეულები (ბოლოვდება -zig-ზე): zwanzig (20), dreißig (30 - ß-ით!), vierzig (40), fünfzig (50), sechzig (60), siebzig (70), achtzig (80), neunzig (90), (ein)hundert (100).
• **21-99 რთული რიცხვები:** გერმანელები ჯერ ამბობენ ერთეულს, მერე "და"-ს (und), მერე ათეულს!
  - 21 = einundzwanzig (ერთი-და-ოცი)
  - 35 = fünfunddreißig (ხუთი-და-ოცდაათი)
  - 48 = achtundvierzig
  - 99 = neunundneunzig"""
            }
        ],
        "dialogues": [
            {
                "speaker": "Lukas",
                "text_de": "Hallo Giorgi, wer ist das auf dem Foto?",
                "text_ka": "გამარჯობა გიორგი, ვინ არის ეს ფოტოზე?"
            },
            {
                "speaker": "Giorgi",
                "text_de": "Das ist meine Familie. Das hier sind mein Vater und meine Mutter.",
                "text_ka": "ეს ჩემი ოჯახია. აი ესენი არიან ჩემი მამა და ჩემი დედა."
            },
            {
                "speaker": "Lukas",
                "text_de": "Und hast du auch Geschwister?",
                "text_ka": "და დედმამიშვილებიც გყავს?"
            },
            {
                "speaker": "Giorgi",
                "text_de": "Ja, ich habe einen Bruder und eine Schwester. Mein Bruder heißt Nika und ist 19 Jahre alt.",
                "text_ka": "დიახ, მყავს ერთი ძმა და ერთი და. ჩემს ძმას ნიკა ჰქვია და 19 წლისაა."
            },
            {
                "speaker": "Lukas",
                "text_de": "Sehr schön! Sind deine Eltern noch in Tiflis?",
                "text_ka": "ძალიან კარგი! შენი მშობლები ჯერ კიდევ თბილისში არიან?"
            },
            {
                "speaker": "Giorgi",
                "text_de": "Ja, sie leben und arbeiten in Tiflis.",
                "text_ka": "დიახ, ისინი თბილისში ცხოვრობენ და მუშაობენ."
            }
        ],
        "vocabulary_ids": [
            "vater", "mutter", "eltern", "sohn", "tochter", "bruder", "schwester",
            "geschwister", "grossvater", "grossmutter", "grosseltern", "kind",
            "mann", "frau", "freund", "freundin", "familie", "foto", "jahr", "alt"
        ]
    },
    {
        "id": 3,
        "title_de": "Lektion 3: Essen, Trinken & Einkaufen",
        "title_ka": "გაკვეთილი 3: საჭმელი, სასმელი და საყიდლები",
        "icon": "🍎",
        "description_ka": "პროდუქტები, სასმელები, სუპერმარკეტში შოპინგი, განუსაზღვრელი არტიკლი (ein/eine) და უარყოფა (kein/nicht).",
        "grammar_sections": [
            {
                "title": "1. განუსაზღვრელი არტიკლი (Unbestimmter Artikel: ein, eine)",
                "content_ka": """განუსაზღვრელი არტიკლი გამოიყენება მაშინ, როდესაც საგანს ან პიროვნებას პირველად ვახსენებთ, ან ზოგადად ერთ რომელიმე ნივთზე ვსაუბრობთ:
• der -> **ein** (ein Apfel - ერთი ვაშლი)
• das -> **ein** (ein Brot - ერთი პური)
• die -> **eine** (eine Banane - ერთი ბანანი)
• **მრავლობითში განუსაზღვრელი არტიკლი არ არსებობს!**
  - Das ist ein Apfel (მხოლობითი). -> Das sind Äpfel (მრავლობითი - არტიკლის გარეშე)."""
            },
            {
                "title": "2. უარყოფა: kein vs. nicht (ქართველებისთვის უმნიშვნელოვანესი განსხვავება)",
                "content_ka": """ქართულში ყველგან ვიყენებთ "არ"-ს ან "არა"-ს. გერმანულში კი არსებობს მკაცრი დაყოფა:

• **kein / keine** გამოიყენება მხოლოდ **არსებითი სახელის** უარსაყოფად (რომელსაც ჩვეულებრივ ექნებოდა ein ან არაფერი):
  - Das ist **ein** Apfel. -> Das ist **kein** Apfel. (ეს არ არის ვაშლი - მამრობითი/საშუალო)
  - Das ist **eine** Tomate. -> Das ist **keine** Tomate. (ეს არ არის პომიდორი - მდედრობითი)
  - Ich habe **keine** Zeit. (დრო არ მაქვს - განყენებული არსებითი)
  - Ich esse **keine** Äpfel. (ვაშლებს არ ვჭამ - მრავლობითი)

• **nicht** გამოიყენება ყველა სხვა შემთხვევაში (ზმნის, ზედსართავის, საკუთარი სახელის ან განსაზღვრული არტიკლის უარსაყოფად):
  - Ich trinke **nicht**. (არ ვსვამ - ზმნის უარყოფა)
  - Der Kaffee ist **nicht** süß. (ყავა არ არის ტკბილი - ზედსართავი სახელის უარყოფა)
  - Das ist **nicht** Giorgi. (ეს არ არის გიორგი)
  - Das ist **nicht der** Apfel von Anna. (ეს არ არის ანას ვაშლი - განსაზღვრული არტიკლით)"""
            },
            {
                "title": "3. ფასები და ზომის ერთეულები (Preise & Mengen)",
                "content_ka": """• Was kostet das? (რა ღირს ეს?)
• Was kosten die Tomaten? (რა ღირს პომიდვრები?)
• Das kostet 2,50 € (zwei Euro fünfzig).
• ein Kilo Äpfel (ერთი კილო ვაშლი)
• ein Liter Milch (ერთი ლიტრი რძე)
• 500 Gramm Käse (500 გრამი ყველი)
• eine Flasche Wasser (ერთი ბოთლი წყალი)"""
            }
        ],
        "dialogues": [
            {
                "speaker": "Verkäufer",
                "text_de": "Guten Tag! Was möchten Sie, bitte?",
                "text_ka": "გამარჯობა! რას ინებებთ, გეთაყვა?"
            },
            {
                "speaker": "Kunde",
                "text_de": "Guten Tag! Ich brauche ein Kilo Äpfel und ein Brot.",
                "text_ka": "გამარჯობა! მჭირდება ერთი კილო ვაშლი და ერთი პური."
            },
            {
                "speaker": "Verkäufer",
                "text_de": "Möchten Sie auch Käse? Der Käse hier ist sehr frisch.",
                "text_ka": "ყველიც გნებავთ? ეს ყველი აქ ძალიან ახალია."
            },
            {
                "speaker": "Kunde",
                "text_de": "Nein danke, ich brauche keinen Käse. Aber haben Sie Orangensaft?",
                "text_ka": "არა გმადლობთ, ყველი არ მჭირდება. მაგრამ გაქვთ ფორთოხლის წვენი?"
            },
            {
                "speaker": "Verkäufer",
                "text_de": "Ja, natürlich. Hier ist eine Flasche Saft. Das macht zusammen 6 Euro 40.",
                "text_ka": "დიახ, რა თქმა უნდა. აი ერთი ბოთლი წვენი. სულ იქნება 6 ევრო და 40 ცენტი."
            }
        ],
        "vocabulary_ids": [
            "apfel", "banane", "brot", "brotchen", "kase", "fleisch", "fisch",
            "milch", "wasser", "kaffee", "tee", "bier", "wein", "kartoffel",
            "tomate", "ei", "zucker", "salz", "fruhstuck", "mittagessen", "abendessen"
        ]
    },
    {
        "id": 4,
        "title_de": "Lektion 4: Meine Wohnung & Möbel",
        "title_ka": "გაკვეთილი 4: ჩემი ბინა და ავეჯი (აკუზატივი)",
        "icon": "🏠",
        "description_ka": "ბინის აღწერა, ოთახები, ავეჯი და უმნიშვნელოვანესი გრამატიკული თემა: ბრალდებითი ბრუნვა (Akkusativ).",
        "grammar_sections": [
            {
                "title": "1. ბრალდებითი ბრუნვა (Der Akkusativ)",
                "content_ka": """გერმანულში არსებობს 4 ბრუნვა. მეორე ბრუნვაა **Akkusativ** (ბრალდებითი), რომელიც პასუხობს კითხვებზე: **Wen?** (ვის?) და **Was?** (რას?).
გამოიყენება პირდაპირი ობიექტის აღსანიშნავად ისეთი ზმნების შემდეგ, როგორიცაა: *haben* (ქონა), *brauchen* (საჭიროება), *kaufen* (ყიდვა), *sehen* (დანახვა), *suchen* (ძებნა), *finden* (მიჩნევა/პოვნა), *essen* (ჭამა), *trinken* (სმა).

> **დიდი შვება ქართველებისთვის:**
> Akkusativ-ში ფორმას იცვლის **მხოლოდ მამრობითი სქესი (der)**!
> მდედრობითი (die), საშუალო (das) და მრავლობითი (die) უცვლელი რჩება!

• **მამრობითი (Maskulinum):**
  - der Tisch -> **den** Tisch (Ich habe **den** Tisch)
  - ein Tisch -> **einen** Tisch (Ich kaufe **einen** Tisch)
  - kein Tisch -> **keinen** Tisch (Ich habe **keinen** Tisch)
• **საშუალო (Neutrum):**
  - das Bett -> **das** Bett (Ich habe **das** Bett)
  - ein Bett -> **ein** Bett
  - kein Bett -> **kein** Bett
• **მდედრობითი (Femininum):**
  - die Lampe -> **die** Lampe (Ich sehe **die** Lampe)
  - eine Lampe -> **eine** Lampe
  - keine Lampe -> **keine** Lampe
• **მრავლობითი (Plural):**
  - die Stühle -> **die** Stühle
  - keine Stühle -> **keine** Stühle"""
            },
            {
                "title": "2. ოთახები და საცხოვრებელი სივრცე",
                "content_ka": """• die Wohnung (ბინა), das Haus (სახლი), das Zimmer (ოთახი)
• das Wohnzimmer (მისაღები ოთახი / ზალა)
• das Schlafzimmer (საძინებელი ოთახი)
• die Küche (სამზარეულო)
• das Badezimmer / das Bad (სააბაზანო)
• der Flur (დერეფანი / შემოსასვლელი)
• der Balkon (აივანი)"""
            },
            {
                "title": "3. ზედსართავი სახელები ბინის აღსაწერად",
                "content_ka": """როდესაც ზედსართავი სახელი დგას ზმნა sein-ის შემდეგ, ის დაბოლოებას არ იღებს:
• Die Wohnung ist **groß** (დიდი) / **klein** (პატარა).
• Das Zimmer ist **hell** (ნათელი) / **dunkel** (ბნელი).
• Die Miete ist **teuer** (ძვირი) / **billig** (იაფი) / **günstig** (ხელსაყრელი).
• Das Sofa ist **bequem** (მოხერხებული) / **unbequem** (მოუხერხებელი).
• Die Küche ist **modern** (თანამედროვე) / **alt** (ძველი)."""
            }
        ],
        "dialogues": [
            {
                "speaker": "David",
                "text_de": "Giorgi, wie findest du deine neue Wohnung in Berlin?",
                "text_ka": "გიორგი, როგორ მოგწონს შენი ახალი ბინა ბერლინში?"
            },
            {
                "speaker": "Giorgi",
                "text_de": "Sie ist sehr schön und hell! Sie hat zwei Zimmer, eine Küche und einen Balkon.",
                "text_ka": "ძალიან ლამაზი და ნათელია! აქვს ორი ოთახი, სამზარეულო და აივანი."
            },
            {
                "speaker": "David",
                "text_de": "Hast du schon alle Möbel?",
                "text_ka": "უკვე ყველა ავეჯი გაქვს?"
            },
            {
                "speaker": "Giorgi",
                "text_de": "Nein, ich habe ein Bett und einen Schrank, aber ich brauche noch einen Schreibtisch und einen Stuhl.",
                "text_ka": "არა, საწოლი და კარადა მაქვს, მაგრამ კიდევ მჭირდება საწერი მაგიდა და ერთი სკამი."
            },
            {
                "speaker": "David",
                "text_de": "Wir können am Samstag zu IKEA fahren und einen Schreibtisch kaufen!",
                "text_ka": "შაბათს შეგვიძლია IKEA-ში წავიდეთ და საწერი მაგიდა ვიყიდოთ!"
            }
        ],
        "vocabulary_ids": [
            "wohnung", "haus", "zimmer", "kuche", "bad", "schlafzimmer", "wohnzimmer",
            "balkon", "tisch", "stuhl", "bett", "sofa", "schrank", "lampe",
            "teppich", "bild", "gross", "klein", "hell", "dunkel", "teuer", "billig"
        ]
    },
    {
        "id": 5,
        "title_de": "Lektion 5: Mein Tag & Uhrzeit",
        "title_ka": "გაკვეთილი 5: ჩემი დღის რეჟიმი და საათი",
        "icon": "⏰",
        "description_ka": "საათის თქმა (ოფიციალური და სასაუბრო), დღის მონაკვეთები და განცალკევებადი ზმნები (trennbare Verben).",
        "grammar_sections": [
            {
                "title": "1. საათის თქმა (Die Uhrzeit)",
                "content_ka": """გერმანულში საათის კითხვა ორნაირად ისმება:
• **Wie spät ist es?** (რომელი საათია?)
• **Wie viel Uhr ist es?** (რამდენი საათია?)

არსებობს ორი სისტემა:
1. **ოფიციალური დრო (რადიოში, მატარებლის სადგურზე, ტელევიზიაში - 24-საათიანი):**
   - 08:00 = Es ist acht Uhr.
   - 14:15 = Es ist vierzehn Uhr fünfzehn.
   - 19:30 = Es ist neunzehn Uhr dreißig.
   - 20:45 = Es ist zwanzig Uhr fünfundvierzig.

2. **არაფორმალური / სასაუბრო დრო (ყოველდღიურ მეტყველებაში):**
   - **nach** (შემდეგ / გადაცილებული): 08:10 -> Es ist zehn **nach** acht (რვის ათი წუთია).
   - **vor** (აკლია): 07:50 -> Es ist zehn **vor** acht (ათი წუთი აკლია რვას).
   - **Viertel** (მეოთხედი = 15 წუთი):
     - 08:15 -> Es ist **Viertel nach** acht.
     - 08:45 -> Es ist **Viertel vor** neun.
   - **halb** (ნახევარი):
     - 08:30 -> Es ist **halb neun**! (ყურადღება! გერმანულში "halb neun" ნიშნავს, რომ ცხრას აკლია ნახევარი, ანუ 8:30-ია!)."""
            },
            {
                "title": "2. განცალკევებადი ზმნები (Trennbare Verben)",
                "content_ka": """გერმანულ ენას აქვს უნიკალური მოვლენა: გარკვეული წინსართები (Präfixe) უღლებისას სცილდება ზმნას და **გადადის წინადადების სულ ბოლოში**!
ყველაზე გავრცელებული განცალკევებადი წინსართებია: **ab-, an-, auf-, aus-, ein-, mit-, vor-, zu-**.

• **aufstehen** (ადგომა):
  - Ich **stehe** jeden Tag um 7 Uhr **auf**. (მე ყოველდღე 7 საათზე ვდგები.)
• **einkaufen** (საყიდლებზე წასვლა):
  - Wir **kaufen** am Samstag im Supermarkt **ein**.
• **anrufen** (დარეკვა):
  - Er **ruft** seine Mutter **an**.
• **fernsehen** (ტელევიზორის ყურება):
  - Am Abend **sieht** er **fern**."""
            },
            {
                "title": "3. დროის წინდებულები: um, am, im",
                "content_ka": """• **um** გამოიყენება ზუსტ საათთან:
  - **um** 8 Uhr (8 საათზე), **um** wie viel Uhr? (რომელ საათზე?)
• **am** (an + dem) გამოიყენება დღეებთან და დღის მონაკვეთებთან:
  - **am** Montag (ორშაბათს), **am** Wochenende (შაბათ-კვირას)
  - **am** Morgen (დილით), **am** Vormittag, **am** Nachmittag, **am** Abend (საღამოს)
  - *გამონაკლისი:* **in der Nacht** (ღამით).
• **im** (in + dem) გამოიყენება თვეებთან და სეზონებთან:
  - **im** Januar, **im** Sommer, **im** Winter."""
            }
        ],
        "dialogues": [
            {
                "speaker": "Marie",
                "text_de": "Wann stehst du normalerweise auf, Giorgi?",
                "text_ka": "როდის დგები ჩვეულებრივ, გიორგი?"
            },
            {
                "speaker": "Giorgi",
                "text_de": "Ich stehe meistens um halb acht auf. Und du?",
                "text_ka": "უმეტესად რვის ნახევარზე (7:30) ვდგები. შენ?"
            },
            {
                "speaker": "Marie",
                "text_de": "Um sieben Uhr. Dann frühstücke ich und fahre um Viertel nach acht zur Uni.",
                "text_ka": "შვიდ საათზე. მერე ვსაუზმობ და რვის თხუთმეტ წუთზე მივდივარ უნივერსიტეტში."
            },
            {
                "speaker": "Giorgi",
                "text_de": "Was machst du heute Abend? Gehen wir ins Kino?",
                "text_ka": "რას აკეთებ ამ საღამოს? წავიდეთ კინოში?"
            },
            {
                "speaker": "Marie",
                "text_de": "Gerne! Der Film fängt um acht Uhr an. Treffen wir uns um halb acht?",
                "text_ka": "სიამოვნებით! ფილმი იწყება რვა საათზე. შევხვდეთ რვის ნახევარზე (7:30)?"
            }
        ],
        "vocabulary_ids": [
            "uhr", "uhrzeit", "stunde", "minute", "tag", "morgen", "vormittag",
            "mittag", "nachmittag", "abend", "nacht", "woche", "wochenende",
            "aufstehen", "fruhstucken", "arbeiten", "anrufen", "einkaufen", "fernsehen", "schlafen"
        ]
    },
    {
        "id": 6,
        "title_de": "Lektion 6: Freizeit, Hobbys & Modalverben",
        "title_ka": "გაკვეთილი 6: თავისუფალი დრო და მოდალური ზმნები",
        "icon": "⚽",
        "description_ka": "ჰობი, სპორტი, კვირის დღეები და მოდალური ზმნები (können, wollen, möchten).",
        "grammar_sections": [
            {
                "title": "1. მოდალური ზმნები (Modalverben: können, wollen, möchten)",
                "content_ka": """მოდალური ზმნები გამოხატავენ დამოკიდებულებას მოქმედების მიმართ (შესაძლებლობა, სურვილი, ნებართვა).
გაითვალისწინეთ ორი უმთავრესი წესი:
1. **ich და er/sie/es პირებს ყოველთვის აქვთ იდენტური ფორმა და არ აქვთ დაბოლოება!**
2. **წინადადების ჩარჩო (Satzklammer):** მოდალური ზმნა იუღლება და დგას მე-2 ადგილზე, ხოლო მეორე (ძირითადი) ზმნა მიდის **წინადადების სულ ბოლოში ინფინიტივში** (უცვლელ ფორმაში)!

• **können** (შეძლება, უნარი):
  - ich kann, du kannst, er/sie/es kann, wir können, ihr könnt, sie/Sie können
  - *მაგალითად:* Ich **kann** sehr gut Deutsch **sprechen**. (მე შემიძლია ძალიან კარგად გერმანულად ლაპარაკი.)
• **wollen** (მტკიცე ნდომა, გადაწყვეტილება):
  - ich will, du willst, er/sie/es will, wir wollen, ihr wollt, sie/Sie wollen
  - *მაგალითად:* Er **will** heute Fußball **spielen**. (მას უნდა დღეს ფეხბურთი ითამაშოს.)
• **möchten** (სურვილი - "მინდა / მსურს"):
  - ich möchte, du möchtest, er/sie/es möchte, wir möchten, ihr möchtet, sie/Sie möchten
  - *მაგალითად:* Wir **möchten** am Wochenende nach München **fahren**."""
            },
            {
                "title": "2. კვირის დღეები (Wochentage)",
                "content_ka": """ყველა კვირის დღე არის **მამრობითი სქესის (der)** და იხმარება წინდებულით **am**:
• der Montag (ორშაბათი) -> am Montag
• der Dienstag (სამშაბათი) -> am Dienstag
• der Mittwoch (ოთხშაბათი) -> am Mittwoch
• der Donnerstag (ხუთშაბათი) -> am Donnerstag
• der Freitag (პარასკევი) -> am Freitag
• der Samstag / Sonnabend (შაბათი) -> am Samstag
• der Sonntag (კვირა) -> am Sonntag"""
            }
        ],
        "dialogues": [
            {
                "speaker": "Stefan",
                "text_de": "Was machst du in deiner Freizeit, Giorgi?",
                "text_ka": "რას აკეთებ თავისუფალ დროს, გიორგი?"
            },
            {
                "speaker": "Giorgi",
                "text_de": "Ich spiele gern Gitarre und höre Musik. Und ich schwimme am Wochenende.",
                "text_ka": "სიამოვნებით ვუკრავ გიტარაზე და ვუსმენ მუსიკას. და შაბათ-კვირას ვცურავ."
            },
            {
                "speaker": "Stefan",
                "text_de": "Kannst du auch Schach spielen?",
                "text_ka": "ჭადრაკის თამაშიც შეგიძლია?"
            },
            {
                "speaker": "Giorgi",
                "text_de": "Ja, ein bisschen. Mein Großvater hat es mir beigebracht. Willst du eine Partie spielen?",
                "text_ka": "კი, ცოტა. ბაბუაჩემმა მასწავლა. გინდა ერთი პარტია ვითამაშოთ?"
            },
            {
                "speaker": "Stefan",
                "text_de": "Ja, sehr gerne! Am Sonntag habe ich Zeit.",
                "text_ka": "კი, დიდი სიამოვნებით! კვირას მექნება დრო."
            }
        ],
        "vocabulary_ids": [
            "freizeit", "hobby", "sport", "musik", "buch", "kino", "theater",
            "fussball", "schwimmen", "lesen", "horen", "spielen", "tanzen",
            "konnen", "wollen", "mochten", "montag", "dienstag", "mittwoch", "donnerstag", "freitag", "samstag", "sonntag"
        ]
    },
    {
        "id": 7,
        "title_de": "Lektion 7: Unterwegs in der Stadt & Dativ",
        "title_ka": "გაკვეთილი 7: ქალაქში ორიენტაცია და დატივი",
        "icon": "🚇",
        "description_ka": "ქალაქის ობიექტები, ტრანსპორტი, გზის კითხვა და მიცემითი ბრუნვა (Dativ).",
        "grammar_sections": [
            {
                "title": "1. მიცემითი ბრუნვა (Der Dativ)",
                "content_ka": """დატივი გერმანულში პასუხობს კითხვებზე: **Wo?** (სად?) და **Wem?** (ვის?).
ეს არის ერთ-ერთი ყველაზე მნიშვნელოვანი ბრუნვა.

როგორ იცვლება არტიკლები დატივში:
• **მამრობითი (der) -> dem** (der Bahnhof -> **dem** Bahnhof)
• **საშუალო (das) -> dem** (das Hotel -> **dem** Hotel)
• **მდედრობითი (die) -> der** (die Bank -> **der** Bank) - ყურადღება! მდედრობითი ხდება der!
• **მრავლობითი (die) -> den + n** (die Museen -> **den** Museen)

განუსაზღვრელი არტიკლი დატივში:
• der/das -> **einem** (mit **einem** Freund, in **einem** Hotel)
• die -> **einer** (in **einer** Stadt)
• kein -> **keinem** (m/n), **keiner** (f), **keinen ...n** (pl)"""
            },
            {
                "title": "2. წინდებულები, რომლებიც მუდამ Dativ-ს მოითხოვენ",
                "content_ka": """დაიმახსოვრეთ ეს 7 წინდებული - მათ შემდეგ მუდამ დატივი გამოიყენება!
**aus, bei, mit, nach, seit, von, zu**

• **mit** (ტრანსპორტთან ან ადამიანთან):
  - Ich fahre **mit dem** Bus / **mit dem** Zug / **mit der** U-Bahn. (ავტობუსით / მატარებლით / მეტროთი მივდივარ.)
• **zu** (მიმართულება ობიექტისკენ / პირისკენ):
  - zu + dem = **zum** (Ich gehe **zum** Bahnhof / **zum** Arzt)
  - zu + der = **zur** (Ich gehe **zur** Bank / **zur** Post)
• **bei** (ვინმესთან ყოფნა):
  - bei + dem = **beim** (Ich bin **beim** Arzt)."""
            },
            {
                "title": "3. გზის კითხვა და ახსნა (Nach dem Weg fragen)",
                "content_ka": """• Entschuldigung, wo ist der Bahnhof? (უკაცრავად, სად არის სადგური?)
• Wie komme ich zum Museum? (როგორ მივიდე მუზეუმამდე?)
• Gehen Sie **geradeaus**! (იარეთ პირდაპირ!)
• Biegen Sie nach **links** / nach **rechts** ab! (შეუხვიეთ მარცხნივ / მარჯვნივ!)
• Die Bank ist an der Ecke auf der linken Seite. (ბანკი კუთხეშია, მარცხენა მხარეს.)"""
            }
        ],
        "dialogues": [
            {
                "speaker": "Tourist",
                "text_de": "Entschuldigung, wissen Sie, wo die Post ist?",
                "text_ka": "უკაცრავად, ხომ არ იცით, სად არის ფოსტა?"
            },
            {
                "speaker": "Passant",
                "text_de": "Ja, das ist ganz einfach. Gehen Sie hier geradeaus bis zur Kreuzung.",
                "text_ka": "დიახ, ძალიან მარტივია. იარეთ აქ პირდაპირ გზაჯვარედინამდე."
            },
            {
                "speaker": "Tourist",
                "text_de": "Und an der Kreuzung?",
                "text_ka": "და გზაჯვარედინზე?"
            },
            {
                "speaker": "Passant",
                "text_de": "Biegen Sie nach rechts ab. Die Post ist gleich neben der Bank.",
                "text_ka": "შეუხვიეთ მარჯვნივ. ფოსტა პირდაპირ ბანკის გვერდითაა."
            },
            {
                "speaker": "Tourist",
                "text_de": "Vielen Dank für Ihre Hilfe!",
                "text_ka": "დიდი მადლობა თქვენი დახმარებისთვის!"
            }
        ],
        "vocabulary_ids": [
            "stadt", "strasse", "platz", "bahnhof", "flughafen", "hotel", "bank",
            "post", "apotheke", "krankenhaus", "museum", "kirche", "bus", "zug",
            "u_bahn", "taxi", "fahren", "gehen", "fliegen", "geradeaus", "links", "rechts"
        ]
    },
    {
        "id": 8,
        "title_de": "Lektion 8: Beruf, Arbeit & Alltag",
        "title_ka": "გაკვეთილი 8: პროფესია, სამუშაო და მოდალური ზმნა müssen",
        "icon": "💼",
        "description_ka": "პროფესიები, სამუშაო დღე, CV-ს საწყისები და მოდალური ზმნები: müssen (ვალდებულება) და dürfen (ნებართვა).",
        "grammar_sections": [
            {
                "title": "1. პროფესიები და მდედრობითი ფორმა -in",
                "content_ka": """გერმანულში ქალის პროფესიის დასასახელებლად მამრობით ფორმას ემატება სუფიქსი **-in** (და ზოგჯერ უმლაუტი):
• der Lehrer (მასწავლებელი კაცი) -> die Lehrer**in** (მასწავლებელი ქალი)
• der Arzt (ექიმი კაცი) -> die **Ärztin** (ექიმი ქალი)
• der Student (სტუდენტი ბიჭი) -> die Student**in** (სტუდენტი გოგო)
• der Kellner (მიმტანი კაცი) -> die Kellner**in** (მიმტანი ქალი)
• der Verkäufer -> die Verkäufer**in**

მრავლობით რიცხვში მდედრობითი იღებს დაბოლოებას **-innen**:
• die Lehrerinnen, die Ärztinnen, die Studentinnen."""
            },
            {
                "title": "2. მოდალური ზმნები: müssen და dürfen",
                "content_ka": """• **müssen** (აუცილებლობა, ვალდებულება - "უნდა"):
  - ich muss, du musst, er/sie/es muss, wir müssen, ihr müsst, sie/Sie müssen
  - *მაგალითად:* Ich **muss** heute viel **arbeiten**. (მე დღეს ბევრი უნდა ვიმუშაო.)
  - Er **muss** um 6 Uhr **aufstehen**. (ის 6 საათზე უნდა ადგეს.)

• **dürfen** (ნებართვა, უფლება):
  - ich darf, du darfst, er/sie/es darf, wir dürfen, ihr dürft, sie/Sie dürfen
  - უარყოფასთან ერთად (**nicht dürfen**) ნიშნავს მკაცრ აკრძალვას!
  - *მაგალითად:* Hier **darf** man **nicht** rauchen! (აქ მოწევა აკრძალულია / არ შეიძლება!)"""
            },
            {
                "title": "3. წინდებულები პროფესიებთან: als, bei, seit",
                "content_ka": """• **als** (როგორც): Ich arbeite **als** Programmierer / **als** Arzt.
• **bei** (+ Dativ) (კომპანიასთან): Ich arbeite **bei** Siemens / **bei** BMW.
• **seit** (+ Dativ) (რა დროიდანაც / უკვე რამდენი ხანია): Ich arbeite **seit einem** Jahr hier."""
            }
        ],
        "dialogues": [
            {
                "speaker": "Klara",
                "text_de": "Was bist du von Beruf, Giorgi?",
                "text_ka": "რა პროფესიის ხარ, გიორგი?"
            },
            {
                "speaker": "Giorgi",
                "text_de": "Ich bin Informatiker. Und ich arbeite als Softwareentwickler bei einer Firma.",
                "text_ka": "მე ინფორმატიკოსი ვარ. და ვმუშაობ პროგრამულ დეველოპერად ერთ ფირმაში."
            },
            {
                "speaker": "Klara",
                "text_de": "Macht dir die Arbeit Spaß?",
                "text_ka": "სამსახური გსიამოვნებს?"
            },
            {
                "speaker": "Giorgi",
                "text_de": "Ja, sehr! Aber manchmal muss ich Überstunden machen und am Wochenende arbeiten.",
                "text_ka": "კი, ძალიან! მაგრამ ზოგჯერ მიწევს ზეგანაკვეთურად მუშაობა და შაბათ-კვირას მუშაობა."
            }
        ],
        "vocabulary_ids": [
            "beruf", "arbeit", "chef", "kollege", "kollegin", "arzt", "arztin",
            "lehrer", "lehrerin", "student", "studentin", "informatiker", "kellner",
            "mussen", "durfen", "arbeiten", "verdienen", "geld", "zeit", "stunde"
        ]
    },
    {
        "id": 9,
        "title_de": "Lektion 9: Körper, Gesundheit & Imperativ",
        "title_ka": "გაკვეთილი 9: სხეული, ჯანმრთელობა და ბრძანებითი კილო",
        "icon": "🩺",
        "description_ka": "სხეულის ნაწილები, ექიმთან ვიზიტი, ტკივილის გამოხატვა, ბრძანებითი კილო (Imperativ) და მოდალური ზმნა sollen.",
        "grammar_sections": [
            {
                "title": "1. სხეულის ნაწილები და ტკივილი (Schmerzen)",
                "content_ka": """გერმანულში ტკივილის გამოხატვა ორი ძირითადი გზით ხდება:
1. **... tut weh / ... tun weh** (მტკივა):
   - Mein Kopf **tut weh**. (თავი მტკივა - მხოლობითი)
   - Meine Augen **tun weh**. (თვალები მტკივა - მრავლობითი)
2. **Kopfschmerzen / Bauchschmerzen haben** (ტკივილის ქონა):
   - Ich habe Kopfschmerzen. (თავის ტკივილი მაქვს)
   - Er hat Halsschmerzen. (ყელის ტკივილი აქვს)
   - Sie hat Fieber. (სიცხე აქვს)"""
            },
            {
                "title": "2. ბრძანებითი კილო (Der Imperativ)",
                "content_ka": """ბრძანებითი კილო გამოიყენება თხოვნის, რჩევის ან ბრძანების მისაცემად.
გერმანულში 3 ძირითადი ფორმაა:

1. **du-ფორმა (შენობით):**
   იღება ზმნის du-ფორმიდან და აკლდება **du** და დაბოლოება **-st**!
   - du kommst -> **Komm!** (მოდი!)
   - du machst -> **Mach!** (გააკეთე!)
   - du trinkst -> **Trink viel Wasser!** (დალიე ბევრი წყალი!)
   - *ყურადღება:* თუ ზმნას აქვს e->i ცვლილება, ეს რჩება: du sprichst -> **Sprich!** (ილაპარაკე!). მაგრამ უმლაუტი a->ä არ გამოიყენება: du fährst -> **Fahr!**

2. **ihr-ფორმა (თქვენობით - ბავშვებთან/მეგობრებთან):**
   ზუსტად ზმნის ihr-ფორმაა, ოღონდ ნაცვალსახელი ihr აღარ იწერება!
   - ihr kommt -> **Kommt!** (მოდით!)
   - ihr macht -> **Macht die Hausaufgabe!** (გააკეთეთ საშინაო დავალება!)

3. **Sie-ფორმა (თავაზიანი ფორმა):**
   ინფინიტივს ემატება Sie (ოღონდ შებრუნებული თანმიმდევრობით):
   - **Kommen Sie bitte!** (მობრძანდით, გეთაყვა!)
   - **Trinken Sie den Tee!** (დალიეთ ჩაი!)
   - *გამონაკლისი:* sein -> **Seien Sie ruhig!** (იყავით მშვიდად!)."""
            },
            {
                "title": "3. მოდალური ზმნა sollen (რჩევა / ექიმის მითითება)",
                "content_ka": """ზმნა **sollen** გამოიყენება მაშინ, როდესაც ვიღაც (მაგ. ექიმი) გვაძლევს რჩევას ან დავალებას:
• ich soll, du sollst, er/sie/es soll, wir sollen, ihr sollt, sie/Sie sollen
• Der Arzt sagt: Sie **sollen** im Bett **bleiben** und Tabletten **nehmen**. (ექიმი ამბობს: თქვენ ლოგინში უნდა დარჩეთ და აბები მიიღოთ.)"""
            }
        ],
        "dialogues": [
            {
                "speaker": "Arzt",
                "text_de": "Guten Tag, Herr Beridze. Was fehlt Ihnen denn?",
                "text_ka": "გამარჯობა, ბატონო ბერიძე. რა გაწუხებთ?"
            },
            {
                "speaker": "Giorgi",
                "text_de": "Guten Tag, Herr Doktor. Ich fühle mich nicht gut. Mein Kopf tut sehr weh und ich habe Husten.",
                "text_ka": "გამარჯობა, ექიმო. თავს კარგად არ ვგრძნობ. თავი ძალიან მტკივა და ხველა მაქვს."
            },
            {
                "speaker": "Arzt",
                "text_de": "Haben Sie auch Fieber?",
                "text_ka": "სიცხეც გაქვთ?"
            },
            {
                "speaker": "Giorgi",
                "text_de": "Ja, heute Morgen hatte ich 38,5 Grad.",
                "text_ka": "დიახ, დღეს დილით 38.5 მქონდა."
            },
            {
                "speaker": "Arzt",
                "text_de": "Sie haben eine Grippe. Bleiben Sie drei Tage im Bett und nehmen Sie diese Medikamente!",
                "text_ka": "გრიპი გაქვთ. დარჩით სამი დღე ლოგინში და მიიღეთ ეს მედიკამენტები!"
            }
        ],
        "vocabulary_ids": [
            "korper", "kopf", "auge", "ohr", "nase", "mund", "hals", "arm",
            "hand", "bauch", "bein", "fuss", "schmerz", "fieber", "husten",
            "medikament", "tablette", "krank", "gesund", "bleiben", "sollen"
        ]
    },
    {
        "id": 10,
        "title_de": "Lektion 10: Im Urlaub & Das Perfekt",
        "title_ka": "გაკვეთილი 10: შვებულება და წარსული დრო (Das Perfekt)",
        "icon": "🏖️",
        "description_ka": "A1-ის გვირგვინი: წარსული დრო (Perfekt) - როგორ მოვყვეთ წარსულ ამბებზე haben და sein დამხმარე ზმნებით.",
        "grammar_sections": [
            {
                "title": "1. წარსული დრო (Das Perfekt) - სტრუქტურა",
                "content_ka": """გერმანულ სასაუბრო ენაში წარსული მოვლენების გადმოსაცემად უმეტესად გამოიყენება **Perfekt**.
მისი ფორმულაა:
**haben / sein** (აწმყოში უღლებული მე-2 ადგილზე) + ... + **Partizip II** (წინადადების სულ ბოლოს!).

*მაგალითად:*
• Ich **habe** gestern ein Buch **gekauft**. (მე გუშინ წიგნი ვიყიდე.)
• Wir **sind** nach Berlin **gefahren**. (ჩვენ ბერლინში გავემგზავრეთ.)"""
            },
            {
                "title": "2. დამხმარე ზმნის არჩევა: haben თუ sein?",
                "content_ka": """ეს არის ქართველებისთვის ყველაზე საკვანძო წესი:

• **sein გამოიყენება მხოლოდ მაშინ, როდესაც ზმნა გამოხატავს:**
  1. **ადგილმდებარეობის შეცვლას (გადაადგილებას A წერტილიდან B-ში):**
     *gehen* (წასვლა ფეხით) -> ist gegangen
     *fahren* (მგზავრობა) -> ist gefahren
     *fliegen* (ფრენა) -> ist geflogen
     *kommen* (მოსვლა) -> ist gekommen
     *reisen* (მოგზაურობა) -> ist gereist
  2. **მდგომარეობის შეცვლას:**
     *aufstehen* (ადგომა) -> ist aufgestanden
     *einschlafen* (ჩაძინება) -> ist eingeschlafen
  3. **გამონაკლისები:**
     *bleiben* (დარჩენა) -> ist geblieben
     *sein* (ყოფნა) -> ist gewesen

• **haben გამოიყენება ყველა სხვა შემთხვევაში (ზმნების 90%):**
  - Ich habe gemacht, gearbeitet, gegessen, getrunken, gelernt, gelesen, geschlafen..."""
            },
            {
                "title": "3. Partizip II-ის წარმოება (როგორ ვაწარმოოთ ზმნის მე-3 ფორმა)",
                "content_ka": """1. **რეგულარული (სუსტი) ზმნები:**
   **ge- + ფუძე + -t**
   - machen -> **ge**mach**t**
   - lernen -> **ge**lern**t**
   - kaufen -> **ge**kauf**t**

2. **არარეგულარული (ძლიერი) ზმნები:**
   **ge- + შეცვლილი ფუძე + -en**
   - trinken -> **ge**trunk**en**
   - essen -> **ge**gess**en**
   - schreiben -> **ge**schrieb**en**
   - sehen -> **ge**seh**en**

3. **განცალკევებადი ზმნები:** **ge-** ჯდება წინსართსა და ფუძეს შორის!
   - aufstehen -> auf**ge**standen
   - einkaufen -> ein**ge**kauft

4. **ზმნები, რომლებიც ბოლოვდება -ieren-ზე:** **არ იღებენ ge-ს!**
   - studieren -> studier**t**
   - telefonieren -> telefonier**t**."""
            }
        ],
        "dialogues": [
            {
                "speaker": "Sophie",
                "text_de": "Hallo Giorgi! Wie war dein Urlaub?",
                "text_ka": "გამარჯობა გიორგი! როგორი იყო შენი შვებულება?"
            },
            {
                "speaker": "Giorgi",
                "text_de": "Hallo Sophie! Es war fantastisch! Ich bin nach Wien geflogen und habe dort fünf Tage verbracht.",
                "text_ka": "გამარჯობა სოფი! ფანტასტიკური იყო! ვენაში გავფრინდი და იქ ხუთი დღე გავატარე."
            },
            {
                "speaker": "Sophie",
                "text_de": "Toll! Was hast du in Wien gemacht?",
                "text_ka": "მაგარია! რა გააკეთე ვენაში?"
            },
            {
                "speaker": "Giorgi",
                "text_de": "Ich habe viele Museen besucht, Sachertorte gegessen und die Stadt besichtigt.",
                "text_ka": "ბევრი მუზეუმი მოვინახულე, ზახერტორტი ვჭამე და ქალაქი დავათვალიერე."
            },
            {
                "speaker": "Sophie",
                "text_de": "Hast du auch Souvenirs gekauft?",
                "text_ka": "სუვენირებიც იყიდე?"
            },
            {
                "speaker": "Giorgi",
                "text_de": "Ja, ich habe Schokolade für meine Familie in Georgien gekauft!",
                "text_ka": "დიახ, შოკოლადი ვიყიდე ჩემი ოჯახისთვის საქართველოში!"
            }
        ],
        "vocabulary_ids": [
            "urlaub", "reise", "meer", "strand", "berge", "hotel", "koffer",
            "pass", "flugzeug", "ticket", "reisen", "fliegen", "bleiben",
            "besuchen", "sehen", "essen", "trinken", "kaufen", "gestern", "heute", "morgen"
        ]
    }
]

print(f"Loaded {len(lessons)} comprehensive lessons.")
