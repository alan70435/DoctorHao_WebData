"""Editorial briefs. Original schematic artwork; clinical sign-off remains pending."""
REVIEW_DATE = '2026-09-10'
SOURCES = {
 'acl': ('AAOS • ACL injury', 'https://www.orthoinfo.org/treatment/acl-injury-does-it-require-surgery'),
 'meniscus': ('AAOS • Meniscus tears', 'https://www.orthoinfo.org/en/diseases--conditions/meniscus-tears-video/'),
 'shoulder': ('AAOS • Rotator cuff tears', 'https://www.orthoinfo.org/diseases--conditions/rotator-cuff-tears/'),
 'capsule': ('AAOS • Frozen shoulder', 'https://www.orthoinfo.org/diseases--conditions/frozen-shoulder/'),
 'achilles': ('AAOS • Achilles tendon rupture', 'https://www.orthoinfo.org/diseases--conditions/achilles-tendon-rupture-tear-video/'),
 'pes': ('AAOS • Pes anserine bursitis', 'https://www.orthoinfo.org/diseases--conditions/pes-anserine-knee-tendon-bursitis'),
 'foot': ('AAOS • Plantar fasciitis', 'https://www.orthoinfo.org/diseases--conditions/plantar-fasciitis-and-bone-spurs'),
 'hamstring': ('AAOS • Hamstring muscle injuries', 'https://www.orthoinfo.org/en/diseases--conditions/hamstring-muscle-injuries'),
 'ulnar': ('AAOS • Cubital tunnel syndrome', 'https://www.orthoinfo.org/diseases--conditions/ulnar-nerve-entrapment-at-the-elbow/'),
 'vein': ('NHLBI • Varicose veins', 'https://www.nhlbi.nih.gov/health/varicose-veins'),
 'clot': ('NHLBI • Venous thromboembolism', 'https://www.nhlbi.nih.gov/health/venous-thromboembolism'),
 'concussion': ('CDC • Responding to concussion', 'https://www.cdc.gov/heads-up/response/index.html'),
 'consensus': ('BJSM • Amsterdam concussion consensus', 'https://bjsm.bmj.com/content/57/11/695'),
 'activity': ('WHO • Physical activity', 'https://www.who.int/europe/news-room/fact-sheets/item/physical-activity'),
 'weight': ('NIDDK • Factors affecting weight', 'https://www.niddk.nih.gov/health-information/weight-management/adult-overweight-obesity/factors-affecting-weight-health'),
 'medication': ('NIDDK • Prescription weight management', 'https://www.niddk.nih.gov/health-information/weight-management/prescription-medications-treat-overweight-obesity'),
 'diabetes': ('NIDDK • Healthy living with diabetes', 'https://www.niddk.nih.gov/health-information/diabetes/overview/healthy-living-with-diabetes'),
 'supplements': ('NIH ODS • Exercise and supplements', 'https://ods.od.nih.gov/factsheets/ExerciseAndAthleticPerformance-HealthProfessional/'),
 'painmedicine': ('FDA • Acetaminophen safety', 'https://www.fda.gov/consumers/consumer-updates/dont-overuse-acetaminophen'),
}
# slug | 3-D scene | short title | three independently readable callouts | references | safety note
BRIEFS = '''
achilles-rupture-return|achilles|阿基里斯腱：力量的連結|小腿肌群：腓腸肌與比目魚肌的力量經肌腱傳遞。|阿基里斯腱：連接小腿後側肌群與跟骨；圖中橘色為關注區。|回到運動：依傷勢、治療與功能評估循序恢復，不以天數單獨決定。|achilles|突然啪一聲、推蹬無力或無法正常走路，應及時就醫。
acl-tear-return-to-play|knee-acl|前十字韌帶與膝穩定|股骨與脛骨：韌帶位在兩骨之間，圖中部分結構移開以利觀看。|前十字韌帶：協助限制脛骨過度向前位移，並參與旋轉穩定。|功能恢復：回場需綜合肌力、動作控制及醫療評估，不只看影像。|acl|模型為簡化示意，不能判斷個人的撕裂程度或回場日期。
alcohol-and-weight-loss|nutrition-alcohol|酒精與體重管理|酒精飲品：也會帶入能量；飲用量與頻率都值得記錄。|生活脈絡：飲食、睡眠與活動需一起看，不把單一飲品當成減重法。|個別風險：用藥、肝臟疾病及其他健康狀況，應與醫療人員討論。|weight|不建議為了健康或減重開始飲酒；本圖不宣稱任何酒類有保健功效。
athletes-and-blood-clots|vein-clot|血栓：運動員也要留意|靜脈管腔：圖中藍色為靜脈示意，不是動脈斑塊。|血塊：深層靜脈血栓可影響回流；部分血塊可能移至肺部。|警覺症狀：單側肢體腫痛需評估；突發胸痛或呼吸困難需緊急就醫。|clot|無症狀也不能排除血栓；請勿用揉捏小腿或自行測試代替診斷。
badminton-is-not-leisure|shoulder-load|羽球：肩部負荷與控制|肩胛骨：肩帶的活動與控制是揮拍動作的一環。|旋轉肌袖：包覆肱骨頭的肌腱群，協助肩部動作與穩定。|負荷安排：反覆過頭揮拍的強度、恢復與症狀要一起評估。|shoulder,activity|這是肩部重點圖，不代表羽球傷害只發生在肩膀。
basketball-injury-prevention|ankle-lateral|籃球：認識踝外側結構|脛骨與腓骨：構成踝部上方的骨性結構。|外側韌帶：足部內翻時，踝外側組織可能受到牽拉。|恢復控制：逐步重建活動、肌力與平衡，再評估跑跳需求。|foot,activity|不能負重、明顯變形或持續腫痛應就醫；本圖不提供傷勢分級。
calf-muscle-tear|calf-tear|網球腿：不只是小腿痠|腓腸肌：位於小腿後側表層，跨過膝關節與踝關節。|肌腱交界：肌肉與肌腱交接處，是需要評估的區域之一。|鑑別診斷：小腿痛可能來自多種問題，不能只依疼痛位置定論。|achilles,clot|單側小腿腫痛需排除血栓等問題，不應一律當成拉傷。
deadlift-everyone-should-learn|movement-hinge|硬舉：先認識髖折疊|髖部後移：軀幹與髖部協調，練習可控制的活動範圍。|軀幹穩定：呼吸、軀幹控制與負荷需配合個人能力。|循序增加：先學動作，再調整重量；不是所有人都需相同姿勢或重量。|activity|人偶為動作概念示意，不是個別化教學或下背痛的保證療法。
diabetes-aunt-three-things|metabolism-diabetes|糖尿病照護：三個面向|飲食計畫：食物種類、份量與用餐習慣一起調整。|規律活動：依身體能力與用藥狀況安排活動。|追蹤與用藥：記錄血糖並按醫療團隊建議治療，不自行停藥。|diabetes|個案的血糖改善幅度不能直接套用到其他人。
does-jogging-hurt-knees|knee-overview|慢跑與膝蓋：看懂結構|關節軟骨：覆蓋骨端，與半月板不是同一種結構。|半月板：位在股骨與脛骨間，協助負荷分散。|負荷管理：把跑量、肌力、恢復及既有症狀一起考量。|meniscus,activity|不以圖像暗示跑步會保證軟骨增生，或任何膝痛都可繼續跑。
eating-for-training|nutrition-recovery|訓練後：補充與恢復|主食：碳水化合物是訓練後營養規劃的一部分。|蛋白質來源：從日常食物與整日攝取量一起考量。|水分與休息：依流汗、環境與訓練量調整，讓恢復跟上負荷。|supplements|餐盤是食物類別示意，不是固定份量、比例或通用營養處方。
fish-oil-and-vitamin-d|nutrition-supplements|補充之前，先評估需求|日常飲食：先確認食物來源與平常攝取情況。|補充品：魚油與維生素 D 不是同一種營養素，也不能相互替代。|專業評估：劑量、檢驗需求與藥物交互作用，需個別確認。|supplements|不宣稱補充品能保證預防疾病；不提供自行加量建議。
fried-food-and-mood|nutrition-mood|飲食與情緒：別畫上等號|飲食習慣：評估的是整體飲食模式，而不只一份食物。|情緒與睡眠：心理健康也受到睡眠、壓力與生活環境影響。|研究解讀：观察到關聯不等於證明因果，不能用飲食圖診斷憂鬱症。|weight|此圖不把油炸食物描繪成造成憂鬱症的單一原因。
frozen-shoulder-self-check|shoulder-capsule|五十肩：關節囊的改變|球與窩：肱骨頭與肩胛骨關節窩構成肩關節。|關節囊：五十肩可能出現關節囊增厚、緊縮與活動受限。|診察重點：主動與被動活動、病史及其他原因需一起評估。|capsule|在家動作只能提供症狀線索，不能單憑三個動作確診。
glp1-during-treatment|metabolism-care|體重治療：用藥以外的事|飲食支持：維持足夠營養與水分，不以極端少吃為目標。|活動與肌力：依能力安排有氧與阻力訓練，照顧日常功能。|定期追蹤：副作用、療效與後續計畫由醫療團隊共同評估。|medication,activity|請勿依示意圖自行改劑量、移動注射日期或停藥。
glp1-precautions-and-contraindications|safety-screening|用藥前：把資訊說清楚|藥物清單：處方藥、成藥及補充品都要告知。|相關病史：個人與家族病史、懷孕計畫等交由醫師評估。|依品項確認：不同藥物的適應症與注意事項，以當地核准仿單為準。|medication|這不是完整禁忌清單，也不能代替處方評估。
glp1-what-it-is-and-who-fits|metabolism-appetite|GLP-1：訊號，不是溶脂|腸道與訊號：GLP-1 是與進食反應相關的荷爾蒙之一。|食慾調節：相關藥物可作用於調節食慾與進食的訊號路徑。|整體治療：藥物搭配營養、活動與追蹤，不是直接把脂肪溶掉。|medication|器官採分離排列的概念圖，位置與大小非解剖比例；GLP-1 不是胰島素。
glute-training-best-exercises|hip-glutes|臀肌：不只是外觀|臀大肌：參與髖部伸展，和日常起身、登階等動作相關。|臀中肌區：位在髖外側，參與髖部控制與骨盆穩定。|訓練安排：動作選擇需配合目標、能力與症狀，不只看單次研究排名。|activity|肌群為分層簡化示意，不是精確肌電圖或個人訓練處方。
gym-trap-cards|movement-training|器材沒有代替動作控制|起始設定：座椅、支點與行程需配合自己的身體。|動作控制：能控制的範圍與負荷，比勉強完成更重要。|尋求回饋：有不適或不確定時，請合格教練或醫療人員協助。|activity|不把某種器材一概標為危險，也不以人偶示意取代現場指導。
gymnastics-injuries|wrist-load|體操：上肢承重的提醒|前臂骨：橈骨與尺骨把負荷傳往肘與肩。|腕部結構：小骨、韌帶與肌腱共同參與支撐。|成長中的運動員：持續疼痛或功能改變，應接受適齡評估。|activity|兒少骨骼仍在發育；本模型不顯示或判讀生長板傷勢。
hamstring-strain-curry|hamstrings|腿後肌：從受傷到回場|腿後肌群：位在大腿後側，與髖伸展、膝屈曲有關。|受力區域：衝刺或拉長狀態下受力，可能造成肌肉肌腱損傷。|功能性進程：恢復活動、肌力及專項能力，再由團隊評估回場。|hamstring|不以球員個案或固定週數預測個人恢復時間。
hiking-is-strength-training|movement-step|登山：上坡與下坡的控制|踏階：髖、膝與踝協同完成向上移動。|下坡：重心下降也需要肌肉控制，不只是往下走。|行程安排：路線、負重、體力與休息要一起規劃。|activity|圖中的階梯為概念模型，不代表特定登山路線或固定關節受力倍數。
how-much-exercise-per-week|movement-week|每週活動：有氧加肌力|有氧活動：一般成人每週可朝 150–300 分鐘中等強度活動累積。|肌力活動：每週至少 2 天，涵蓋主要肌群。|從能力出發：少量活動也有價值，逐漸建立可持續的習慣。|activity|上述是一般成人指引，不適用於所有病況；兒少與高齡者另有重點。
knee-oa-treatment-options|knee-oa|膝關節炎：結構與功能|關節表面：退化可能伴隨軟骨變薄與骨端改變，表現因人而異。|周邊肌力：膝部功能也受到肌力、活動與負荷影響。|共同決策：治療要整合症狀、功能需求與個別風險。|meniscus,activity|橘色只是關注區，不代表疼痛程度；不暗示注射可保證軟骨再生。
knee-pain-diagnosis-first|knee-overview|膝痛：先知道哪裡出問題|骨與軟骨：骨端關節面只是膝部評估的一部分。|韌帶與半月板：不同組織可能出現相似的疼痛或卡住感。|整體診察：病史、動作與必要檢查一起判斷，不能只看痛點。|meniscus,acl|模型不能定位個人的病灶；原有門診照片與草圖仍保留。
mcl-sprain-grades|knee-mcl|內側副韌帶：膝內側支撐|內側位置：MCL 位在膝內側，與外側的腓骨分處不同側。|連接兩骨：連接股骨與脛骨，參與抵抗膝部外翻受力。|傷勢評估：拉傷程度與穩定性需實際檢查，不能只依腫痛分級。|acl|圖中不以顏色代替第一、二、三級診斷，也不預設恢復天數。
meal-order-veg-protein-carb|nutrition-order|用餐順序：只是其中一環|蔬菜：可以從蔬菜開始安排均衡的一餐。|蛋白質：與其他食物共同搭配，而不是排除主食。|主食與份量：整餐份量、食物種類及用藥同樣重要。|diabetes|不把纖維畫成腸道保護膜；順序不是保證血糖穩定的唯一條件。
meniscus-tear-embiid|knee-meniscus|半月板：膝內的纖維軟骨|兩片半月板：內、外側各一片，位在股骨與脛骨之間。|負荷分散：協助關節承重與穩定，不等於覆蓋骨端的關節軟骨。|撕裂評估：位置、型態、症狀與個人需求影響治療選擇。|meniscus|示意圖不代表任何特定運動員的影像或實際傷勢。
msk-ultrasound-self-study|assessment-ultrasound|肌骨超音波：從定位開始|探頭：聲波由探頭進出，檢查方向需對照解剖。|組織層次：皮膚下有不同軟組織，不能只憑亮暗判讀病灶。|動態評估：影像需结合病史、理學檢查及專業操作。|shoulder,ulnar|畫面完全是模擬聲束與組織，不是超音波檢查影像。
numbness-nerve-hydrodissection|elbow-ulnar|手麻：以尺神經為例|肘內側：尺神經經過肘部內側附近的通道。|神經走向：壓迫可能影響前臂與手部感覺；分布需實際檢查。|治療評估：先釐清原因，再決定活動調整、復健或其他處理。|ulnar|本圖不顯示穿刺路徑；神經解套須由合格醫療人員評估與施作。
painkillers-headache-menstrual|safety-medication|止痛藥：先讀成分|成分名稱：不同商品可能含相同成分，不能只看包裝。|避免重複：成藥、感冒藥與處方藥需一起核對。|個別安全：病史、其他用藥與症狀會影響選擇，請諮詢醫藥人員。|painmedicine|本圖不提供通用劑量；突發劇烈或異常頭痛應及時就醫。
pes-anserine-bursitis|knee-pes|鵝掌區：在膝內側下方|三條肌腱：縫匠肌、股薄肌與半腱肌的肌腱匯向脛骨內側。|鵝掌滑囊：在肌腱與深層組織間，協助減少摩擦。|相似症狀：此區疼痛也需與內側韌帶、半月板等問題區分。|pes|位置為簡化示意；鵝掌肌腱問題與滑囊發炎不能只憑痛點混為一談。
pickleball-injury-risks|elbow-tendon|匹克球：上肢也要準備|肘部骨點：肌腱附著於骨骼周邊，是受力傳遞的一環。|前臂伸肌：反覆握拍與揮拍可能增加相關組織負荷。|全身準備：除了上肢，步伐、平衡與跌倒風險也要一起注意。|activity|本圖只聚焦肘部；腕部骨折、踝傷等仍需個別評估。
plantar-fasciitis-morning-heel-pain|plantar-fascia|足底筋膜：腳跟到前足|跟骨：足底筋膜由腳跟附近向前延伸。|筋膜扇形束：沿足底延展，參與支撐足弓。|疼痛線索：晨起第一步痛是常見表現，但仍需排除其他原因。|foot|骨刺不等於疼痛原因；不依單一症狀自行確診。
quick-weight-loss-pill-bags|safety-weightpills|減重藥袋：來路與成分要清楚|核對來源：確認提供者、完整藥名與使用說明。|別追求極速：體重變化不等於脂肪變化，也可能涉及水分與肌肉。|安全追蹤：出現不適或對成分不清楚，請先詢問醫師或藥師。|medication,weight|不提供減重藥混搭方式、利尿或瀉藥操作，也不承諾快速減重。
rotator-cuff-housework|shoulder-cuff|旋轉肌袖：肩部的協同|肩胛骨與肱骨：骨性結構是肩部動作的基礎。|旋轉肌袖：四條肌肉及其肌腱共同參與抬手與旋轉。|肩峰下空間：反覆負荷與軟組織問題需结合症狀評估。|shoulder|圖中特別呈現棘上肌腱；不代表所有肩痛都是肌袖撕裂。
runners-knee-and-patellar-strap|knee-patellar|膝前痛：先分清位置|髕股區域：髕骨與股骨之間的區域可能出現疼痛。|髕骨肌腱：位在髕骨下方，連接至脛骨，與前者不同。|依原因處理：護具是否合適需看診斷、負荷與個人反應。|meniscus,activity|髕股疼痛與髕腱病不能當成同一種病；髕骨帶不是通用解方。
runners-need-strength|movement-running|跑者肌力：把控制補起來|髖部控制：讓髖與軀幹一起參與動作。|膝踝協作：練習肌力、平衡與可控制的落地。|負荷搭配：跑量、肌力訓練與恢復需整體安排。|activity|人偶不呈現實際受力數值，也不保證做某一動作就不會受傷。
sideline-doctor-abcde|assessment-abcde|場邊評估：先處理危急狀況|先求援：確認現場安全並啟動緊急應變。|系統評估：由受訓人員以 ABCDE 等架構持續評估。|再決定處置：生命威脅優先；後續轉送與回場由專業團隊判斷。|concussion|ABCDE：Airway、Breathing、Circulation、Disability、Exposure；不是自行復位指南。
sport-related-concussion|brain-concussion|疑似腦震盪：立即停止運動|辨識：頭部或身體撞擊後，留意症狀與行為改變。|移出比賽：疑似腦震盪應立即停止參賽，當天不回場。|醫療評估：持續觀察警訊，由醫療人員評估及安排漸進恢復。|concussion,consensus|本圖不把出血當作腦震盪必要條件；不以固定天數承諾回場。
squat-essentials|movement-squat|深蹲：控制優先於重量|髖膝踝協調：依個人能力選擇能控制的深度與站姿。|軀幹與呼吸：建立可維持的穩定與呼吸節奏。|逐步增加：先練習再調整負荷，有不適時重新評估。|activity|沒有適合所有人的單一重量目標；人偶不是動作合格判定器。
start-exercise-with-weight-loss|movement-week|體重照護：讓活動成為日常|有氧選擇：走路、騎車等活動可依喜好與能力安排。|肌力訓練：與有氧互補，重視日常功能及肌肉健康。|可持續性：從能做到的份量開始，留意飲食、睡眠與恢復。|activity,medication|不將游泳或其他運動標為對所有疾病都安全，需依個別狀況調整。
strength-is-maintenance-and-treatment|muscle-fibers|肌肉健康：力量與功能|肌纖維：肌肉以纖維結構組成，圖中放大以利觀看。|神經肌肉控制：力量與動作協調共同影響日常功能。|阻力與營養：訓練、營養與恢復是長期照護的一部分。|activity,supplements|未呈現肌少症診斷切點；不能只看圖或小腿圍自行診斷。
supplements-overview-ranking|nutrition-supplements|補劑不是訓練的捷徑|先有基礎：規律訓練、充足飲食與恢復仍是核心。|看目標與證據：不同補充品、運動種類與個體反應並不相同。|注意品質：核對成分、來源與交互作用，競技選手更需留意禁藥風險。|supplements|不以排行榜保證效果，也不提供所有人通用的補充劑量。
supplements-vs-medication-cholesterol|safety-medication|血脂管理：不是包裝比較|處方藥：依個人心血管風險與檢查結果評估。|補充品：不能因為標榜天然，就視為與藥物相同。|共同核對：把藥品與補充品清單一起交給醫師或藥師。|supplements,painmedicine|不自行以保健食品替換處方；圖中不做療效百分比比較。
trigger-point-injection|muscle-trigger|肌筋膜疼痛：先評估再處理|肌肉纖維：圖中肌束為放大示意，不是影像檢查結果。|關注區域：局部壓痛只是線索，需要结合病史與檢查。|治療選擇：不同處理有各自適應情況、限制與風險。|activity|橘色不代表可見的病灶；圖中不提供進針深度、角度或施打步驟。
varicose-veins-and-lifting|vein-valve|靜脈回流：瓣膜與肌肉|靜脈瓣膜：協助血液朝心臟方向回流。|小腿活動：肌肉收縮與放鬆可以協助靜脈回流。|症狀與評估：腫脹、不適或皮膚改變需讓醫療人員評估。|vein|不將固定心率或重量百分比當作所有人的安全上限。
weight-and-joint-pain|metabolism-body|體重與功能：一起照顧|關節負荷：體重、活動與肌力共同影響關節使用。|整體健康：症狀還可能牽涉睡眠及其他健康問題。|整合照護：以營養、活動與必要治療共同支持生活功能。|weight,medication|不把體重視為疼痛的唯一原因，也不保證減重後所有症狀都會消失。
weight-is-not-the-only-number|metabolism-body|健康不只是一個數字|身體組成：體重不能完整表示肌肉、脂肪與健康狀況。|生活功能：飲食、睡眠、活動與精神狀況同樣值得關心。|個別目標：與醫療團隊一起設定適合自己的健康方向。|weight|不以體型定義價值，也不鼓勵正常或過輕者為外觀追求用藥減重。
why-diet-and-exercise-alone-is-hard|metabolism-appetite|體重調節：不只是意志力|生理訊號：食慾與能量調節涉及多種生理因素。|生活環境：飲食可近性、睡眠、壓力與活動環境都有影響。|支持而非責備：找出可調整的因素，必要時加入專業協助。|weight,medication|不以單一平均降幅推估個人結果，也不把困難歸咎於自制力。
yamamoto-no-weight-training|movement-agility|運動表現：訓練需要個別化|基礎能力：力量、控制與恢復是安排訓練時的考量。|專項需求：速度、協調與技巧需配合不同運動項目。|個別調整：考慮賽季、疲勞與傷勢，不直接照抄名人課表。|activity|人偶不代表特定球員；不把新聞標題當成個人訓練建議。
you-need-a-coach|movement-coach|好訓練：看見細節與回饋|先評估：能力、目標與不適需要先說清楚。|動作回饋：由合格教練協助觀察與調整，再循序增加負荷。|持續追蹤：用紀錄了解進步與疲勞，必要時轉介醫療評估。|activity|模型是教學概念，不暗示沒有教練就必定受傷或無法進步。
'''.strip()

def briefs():
    items = []
    for line in BRIEFS.splitlines():
        cells = line.replace('观察', '觀察').replace('结合', '結合').split('|')
        if len(cells) != 8:
            raise ValueError(f'Invalid brief: {cells[0]} ({len(cells)} columns)')
        slug, scene, title, p1, p2, p3, refs, caution = cells
        points = []
        for point in (p1, p2, p3):
            heading, text = point.split('：', 1)
            points.append({'heading': heading, 'text': text})
        items.append({'slug': slug, 'scene': scene, 'title': title, 'points': points,
                      'sourceIds': refs.split(','), 'caution': caution,
                      'reviewStatus': 'clinician-review-pending'})
    assert len(items) == 52 and len({i['slug'] for i in items}) == 52
    return items
