from app.services.translator import translate

# Highly localized knowledge base for supported crops in CropGuard AI v13.
# Diseases are indexed by their standardized English disease name.
KNOWLEDGE_BASE = {   'Apple Black Rot': {   'en': {   'causes': ['Botryosphaeria obtusa fungus', 'Dead wood and warm, wet conditions'],
                                     'display_name': 'Apple Black Rot',
                                     'prevention': [   'Remove mummified fruit and dead branches from the orchard',
                                                       'Avoid pruning wounds during wet weather'],
                                     'symptoms': [   'Frogeye leaf spots with purple borders',
                                                     'Sunken reddish-brown cankers on bark',
                                                     'Rotting fruit with concentric rings of black pustules'],
                                     'treatments': [   'Prune and burn infected twigs and cankered branches',
                                                       'Spray Copper Hydroxide or Thiophanate-methyl weekly']},
                           'hi': {   'causes': [   'बोट्रियोस्फेरिया ओबटुसा कवक',
                                                   'सूखी लकड़ी और गर्म, आर्द्र परिस्थितियां'],
                                     'display_name': 'सेब का काला सड़न रोग',
                                     'prevention': [   'बगीचे से सड़े-सूखे फलों और सूखी शाखाओं को हटा दें',
                                                       'गीले मौसम में छंटाई करने से बचें'],
                                     'symptoms': [   'बैंगनी किनारों के साथ मेंढक की आंख जैसे पत्ती के धब्बे',
                                                     'छाल पर धंसे हुए लाल-भूरे रंग के घाव (कैंकर)',
                                                     'काले दानों के संकेंद्रित छल्लों के साथ सड़ते हुए फल'],
                                     'treatments': [   'संक्रमित टहनियों और घाव वाली शाखाओं को काटकर जला दें',
                                                       'कॉपर हाइड्रॉक्साइड या थियोफैनेट-मिथाइल का साप्ताहिक छिड़काव '
                                                       'करें']},
                           'te': {   'causes': [   'బోట్రియోస్ఫేరియా ఒబ్టుసా శిలీంద్రం',
                                                   'ఎండిన కొమ్మలు మరియు వేడి, తడి వాతావరణ పరిస్థితులు'],
                                     'display_name': 'ఆపిల్ నల్ల కుళ్లు వ్యాధి',
                                     'prevention': [   'ఎండిపోయిన పండ్లను మరియు ఎండిన కొమ్మలను తోట నుండి తొలగించండి',
                                                       'తడి వాతావरणంలో కొమ్మలను కత్తిరించవద్దు'],
                                     'symptoms': [   'ఊదా రంగు అంచులతో కూడిన కప్ప కన్ను వంటి ఆకు మచ్చలు',
                                                     'చెట్టు బెరడుపై కుంగిపోయిన ఎరుపు-గోధుమ రంగు పుండ్లు',
                                                     'నల్లటి బొబ్బలతో కుళ్ళిపోయే పండ్లు'],
                                     'treatments': [   'వ్యాధి సోకిన కొమ్మలను కత్తిరించి కాల్చివేయండి',
                                                       'వారానికి ఒకసారి కాపర్ హైడ్రాక్సైడ్ లేదా థియోఫానేట్-మిథైల్ '
                                                       'పిచికారీ చేయండి']}},
    'Apple Cedar Rust': {   'en': {   'causes': [   'Gymnosporangium juniperi-virginianae fungus',
                                                    'Alternate hosts (Apple & Red Cedar trees) near each other'],
                                      'display_name': 'Apple Cedar Rust',
                                      'prevention': [   'Avoid planting apple trees near red cedar trees',
                                                        'Remove cedar galls in late winter before they release spores'],
                                      'symptoms': [   'Bright orange-yellow spots on upper leaf surfaces',
                                                      'Tubular structures (aecia) on leaf undersides',
                                                      'Deformed orange growths on cedar tree hosts'],
                                      'treatments': [   'Spray Myclobutanil 10 WP at 1g/L at bloom',
                                                        'Use Mancozeb 75 WP at pink bud stage']},
                            'hi': {   'causes': [   'जिमनोस्पोरैंजियम जुनिपेरी-वर्जिनियाने कवक',
                                                    'सेब और लाल देवदार के पेड़ एक-दूसरे के पास होना'],
                                      'display_name': 'सेब का देवदार जंग रोग',
                                      'prevention': [   'लाल देवदार के पेड़ों के पास सेब के पेड़ लगाने से बचें',
                                                        'सर्दियों के अंत में देवदार की गांठों को हटा दें'],
                                      'symptoms': [   'पत्तियों की ऊपरी सतह पर चमकीले नारंगी-पीले धब्बे',
                                                      'पत्तियों के निचले हिस्से पर नलीदार संरचनाएं',
                                                      'देवदार के पेड़ों पर नारंगी रंग की गांठें'],
                                      'treatments': [   'फूल आने पर माइक्लोबुटानिल 10 WP @ 1 ग्राम/लीटर का छिड़काव '
                                                        'करें',
                                                        'गुलाबी कली की अवस्था में मैंकोजेब 75 WP का प्रयोग करें']},
                            'te': {   'causes': [   'జిమ్నోస్పోరాంజియం జునిపెరి-వర్జీనియాని శిలీంద్రం',
                                                    'ఆపిల్ మరియు సిడార్ చెట్లు పక్కపక్కనే ఉండటం'],
                                      'display_name': 'ఆపిల్ సిడార్ రస్ట్ వ్యాధి',
                                      'prevention': [   'సిడార్ చెట్ల సమీపంలో ఆపిల్ చెట్లను నాటడం నివారించండి',
                                                        'శీతాకాలం చివరలో సిడార్ చెట్ల గడ్డలను తొలగించండి'],
                                      'symptoms': [   'ఆకు పైభాగంలో ప్రకాశవంతమైన నారింజ-పసుపు మచ్చలు',
                                                      'ఆకు వెనుక భాగంలో గొట్టాల వంటి నిర్మాణాలు',
                                                      'సిడార్ చెట్లపై నారింజ రంగు గడ్డలు'],
                                      'treatments': [   'పూత సమయంలో మైక్లోబుటానిల్ 10 WP ని లీటరు నీటికి 1 గ్రా కలిపి '
                                                        'పిచికారీ చేయండి',
                                                        'మొగ్గ దశలో మాంకోజెబ్ 75 WP వాడండి']}},
    'Apple Scab': {   'en': {   'causes': [   'Venturia inaequalis fungus',
                                              'Cool, wet spring weather and damp fallen leaves'],
                                'display_name': 'Apple Scab',
                                'prevention': [   'Rake and destroy fallen leaves in autumn',
                                                  'Prune tree canopy to improve airflow and sunlight'],
                                'symptoms': [   'Olive-green to brown velvety spots on leaves',
                                                'Leaves turn yellow and drop early',
                                                'Deformed or cracked fruit with scabby spots'],
                                'treatments': [   'Apply Captan 50 WP at 2g/L or Mancozeb 75 WP at 2g/L',
                                                  'Apply systemic fungicides like Tebuconazole 250 EC']},
                      'hi': {   'causes': ['वेन्चुरिया इनइक्वलिस कवक', 'ठंडा, गीला वसंत मौसम और नम गिरी हुई पत्तियां'],
                                'display_name': 'सेब का पपड़ी रोग (स्कैब)',
                                'prevention': [   'पतझड़ में गिरी हुई पत्तियों को इकट्ठा कर नष्ट करें',
                                                  'हवा और धूप के लिए पेड़ की छंटाई करें'],
                                'symptoms': [   'पत्तियों पर जैतून-हरे से भूरे रंग के मखमली धब्बे',
                                                'पत्तियां पीली होकर जल्दी गिर जाती हैं',
                                                'खुरदुरे धब्बों वाले विकृत या फटे हुए फल'],
                                'treatments': [   'कैप्टन 50 WP @ 2 ग्राम/लीटर या मैंकोजेब 75 WP @ 2 ग्राम/लीटर का '
                                                  'छिड़काव करें',
                                                  'टेबुकोनाज़ोल 250 EC जैसे प्रणालीगत कवकनाशी का उपयोग करें']},
                      'te': {   'causes': [   'వెంచురియా ఇనెక్వాలిస్ శిలీంద్రం',
                                              'చల్లని, తడి వసంత వాతావరణం మరియు నేలపై పడి ఉన్న ఆకులు'],
                                'display_name': 'ఆపిల్ స్కాబ్ వ్యాధి',
                                'prevention': [   'శరదృతువులో రాలిన ఆకులను సేకరించి నాశనం చేయండి',
                                                  'గాలి, వెలుతురు కోసం చెట్టు కొమ్మలను కత్తిరించండి'],
                                'symptoms': [   'ఆకులపై ఆలివ్-ఆకుపచ్చ నుండి గోధుమ రంగు వెల్వెట్ మచ్చలు',
                                                'ఆకులు పసుపు రంగులోకి మారి త్వరగా రాలిపోతాయి',
                                                'మచ్చలతో కూడిన వికృతమైన లేదా పగిలిన పండ్లు'],
                                'treatments': [   'కాప్టాన్ 50 WP ని లీటరు నీటికి 2 గ్రా లేదా మాంకోజెబ్ 75 WP ని 2 '
                                                  'గ్రా కలిపి పిచికారీ చేయండి',
                                                  'టెబుకోనజోల్ 250 EC వంటి ద్రవ శిలీంద్రనాశకాలను వాడండి']}},
    'Chilli Bacterial Spot': {   'en': {   'causes': [   'Xanthomonas campestris pv. vesicatoria bacterium',
                                                         'Warm, humid weather and contaminated seeds'],
                                           'display_name': 'Chilli Bacterial Spot',
                                           'prevention': [   'Treat seeds with hot water before planting',
                                                             'Rotate crops for at least 2 years with non-solanaceous '
                                                             'crops'],
                                           'symptoms': [   'Small, water-soaked spots on leaves that turn dark brown',
                                                           'Spots have raised light brown centers on leaf undersides',
                                                           'Leaves turn yellow and shed, exposing fruit to sunscald'],
                                           'treatments': [   'Spray Copper Oxychloride 50 WP at 3g/L + Streptocycline '
                                                             '1g/10L',
                                                             'Spray Copper Hydroxide weekly in wet periods']},
                                 'hi': {   'causes': [   'जैंथोमोनास कैम्पस्ट्रिस जीवाणु',
                                                         'गर्म, आर्द्र मौसम और दूषित बीज'],
                                           'display_name': 'मिर्च का जीवाणु धब्बा रोग',
                                           'prevention': [   'बोने से पहले बीजों का गर्म पानी से उपचार करें',
                                                             'गैर-सोलेनेसी फसलों के साथ कम से कम 2 साल का फसल चक्र '
                                                             'अपनाएं'],
                                           'symptoms': [   'पत्तियों पर छोटे, जलाक्रांत धब्बे जो गहरे भूरे रंग के हो '
                                                           'जाते हैं',
                                                           'पत्तियों के निचले हिस्से पर उभरे हुए हल्के भूरे केंद्र '
                                                           'वाले धब्बे',
                                                           'पत्तियां पीली होकर गिर जाती हैं, जिससे फल धूप से झुलस जाते '
                                                           'हैं'],
                                           'treatments': [   'कॉपर ऑक्सीक्लोराइड 50 WP @ 3 ग्राम/लीटर + '
                                                             'स्ट्रेप्टोसाइक्लिन 1 ग्राम/10 लीटर का छिड़काव करें',
                                                             'गीले समय में साप्ताहिक रूप से कॉपर हाइड्रॉक्साइड का '
                                                             'छिड़काव करें']},
                                 'te': {   'causes': [   'జాంతోమోనాస్ క్యాంపెస్ట్రిస్ బ్యాక్టీరియా',
                                                         'వేడి, తేమతో కూడిన వాతావరణం మరియు సోకిన విత్తనాలు'],
                                           'display_name': 'మిరప బ్యాక్టీరియల్ మచ్చ వ్యాధి',
                                           'prevention': [   'నాటడానికి ముందు వేడి నీటితో విత్తన శుద్ధి చేయండి',
                                                             'టమోటా, బంగాళాదుంప కాకుండా ఇతర పంటలతో 2 సంవత్సరాల '
                                                             'మార్పిడి చేయండి'],
                                           'symptoms': [   'ఆకులపై చిన్న నీటి మచ్చలు ఏర్పడి నల్లగా మారడం',
                                                           'ఆకుల కింది భాగంలో ఉబ్బిన గోధుమ రంగు మచ్చలు కనిపించడం',
                                                           'ఆకులు పసుపు రంగులోకి మారి రాలిపోవడం మరియు కాయలపై మచ్చలు'],
                                           'treatments': [   'కాపర్ ఆక్సిక్లోరైడ్ 50 WP ని 3 గ్రా + స్ట్రెప్టోసైక్లిన్ '
                                                             '1 గ్రా చొప్పున 10 లీటర్ల నీటికి కలిపి పిచికారీ చేయండి',
                                                             'తడి కాలంలో ప్రతి వారం కాపర్ హైడ్రాక్సైడ్ వాడండి']}},
    'Cotton Bacterial Blight': {   'en': {   'causes': [   'Xanthomonas citri subsp. malvacearum bacterium',
                                                           'High humidity and overhead splashing water'],
                                             'display_name': 'Cotton Bacterial Blight',
                                             'prevention': [   'Use acid-delinted disease-free seed',
                                                               'Incorporate crop residues deeply',
                                                               'Avoid late season overhead irrigation'],
                                             'symptoms': [   'Angular water-soaked spots on leaves turning brown',
                                                             'Black cankers on stems (blackarm phase)',
                                                             'Water-soaked lesions on bolls leading to boll rot'],
                                             'treatments': [   'Spray Streptocycline at 0.1g/L and Copper Oxychloride '
                                                               'at 2.5g/L',
                                                               'Apply bio-bactericide formulations']},
                                   'hi': {   'causes': [   'जैंथोमोनास सिट्री जीवाणु',
                                                           'उच्च आर्द्रता और छिटकते पानी की बूंदें'],
                                             'display_name': 'कपास का जीवाणु झुलसा रोग',
                                             'prevention': [   'एसिड-डिलिंटेड रोगमुक्त बीजों का उपयोग करें',
                                                               'फसल अवशेषों को गहराई से दबाएं'],
                                             'symptoms': [   'पत्तियों पर कोणीय पानी से लथपथ धब्बे जो भूरे रंग के हो '
                                                             'जाते हैं',
                                                             'तनों पर काले घाव',
                                                             'कपास के गोलों पर सड़न'],
                                             'treatments': [   'कॉपर ऑक्सीक्लोराइड @ 2.5 ग्राम/लीटर के साथ '
                                                               'स्ट्रेप्टोसाइक्लिन @ 0.1 ग्राम/लीटर का छिड़काव करें']},
                                   'te': {   'causes': [   'జాంతోమోనాస్ సిట్రీ సబ్\u200cస్పీషిస్ మాల్వేసియారమ్ '
                                                           'బాక్టీరియా',
                                                           'అధిక తేమ మరియు వర్షపు జల్లుల నీరు చిమ్మడం'],
                                             'display_name': 'పత్తి బాక్టీరియా నల్ల మచ్చ తెగులు',
                                             'prevention': [   'యాసిడ్-డీలింట్ చేసిన రోగరహిత విత్తనాలను వాడండి',
                                                               'పంట వ్యర్థాలను లోతుగా దున్నండి'],
                                             'symptoms': [   'ఆకులపై కోణీయ ఆకారంలో నీటితో నిండిన గోధుమ రంగు మచ్చలు',
                                                             'కాండంపై నల్లటి పుండ్లు',
                                                             'పత్తి కాయలపై నీటితో నిండిన మచ్చలు మరియు కాయ కుళ్లు'],
                                             'treatments': [   'స్ట్రెప్టోసైక్లిన్ 0.1 గ్రా మరియు కాపర్ ఆక్సిక్లోరైడ్ '
                                                               '2.5 గ్రా లీటరు నీటికి కలిపి పిచికారీ చేయండి']}},
    'Cotton Leaf Curl Virus': {   'en': {   'causes': [   'Cotton Leaf Curl Virus (Begomovirus) transmitted by '
                                                          'Whitefly vector'],
                                            'display_name': 'Cotton Leaf Curl Virus',
                                            'prevention': [   'Sow resistant cotton hybrids',
                                                              'Remove alternative hosts and weed reservoirs',
                                                              'Maintain field borders clean'],
                                            'symptoms': [   'Upward and downward curling of leaf margins',
                                                            'Thickening of leaf veins',
                                                            'Stunted plants and reduced boll size'],
                                            'treatments': [   'Control Whiteflies: Spray Imidacloprid 17.8 SL at '
                                                              '0.3ml/L or Acetamiprid 20 SP at 0.2g/L',
                                                              'Apply organic neem oil spray 1.5%']},
                                  'hi': {   'causes': ['सफेद मक्खी द्वारा फैलाया जाने वाला कॉटन लीफ कर्ल वायरस'],
                                            'display_name': 'कपास का पत्ती मरोड़ रोग',
                                            'prevention': [   'रोग प्रतिरोधी संकर किस्मों को बोएं',
                                                              'वैकल्पिक खरपतवार मेजबानों को हटा दें'],
                                            'symptoms': [   'पत्ती के किनारों का ऊपर और नीचे की ओर मुड़ना',
                                                            'पत्ती की शिराओं का मोटा होना',
                                                            'बौने पौधे और छोटे गोले'],
                                            'treatments': [   'सफेद मक्खियों का नियंत्रण: इमिडाक्लोप्रिड 17.8 SL @ 0.3 '
                                                              'मिली/लीटर का छिड़काव करें',
                                                              'नीम के तेल 1.5% का उपयोग करें']},
                                  'te': {   'causes': ['తెల్లదోమ ద్వారా వ్యాపించే పత్తి ఆకు ముడుత వైరస్ (బెగోమోవైరస్)'],
                                            'display_name': 'పత్తి ఆకు ముడుత వైరస్ తెగులు',
                                            'prevention': [   'తెగులును తట్టుకునే రకాల హైబ్రిడ్ పత్తిని నాటండి',
                                                              'వైరస్ నిలిచే కలుపు మొక్కలను నివారించండి'],
                                            'symptoms': [   'ఆకు అంచులు పైకి లేదా క్రిందికి ముడుచుకుపోవడం',
                                                            'ఆకు ఈనెలు లావుగా మారడం',
                                                            'మొక్కలు ఎదుగకుండా గిడసబారిపోవడం మరియు చిన్న కాయలు కావడం'],
                                            'treatments': [   'తెల్లదోమ నివారణకు: ఇమిడాక్లోప్రిడ్ 17.8 SL ని లీటరు '
                                                              'నీటికి 0.3 మి.లీ లేదా ఎసిటామిప్రిడ్ 20 SP ని 0.2 గ్రా '
                                                              'కలిపి పిచికారీ చేయండి',
                                                              '1.5% సేంద్రీయ వేప నూనె పిచికారీ చేయండి']}},
    'Cotton Verticillium Wilt': {   'en': {   'causes': [   'Verticillium dahliae fungus surviving in soil',
                                                            'Cool, damp weather and high soil pH'],
                                              'display_name': 'Cotton Verticillium Wilt',
                                              'prevention': [   'Rotate crops with non-hosts like maize',
                                                                'Maintain proper potash fertilizer levels',
                                                                'Avoid waterlogging'],
                                              'symptoms': [   'Tiger-stripe pattern of chlorosis and necrosis between '
                                                              'leaf veins',
                                                              'Sudden wilting of foliage starting from bottom leaves',
                                                              'Vascular browning inside cut stems'],
                                              'treatments': [   'Drench soil with Carbendazim 50 WP at 2g/L',
                                                                'Apply Trichoderma viride bio-fungicide']},
                                    'hi': {   'causes': ['मिट्टी में रहने वाला वर्टिसिलियम डाहलिया कवक'],
                                              'display_name': 'कपास का विल्ट (सूखा) रोग',
                                              'prevention': [   'मक्का जैसी गैर-मेजबान फसलों के साथ फसल चक्र अपनाएं',
                                                                'जलभराव से बचें'],
                                              'symptoms': [   'पत्ती की शिराओं के बीच पीलापन और झुलसा',
                                                              'नीचे की पत्तियों से शुरू होकर पूरे पौधे का सूखना',
                                                              'तने के अंदर भूरापन'],
                                              'treatments': [   'कार्बेन्डाजिम 50 WP @ 2 ग्राम/लीटर से मिट्टी भिगोएं',
                                                                'ट्राइकोडर्मा विरिडी जैव कवकनाशी का उपयोग करें']},
                                    'te': {   'causes': ['నేలలో నివసించే వర్టిసిల్లియమ్ డాలియా శిలీంద్రం'],
                                              'display_name': 'పత్తి వర్టిసిల్లియమ్ వడలు తెగులు',
                                              'prevention': [   'మొక్కజొన్న వంటి ఇతర పంటలతో పంట మార్పిడి చేయండి',
                                                                'పొటాష్ ఎరువులను తగినంత వాడండి',
                                                                'పొలంలో నీరు నిల్వ ఉండకుండా చూసుకోండి'],
                                              'symptoms': [   'ఆకు ఈనెల మధ్య పులి చారల వంటి పసుపు మరియు ఎండు మచ్చలు',
                                                              'క్రింది ఆకుల నుండి మొదలై పై ఆకుల వరకు హఠాత్తుగా '
                                                              'వడలిపోవడం',
                                                              'కాండం కత్తిరించి చూస్తే లోపల గోధుమ రంగు ఈనెలు '
                                                              'కనిపించడం'],
                                              'treatments': [   'కార్బెండజిమ్ 50 WP ని లీటరు నీటికి 2 గ్రా చొప్పున '
                                                                'కలిపి నేలపై పోయండి',
                                                                'ట్రైకోడెర్మా విరిడి జీవ శిలీంద్రనాశకాన్ని వాడండి']}},
    'Grape Black Measles': {   'en': {   'causes': [   'Various wood-rotting fungi entering pruning wounds',
                                                       'High summer heat'],
                                         'display_name': 'Grape Black Measles (Esca)',
                                         'prevention': [   'Avoid pruning during wet periods',
                                                           'Disinfect pruning shears with bleach/spirit between vines'],
                                         'symptoms': [   'Interveinal leaf stripes (tiger-stripe pattern) of yellow '
                                                         'and brown',
                                                         'Specks or measles-like dark spots on fruit',
                                                         'Sudden wilting of shoots or vine collapse (apoplexy)'],
                                         'treatments': [   'Apply protective paint (liquid copper) on large pruning '
                                                           'wounds',
                                                           'No cure once wood is deeply infected; prune away infected '
                                                           'trunk']},
                               'hi': {   'causes': [   'लकड़ी सड़ाने वाले कवक जो छंटाई के घावों से प्रवेश करते हैं',
                                                       'गर्मियों का अत्यधिक तापमान'],
                                         'display_name': 'अंगूर का काला खसरा रोग (एस्का)',
                                         'prevention': [   'गीले मौसम में छंटाई से बचें',
                                                           'बेलों के बीच छंटाई कटर को ब्लीच/स्पिरिट से कीटाणुरहित '
                                                           'करें'],
                                         'symptoms': [   'पत्तियों की नसों के बीच पीले और भूरे रंग की पट्टियां '
                                                         '(बाघ-धारी पैटर्न)',
                                                         'फलों पर छोटे धब्बे या खसरे जैसे काले निशान',
                                                         'टहनियों का अचानक मुरझाना या बेल का सूखना'],
                                         'treatments': [   'छंटाई के बड़े घावों पर सुरक्षात्मक कॉपर पेस्ट लगाएं',
                                                           'लकड़ी संक्रमित होने पर कोई इलाज नहीं; संक्रमित तने को काट '
                                                           'दें']},
                               'te': {   'causes': [   'కత్తిరింపు గాయాల ద్వారా చెక్కను కుళ్ళింపజేసే వివిధ శిలీంధ్రాలు '
                                                       'ప్రవేశించడం',
                                                       'ఎండ తీవ్రత అధికంగా ఉండటం'],
                                         'display_name': 'ద్రాక్ష బ్లాక్ మీజిల్స్ వ్యాధి (ఎస్కా)',
                                         'prevention': [   'తడి వాతావరణంలో కొమ్మలను కత్తిరించవద్దు',
                                                           'కత్తిరింపు కత్తెరను ఒక తీగ నుండి ఇంకో తీగకు మార్చేటప్పుడు '
                                                           'శానిటైజ్ చేయండి'],
                                         'symptoms': [   'ఆకులపై పసుపు మరియు గోధుమ రంగు పులి చారల వంటి గుర్తులు',
                                                         'పండ్లపై పొక్కులు లేదా నల్లటి మచ్చలు ఏర్పడటం',
                                                         'కొమ్మలు అకస్మాత్తుగా వాడిపోవడం లేదా తీగ చనిపోవడం'],
                                         'treatments': [   'పెద్ద కత్తిరింపు గాయాలపై కాపర్ పేస్ట్ లేదా రక్షణ పూత '
                                                           'పూయండి',
                                                           'కాండం లోపల వ్యాధి సోకితే నివారణ లేదు; సోకిన కొమ్మను '
                                                           'కత్తిరించండి']}},
    'Grape Black Rot': {   'en': {   'causes': [   'Guignardia bidwellii fungus',
                                                   'Warm, wet spring weather and infected overwintered mummies'],
                                     'display_name': 'Grape Black Rot',
                                     'prevention': [   'Remove and burn all shriveled grape mummies from vines',
                                                       'Prune vines and weeds to maximize airflow and sunlight'],
                                     'symptoms': [   'Small, reddish-brown circular spots on leaves with dark borders',
                                                     'Young green shoots develop purple cankers',
                                                     'Fruit shrivels, turns black, and becomes dry mummies'],
                                     'treatments': [   'Apply Mancozeb 75 WP or Captan 50 WP at 2g/L',
                                                       'Apply systemic Myclobutanil or Tebuconazole after bloom']},
                           'hi': {   'causes': [   'गुइग्नार्डिया बिडवेली कवक',
                                                   'गर्म, नम वसंत का मौसम और पिछले वर्ष के संक्रमित अवशेष'],
                                     'display_name': 'अंगूर का काला सड़न रोग',
                                     'prevention': [   'बेलों से सभी सूखे-सड़े अंगूरों (ममियों) को हटाकर जला दें',
                                                       'हवा और धूप के प्रवाह को बढ़ाने के लिए छंटाई करें'],
                                     'symptoms': [   'पत्तियों पर काले किनारों वाले छोटे, लाल-भूरे रंग के गोलाकार '
                                                     'धब्बे',
                                                     'युवा हरी टहनियों पर बैंगनी रंग के कैंकर (घाव) विकसित होना',
                                                     'फल सिकुड़ जाते हैं, काले पड़ जाते हैं और ममी की तरह सूख जाते '
                                                     'हैं'],
                                     'treatments': [   'मैंकोजेब 75 WP या कैप्टन 50 WP @ 2 ग्राम/लीटर का छिड़काव करें',
                                                       'फूल आने के बाद माइक्लोबुटानिल या टेबुकोनाज़ोल का प्रयोग करें']},
                           'te': {   'causes': [   'గుయ్నార్డియా బిడ్\u200cవెల్లి శిలీంద్రం',
                                                   'వసంతకాలంలో వేడి, తడి వాతావरणం మరియు నేలపై పడి ఉన్న పాత పండ్లు'],
                                     'display_name': 'ద్రాక్ష నల్ల కుళ్లు వ్యాధి',
                                     'prevention': [   'తీగలకు ఉన్న ఎండిన ద్రాక్ష పండ్లను తొలగించి కాల్చివేయండి',
                                                       'గాలి, వెలుతురు తగిలేలా కత్తిరింపులు చేయండి'],
                                     'symptoms': [   'ఆకులపై నల్లటి అంచులతో కూడిన చిన్న, ఎరుపు-गोధుమ గుండ్రటి మచ్చలు',
                                                     'చిగుళ్లపై ఊదా రంగు పుండ్లు ఏర్పడతాయి',
                                                     'పండ్లు కుదించుకుపోయి, నల్లగా మారి ఎండిపోతాయి'],
                                     'treatments': [   'మాంకోజెబ్ 75 WP లేదా కాప్టాన్ 50 WP ని లీటరు నీటికి 2 గ్రా '
                                                       'కలిపి పిచికారీ చేయండి',
                                                       'పూత తర్వాత మైక్లోబుటానిల్ లేదా టెబుకోనజోల్ వాడండి']}},
    'Grape Leaf Blight': {   'en': {   'causes': [   'Pseudocercospora vitis fungus',
                                                     'High relative humidity and warm weather'],
                                       'display_name': 'Grape Leaf Blight',
                                       'prevention': [   'Gather and burn fallen leaves to reduce inoculums',
                                                         'Maintain proper plant density for airflow'],
                                       'symptoms': [   'Large irregular dark brown spots on leaves',
                                                       'Leaf edges wither and curl',
                                                       'Premature defoliation, leaving vines bare'],
                                       'treatments': [   'Spray Mancozeb 75 WP at 2g/L',
                                                         'Apply Copper Oxychloride 50 WP at 3g/L or Carbendazim']},
                             'hi': {   'causes': ['स्यूडोसर्कोस्पोरा विटिस कवक', 'उच्च सापेक्ष आर्द्रता और गर्म मौसम'],
                                       'display_name': 'अंगूर का पत्ती झुलसा रोग',
                                       'prevention': [   'संक्रमण कम करने के लिए गिरी हुई पत्तियों को इकट्ठा कर जलाएं',
                                                         'हवा के प्रवाह के लिए पौधों के बीच उचित दूरी रखें'],
                                       'symptoms': [   'पत्तियों पर बड़े अनियमित गहरे भूरे रंग के धब्बे',
                                                       'पत्तियों के किनारे मुरझा जाते हैं और मुड़ जाते हैं',
                                                       'पत्तियां समय से पहले गिर जाती हैं, जिससे बेल खाली हो जाती है'],
                                       'treatments': [   'मैंकोजेब 75 WP @ 2 ग्राम/लीटर का छिड़काव करें',
                                                         'कॉपर ऑक्सीक्लोराइड 50 WP @ 3 ग्राम/लीटर या कार्बेन्डाजिम '
                                                         'लगाएं']},
                             'te': {   'causes': [   'సూడోసెర్కోస్పోరా విటిస్ శిలీంద్రం',
                                                     'గాలిలో అధిక తేమ మరియు వేడి వాతావరణం'],
                                       'display_name': 'ద్రాక్ష ఆకు మచ్చ వ్యాధి',
                                       'prevention': [   'నేలపై పడిన ఆకులను సేకరించి కాల్చడం ద్వారా వ్యాప్తిని '
                                                         'తగ్గించండి',
                                                         'తీగలు గుబురుగా లేకుండా గాలి తగిలేలా ఉంచండి'],
                                       'symptoms': [   'ఆకులపై పెద్ద అసమాన గోధుమ రంగు మచ్చలు',
                                                       'ఆకు అంచులు ముడుచుకుని ఎండిపోతాయి',
                                                       'ఆకులు అకాలంగా రాలిపోయి, తీగలు బోసిపోతాయి'],
                                       'treatments': [   'మాంకోజెబ్ 75 WP ని లీటరు నీటికి 2 గ్రా కలిపి పిచికారీ చేయండి',
                                                         'కాపర్ ఆక్సిక్లోరైడ్ 50 WP ని 3 గ్రా లేదా కార్బండిజం పిచికారీ '
                                                         'చేయండి']}},
    'Groundnut Leaf Spot': {   'en': {   'causes': [   'Cercospora arachidicola / Phaeoisariopsis personata fungus',
                                                       'Warm, wet conditions and dense canopy'],
                                         'display_name': 'Groundnut Leaf Spot (Tikka)',
                                         'prevention': [   'Remove crop debris after harvest',
                                                           'Sow early in the season',
                                                           'Rotate groundnut with sorghum or maize'],
                                         'symptoms': [   'Circular dark brown spots on upper leaf surfaces (Early leaf '
                                                         'spot)',
                                                         'Subcircular black spots on leaf undersides (Late leaf spot)',
                                                         'Severe defoliation under high humidity'],
                                         'treatments': [   'Spray Hexaconazole 5 EC at 2ml/L or Carbendazim 12% + '
                                                           'Mancozeb 63% WP at 2g/L',
                                                           'Apply organic Neem Seed Kernel Extract (NSKE) 5%']},
                               'hi': {   'causes': ['सर्कोस्पोरा और फेओइसारियोप्सिस कवक'],
                                         'display_name': 'मूंगफली का टिक्का रोग',
                                         'prevention': [   'कटाई के बाद फसल अवशेष हटा दें',
                                                           'जल्दी बुवाई करें',
                                                           'ज्वार या मक्का के साथ फसल चक्र अपनाएं'],
                                         'symptoms': [   'पत्तियों की ऊपरी सतह पर गोलाकार गहरे भूरे रंग के धब्बे',
                                                         'पत्तियों के निचले हिस्से पर काले धब्बे',
                                                         'अत्यधिक पत्ती झड़ना'],
                                         'treatments': [   'हेक्साकोनाज़ोल 5 EC @ 2 मिली/लीटर या कार्बेन्डाजिम + '
                                                           'मैंकोजेब @ 2 ग्राम/लीटर का छिड़काव करें']},
                               'te': {   'causes': [   'సెర్కోస్పోరా అరాచిడికోలా మరియు ఫెయియోఇసారియోప్సిస్ పెర్సోనాటా '
                                                       'శిలీంద్రం'],
                                         'display_name': 'వేరుశనగ ఆకుమచ్చ తెగులు (టిక్కా వ్యాధి)',
                                         'prevention': [   'పంట కోత తర్వాత వ్యర్థాలను తొలగించండి',
                                                           'సీజన్ ప్రారంభంలోనే విత్తండి',
                                                           'జొన్న లేదా మొక్కజొన్నతో పంట మార్పిడి చేయండి'],
                                         'symptoms': [   'ఆకుల పైభాగంలో గుండ్రని ముదురు గోధుమ రంగు మచ్చలు',
                                                         'ఆకు వెనుక భాగంలో నల్లటి మచ్చలు',
                                                         'తీవ్రమైన తేమ వల్ల ఆకులు రాలిపోవడం'],
                                         'treatments': [   'హెక్సాకొనజోల్ 5 EC ని లీటరు నీటికి 2 మి.లీ లేదా '
                                                           'కార్బెండజిమ్ + మాంకోజెబ్ కలిపిన పౌడర్ ని 2 గ్రా కలిపి '
                                                           'పిచికారీ చేయండి',
                                                           '5% వేప గింజల కషాయాన్ని (NSKE) వాడండి']}},
    'Groundnut Rust': {   'en': {   'causes': [   'Puccinia arachidis fungus',
                                                  'Windborne urediniospores and warm weather with wetness'],
                                    'display_name': 'Groundnut Rust',
                                    'prevention': [   'Destroy self-sown groundnut plants before planting season',
                                                      'Sow rust-resistant varieties',
                                                      'Maintain wide row spacing'],
                                    'symptoms': [   'Small, reddish-brown pustules on leaf undersides',
                                                    'Pustules rupture releasing rusty brown powder',
                                                    'Leaves dry up and curl but remain attached to stem'],
                                    'treatments': [   'Spray Tebuconazole 250 EC at 1ml/L or Chlorothalonil 75 WP at '
                                                      '2g/L',
                                                      'Spray organic copper hydroxide formulation']},
                          'hi': {   'causes': ['पुकिनिया अराचिडिस कवक'],
                                    'display_name': 'मूंगफली का रस्ट (गेरुआ) रोग',
                                    'prevention': ['जंग प्रतिरोधी किस्में बोएं', 'कतारों के बीच पर्याप्त दूरी रखें'],
                                    'symptoms': [   'पत्तियों के निचले हिस्से पर छोटे, लाल-भूरे रंग के दाने',
                                                    'नारंगी-भूरा जंग जैसा पाउडर उड़ना',
                                                    'पत्तियां सूखकर मुड़ जाती हैं'],
                                    'treatments': [   'टेबुकोनाज़ोल 250 EC @ 1 मिली/लीटर या क्लोरोथैलोनिल 75 WP @ 2 '
                                                      'ग्राम/लीटर का छिड़काव करें']},
                          'te': {   'causes': ['పుస్సినియా అరాచిడిస్ శిలీంద్రం'],
                                    'display_name': 'వేరుశనగ తుప్పు తెగులు',
                                    'prevention': [   'పంటల మధ్య తగినంత దూరం ఉంచండి',
                                                      'తుప్పు తెగులు తట్టుకునే రకాలను నాటండి'],
                                    'symptoms': [   'ఆకు వెనుక భాగంలో చిన్న ఎర్రటి-గోధుమ రంగు బొబ్బలు',
                                                    'బొబ్బలు పగిలి తుప్పు రంగు పొడి రాలడం',
                                                    'ఆకులు ఎండిపోయి ముడుచుకుపోయినా కొమ్మలకే అతుక్కుని ఉండటం'],
                                    'treatments': [   'టెబుకోనజోల్ 250 EC ని లీటరు నీటికి 1 మి.లీ లేదా క్లోరోథలోనిల్ '
                                                      '75 WP ని 2 గ్రా కలిపి పిచికారీ చేయండి']}},
    'Groundnut Stem Rot': {   'en': {   'causes': [   'Sclerotium rolfsii fungus surviving in soil',
                                                      'High soil temperature (25-35C) and wet soil'],
                                        'display_name': 'Groundnut Stem Rot',
                                        'prevention': [   'Avoid deep planting of seeds',
                                                          'Practice deep summer ploughing to bury fungal structures',
                                                          'Do not allow organic debris to pile at stem base'],
                                        'symptoms': [   'Sudden wilting of whole branches or plants',
                                                        'Fan-shaped white mycelial growth at the stem base and soil '
                                                        'surface',
                                                        'Small mustard seed-like sclerotia on infected tissue'],
                                        'treatments': [   'Apply Trichoderma harzianum formulation in soil at '
                                                          '10kg/hectare',
                                                          'Drench stem base with Hexaconazole or Tebuconazole']},
                              'hi': {   'causes': ['मिट्टी में रहने वाला स्क्लेरोटियम रॉल्फ्सि कवक'],
                                        'display_name': 'मूंगफली का तना सड़न रोग',
                                        'prevention': ['गहरी बुवाई से बचें', 'गर्मी में गहरी जुताई करें'],
                                        'symptoms': [   'तने के आधार पर सफेद कवकजाल का बढ़ना',
                                                        'पौधों का अचानक मुरझाना',
                                                        'सरसों के बीज जैसी छोटी गांठें'],
                                        'treatments': [   'ट्राइकोडर्मा हार्ज़ियानम @ 10 किलोग्राम/हेक्टेयर मिट्टी में '
                                                          'डालें',
                                                          'तने के आधार पर हेक्साकोनाज़ोल का छिड़काव करें']},
                              'te': {   'causes': [   'నేలలో ఉండే స్క్లేరోటియం రోల్ఫ్సి శిలీంద్రం',
                                                      'అధిక నేల ఉష్ణోగ్రత (25-35C) మరియు తడి నేల'],
                                        'display_name': 'వేరుశనగ కాండం కుళ్లు తెగులు',
                                        'prevention': [   'విత్తనాలను ఎక్కువ లోతులో నాటవద్దు',
                                                          'వేసవిలో లోతుగా దుక్కి దున్నండి',
                                                          'కాండం మొదళ్ల వద్ద వ్యర్థాలు పేరుకుపోకుండా చూడండి'],
                                        'symptoms': [   'మొక్కలు లేదా కొమ్మలు హఠాత్తుగా వడలిపోవడం',
                                                        'కాండం మొదలు వద్ద మరియు నేల ఉపరితలంపై తెల్లటి బూజు పెరగడం',
                                                        'ఆవ గింజల వంటి చిన్న గింజలు సోకిన భాగాలపై ఏర్పడటం'],
                                        'treatments': [   'ట్రైకోడెర్మా హర్జియానమ్ పొడిని హెక్టారుకు 10 కిలోల చొప్పున '
                                                          'మట్టిలో కలపండి',
                                                          'హెక్సాకొనజోల్ లేదా టెబుకొనజోల్\u200cను కొమ్మల మొదళ్ల వద్ద '
                                                          'పిచికారీ చేయండి']}},
    'Healthy': {   'en': {   'causes': [   'Excellent soil nutrition',
                                           'Optimal irrigation and sunlight',
                                           'Good preventive management'],
                             'display_name': 'Healthy Leaf',
                             'prevention': [   'Continue regular monitoring',
                                               'Maintain proper crop spacing and weed control'],
                             'symptoms': [   'Leaf is uniformly green and healthy',
                                             'No spots, lesions, wilt, or abnormal growth'],
                             'treatments': [   'No chemical treatments needed',
                                               'Apply organic neem cake if nearby crops are diseased']},
                   'hi': {   'causes': ['उत्कृष्ट मिट्टी पोषण', 'इष्टतम सिंचाई और धूप', 'अच्छा निवारक प्रबंधन'],
                             'display_name': 'स्वस्थ पत्ता',
                             'prevention': [   'नियमित निगरानी जारी रखें',
                                               'फसल की उचित दूरी और खरपतवार नियंत्रण बनाए रखें'],
                             'symptoms': [   'पत्ती पूरी तरह से हरी और स्वस्थ है',
                                             'कोई धब्बे, झुलसा, या असामान्य वृद्धि नहीं है'],
                             'treatments': [   'किसी रासायनिक उपचार की आवश्यकता नहीं है',
                                               'यदि पास की फसलें रोगग्रस्त हैं तो जैविक नीम की खली डालें']},
                   'te': {   'causes': [   'అద్భుతమైన నేల పోషణ',
                                           'సరైన నీటి పారుదల మరియు సూర్యరశ్మి',
                                           'మంచి నివారణ నిర్వహణ'],
                             'display_name': 'ఆరోగ్యకరమైన ఆకు',
                             'prevention': [   'క్రమం తప్పకుండా పర్యవేక్షించడం కొనసాగించండి',
                                               'సరైన పంట అంతరం మరియు కలుపు నియంత్రణను నిర్వహించండి'],
                             'symptoms': [   'ఆకు పూర్తిగా ఆకుపచ్చగా మరియు ఆరోగ్యంగా ఉంది',
                                             'మచ్చలు, వాడిపోవడం లేదా అసాధారణ పెరుగుదల లేదు'],
                             'treatments': [   'ఎటువంటి రసాయన చికిత్సలు అవసరం లేదు',
                                               'సమీప పంటలకు తెగుళ్లు సోకితే సేంద్రీయ వేప పిండిని వాడండి']}},
    'Maize Common Rust': {   'en': {   'causes': [   'Puccinia sorghi fungus',
                                                     'Cool temperature (16-23C) and high humidity (continuous dew)'],
                                       'display_name': 'Maize Common Rust',
                                       'prevention': [   'Plant rust-resistant hybrid maize varieties',
                                                         'Manage weed hosts like Oxalis near the field'],
                                       'symptoms': [   'Powdery golden-brown to cinnamon-brown pustules on leaves',
                                                       'Pustules erupt on both upper and lower leaf surfaces',
                                                       'Leaves yellow, wither, and die early in severe cases'],
                                       'treatments': [   'Apply Propiconazole 25 EC at 1ml/L at first rust sign',
                                                         'Apply Mancozeb 75 WP at 2g/L every 10 days']},
                             'hi': {   'causes': [   'पुक्सिनिया सोर्गी कवक',
                                                     'ठंडा तापमान (16-23 डिग्री सेल्सियस) और उच्च आर्द्रता (लगातार '
                                                     'ओस)'],
                                       'display_name': 'मक्के का आम जंग रोग',
                                       'prevention': [   'जंग-प्रतिरोधी संकर मक्का किस्में लगाएं',
                                                         'खेत के पास ऑक्सालिस जैसे खरपतवार मेजबानों को नष्ट करें'],
                                       'symptoms': [   'पत्तियों पर सुनहरे-भूरे से दालचीनी-भूरे रंग के पाउडर वाले दाने '
                                                       '(पस्ट्यूल)',
                                                       'पत्तियों की ऊपरी और निचली दोनों सतहों पर दाने उभरते हैं',
                                                       'पत्तियां पीली होकर मुरझा जाती हैं और जल्दी मर जाती हैं'],
                                       'treatments': [   'जंग के पहले लक्षण दिखने पर प्रोपिकोनाज़ोल 25 EC @ 1 '
                                                         'मिली/लीटर लगाएं',
                                                         'मैंकोजेब 75 WP @ 2 ग्राम/लीटर का हर 10 दिनों में छिड़काव '
                                                         'करें']},
                             'te': {   'causes': [   'పుస్సినియా సోర్గి శిలీంద్రం',
                                                     'చల్లని ఉష్ణోగ్రత (16-23C) మరియు అధిక తేమ (మంచు కురవడం)'],
                                       'display_name': 'మొక్కజొన్న సాధారణ రస్ట్ వ్యాధి',
                                       'prevention': [   'రస్ట్ నిరోధక రకాలను ఎంచుకోండి',
                                                         'పొలం చుట్టుపక్కల కలుపు మొక్కలను తొలగించండి'],
                                       'symptoms': [   'ఆకులపై బంగారు-గోధుమ రంగు పొడి బొబ్బలు',
                                                       'ఆకు పైభాగం మరియు కింది భాగం రెండింటిపై బొబ్బలు వస్తాయి',
                                                       'ఆకులు పసుపు రంగులోకి మారి ఎండిపోతాయి'],
                                       'treatments': [   'రస్ట్ కనిపించిన వెంటనే ప్రొపికోనజోల్ 25 EC ని లీటరు నీటికి 1 '
                                                         'మి.లీ కలిపి పిచికారీ చేయండి',
                                                         'మాంకోజెబ్ 75 WP ని 2 గ్రా కలిపి ప్రతి 10 రోజులకు పిచికారీ '
                                                         'చేయండి']}},
    'Maize Gray Leaf Spot': {   'en': {   'causes': [   'Cercospora zeae-maydis fungus',
                                                        'High relative humidity and wet leaf surfaces from rain or '
                                                        'dew'],
                                          'display_name': 'Maize Gray Leaf Spot',
                                          'prevention': [   'Deep-plow crop residues after harvest',
                                                            'Rotate crops with non-host plants for 2 years'],
                                          'symptoms': [   'Rectangular, gray-to-tan leaf lesions between veins',
                                                          'Lesions merge, causing severe leaf blighting',
                                                          'Premature plant death and stalk lodging'],
                                          'treatments': [   'Apply Pyraclostrobin or Azoxystrobin 23 SC at 1ml/L',
                                                            'Apply Propiconazole 25 EC at 1ml/L at disease onset']},
                                'hi': {   'causes': [   'सर्कोस्पोरा ज़ी-मेयडिस कवक',
                                                        'उच्च सापेक्ष आर्द्रता और बारिश या ओस से पत्तियों का गीला '
                                                        'होना'],
                                          'display_name': 'मक्के का धूसर पत्ती धब्बा रोग',
                                          'prevention': [   'कटाई के बाद फसल के अवशेषों की गहरी जुताई करें',
                                                            'गैर-मेजबान फसलों के साथ 2 साल का फसल चक्र अपनाएं'],
                                          'symptoms': [   'शिराओं के बीच आयताकार, धूसर से भूरे रंग के धब्बे',
                                                          'धब्बे आपस में मिलकर पत्तियों को पूरी तरह झुलसा देते हैं',
                                                          'पौधे की समय से पहले मृत्यु और तने का गिरना'],
                                          'treatments': [   'पायराक्लोस्ट्रोबिन या एज़ोक्सीस्ट्रोबिन 23 SC @ 1 '
                                                            'मिली/लीटर का छिड़काव करें',
                                                            'रोग की शुरुआत में प्रोपिकोनाज़ोल 25 EC @ 1 मिली/लीटर '
                                                            'डालें']},
                                'te': {   'causes': [   'సెర్కోస్పోరా జీ-మేడిస్ శిలీంద్రం',
                                                        'గాలిలో అధిక తేమ మరియు వర్షం లేదా మంచు వల్ల ఆకులు తడవడం'],
                                          'display_name': 'మొక్కజొన్న బూడిద ఆకు మచ్చ వ్యాధి',
                                          'prevention': [   'పంట కోత తర్వాత మిగిలిన భాగాలను లోతుగా దున్నండి',
                                                            'మొక్కజొన్నేతర పంటలతో 2 సంవత్సరాల మార్పిడి చేయండి'],
                                          'symptoms': [   'ఆకు ఈనెల మధ్య దీర్ఘచతురస్రాకార బూడిద రంగు మచ్చలు',
                                                          'మచ్చలు కలిసిపోయి ఆకులు ఎండిపోతాయి',
                                                          'మొక్కలు అకాలంగా చనిపోవడం మరియు కాండం బలహీనపడటం'],
                                          'treatments': [   'పైరాక్లోస్ట్రోబిన్ లేదా అజోక్సిస్ట్రోబిన్ 23 SC ని లీటరు '
                                                            'నీటికి 1 మి.లీ కలిపి పిచికారీ చేయండి',
                                                            'వ్యాధి ప్రారంభంలో ప్రొపికోనజోల్ 25 EC వాడండి']}},
    'Maize Northern Leaf Blight': {   'en': {   'causes': [   'Exserohilum turcicum fungus',
                                                              'Moderate temperatures (18-27C) and wet conditions'],
                                                'display_name': 'Maize Northern Leaf Blight',
                                                'prevention': [   'Rotate crops with legumes or other non-grasses',
                                                                  'Tillage to bury infected residue and plant '
                                                                  'resistant hybrids'],
                                                'symptoms': [   'Long, cigar-shaped, grayish-green or tan lesions on '
                                                                'leaves',
                                                                'Lesions appear first on lower leaves and progress '
                                                                'upwards',
                                                                'Complete leaf death and drying under high pressure'],
                                                'treatments': [   'Apply Mancozeb 75 WP at 2g/L at pre-tasseling stage',
                                                                  'Spray Azoxystrobin or Tebuconazole if severity '
                                                                  'increases']},
                                      'hi': {   'causes': [   'एक्ससेरोहिलम टर्सिकम कवक',
                                                              'मध्यम तापमान (18-27 डिग्री सेल्सियस) और आर्द्र '
                                                              'परिस्थितियां'],
                                                'display_name': 'मक्के का उत्तरी पत्ती झुलसा रोग',
                                                'prevention': [   'दलहन या अन्य गैर-घास फसलों के साथ फसल चक्र अपनाएं',
                                                                  'गहरी जुताई करें और प्रतिरोधी संकर मक्का लगाएं'],
                                                'symptoms': [   'पत्तियों पर लंबे, सिगार के आकार के, सलेटी-हरे या भूरे '
                                                                'रंग के घाव',
                                                                'घाव पहले निचली पत्तियों पर दिखाई देते हैं और ऊपर '
                                                                'बढ़ते हैं',
                                                                'गंभीर संक्रमण में पत्तियां पूरी तरह सूखकर नष्ट हो '
                                                                'जाती हैं'],
                                                'treatments': [   'नरमंजरी (टैसेलिंग) आने से पहले मैंकोजेब 75 WP @ 2 '
                                                                  'ग्राम/लीटर का छिड़काव करें',
                                                                  'संक्रमण बढ़ने पर एज़ोक्सीस्ट्रोबिन या टेबुकोनाज़ोल '
                                                                  'का छिड़काव करें']},
                                      'te': {   'causes': [   'ఎక్సెరోహిలం టర్సికమ్ శిలీంద్రం',
                                                              'మధ్యస్థ ఉష్णోగ్రతలు (18-27C) మరియు తడి పరిస్థితులు'],
                                                'display_name': 'మొక్కజొన్న నార్తర్న్ లీఫ్ బ్లైట్ వ్యాధి',
                                                'prevention': [   'మొక్కజొన్న తర్వాత పప్పుధాన్యాల పంటలను మార్పిడి '
                                                                  'చేయండి',
                                                                  'పంట వ్యర్థాలను లోతుగా దున్నడం మరియు నిరోధక రకాలను '
                                                                  'నాటడం'],
                                                'symptoms': [   'ఆకులపై పొడవాటి, సిగార్ ఆకారపు బూడిద-ఆకుపచ్చ మచ్చలు',
                                                                'మచ్చలు మొదట కింది ఆకులపై కనిపించి పైకి వ్యాపిస్తాయి',
                                                                'తీవ్రమైన దశలో ఆకులన్నీ ఎండిపోతాయి'],
                                                'treatments': [   'మొక్కజొన్న పొత్తు దశకు ముందు మాంకోజెబ్ 75 WP ని '
                                                                  'లీటరు నీటికి 2 గ్రా కలిపి పిచికారీ చేయండి',
                                                                  'అజోక్సిస్ట్రోబిన్ లేదా టెబుకోనజోల్ పిచికారీ '
                                                                  'చేయండి']}},
    'Potato Early Blight': {   'en': {   'causes': [   'Alternaria solani fungus',
                                                       'Alternating wet and dry periods on leaves'],
                                         'display_name': 'Potato Early Blight',
                                         'prevention': [   'Ensure balanced nitrogen fertilization',
                                                           'Remove and destroy crop debris immediately after harvest'],
                                         'symptoms': [   'Dark brown circular spots on older leaves with concentric '
                                                         'rings (target board pattern)',
                                                         'Yellow halo surrounding leaf lesions',
                                                         'Leathery, sunken black spots on potato tubers'],
                                         'treatments': [   'Apply Mancozeb 75 WP at 2g/L or Chlorothalonil 75 WP at '
                                                           '2g/L',
                                                           'Apply systemic Azoxystrobin 23 SC at 1ml/L']},
                               'hi': {   'causes': [   'अल्टरनेरिया सोलेनी कवक',
                                                       'पत्तियों पर बारी-बारी से आने वाले गीले और सूखे समय'],
                                         'display_name': 'आलू का अगेती झुलसा रोग',
                                         'prevention': [   'संतुलित नाइट्रोजन उर्वरक सुनिश्चित करें',
                                                           'कटाई के तुरंत बाद फसल के अवशेषों को हटाकर नष्ट करें'],
                                         'symptoms': [   'पुरानी पत्तियों पर संकेंद्रित छल्लों (लक्षित बोर्ड पैटर्न) '
                                                         'वाले गहरे भूरे रंग के धब्बे',
                                                         'पत्तियों के घावों के चारों ओर पीला प्रभामंडल',
                                                         'आलू के कंदों पर चमड़े जैसे, धंसे हुए काले धब्बे'],
                                         'treatments': [   'मैंकोजेब 75 WP @ 2 ग्राम/लीटर या क्लोरोथैलोनिल 75 WP @ 2 '
                                                           'ग्राम/लीटर का छिड़काव करें',
                                                           'प्रणालीगत एज़ोक्सीस्ट्रोबिन 23 SC @ 1 मिली/लीटर लगाएं']},
                               'te': {   'causes': [   'ఆల్టర్నేరియా సొలాని శిలీంద్రం',
                                                       'ఆకులపై తడి మరియు పొడి వాతావరణం పదే పదే మారడం'],
                                         'display_name': 'బంగాళాదుంప ముందస్తు బ్లైట్ వ్యాధి',
                                         'prevention': [   'నత్రజని ఎరువులను సమతుల్యంగా వాడండి',
                                                           'పంట కోత తర్వాత మిగిలిన వ్యర్థాలను కాల్చివేయండి'],
                                         'symptoms': [   'ముసలి ఆకులపై ఏకకేంద్ర వలయాలతో కూడిన నల్లటి మచ్చలు (టార్గెట్ '
                                                         'బోర్డ్ ఆకారం)',
                                                         'మచ్చల చుట్టూ పసుపు రంగు వలయం ఏర్పడటం',
                                                         'దుంపలపై కుంగిపోయిన నల్లటి మచ్చలు'],
                                         'treatments': [   'మాంకోజెబ్ 75 WP ని లీటరు నీటికి 2 గ్రా లేదా క్లోరోథలోనిల్ '
                                                           '2 గ్రా కలిపి పిచికారీ చేయండి',
                                                           'అజోక్సిస్ట్రోబిన్ 23 SC ని లీటరు నీటికి 1 మి.లీ కలిపి '
                                                           'పిచికారీ చేయండి']}},
    'Potato Late Blight': {   'en': {   'causes': [   'Phytophthora infestans oomycete (fungal-like organism)',
                                                      'Cool, very wet, humid weather'],
                                        'display_name': 'Potato Late Blight',
                                        'prevention': [   'Use certified disease-free seed tubers',
                                                          'Avoid overhead sprinkler irrigation and destroy infected '
                                                          'cull piles'],
                                        'symptoms': [   'Large, dark water-soaked lesions expanding rapidly on leaves',
                                                        'White velvety mold on leaf undersides in wet weather',
                                                        'Tubers rot, turning reddish-brown and mushy'],
                                        'treatments': [   'Apply Metalaxyl + Mancozeb (Ridomil Gold) at 2.5g/L '
                                                          'immediately',
                                                          'Spray Cymoxanil + Mancozeb at 2g/L']},
                              'hi': {   'causes': [   'फाइटोफ्थोरा इन्फेस्टन्स ऊमीसीट (कवक जैसा जीव)',
                                                      'ठंडा, बहुत गीला और आर्द्र मौसम'],
                                        'display_name': 'आलू का पछेती झुलसा रोग',
                                        'prevention': [   'प्रमाणित रोग-मुक्त बीज कंदों का उपयोग करें',
                                                          'ऊपर से पानी देने वाली सिंचाई से बचें और संक्रमित अवशेषों के '
                                                          'ढेरों को नष्ट करें'],
                                        'symptoms': [   'पत्तियों पर तेजी से फैलने वाले बड़े, गहरे जलाक्रांत घाव',
                                                        'गीले मौसम में पत्तियों के निचले हिस्से पर सफेद मखमली फफूंद',
                                                        'कंद सड़ जाते हैं, लाल-भूरे रंग के और पिलपिले हो जाते हैं'],
                                        'treatments': [   'मेटालैक्सिल + मैंकोजेब (रिडोमिल गोल्ड) @ 2.5 ग्राम/लीटर '
                                                          'तुरंत लगाएं',
                                                          'साइमोक्सानिल + मैंकोजेब @ 2 ग्राम/लीटर का छिड़काव करें']},
                              'te': {   'causes': [   'ఫైటోఫ్తోరా ఇన్ఫెస్టాన్స్ అనే శిలీంధ్ర జాతి జీవి',
                                                      'చల్లని, అధిక తేమ మరియు తడి వాతావరణం'],
                                        'display_name': 'బంగాళాదుంప లేట్ బ్లైట్ వ్యాధి',
                                        'prevention': [   'తెగులు లేని విత్తన దుంపలను మాత్రమే వాడండి',
                                                          'ఆకులపై నీరు పడేలా పిచికారీ చేయవద్దు మరియు సోకిన కుప్పలను '
                                                          'నాశనం చేయండి'],
                                        'symptoms': [   'ఆకులపై వేగంగా విస్తరించే నల్లటి నీటి Lesions',
                                                        'తడి వాతావరణంలో ఆకు కింది భాగంలో తెల్లటి బూజు పచ్చని పూత',
                                                        'దుంపలు ఎరుపు-గోధుమ రంగులోకి మారి కుళ్ళిపోవడం'],
                                        'treatments': [   'మెటాలాక్సిల్ + మాంకోజెబ్ (రిడోమిల్ గోల్డ్) ని లీటరుకు 2.5 '
                                                          'గ్రా కలిపి వెంటనే పిచికారీ చేయండి',
                                                          'సైమోక్సానిల్ + మాంకోజెబ్ ని 2 గ్రా పిచికారీ చేయండి']}},
    'Rice Bacterial Leaf Blight': {   'en': {   'causes': [   'Xanthomonas oryzae pv. oryzae bacterium',
                                                              'Warm temperatures (25-34C), wind damage, and high '
                                                              'moisture'],
                                                'display_name': 'Rice Bacterial Leaf Blight',
                                                'prevention': [   'Secure seedbed drainage',
                                                                  'Avoid excessive nitrogen application',
                                                                  'Keep field borders clean of weeds'],
                                                'symptoms': [   'Water-soaked yellowish stripes starting from leaf '
                                                                'tips',
                                                                'Bacterial ooze droplets (milky white dew) on young '
                                                                'leaves',
                                                                'Wilt and drying of whole leaf blades (Kresek phase)'],
                                                'treatments': [   'Spray Streptocycline at 0.1g/L combined with Copper '
                                                                  'Oxychloride at 2.5g/L',
                                                                  'Apply biocontrol Pseudomonas fluorescens']},
                                      'hi': {   'causes': [   'जैंथोमोनास ओरिज़ी जीवाणु',
                                                              'गर्म तापमान (25-34C) और उच्च नमी'],
                                                'display_name': 'धान का जीवाणु झुलसा रोग',
                                                'prevention': [   'उचित जल निकासी सुनिश्चित करें',
                                                                  'नाइट्रोजन का अत्यधिक उपयोग रोकें',
                                                                  'खरपतवार हटा दें'],
                                                'symptoms': [   'पत्तियों की युक्तियों से शुरू होने वाली पानी से लथपथ '
                                                                'पीली पट्टियां',
                                                                'युवा पत्तियों पर जीवाणु स्राव की बूंदें',
                                                                'पूरी पत्ती का सूखना और झुलसना'],
                                                'treatments': [   'कॉपर ऑक्सीक्लोराइड @ 2.5 ग्राम/लीटर के साथ '
                                                                  'स्ट्रेप्टोसाइक्लिन @ 0.1 ग्राम/लीटर का छिड़काव करें',
                                                                  'स्यूडोमोनास फ्लोरेसेंस का उपयोग करें']},
                                      'te': {   'causes': [   'జాంతోమోనాస్ ఒరైజే పివి ఒరైజే బాక్టీరియా',
                                                              'వెచ్చని ఉష్ణోగ్రతలు (25-34C), బలమైన గాలుల వల్ల కలిగే '
                                                              'గాయాలు మరియు అధిక తేమ'],
                                                'display_name': 'వరి బాక్టీరియా ఆకు ఎండు తెగులు',
                                                'prevention': [   'నర్సరీలలో నీటి పారుదల సరిగ్గా ఉంచండి',
                                                                  'నత్రజని ఎరువులను మోతాదుకు మించి వాడొద్దు',
                                                                  'పొలం గట్లపై కలుపు మొక్కలను నివారించండి'],
                                                'symptoms': [   'ఆకు చివరల నుండి మొదలై క్రిందికి వ్యాపించే నీటితో '
                                                                'నిండిన పసుపు రంగు గీతలు',
                                                                'లేత ఆకులపై తెల్లటి బాక్టీరియా ద్రవ బిందువులు',
                                                                'ఆకులు పూర్తిగా ఎండిపోవడం (క్రెసెక్ దశ)'],
                                                'treatments': [   'లీటరు నీటికి స్ట్రెప్టోసైక్లిన్ 0.1 గ్రా మరియు '
                                                                  'కాపర్ ఆక్సిక్లోరైడ్ 2.5 గ్రా కలిపి పిచికారీ చేయండి',
                                                                  'సూడోమోనాస్ ఫ్లోరోసెన్స్ జీవ నియంత్రణను వాడండి']}},
    'Rice Blast Disease': {   'en': {   'causes': [   'Pyricularia oryzae fungus',
                                                      'High relative humidity (>90%) and leaf wetness',
                                                      'Excessive nitrogen fertilizer application'],
                                        'display_name': 'Rice Blast Disease',
                                        'prevention': [   'Use blast-resistant varieties like Swarna Prabha',
                                                          'Avoid excessive nitrogen application',
                                                          'Maintain proper seed rate and clean irrigation channels'],
                                        'symptoms': [   'Spindle-shaped lesions with brown borders and gray centers on '
                                                        'leaves',
                                                        'Collar rot and neck rot at the base of the panicle',
                                                        'Stunted growth and lodging of crops'],
                                        'treatments': [   'Spray Tricyclazole 75 WP at 0.6g/L or Isoprothiolane 40 EC '
                                                          'at 1.5ml/L',
                                                          'Apply organic Pseudomonas fluorescens formulation at 5g/L']},
                              'hi': {   'causes': [   'पाइरीकुलेरिया ओरिज़ी कवक',
                                                      'उच्च सापेक्ष आर्द्रता (>90%)',
                                                      'नाइट्रोजन उर्वरक का अत्यधिक उपयोग'],
                                        'display_name': 'धान का ब्लास्ट रोग',
                                        'prevention': [   'ब्लास्ट-प्रतिरोधी किस्मों का उपयोग करें',
                                                          'नाइट्रोजन का संतुलित उपयोग करें',
                                                          'उचित सिंचाई चैनल बनाए रखें'],
                                        'symptoms': [   'पत्तियों पर भूरे रंग के किनारों और भूरे रंग के केंद्रों के '
                                                        'साथ धुरी के आकार के धब्बे',
                                                        'बालियों के आधार पर सड़ांध',
                                                        'फसल का विकास रुकना'],
                                        'treatments': [   'ट्राइसाइक्लाजोल 75 WP @ 0.6 ग्राम/लीटर या आइसोप्रोधियोलेन '
                                                          '40 EC @ 1.5 मिली/लीटर का छिड़काव करें',
                                                          'स्यूडोमोनास फ्लोरेसेंस @ 5 ग्राम/लीटर का उपयोग करें']},
                              'te': {   'causes': [   'పైరికులేరియా ఒరైజే శిలీంద్రం',
                                                      'అధిక తేమ శాతం (>90%) మరియు ఆకులు తడిగా ఉండటం',
                                                      'నత్రజని ఎరువుల మితిమీరిన వాడకం'],
                                        'display_name': 'వరి అగ్గి తెగులు',
                                        'prevention': [   'స్వర్ణ ప్రభ వంటి అగ్గి తెగులు తట్టుకునే రకాలను వాడండి',
                                                          'నత్రజని ఎరువులను మోతాదుకు మించి వాడొద్దు',
                                                          'పొలంలో నీటి పారుదల కాలువలను శుభ్రంగా ఉంచండి'],
                                        'symptoms': [   'ఆకులపై గోధుమ రంగు అంచులతో, బూడిద రంగు కేంద్రాలతో నూలు కండె '
                                                        'ఆకారపు మచ్చలు',
                                                        'కంకి మెడ వద్ద కుళ్ళిపోవడం (మెడ కుళ్లు)',
                                                        'మొక్క ఎదుగుదల క్షీణించడం'],
                                        'treatments': [   'ట్రైసైక్లాజోల్ 75 WP ని లీటరు నీటికి 0.6 గ్రా లేదా '
                                                          'ఐసోప్రోతియోలేన్ 40 EC ని 1.5 మి.లీ కలిపి పిచికారీ చేయండి',
                                                          'సేంద్రీయ సూడోమోనాస్ ఫ్లోరోసెన్స్ 5 గ్రా/లీటరు చొప్పున '
                                                          'వాడండి']}},
    'Rice Brown Spot': {   'en': {   'causes': [   'Cochliobolus miyabeanus fungus',
                                                   'Nutrient-deficient soils (potassium and silicon deficiency)',
                                                   'Prolonged leaf wetness'],
                                     'display_name': 'Rice Brown Spot',
                                     'prevention': [   'Practice balanced fertilization with adequate potash',
                                                       'Use certified disease-free seeds',
                                                       'Provide good field drainage'],
                                     'symptoms': [   'Oval dark brown lesions with yellow halos on leaf blades',
                                                     'Dirty black spots on glumes and grains',
                                                     'Poor grain filling and reduced germination rate'],
                                     'treatments': [   'Spray Mancozeb 75 WP at 2g/L or Propiconazole 25 EC at 1ml/L',
                                                       'Apply soil silicon fertilizer and potash']},
                           'hi': {   'causes': [   'कोक्लीओबोलस मियाबीनस कवक',
                                                   'पोषक तत्वों की कमी वाली मिट्टी',
                                                   'लंबे समय तक पत्तियों का गीला रहना'],
                                     'display_name': 'धान का भूरा धब्बा रोग',
                                     'prevention': [   'पोटाश की पर्याप्त मात्रा के साथ संतुलित खाद डालें',
                                                       'प्रमाणित बीज का उपयोग करें',
                                                       'खेत में जल निकासी की व्यवस्था करें'],
                                     'symptoms': [   'पत्ती के ब्लेड पर पीले प्रभामंडल के साथ अंडाकार गहरे भूरे रंग के '
                                                     'धब्बे',
                                                     'दानों पर काले धब्बे',
                                                     'अपूर्ण दाना भरना और कम अंकुरण'],
                                     'treatments': [   'मैंकोजेब 75 WP @ 2 ग्राम/लीटर या प्रोपिकोनाज़ोल 25 EC @ 1 '
                                                       'मिली/लीटर का छिड़काव करें',
                                                       'मिट्टी में सिलिकॉन और पोटाश डालें']},
                           'te': {   'causes': [   'కోక్లియాబోలస్ మియాబియానస్ శిలీంద్రం',
                                                   'పోషకాల లోపం గల నేలలు (పొటాషియం మరియు సిలికాన్ లోపం)',
                                                   'ఆకులు ఎక్కువ సేపు తడిగా ఉండటం'],
                                     'display_name': 'వరి గోధుమ రంగు మచ్చ తెగులు',
                                     'prevention': [   'సమతుల్య ఎరువులను ముఖ్యంగా తగినంత పొటాష్\u200cను వాడండి',
                                                       'రోగ రహిత ధృవీకరించబడిన విత్తనాలను వాడండి',
                                                       'పొలంలో నిరుపయోగ నీటిని త్వరగా తొలగించండి'],
                                     'symptoms': [   'ఆకు బ్లేడ్\u200cలపై పసుపు రంగు వలయాలతో కూడిన గుండ్రని గోధుమ రంగు '
                                                     'మచ్చలు',
                                                     'గింజలపై నల్లటి మచ్చలు',
                                                     'గింజలు సరిగ్గా నిండకపోవడం మరియు తక్కువ మొలక శాతం'],
                                     'treatments': [   'మాంకోజెబ్ 75 WP ని లీటరు నీటికి 2 గ్రా లేదా ప్రొపికోనజోల్ 25 '
                                                       'EC ని 1 మి.లీ కలిపి పిచికారీ చేయండి',
                                                       'నేలకు సిలికాన్ మరియు పొటాష్ ఎరువులు అందించండి']}},
    'Tomato Bacterial Spot': {   'en': {   'causes': [   'Xanthomonas perforans bacterium',
                                                         'Warm, rainy conditions and overhead sprinkler watering'],
                                           'display_name': 'Tomato Bacterial Spot',
                                           'prevention': [   'Use certified pathogen-free seeds and seedlings',
                                                             'Avoid touching plants when they are wet with dew or '
                                                             'rain'],
                                           'symptoms': [   'Small dark spots on leaves with yellow halos',
                                                           'Leaf spots dry and turn paper-thin or tear',
                                                           'Small scab-like lesions on tomato fruit'],
                                           'treatments': [   'Spray Copper Hydroxide 77 WP at 3g/L + Streptocycline '
                                                             '1g/10L',
                                                             'Apply Mancozeb to copper mixtures to increase efficacy']},
                                 'hi': {   'causes': [   'जैंथोमोनास परफोरन्स जीवाणु',
                                                         'गर्म, बरसाती परिस्थितियां और फव्वारा सिंचाई'],
                                           'display_name': 'टमाटर का जीवाणु धब्बा रोग',
                                           'prevention': [   'प्रमाणित रोग-मुक्त बीज और पौध का ही उपयोग करें',
                                                             'ओस या बारिश से भीगे होने पर पौधों को छूने से बचें'],
                                           'symptoms': [   'पत्तियों पर पीले प्रभामंडल के साथ छोटे काले धब्बे',
                                                           'पत्तियों के धब्बे सूखकर कागज जैसे पतले हो जाते हैं या फट '
                                                           'जाते',
                                                           'टमाटर के फलों पर पपड़ीदार छोटे घाव'],
                                           'treatments': [   'कॉपर हाइड्रॉक्साइड 77 WP @ 3 ग्राम/लीटर + '
                                                             'स्ट्रेप्टोसाइक्लिन 1 ग्राम/10 लीटर छिड़कें',
                                                             'प्रभाव बढ़ाने के लिए कॉपर मिश्रण के साथ मैंकोजेब '
                                                             'मिलाएं']},
                                 'te': {   'causes': [   'జాంతోమోనాస్ పెర్ఫోరాన్స్ బ్యాక్టీరియా',
                                                         'వేడి, వర్షపు వాతావరణం మరియు ఆకులపై నీరు పిచికారీ చేయడం'],
                                           'display_name': 'టమోటా బ్యాక్టీరియల్ మచ్చ వ్యాధి',
                                           'prevention': [   'తెగులు లేని విత్తనాలను మరియు నారు మొక్కలను మాత్రమే '
                                                             'వాడండి',
                                                             'ఆకులు తడిగా ఉన్నప్పుడు వాటిని తాకవద్దు'],
                                           'symptoms': [   'ఆకులపై పసుపు రంగు వలయాలతో కూడిన చిన్న నల్లటి మచ్చలు',
                                                           'ఆకు మచ్చలు ఎండిపోయి కాగితంలా పలచగా మారి చిరిగిపోవడం',
                                                           'పండ్లపై చిన్న పుండ్లు వంటి మచ్చలు'],
                                           'treatments': [   'కాపర్ హైడ్రాక్సైడ్ 77 WP ని 3 గ్రా + స్ట్రెప్టోసైక్లిన్ '
                                                             '1 గ్రా కలిపి 10 లీటర్ల నీటికి పిచికారీ చేయండి',
                                                             'కాపర్ మిశ్రమంతో మాంకోజెబ్ కలిపి పిచికారీ చేస్తే నివారణ '
                                                             'బాగుంటుంది']}},
    'Tomato Early Blight': {   'en': {   'causes': [   'Alternaria solani fungus',
                                                       'Warm, humid conditions and splashing rain or irrigation water'],
                                         'display_name': 'Tomato Early Blight',
                                         'prevention': [   'Prune lower leaves up to 1 foot above ground to block soil '
                                                           'splash',
                                                           'Apply thick mulch under plants to prevent soil contact'],
                                         'symptoms': [   'Concentric dark rings (target spots) on older leaves first',
                                                         'Leaves yellow and drop, exposing fruit to sunscald',
                                                         'Dark, leathery spots on stem and near fruit stem'],
                                         'treatments': [   'Spray Mancozeb 75 WP at 2g/L or Chlorothalonil 75 WP at '
                                                           '2g/L',
                                                           'Apply systemic Propiconazole or Azoxystrobin weekly']},
                               'hi': {   'causes': [   'अल्टरनेरिया सोलेनी कवक',
                                                       'गर्म, आर्द्र परिस्थितियां और पानी के छींटे'],
                                         'display_name': 'टमाटर का अगेती झुलसा रोग',
                                         'prevention': [   'मिट्टी के छींटों से बचाने के लिए निचली पत्तियों को जमीन से '
                                                           '1 फीट ऊपर तक काट दें',
                                                           'पौधों के नीचे सूखी घास/मल्च बिछाएं'],
                                         'symptoms': [   'पहले पुरानी पत्तियों पर संकेंद्रित काले छल्ले (लक्षित धब्बे)',
                                                         'पत्तियां पीली होकर गिर जाती हैं, जिससे फल धूप से झुलस जाते '
                                                         'हैं',
                                                         'तने और फल के डंठल के पास गहरे, चमड़े जैसे धब्बे'],
                                         'treatments': [   'मैंकोजेब 75 WP @ 2 ग्राम/लीटर या क्लोरोथैलोनिल 75 WP @ 2 '
                                                           'ग्राम/लीटर छिड़कें',
                                                           'प्रणालीगत प्रोपिकोनाज़ोल या एज़ोक्सीस्ट्रोबिन का साप्ताहिक '
                                                           'प्रयोग करें']},
                               'te': {   'causes': [   'ఆల్టర్నేరియా సొలాని శిలీంద్రం',
                                                       'వేడి, తేమతో కూడిన వాతావరణం మరియు ఆకులపై పడే నీటి చినుకులు'],
                                         'display_name': 'టమోటా ముందస్తు బ్లైట్ వ్యాధి',
                                         'prevention': [   'నేల నుండి నీటి చినుకులు పడకుండా కింది ఆకులను 1 అడుగు వరకు '
                                                           'కత్తిరించండి',
                                                           'మొక్కల మొదళ్ల వద్ద ఎండు గడ్డి లేదా మల్చింగ్ షీట్ వాడండి'],
                                         'symptoms': [   'మొదట ముసలి ఆకులపై ఏకకేంద్ర వలయాలతో కూడిన నల్లటి మచ్చలు',
                                                         'ఆకులు పసుపు రంగులోకి మారి రాలిపోవడం',
                                                         'కాండం మరియు కాయల కాడల వద్ద నల్లటి మచ్చలు'],
                                         'treatments': [   'మాంకోజెబ్ 75 WP ని లీటరు నీటికి 2 గ్రా లేదా క్лоరోథలోనిల్ '
                                                           '2 గ్రా కలిపి పిచికారీ చేయండి',
                                                           'ప్రొపికోనజోల్ లేదా అజోక్సిస్ట్రోబిన్ వారానికి ఒకసారి '
                                                           'పిచికారీ చేయండి']}},
    'Tomato Late Blight': {   'en': {   'causes': ['Phytophthora infestans oomycete', 'Cool, wet, humid weather'],
                                        'display_name': 'Tomato Late Blight',
                                        'prevention': [   'Grow late blight resistant tomato varieties',
                                                          'Do not compost infected plant debris; burn or bury them '
                                                          'deep'],
                                        'symptoms': [   'Large brown-black water-soaked patches on leaves',
                                                        'White velvety growth on leaf undersides in high humidity',
                                                        'Large dark brown firm spots on tomato fruit, rotting quickly'],
                                        'treatments': [   'Spray Metalaxyl + Mancozeb (Ridomil Gold) at 2.5g/L '
                                                          'immediately',
                                                          'Spray Cymoxanil + Mancozeb at 2g/L on a 7-day schedule']},
                              'hi': {   'causes': ['फाइटोफ्थोरा इन्फेस्टन्स ऊमीसीट', 'ठंडा, गीला और आर्द्र मौसम'],
                                        'display_name': 'टमाटर का पछेती झुलसा रोग',
                                        'prevention': [   'पछेती झुलसा प्रतिरोधी टमाटर की किस्में उगाएं',
                                                          'संक्रमित पौधों के कचरे की खाद न बनाएं; उन्हें जला दें या '
                                                          'गहरा दफन करें'],
                                        'symptoms': [   'पत्तियों पर बड़े भूरे-काले जलाक्रांत धब्बे',
                                                        'उच्च आर्द्रता में पत्तियों के निचले हिस्से पर सफेद मखमली '
                                                        'फफूंद',
                                                        'टमाटर के फलों पर बड़े गहरे भूरे रंग के कड़े धब्बे, फल जल्दी '
                                                        'सड़ते हैं'],
                                        'treatments': [   'मेटालैक्सिल + मैंकोजेब (रिडोमिल गोल्ड) @ 2.5 ग्राम/लीटर '
                                                          'तुरंत छिड़कें',
                                                          '7 दिनों के अंतराल पर साइमोक्सानिल + मैंकोजेब @ 2 ग्राम/लीटर '
                                                          'छिड़कें']},
                              'te': {   'causes': [   'ఫైటోఫ్తోరా ఇన్ఫెస్టాన్స్ అనే శిలీంధ్ర జాతి జీవి',
                                                      'చల్లని, తడి మరియు తేమతో కూడిన వాతావరణం'],
                                        'display_name': 'టమోటా లేట్ బ్లైట్ వ్యాధి',
                                        'prevention': [   'లేట్ బ్లైట్ తట్టుకునే టమోటా రకాలను నాటండి',
                                                          'తెగులు సోకిన మొక్క వ్యర్థాలతో ఎరువు తయారు చేయవద్దు; వాటిని '
                                                          'కాల్చండి'],
                                        'symptoms': [   'ఆకులపై పెద్ద నల్లటి నీటి Lesions',
                                                        'గాలిలో తేమ ఎక్కువగా ఉన్నప్పుడు ఆకు కింది భాగంలో తెల్లటి పూత',
                                                        'కాయలపై పెద్ద గోధుమ రంగు మచ్చలు ఏర్పడి కాయలు కుళ్ళిపోవడం'],
                                        'treatments': [   'మెటాలాక్సిల్ + మాంకోజెబ్ (రిడోమిల్ గోల్డ్) ని లీటరుకు 2.5 '
                                                          'గ్రా కలిపి వెంటనే పిచికారీ చేయండి',
                                                          'సైమోక్సానిల్ + మాంకోజెబ్ ని 2 గ్రా చొప్పున ప్రతి 7 రోజులకు '
                                                          'పిచికారీ చేయండి']}},
    'Tomato Leaf Mold': {   'en': {   'causes': [   'Passalora fulva fungus',
                                                    'High relative humidity (above 85%) and poor ventilation in '
                                                    'greenhouses'],
                                      'display_name': 'Tomato Leaf Mold',
                                      'prevention': [   'Space plants widely and prune to improve air circulation',
                                                        'Water plants at the base to avoid wetting leaves'],
                                      'symptoms': [   'Pale green-to-yellow spots on upper leaf surfaces',
                                                      'Olive-green to purple velvety mold on leaf undersides',
                                                      'Leaves wither and drop, reducing fruit yield'],
                                      'treatments': [   'Spray Chlorothalonil 75 WP at 2g/L or Carbendazim at 1g/L',
                                                        'Apply Copper Hydroxide if disease persists']},
                            'hi': {   'causes': [   'पासालोरा फुल्वा कवक',
                                                    'ग्रीनहाउस में उच्च सापेक्ष आर्द्रता (85% से अधिक) और खराब '
                                                    'वेंटिलेशन'],
                                      'display_name': 'टमाटर का पत्ता मोल्ड रोग',
                                      'prevention': [   'हवा के लिए पौधों के बीच पर्याप्त दूरी रखें और छंटाई करें',
                                                        'पत्तियों को गीला करने से बचने के लिए जड़ों में पानी दें'],
                                      'symptoms': [   'पत्तियों की ऊपरी सतह पर हल्के हरे-पीले धब्बे',
                                                      'पत्तियों के निचले हिस्से पर जैतून-हरे से बैंगनी रंग का मखमली '
                                                      'फफूंद',
                                                      'पत्तियां मुरझाकर गिर जाती हैं, जिससे फल की उपज कम हो जाती है'],
                                      'treatments': [   'क्लोरोथैलोनिल 75 WP @ 2 ग्राम/लीटर या कार्बेन्डाजिम @ 1 '
                                                        'ग्राम/लीटर छिड़कें',
                                                        'यदि रोग बना रहता है तो कॉपर हाइड्रॉक्साइड का प्रयोग करें']},
                            'te': {   'causes': [   'పాసలోరా ఫుల్వా శిలీంద్రం',
                                                    'గాలిలో అధిక తేమ (85% పైగా) మరియు గాలి వెలుతురు తక్కువగా ఉండటం'],
                                      'display_name': 'టమోటా ఆకు బూజు వ్యాధి',
                                      'prevention': [   'మొక్కల మధ్య తగినంత దూరం ఉంచండి మరియు కింది కొమ్మలను '
                                                        'కత్తిరించండి',
                                                        'మొక్కల మొదళ్ల వద్ద మాత్రమే నీరు పోయండి'],
                                      'symptoms': [   'ఆకు పైభాగాన లేత పసుపు మచ్చలు',
                                                      'ఆకు వెనుక వైపు ఆలివ్-ఆకుపచ్చ లేదా ఊదా రంగు వెల్వెట్ బూజు',
                                                      'ఆకులు ఎండిపోయి రాలిపోవడం వల్ల దిగుబడి తగ్గడం'],
                                      'treatments': [   'క్లోరోథలోనిల్ 75 WP ని లీటరు నీటికి 2 గ్రా లేదా కార్బండిజం ని '
                                                        '1 గ్రా కలిపి పిచికారీ చేయండి',
                                                        'తీవ్రత తగ్గకపోతే కాపర్ హైడ్రాక్సైడ్ పిచికారీ చేయండి']}},
    'Tomato Mosaic Virus': {   'en': {   'causes': [   'Tobamovirus transmitted mechanically via tools, hands, and '
                                                       'seed coats'],
                                         'display_name': 'Tomato Mosaic Virus',
                                         'prevention': [   'Soak seeds in 10% Trisodium Phosphate solution before '
                                                           'sowing',
                                                           'Grow mosaic virus resistant tomato varieties'],
                                         'symptoms': [   'Mottled light and dark green patterns on leaves (mosaic '
                                                         'pattern)',
                                                         'Leaf leaflets become narrow and distorted (fern-leaf '
                                                         'appearance)',
                                                         'Internal browning of tomato fruit wall'],
                                         'treatments': [   'No chemical treatment cures a viral infection; remove '
                                                           'infected plants',
                                                           'Wash hands and tools with soap/deet after handling '
                                                           'infected plants']},
                               'hi': {   'causes': ['टोबैमोवायरस, जो औजारों, हाथों और बीजों के माध्यम से फैलता है'],
                                         'display_name': 'टमाटर का मोज़ेक वायरस',
                                         'prevention': [   'बुवाई से पहले बीजों को 10% ट्राइसोडियम फॉस्फेट घोल में '
                                                           'भिगोएं',
                                                           'मोज़ेक वायरस प्रतिरोधी किस्में उगाएं'],
                                         'symptoms': [   'पत्तियों पर हल्के और गहरे हरे रंग के चितकबरे पैटर्न (मोज़ेक)',
                                                         'पत्तियां संकीर्ण और विकृत हो जाती हैं (फर्न जैसी पत्ती)',
                                                         'टमाटर के फल की दीवार का आंतरिक रूप से भूरा होना'],
                                         'treatments': [   'कोई रासायनिक उपचार नहीं; संक्रमित पौधों को तुरंत हटा दें',
                                                           'संक्रमित पौधों को छूने के बाद साबुन से हाथ और औजारों को '
                                                           'धोएं']},
                               'te': {   'causes': [   'చేతులు, వ్యవసాయ పనిముట్ల ద్వారా మెకానికల్\u200cగా వ్యాపించే '
                                                       'టొబామోవైరస్'],
                                         'display_name': 'టమోటా మొజాయిక్ వైరస్',
                                         'prevention': [   'విత్తే ముందు విత్తనాలను 10% ట్రైసోడియం ఫాస్ఫేట్ ద్రావణంలో '
                                                           'నానబెట్టండి',
                                                           'వైరస్ నిరోధక రకాలను ఎంచుకోండి'],
                                         'symptoms': [   'ఆకులపై ఆకుపచ్చ మరియు పసుపు రంగుల చారలు (మొజాయిక్ ఆకారం)',
                                                         'ఆకులు చిన్నవిగా మారి రూపాన్ని కోల్పోవడం',
                                                         'కాయల లోపల గోధుమ రంగులోకి మారడం'],
                                         'treatments': [   'వైరస్ తెగుళ్లకు కెమికల్ నివారణ లేదు; సోకిన మొక్కలను '
                                                           'పీకివేయండి',
                                                           'పనిముట్లను సబ్బు నీటితో శుభ్రం చేయండి']}},
    'Tomato Septoria Leaf Spot': {   'en': {   'causes': [   'Septoria lycopersici fungus',
                                                             'Warm, wet conditions and fungal spores overwintering on '
                                                             'debris'],
                                               'display_name': 'Tomato Septoria Leaf Spot',
                                               'prevention': [   'Remove and burn all infected crop residues after '
                                                                 'harvest',
                                                                 'Rotate tomato crops with corn or beans for 2 years'],
                                               'symptoms': [   'Numerous small circular spots on lower leaves with '
                                                               'dark borders and grey centers',
                                                               'Tiny black specks (fruiting bodies) inside leaf spot '
                                                               'centers',
                                                               'Severe spotting causes leaves to yellow, dry, and fall '
                                                               'off'],
                                               'treatments': [   'Spray Chlorothalonil 75 WP at 2g/L or Mancozeb 75 WP '
                                                                 'at 2g/L',
                                                                 'Spray Copper Oxychloride 50 WP at 3g/L']},
                                     'hi': {   'causes': [   'सेप्टोरिया लाइकोपर्सिकी कवक',
                                                             'गर्म, गीला मौसम और कचरे पर जीवित रहने वाले फफूंद के '
                                                             'बीजाणु'],
                                               'display_name': 'टमाटर का सेप्टोरिया पत्ती धब्बा रोग',
                                               'prevention': [   'कटाई के बाद सभी संक्रमित अवशेषों को हटाकर जला दें',
                                                                 'मक्का या फलियों के साथ 2 साल का फसल चक्र अपनाएं'],
                                               'symptoms': [   'निचली पत्तियों पर काले किनारों और सलेटी केंद्र वाले कई '
                                                               'छोटे गोल धब्बे',
                                                               'धब्बों के बीच में छोटे काले डॉट्स (फफूंद के बीजाणु)',
                                                               'गंभीर संक्रमण में पत्तियां पीली होकर सूखती हैं और गिर '
                                                               'जाती हैं'],
                                               'treatments': [   'क्लोरोथैलोनिल 75 WP @ 2 ग्राम/लीटर या मैंकोजेब 75 WP '
                                                                 '@ 2 ग्राम/लीटर छिड़कें',
                                                                 'कॉपर ऑक्सीक्लोराइड 50 WP @ 3 ग्राम/लीटर का छिड़काव '
                                                                 'करें']},
                                     'te': {   'causes': [   'సెప్టోరియా లైకోపెర్సికి శిలీంద్రం',
                                                             'వేడి, తడి వాతావరణం మరియు నేలపై పడిన పాత పంట వ్యర్థాలు'],
                                               'display_name': 'టమోటా సెప్టోరియా ఆకు మచ్చ వ్యాధి',
                                               'prevention': [   'పంట కోత తర్వాత వ్యర్థాలను పొలంలో ఉంచకుండా కాల్చండి',
                                                                 'మొక్కజొన్న లేదా చిక్కుడు జాతి పంటలతో 2 సంవత్సరాల '
                                                                 'మార్पिడి చేయండి'],
                                               'symptoms': [   'కింది ఆకులపై నల్లటి అంచులు మరియు బూడిద రంగు కేంద్రం '
                                                               'ఉన్న చిన్న గుండ్రటి మచ్చలు',
                                                               'మచ్చల మధ్యలో చిన్న నల్లటి చుక్కలు కనిపించడం',
                                                               'ఆకులు పసుపు రంగులోకి మారి ఎండిపోయి రాలిపోవడం'],
                                               'treatments': [   'క్లోరోథలోనిల్ 75 WP ని లీటరు నీటికి 2 గ్రా లేదా '
                                                                 'మాంకోజెబ్ 75 WP ని 2 గ్రా కలిపి పిచికారీ చేయండి',
                                                                 'కాపర్ ఆక్సిక్లోరైడ్ 50 WP ని 3 గ్రా కలిపి పిచికారీ '
                                                                 'చేయండి']}},
    'Tomato Spider Mite': {   'en': {   'causes': [   'Tetranychus urticae (Two-spotted spider mite) insect pest',
                                                      'Hot, dry, dusty weather'],
                                        'display_name': 'Tomato Spider Mite',
                                        'prevention': [   'Keep crops well-watered (under-watered plants attract '
                                                          'mites)',
                                                          'Mist or spray water on leaves to wash away dust and mites'],
                                        'symptoms': [   'Fine yellow speckling or stippling on leaves',
                                                        'Fine webbing on leaf undersides and stems',
                                                        'Leaves bronze, dry up, and drop; plants look stunted'],
                                        'treatments': [   'Apply Abamectin 1.9 EC at 0.5ml/L or Propargite 57 EC at '
                                                          '2ml/L',
                                                          'Apply Neem Oil 5ml/L under leaves for organic control']},
                              'hi': {   'causes': [   'टेट्रानिकस अर्टिकाई (दो-धब्बों वाला मकड़ी घुन) कीट',
                                                      'गर्म, शुष्क और धूल भरा मौसम'],
                                        'display_name': 'टमाटर का मकड़ी घुन रोग',
                                        'prevention': [   'फसलों में अच्छी नमी रखें (तनावग्रस्त पौधों पर घुन जल्दी आते '
                                                          'हैं)',
                                                          'धूल और घुनों को धोने के लिए पत्तियों पर पानी की बौछार करें'],
                                        'symptoms': [   'पत्तियों पर बारीक पीले बिंदु या धब्बे',
                                                        'पत्तियों के निचले हिस्से और तनों पर महीन जाले',
                                                        'पत्तियां कांस्य (भूरे) रंग की होकर सूख जाती हैं; पौधे बौने '
                                                        'दिखते हैं'],
                                        'treatments': [   'एबामेक्टिन 1.9 EC @ 0.5 मिली/लीटर या प्रोपरगाइट 57 EC @ 2 '
                                                          'मिली/लीटर डालें',
                                                          'जैविक नियंत्रण के लिए पत्तियों के नीचे नीम के तेल @ 5 '
                                                          'मिली/लीटर का छिड़काव करें']},
                              'te': {   'causes': [   'టెట్రానిచస్ అర్టికా (రెండు చుక్కల సాలీడు నల్లి) కీటకం',
                                                      'వేడి, పొడి మరియు దూళితో కూడిన వాతావరణం'],
                                        'display_name': 'టమోటా సాలీడు మైట్ వ్యాధి',
                                        'prevention': [   'మొక్కలకు తగినంత నీరు అందించండి (ఎండిపోయిన మొక్కలకు నల్లులు '
                                                          'త్వరగా ఆశిస్తాయి)',
                                                          'ఆకులపై నీరు పిచికారీ చేసి దూళిని కడిగేయండి'],
                                        'symptoms': [   'ఆకులపై చిన్న పసుపు రంగు చుక్కలు',
                                                        'ఆకు వెనుక భాగంలో మరియు కాడలపై సన్నటి సాలీడు గూళ్లు',
                                                        'ఆకులు గోధుమ రంగులోకి మారి ఎండిపోవడం; మొక్కల పెరుగుదల '
                                                        'క్షీణించడం'],
                                        'treatments': [   'అబామెక్టిన్ 1.9 EC ని లీటరు నీటికి 0.5 మి.లీ లేదా '
                                                          'ప్రొపర్గైట్ 57 EC ని 2 మి.లీ కలిపి పిచికారీ చేయండి',
                                                          'సేంద్రీయ పద్ధతిలో నివారణకు వేప నూనెను ఆకుల వెనుక భాగంలో '
                                                          'పిచికారీ చేయండి']}},
    'Tomato Target Spot': {   'en': {   'causes': [   'Corynespora cassiicola fungus',
                                                      'Warm, humid conditions and long periods of leaf wetness'],
                                        'display_name': 'Tomato Target Spot',
                                        'prevention': [   'Prune plants to improve air circulation within canopy',
                                                          'Avoid overhead irrigation and use drip watering'],
                                        'symptoms': [   'Small brown spots on leaves with distinct yellow halos',
                                                        'Lesions have concentric circles resembling a target',
                                                        'Large pitting or target-like sunken spots on tomato fruit'],
                                        'treatments': [   'Spray Mancozeb 75 WP at 2g/L or Chlorothalonil 75 WP at '
                                                          '2g/L',
                                                          'Apply Azoxystrobin or Pyraclostrobin in severe cases']},
                              'hi': {   'causes': [   'कोरिनेस्पोरा कैसियोकोला कवक',
                                                      'गर्म, आर्द्र स्थिति और पत्तियों का लंबे समय तक गीला रहना'],
                                        'display_name': 'टमाटर का लक्षित धब्बा रोग',
                                        'prevention': [   'हवा के संचलन को बढ़ाने के लिए पौधों की छंटाई करें',
                                                          'ऊपर से पानी देने से बचें और ड्रिप सिंचाई का उपयोग करें'],
                                        'symptoms': [   'पत्तियों पर स्पष्ट पीले प्रभामंडल के साथ छोटे भूरे धब्बे',
                                                        'घावों में संकेंद्रित वृत्त होते हैं जो एक लक्ष्य (टारगेट) '
                                                        'जैसे दिखते हैं',
                                                        'टमाटर के फलों पर बड़े धंसे हुए लक्षित आकार के धब्बे'],
                                        'treatments': [   'मैंकोजेब 75 WP @ 2 ग्राम/लीटर या क्लोरोथैलोनिल 75 WP @ 2 '
                                                          'ग्राम/लीटर छिड़कें',
                                                          'गंभीर मामलों में एज़ोक्सीस्ट्रोबिन या पायराक्लोस्ट्रोबिन का '
                                                          'छिड़काव करें']},
                              'te': {   'causes': [   'కోరినేస్పోరా కాస్సికోలా శిలీంద్రం',
                                                      'వేడి, తేమతో కూడిన వాతావరణం మరియు ఆకులు ఎక్కువ సమయం తడిగా ఉండటం'],
                                        'display_name': 'టమోటా టార్గెట్ మచ్చ వ్యాధి',
                                        'prevention': [   'గాలి బాగా తగిలేలా ఆకులను కత్తిరించండి',
                                                          'ఆకులపై నీరు పిచికారీ చేయవద్దు మరియు డ్రిప్ విధానంలో నీరు '
                                                          'అందించండి'],
                                        'symptoms': [   'ఆకులపై స్పష్టమైన పసుపు వలయాలతో కూడిన చిన్న గోధుమ రంగు మచ్చలు',
                                                        'మచ్చలలో ఏకకేంద్ర వలయాలు ఉండి టార్గెట్ బోర్డ్ వలె కనిపించడం',
                                                        'పండ్లపై కుంగిపోయిన నల్లటి మచ్చలు ఏర్పడటం'],
                                        'treatments': [   'మాంకోజెబ్ 75 WP ని లీటరు నీటికి 2 గ్రా లేదా క్లోరోథలోనిల్ 2 '
                                                          'గ్రా కలిపి పిచికారీ చేయండి',
                                                          'తీవ్రంగా ఉన్నప్పుడు అజోక్సిస్ట్రోబిన్ లేదా '
                                                          'పైరాక్లోస్ట్రోబిన్ పిచికారీ చేయండి']}},
    'Tomato Yellow Leaf Curl Virus': {   'en': {   'causes': [   'Begomovirus transmitted by Bemisia tabaci (Whitefly) '
                                                                 'insect vector'],
                                                   'display_name': 'Tomato Yellow Leaf Curl Virus',
                                                   'prevention': [   'Install yellow sticky traps (10-15 per acre) to '
                                                                     'monitor and catch whiteflies',
                                                                     'Use fine insect netting in nurseries'],
                                                   'symptoms': [   'Severe upward curling and cupping of leaf edges',
                                                                   'Leaves yellow along margins and between veins '
                                                                   '(chlorosis)',
                                                                   'Stunted plant growth and failure to produce fruit'],
                                                   'treatments': [   'Spray Imidacloprid 17.8 SL at 0.5ml/L or '
                                                                     'Acetamiprid 20 SP at 0.5g/L',
                                                                     'Remove and bury/burn infected plants immediately '
                                                                     'to prevent spread']},
                                         'hi': {   'causes': ['बेगोमोवायरस, जो सफेद मक्खी कीट द्वारा फैलता है'],
                                                   'display_name': 'टमाटर का पीला पत्ता मरोड़ वायरस',
                                                   'prevention': [   'सफेद मक्खियों के लिए पीले चिपचिपे जाल (10-15 '
                                                                     'प्रति एकड़) लगाएं',
                                                                     'नर्सरी में महीन कीटरोधी नेट का उपयोग करें'],
                                                   'symptoms': [   'पत्तियों के किनारों का ऊपर की ओर मुड़ना और कप जैसा '
                                                                   'होना',
                                                                   'किनारों पर और शिराओं के बीच पत्तियों का पीला पड़ना '
                                                                   '(क्लोरोसिस)',
                                                                   'पौधे का विकास रुकना और फल न बनना'],
                                                   'treatments': [   'इमिडाक्लोप्रिड 17.8 SL @ 0.5 मिली/लीटर या '
                                                                     'एसिटामिप्रिड 20 SP @ 0.5 ग्राम/लीटर का छिड़काव '
                                                                     'करें',
                                                                     'फैलाव रोकने के लिए संक्रमित पौधों को उखाड़कर '
                                                                     'नष्ट करें']},
                                         'te': {   'causes': ['తెల్లదోమల ద్వారా వ్యాపించే బెగోమోవైరస్ తెగులు'],
                                                   'display_name': 'టమోటా పసుపు ఆకు ముడత వైరస్',
                                                   'prevention': [   'పొలంలో పసుపు రంగు జిగురు కార్డ్స్ (ఎకరానికి '
                                                                     '10-15) అమర్చండి',
                                                                     'నారు పెంచే సమయంలో దోమల నెట్ వాడండి'],
                                                   'symptoms': [   'ఆకులు పైకి ముడుచుకుని గిన్నె ఆకారంలా మారడం',
                                                                   'ఆకు అంచులు మరియు ఈనెల మధ్య పసుపు రంగులోకి మారడం',
                                                                   'మొక్కల ఎదుగుదల ఆగిపోవడం మరియు కాయలు కాయకపోవడం'],
                                                   'treatments': [   'తెల్లదోమల నివారణకు ఇమిడాక్లోప్రిడ్ 17.8 SL ని '
                                                                     'లీటరుకు 0.5 మి.లీ లేదా ఎసిటామిప్రిడ్ ని 0.5 గ్రా '
                                                                     'పిచికారీ చేయండి',
                                                                     'వ్యాధి సోకిన మొక్కలను వెంటనే పీకి '
                                                                     'కాల్చివేయండి']}}}

def get_treatment_info(disease_name: str, lang: str = "en") -> dict:
    """
    Returns the symptoms, causes, treatments, and prevention lists for a disease,
    fully translated to the target language (en, hi, te).
    """
    lang = (lang or "en").lower()
    if lang not in ["en", "hi", "te"]:
        lang = "en"
        
    # Match the disease name in the KB
    # Fallback to Healthy if it's healthy or not found
    matched_key = "Healthy"
    
    # Simple matching logic
    cleaned_name = disease_name.lower().replace("_", " ").replace("___", " ")
    
    if "healthy" in cleaned_name:
        matched_key = "Healthy"
    else:
        for key in KNOWLEDGE_BASE.keys():
            if key.lower() in cleaned_name or cleaned_name in key.lower():
                matched_key = key
                break
                
    # Fetch from KB
    entry = KNOWLEDGE_BASE.get(matched_key, KNOWLEDGE_BASE["Healthy"])
    
    # Get localized version, or fallback to english
    localized = entry.get(lang, entry["en"])
    
    # Return formatted dict
    return {
        "display_name": translate(disease_name, "diseases", lang),
        "symptoms": localized["symptoms"],
        "causes": localized["causes"],
        "treatments": localized["treatments"],
        "prevention": localized["prevention"]
    }
