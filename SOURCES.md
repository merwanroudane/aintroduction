# المصادر — Sources

الببليوغرافيا الكاملة للمقرر. **هذا الملف مولَّد آليًا** من ملفات `references.yml`، فلا يُحرَّر يدويًا:

```bash
python scripts/build_sources.py
```

---

## منهج التحقق

لم يُذكر في هذا المقرر مصدر لم يُفحص قبل الاستشهاد به. وإجراء الفحص:

| نوع المصدر | كيف تُحقِّق منه |
|---|---|
| مقال بمعرّف DOI | واجهة Crossref البرمجية، مع مقارنة العنوان والمجلة والسنة والمجلد والصفحات وقائمة المؤلفين بما في الملف |
| مسودة على arXiv | واجهة arXiv البرمجية، مع مقارنة العنوان والمؤلفين وسنة الإيداع |
| فيديو | واجهة oEmbed للتأكد من أن المقطع ما زال متاحًا |
| توثيق أو معيار أو نص قانوني | جلب الصفحة وقراءتها، وتسجيل تاريخ القراءة |

والمواقع التي ترفض الطلبات الآلية (403 لأي نص برمجي) موسومة بـ`bot_blocked` في `references.yml`. ولا يتخطّاها `scripts/check_links.py` إلا إذا حمل المصدر **دليلًا آخر**: معرّف DOI يمكن حلّه، أو تاريخ `browser_verified` يسجّل أن إنسانًا فتح الصفحة. وبغير ذلك يُفحص الرابط كغيره ويُعدّ فشله فشلًا حقيقيًا — حتى لا يختبئ رابط معطوب خلف الوسم.

**لإعادة فحص كل الروابط:**

```bash
python scripts/check_links.py
```

## ما لا يدّعيه هذا المقرر

الانضباط في التوثيق يشمل **الامتناع** عن الادعاء بقدر ما يشمل الإسناد. وسجلات `research/logs/mXX.md` تسجّل لكل محور ما فُحص وما وُجد وما امتنع المحور عن قوله. والقواعد العامة:

- **لا أرقام دقة لأدوات كشف النصوص أو الصور المولَّدة** — تختلف بالأداة والإصدار ونوع المحتوى، وتتقادم فورًا. والمذكور هو الحدود **البنيوية** والنتيجة المعيارية.
- **لا خلاصات قانونية في حقوق المصنفات** — الدعاوى منظورة وتختلف بين الأنظمة. والمذكور هو **الأسئلة التي تُطرح** والإحالة إلى النص الملزم وإلى المختص.
- **لا ادعاءات عن قدرات جيل بعينه من النماذج** — وحين يُذكر حدّ تقني يُذكر معه **سببه البنيوي**، ويُقال صراحةً إنه يتحسن.
- **لا ترتيب ولا تفضيل بين المنتجات** — المقارنة وظيفية، مبنية على وثائق رسمية مؤرَّخة، وتنبّه إلى أنها تتغير.

---

## إحصاء

- **192** مصدرًا: **87** بمعرّف DOI، و**105** برابط مباشر.
- بحسب النوع: مقال محكّم (84)، مسودة بحثية (53)، توثيق رسمي (19)، معيار أو موقف رسمي (13)، كتاب (8)، صفحة ويب (6)، تقرير (5)، نص قانوني (3)، مقرر (1).

---

## أسس الذكاء الاصطناعي — AI Foundations (22)

- **Bostrom, N.** (2014). *Superintelligence: Paths, Dangers, Strategies*. Oxford University Press. <https://global.oup.com/academic/product/superintelligence-9780199678112>  
<sub>كتاب · المحور 3 · تُحقِّق منه في 2026-09-26</sub>
- **Bubeck, S., Chandrasekaran, V., Eldan, R., et al.** (2023). *Sparks of Artificial General Intelligence: Early experiments with GPT-4*. arXiv:2303.12712 (Microsoft Research). <https://arxiv.org/abs/2303.12712>  
<sub>مسودة بحثية · المحور 3 · تُحقِّق منه في 2026-09-26</sub>
- **Chollet, F.** (2019). *On the Measure of Intelligence*. arXiv:1911.01547. <https://arxiv.org/abs/1911.01547>  
<sub>مسودة بحثية · المحور 3 · تُحقِّق منه في 2026-09-26</sub>
- **Goertzel, B.** (2014). *Artificial General Intelligence: Concept, State of the Art, and Future Prospects*. Journal of Artificial General Intelligence, 5(1), 1–48. <https://doi.org/10.2478/jagi-2014-0001>  
<sub>مقال محكّم · المحور 3 · تُحقِّق منه في 2026-09-26</sub>
- **Grace, K., Stewart, H., Sandkühler, J. F., Thomas, S., Weinstein-Raun, B., & Brauner, J.** (2024). *Thousands of AI Authors on the Future of AI*. arXiv:2401.02843. <https://arxiv.org/abs/2401.02843>  
<sub>مسودة بحثية · المحور 3 · تُحقِّق منه في 2026-09-26</sub>
- **Hintze, A.** (2016). *Understanding the four types of AI, from reactive robots to self-aware beings*. The Conversation. <https://theconversation.com/understanding-the-four-types-of-ai-from-reactive-robots-to-self-aware-beings-67616>  
<sub>صفحة ويب · المحور 3 · تُحقِّق منه في 2026-09-26</sub>
- **Jumper, J., Evans, R., Pritzel, A., et al.** (2021). *Highly accurate protein structure prediction with AlphaFold*. Nature, 596, 583–589. <https://doi.org/10.1038/s41586-021-03819-2>  
<sub>مقال محكّم · المحور 1 · تُحقِّق منه في 2026-09-26</sub>
- **Legg, S., & Hutter, M.** (2007). *A Collection of Definitions of Intelligence*. arXiv:0706.3639. <https://arxiv.org/abs/0706.3639>  
<sub>مسودة بحثية · المحور 1 · تُحقِّق منه في 2026-09-26</sub>
- **Legg, S., & Hutter, M.** (2007). *Universal Intelligence: A Definition of Machine Intelligence*. arXiv:0712.3329 (Minds and Machines, 17(4)). <https://arxiv.org/abs/0712.3329>  
<sub>مقال محكّم · المحور 1 · تُحقِّق منه في 2026-09-26</sub>
- **McCarthy, J.** (2007). *What is Artificial Intelligence? (Basic Questions)*. Stanford University. <http://jmc.stanford.edu/artificial-intelligence/what-is-ai/index.html>  
<sub>صفحة ويب · المحور 1 · تُحقِّق منه في 2026-09-26</sub>
- **Mitchell, M.** (2019). *Artificial Intelligence: A Guide for Thinking Humans*. Farrar, Straus and Giroux. <https://melaniemitchell.me/aibook/>  
<sub>كتاب · المحور 3 · تُحقِّق منه في 2026-09-26</sub>
- **Mitchell, M.** (2021). *Why AI is Harder Than We Think*. arXiv:2104.12871. <https://arxiv.org/abs/2104.12871>  
<sub>مسودة بحثية · المحاور 1، 2، 3، 5 · تُحقِّق منه في 2026-09-26</sub>
- **Morris, M. R., Sohl-Dickstein, J., Fiedel, N., et al.** (2023). *Levels of AGI for Operationalizing Progress on the Path to AGI*. arXiv:2311.02462 (Google DeepMind). <https://arxiv.org/abs/2311.02462>  
<sub>مسودة بحثية · المحاور 3، 7 · تُحقِّق منه في 2026-09-26</sub>
- **Premack, D., & Woodruff, G.** (1978). *Does the chimpanzee have a theory of mind?*. Behavioral and Brain Sciences, 1(4), 515–526. <https://doi.org/10.1017/S0140525X00076512>  
<sub>مقال محكّم · المحور 3 · تُحقِّق منه في 2026-09-26</sub>
- **Russell, S.** (2019). *Human Compatible: Artificial Intelligence and the Problem of Control*. Viking. <https://people.eecs.berkeley.edu/~russell/hc.html>  
<sub>كتاب · المحاور 3، 6 · تُحقِّق منه في 2026-09-26</sub>
- **Russell, S., & Norvig, P.** (2021). *Artificial Intelligence: A Modern Approach (4th ed.)*. Pearson. <https://aima.cs.berkeley.edu/>  
<sub>كتاب · المحاور 1، 2، 3، 4، 7 · تُحقِّق منه في 2026-09-26</sub>
- **Silver, D., Huang, A., Maddison, C. J., et al.** (2016). *Mastering the game of Go with deep neural networks and tree search*. Nature, 529, 484–489. <https://doi.org/10.1038/nature16961>  
<sub>مقال محكّم · المحاور 1، 2 · تُحقِّق منه في 2026-09-26</sub>
- **Stanford Institute for Human-Centered AI (HAI)** (2025). *The 2025 AI Index Report*. Stanford University. <https://hai.stanford.edu/ai-index/2025-ai-index-report>  
<sub>تقرير · المحاور 1، 2 · تُحقِّق منه في 2026-09-26</sub>
- **The Royal Swedish Academy of Sciences** (2024). *Press release: The Nobel Prize in Chemistry 2024*. NobelPrize.org. <https://www.nobelprize.org/prizes/chemistry/2024/press-release/>  
<sub>صفحة ويب · المحور 1 · تُحقِّق منه في 2026-09-26</sub>
- **Topol, E. J.** (2019). *High-performance medicine: the convergence of human and artificial intelligence*. Nature Medicine, 25, 44–56. <https://doi.org/10.1038/s41591-018-0300-7>  
<sub>مقال محكّم · المحور 1 · تُحقِّق منه في 2026-09-26</sub>
- **Ullman, T.** (2023). *Large Language Models Fail on Trivial Alterations to Theory-of-Mind Tasks*. arXiv:2302.08399. <https://arxiv.org/abs/2302.08399>  
<sub>مسودة بحثية · المحور 3 · تُحقِّق منه في 2026-09-26</sub>
- **Wang, P.** (2019). *On Defining Artificial Intelligence*. Journal of Artificial General Intelligence, 10(2), 1–37. <https://doi.org/10.2478/jagi-2019-0002>  
<sub>مقال محكّم · المحور 1 · تُحقِّق منه في 2026-09-26</sub>

## تاريخ الذكاء الاصطناعي — AI History (14)

- **Bahdanau, D., Cho, K., & Bengio, Y.** (2014). *Neural Machine Translation by Jointly Learning to Align and Translate*. arXiv:1409.0473 (ICLR 2015). <https://arxiv.org/abs/1409.0473>  
<sub>مسودة بحثية · المحاور 2، 7 · تُحقِّق منه في 2026-09-27</sub>
- **Deng, J., Dong, W., Socher, R., Li, L.-J., Li, K., & Fei-Fei, L.** (2009). *ImageNet: A large-scale hierarchical image database*. 2009 IEEE Conference on Computer Vision and Pattern Recognition (CVPR). <https://doi.org/10.1109/CVPR.2009.5206848>  
<sub>مقال محكّم · المحور 2 · تُحقِّق منه في 2026-09-27</sub>
- **IBM** (2024). *Deep Blue (IBM History)*. IBM. <https://www.ibm.com/history/deep-blue>  
<sub>صفحة ويب · المحور 2 · تُحقِّق منه في 2026-09-27</sub>
- **Lighthill, J.** (1973). *Artificial Intelligence: A General Survey (the Lighthill Report)*. Science Research Council, UK. <https://www.chilton-computing.org.uk/inf/literature/reports/lighthill_report/contents.htm>  
<sub>تقرير · المحور 2 · تُحقِّق منه في 2026-09-27</sub>
- **Lindsay, R. K., Buchanan, B. G., Feigenbaum, E. A., & Lederberg, J.** (1993). *DENDRAL: A case study of the first expert system for scientific hypothesis formation*. Artificial Intelligence, 61(2), 209–261. <https://doi.org/10.1016/0004-3702(93)90068-M>  
<sub>مقال محكّم · المحور 2 · تُحقِّق منه في 2026-09-27</sub>
- **McCarthy, J., Minsky, M. L., Rochester, N., & Shannon, C. E.** (1955). *A Proposal for the Dartmouth Summer Research Project on Artificial Intelligence*. Dartmouth College (the proposal that coined the term; the workshop was held in 1956). <http://raysolomonoff.com/dartmouth/boxa/dart564props.pdf>  
<sub>تقرير · المحور 2 · تُحقِّق منه في 2026-09-27</sub>
- **McCulloch, W. S., & Pitts, W.** (1943). *A logical calculus of the ideas immanent in nervous activity*. The Bulletin of Mathematical Biophysics, 5, 115–133. <https://doi.org/10.1007/BF02478259>  
<sub>مقال محكّم · المحور 2 · تُحقِّق منه في 2026-09-27</sub>
- **Mnih, V., Kavukcuoglu, K., Silver, D., et al.** (2015). *Human-level control through deep reinforcement learning*. Nature, 518, 529–533. <https://doi.org/10.1038/nature14236>  
<sub>مقال محكّم · المحاور 2، 4 · تُحقِّق منه في 2026-09-27</sub>
- **Rosenblatt, F.** (1958). *The perceptron: A probabilistic model for information storage and organization in the brain*. Psychological Review, 65(6), 386–408. <https://doi.org/10.1037/h0042519>  
<sub>مقال محكّم · المحاور 2، 4 · تُحقِّق منه في 2026-09-27</sub>
- **Rumelhart, D. E., Hinton, G. E., & Williams, R. J.** (1986). *Learning representations by back-propagating errors*. Nature, 323, 533–536. <https://doi.org/10.1038/323533a0>  
<sub>مقال محكّم · المحاور 2، 4 · تُحقِّق منه في 2026-09-27</sub>
- **Samuel, A. L.** (1959). *Some Studies in Machine Learning Using the Game of Checkers*. IBM Journal of Research and Development, 3(3), 210–229. <https://doi.org/10.1147/rd.33.0210>  
<sub>مقال محكّم · المحور 2 · تُحقِّق منه في 2026-09-27</sub>
- **Searle, J. R.** (1980). *Minds, brains, and programs*. Behavioral and Brain Sciences, 3(3), 417–424. <https://doi.org/10.1017/S0140525X00005756>  
<sub>مقال محكّم · المحور 2 · تُحقِّق منه في 2026-09-27</sub>
- **Silver, D., Hubert, T., Schrittwieser, J., et al.** (2018). *A general reinforcement learning algorithm that masters chess, shogi, and Go through self-play*. Science, 362(6419), 1140–1144. <https://doi.org/10.1126/science.aar6404>  
<sub>مقال محكّم · المحور 2 · تُحقِّق منه في 2026-09-27</sub>
- **Turing, A. M.** (1950). *Computing Machinery and Intelligence*. Mind, 59(236), 433–460. <https://doi.org/10.1093/mind/LIX.236.433>  
<sub>مقال محكّم · المحاور 1، 2 · تُحقِّق منه في 2026-09-26</sub>

## التعلّم الآلي — Machine Learning (8)

- **Breiman, L.** (2001). *Random Forests*. Machine Learning, 45, 5–32. <https://doi.org/10.1023/A:1010933404324>  
<sub>مقال محكّم · المحور 4 · تُحقِّق منه في 2026-09-28</sub>
- **Cortes, C., & Vapnik, V.** (1995). *Support-vector networks*. Machine Learning, 20, 273–297. <https://doi.org/10.1007/BF00994018>  
<sub>مقال محكّم · المحور 2 · تُحقِّق منه في 2026-09-28</sub>
- **Friedman, J. H.** (2001). *Greedy function approximation: A gradient boosting machine*. The Annals of Statistics, 29(5), 1189–1232. <https://doi.org/10.1214/aos/1013203451>  
<sub>مقال محكّم · المحور 4 · تُحقِّق منه في 2026-09-28</sub>
- **Google** (2026). *Machine Learning Crash Course*. Google for Developers. <https://developers.google.com/machine-learning/crash-course>  
<sub>مقرر · المحور 4 · تُحقِّق منه في 2026-09-28</sub>
- **James, G., Witten, D., Hastie, T., Tibshirani, R., & Taylor, J.** (2023). *An Introduction to Statistical Learning (with Applications in Python)*. Springer. <https://www.statlearning.com/>  
<sub>كتاب · المحاور 4، 5، 6 · تُحقِّق منه في 2026-09-28</sub>
- **Jordan, M. I., & Mitchell, T. M.** (2015). *Machine learning: Trends, perspectives, and prospects*. Science, 349(6245), 255–260. <https://doi.org/10.1126/science.aaa8415>  
<sub>مقال محكّم · المحاور 1، 2 · تُحقِّق منه في 2026-09-26</sub>
- **Mitchell, T. M.** (1997). *Machine Learning*. McGraw-Hill. <http://www.cs.cmu.edu/~tom/mlbook.html>  
<sub>كتاب · المحور 4 · تُحقِّق منه في 2026-09-28</sub>
- **scikit-learn developers** (2026). *Metrics and scoring: quantifying the quality of predictions*. scikit-learn documentation. <https://scikit-learn.org/stable/modules/model_evaluation.html>  
<sub>توثيق رسمي · المحاور 4، 6، 8، 9 · تُحقِّق منه في 2026-09-28</sub>

## التعلّم العميق — Deep Learning (20)

- **Agostinelli, A., Denk, T. I., Borsos, Z., Engel, J., Verzetti, M., Caillon, A., et al.** (2023). *MusicLM: Generating Music From Text*. arXiv:2301.11325. <https://arxiv.org/abs/2301.11325>  
<sub>مسودة بحثية · المحور 9 · تُحقِّق منه في 2026-09-28</sub>
- **Dhariwal, P., & Nichol, A.** (2021). *Diffusion Models Beat GANs on Image Synthesis*. arXiv:2105.05233. <https://arxiv.org/abs/2105.05233>  
<sub>مسودة بحثية · المحور 9 · تُحقِّق منه في 2026-09-28</sub>
- **Esteva, A., Kuprel, B., Novoa, R. A., et al.** (2017). *Dermatologist-level classification of skin cancer with deep neural networks*. Nature, 542, 115–118. <https://doi.org/10.1038/nature21056>  
<sub>مقال محكّم · المحاور 1، 4 · تُحقِّق منه في 2026-09-26</sub>
- **Goodfellow, I., Bengio, Y., & Courville, A.** (2016). *Deep Learning*. MIT Press. <https://www.deeplearningbook.org/>  
<sub>كتاب · المحاور 4، 7 · تُحقِّق منه في 2026-09-28</sub>
- **Goodfellow, I., Pouget-Abadie, J., Mirza, M., Xu, B., Warde-Farley, D., Ozair, S., Courville, A., & Bengio, Y.** (2014). *Generative Adversarial Networks*. arXiv:1406.2661. <https://arxiv.org/abs/1406.2661>  
<sub>مسودة بحثية · المحور 9 · تُحقِّق منه في 2026-09-28</sub>
- **Ho, J., Jain, A., & Abbeel, P.** (2020). *Denoising Diffusion Probabilistic Models*. arXiv:2006.11239. <https://arxiv.org/abs/2006.11239>  
<sub>مسودة بحثية · المحور 9 · تُحقِّق منه في 2026-09-28</sub>
- **Hornik, K., Stinchcombe, M., & White, H.** (1989). *Multilayer feedforward networks are universal approximators*. Neural Networks, 2(5), 359–366. <https://doi.org/10.1016/0893-6080(89)90020-8>  
<sub>مقال محكّم · المحور 4 · تُحقِّق منه في 2026-09-28</sub>
- **Kingma, D. P., & Ba, J.** (2014). *Adam: A Method for Stochastic Optimization*. arXiv:1412.6980 (ICLR 2015). <https://arxiv.org/abs/1412.6980>  
<sub>مسودة بحثية · المحور 4 · تُحقِّق منه في 2026-09-28</sub>
- **Krizhevsky, A., Sutskever, I., & Hinton, G. E.** (2012). *ImageNet classification with deep convolutional neural networks (AlexNet)*. NeurIPS 2012; reprinted in Communications of the ACM, 60(6), 2017. <https://doi.org/10.1145/3065386>  
<sub>مقال محكّم · المحور 2 · تُحقِّق منه في 2026-09-27</sub>
- **LeCun, Y., Bengio, Y., & Hinton, G.** (2015). *Deep learning*. Nature, 521, 436–444. <https://doi.org/10.1038/nature14539>  
<sub>مقال محكّم · المحور 4 · تُحقِّق منه في 2026-09-28</sub>
- **LeCun, Y., Bottou, L., Bengio, Y., & Haffner, P.** (1998). *Gradient-based learning applied to document recognition*. Proceedings of the IEEE, 86(11), 2278–2324. <https://doi.org/10.1109/5.726791>  
<sub>مقال محكّم · المحور 2 · تُحقِّق منه في 2026-09-27</sub>
- **Merchant, A., Batzner, S., Schoenholz, S. S., et al.** (2023). *Scaling deep learning for materials discovery*. Nature, 624, 80–85. <https://doi.org/10.1038/s41586-023-06735-9>  
<sub>مقال محكّم · المحور 1 · تُحقِّق منه في 2026-09-26</sub>
- **Radford, A., Kim, J. W., Hallacy, C., Ramesh, A., Goh, G., Agarwal, S., Sastry, G., Askell, A., Mishkin, P., Clark, J., Krueger, G., & Sutskever, I.** (2021). *Learning Transferable Visual Models From Natural Language Supervision*. arXiv:2103.00020. <https://arxiv.org/abs/2103.00020>  
<sub>مسودة بحثية · المحور 9 · تُحقِّق منه في 2026-09-28</sub>
- **Radford, A., Kim, J. W., Xu, T., Brockman, G., McLeavey, C., & Sutskever, I.** (2022). *Robust Speech Recognition via Large-Scale Weak Supervision*. arXiv:2212.04356. <https://arxiv.org/abs/2212.04356>  
<sub>مسودة بحثية · المحور 9 · تُحقِّق منه في 2026-09-28</sub>
- **Ramesh, A., Dhariwal, P., Nichol, A., Chu, C., & Chen, M.** (2022). *Hierarchical Text-Conditional Image Generation with CLIP Latents*. arXiv:2204.06125. <https://arxiv.org/abs/2204.06125>  
<sub>مسودة بحثية · المحور 9 · تُحقِّق منه في 2026-09-28</sub>
- **Rombach, R., Blattmann, A., Lorenz, D., Esser, P., & Ommer, B.** (2022). *High-Resolution Image Synthesis with Latent Diffusion Models*. arXiv:2112.10752. <https://arxiv.org/abs/2112.10752>  
<sub>مسودة بحثية · المحور 9 · تُحقِّق منه في 2026-09-28</sub>
- **Saharia, C., Chan, W., Saxena, S., Li, L., Whang, J., Denton, E., et al.** (2022). *Photorealistic Text-to-Image Diffusion Models with Deep Language Understanding*. arXiv:2205.11487. <https://arxiv.org/abs/2205.11487>  
<sub>مسودة بحثية · المحور 9 · تُحقِّق منه في 2026-09-28</sub>
- **Singer, U., Polyak, A., Hayes, T., Yin, X., An, J., Zhang, S., et al.** (2022). *Make-A-Video: Text-to-Video Generation without Text-Video Data*. arXiv:2209.14792. <https://arxiv.org/abs/2209.14792>  
<sub>مسودة بحثية · المحور 9 · تُحقِّق منه في 2026-09-28</sub>
- **Zhang, C., Bengio, S., Hardt, M., Recht, B., & Vinyals, O.** (2016). *Understanding deep learning requires rethinking generalization*. arXiv:1611.03530 (ICLR 2017). <https://arxiv.org/abs/1611.03530>  
<sub>مسودة بحثية · المحور 4 · تُحقِّق منه في 2026-09-28</sub>
- **van den Oord, A., Dieleman, S., Zen, H., Simonyan, K., Vinyals, O., Graves, A., et al.** (2016). *WaveNet: A Generative Model for Raw Audio*. arXiv:1609.03499. <https://arxiv.org/abs/1609.03499>  
<sub>مسودة بحثية · المحور 9 · تُحقِّق منه في 2026-09-28</sub>

## النماذج اللغوية الكبيرة — LLMs (16)

- **Bommasani, R., Hudson, D. A., Adeli, E., et al.** (2021). *On the Opportunities and Risks of Foundation Models*. arXiv:2108.07258 (Stanford CRFM). <https://arxiv.org/abs/2108.07258>  
<sub>مسودة بحثية · المحاور 1، 2، 4، 7 · تُحقِّق منه في 2026-09-26</sub>
- **Devlin, J., Chang, M.-W., Lee, K., & Toutanova, K.** (2018). *BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding*. arXiv:1810.04805 (NAACL 2019). <https://arxiv.org/abs/1810.04805>  
<sub>مسودة بحثية · المحور 7 · تُحقِّق منه في 2026-09-28</sub>
- **Hoffmann, J., Borgeaud, S., Mensch, A., et al.** (2022). *Training Compute-Optimal Large Language Models*. arXiv:2203.15556 (NeurIPS 2022). <https://arxiv.org/abs/2203.15556>  
<sub>مسودة بحثية · المحور 1 · تُحقِّق منه في 2026-09-26</sub>
- **Huang, L., Yu, W., Ma, W., et al.** (2023). *A Survey on Hallucination in Large Language Models: Principles, Taxonomy, Challenges, and Open Questions*. arXiv:2311.05232. <https://arxiv.org/abs/2311.05232>  
<sub>مسودة بحثية · المحاور 7، 8 · تُحقِّق منه في 2026-09-28</sub>
- **Ji, Z., Lee, N., Frieske, R., et al.** (2023). *Survey of Hallucination in Natural Language Generation*. ACM Computing Surveys, 55(12), 1–38. <https://doi.org/10.1145/3571730>  
<sub>مقال محكّم · المحور 7 · تُحقِّق منه في 2026-09-28</sub>
- **Kaplan, J., McCandlish, S., Henighan, T., et al.** (2020). *Scaling Laws for Neural Language Models*. arXiv:2001.08361. <https://arxiv.org/abs/2001.08361>  
<sub>مسودة بحثية · المحور 1 · تُحقِّق منه في 2026-09-26</sub>
- **Lewis, P., Perez, E., Piktus, A., et al.** (2020). *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*. arXiv:2005.11401 (NeurIPS 2020). <https://arxiv.org/abs/2005.11401>  
<sub>مسودة بحثية · المحاور 6، 7، 8 · تُحقِّق منه في 2026-09-28</sub>
- **Lewis, P., Perez, E., Piktus, A., et al.** (2020). *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*. arXiv:2005.11401 (NeurIPS 2020). <https://arxiv.org/abs/2005.11401>  
<sub>مسودة بحثية · المحور 7 · تُحقِّق منه في 2026-09-28</sub>
- **Ouyang, L., Wu, J., Jiang, X., et al.** (2022). *Training language models to follow instructions with human feedback*. arXiv:2203.02155 (NeurIPS 2022). <https://arxiv.org/abs/2203.02155>  
<sub>مسودة بحثية · المحور 4 · تُحقِّق منه في 2026-09-28</sub>
- **Ouyang, L., Wu, J., Jiang, X., et al.** (2022). *Training language models to follow instructions with human feedback*. arXiv:2203.02155 (NeurIPS 2022). <https://arxiv.org/abs/2203.02155>  
<sub>مسودة بحثية · المحور 7 · تُحقِّق منه في 2026-09-28</sub>
- **Rawte, V., Sheth, A., & Das, A.** (2023). *A Survey of Hallucination in Large Foundation Models*. arXiv:2309.05922. <https://arxiv.org/abs/2309.05922>  
<sub>مسودة بحثية · المحور 8 · تُحقِّق منه في 2026-09-28</sub>
- **Schaeffer, R., Miranda, B., & Koyejo, S.** (2023). *Are Emergent Abilities of Large Language Models a Mirage?*. arXiv:2304.15004 (NeurIPS 2023). <https://arxiv.org/abs/2304.15004>  
<sub>مسودة بحثية · المحاور 1، 2، 3 · تُحقِّق منه في 2026-09-26</sub>
- **Sennrich, R., Haddow, B., & Birch, A.** (2015). *Neural Machine Translation of Rare Words with Subword Units*. arXiv:1508.07909 (ACL 2016). <https://arxiv.org/abs/1508.07909>  
<sub>مسودة بحثية · المحور 7 · تُحقِّق منه في 2026-09-28</sub>
- **Vaswani, A., Shazeer, N., Parmar, N., et al.** (2017). *Attention Is All You Need*. arXiv:1706.03762 (NeurIPS 2017). <https://arxiv.org/abs/1706.03762>  
<sub>مسودة بحثية · المحاور 2، 7 · تُحقِّق منه في 2026-09-27</sub>
- **Vaswani, A., Shazeer, N., Parmar, N., et al.** (2017). *Attention Is All You Need*. arXiv:1706.03762 (NeurIPS 2017). <https://arxiv.org/abs/1706.03762>  
<sub>مسودة بحثية · المحاور 7، 9 · تُحقِّق منه في 2026-09-28</sub>
- **Yao, S., Zhao, J., Yu, D., et al.** (2022). *ReAct: Synergizing Reasoning and Acting in Language Models*. arXiv:2210.03629 (ICLR 2023). <https://arxiv.org/abs/2210.03629>  
<sub>مسودة بحثية · المحاور 6، 7 · تُحقِّق منه في 2026-09-28</sub>

## هندسة الأوامر — Prompt Engineering (7)

- **Brown, T. B., Mann, B., Ryder, N., et al.** (2020). *Language Models are Few-Shot Learners*. arXiv:2005.14165 (NeurIPS 2020). <https://arxiv.org/abs/2005.14165>  
<sub>مسودة بحثية · المحور 5 · تُحقِّق منه في 2026-09-28</sub>
- **DAIR.AI** (2026). *Prompt Engineering Guide*. promptingguide.ai. <https://www.promptingguide.ai/>  
<sub>صفحة ويب · المحور 5 · تُحقِّق منه في 2026-09-28</sub>
- **Schulhoff, S., Ilie, M., Balepur, N., et al.** (2024). *The Prompt Report: A Systematic Survey of Prompt Engineering Techniques*. arXiv:2406.06608. <https://arxiv.org/abs/2406.06608>  
<sub>مسودة بحثية · المحاور 5، 6، 8 · تُحقِّق منه في 2026-09-28</sub>
- **Wang, X., Wei, J., Schuurmans, D., et al.** (2022). *Self-Consistency Improves Chain of Thought Reasoning in Language Models*. arXiv:2203.11171 (ICLR 2023). <https://arxiv.org/abs/2203.11171>  
<sub>مسودة بحثية · المحور 6 · تُحقِّق منه في 2026-09-28</sub>
- **Wei, J., Wang, X., Schuurmans, D., et al.** (2022). *Chain-of-Thought Prompting Elicits Reasoning in Large Language Models*. arXiv:2201.11903 (NeurIPS 2022). <https://arxiv.org/abs/2201.11903>  
<sub>مسودة بحثية · المحور 6 · تُحقِّق منه في 2026-09-28</sub>
- **White, J., Fu, Q., Hays, S., et al.** (2023). *A Prompt Pattern Catalog to Enhance Prompt Engineering with ChatGPT*. arXiv:2302.11382. <https://arxiv.org/abs/2302.11382>  
<sub>مسودة بحثية · المحور 5 · تُحقِّق منه في 2026-09-28</sub>
- **Zhou, Y., Muresanu, A. I., Han, Z., et al.** (2022). *Large Language Models Are Human-Level Prompt Engineers*. arXiv:2211.01910 (ICLR 2023). <https://arxiv.org/abs/2211.01910>  
<sub>مسودة بحثية · المحور 5 · تُحقِّق منه في 2026-09-28</sub>

## الاقتصاد والذكاء الاصطناعي — Economics + AI (25)

- **Acemoglu, D.** (2024). *The simple macroeconomics of AI*. Economic Policy, 40(121), 13–58. <https://doi.org/10.1093/epolic/eiae042>  
<sub>مقال محكّم · المحور 10 · تُحقِّق منه في 2026-09-28</sub>
- **Acemoglu, D., & Restrepo, P.** (2019). *Automation and New Tasks: How Technology Displaces and Reinstates Labor*. Journal of Economic Perspectives, 33(2), 3–30. <https://doi.org/10.1257/jep.33.2.3>  
<sub>مقال محكّم · المحور 10 · تُحقِّق منه في 2026-09-28</sub>
- **Athey, S., & Imbens, G. W.** (2019). *Machine Learning Methods That Economists Should Know About*. Annual Review of Economics, 11, 685–725. <https://doi.org/10.1146/annurev-economics-080217-053433>  
<sub>مقال محكّم · المحور 10 · تُحقِّق منه في 2026-09-28</sub>
- **Autor, D. H.** (2015). *Why Are There Still So Many Jobs? The History and Future of Workplace Automation*. Journal of Economic Perspectives, 29(3), 3–30. <https://doi.org/10.1257/jep.29.3.3>  
<sub>مقال محكّم · المحور 10 · تُحقِّق منه في 2026-09-28</sub>
- **Baker, S. R., Bloom, N., & Davis, S. J.** (2016). *Measuring Economic Policy Uncertainty*. The Quarterly Journal of Economics, 131(4), 1593–1636. <https://doi.org/10.1093/qje/qjw024>  
<sub>مقال محكّم · المحور 10 · تُحقِّق منه في 2026-09-28</sub>
- **Belloni, A., Chernozhukov, V., & Hansen, C.** (2014). *High-Dimensional Methods and Inference on Structural and Treatment Effects*. Journal of Economic Perspectives, 28(2), 29–50. <https://doi.org/10.1257/jep.28.2.29>  
<sub>مقال محكّم · المحور 10 · تُحقِّق منه في 2026-09-28</sub>
- **Brynjolfsson, E.** (2022). *The Turing Trap: The Promise & Peril of Human-Like Artificial Intelligence*. Daedalus, 151(2), 272–287. <https://doi.org/10.1162/daed_a_01915>  
<sub>مقال محكّم · المحور 1 · تُحقِّق منه في 2026-09-26</sub>
- **Brynjolfsson, E., Li, D., & Raymond, L.** (2025). *Generative AI at Work*. The Quarterly Journal of Economics, 140(2). <https://doi.org/10.1093/qje/qjae044>  
<sub>مقال محكّم · المحور 1 · تُحقِّق منه في 2026-09-26</sub>
- **Brynjolfsson, E., Li, D., & Raymond, L.** (2025). *Generative AI at Work*. The Quarterly Journal of Economics, 140(2), 889–942. <https://doi.org/10.1093/qje/qjae044>  
<sub>مقال محكّم · المحور 10 · تُحقِّق منه في 2026-09-28</sub>
- **Brynjolfsson, E., Rock, D., & Syverson, C.** (2021). *The Productivity J-Curve: How Intangibles Complement General Purpose Technologies*. American Economic Journal: Macroeconomics, 13(1), 333–372. <https://doi.org/10.1257/mac.20180386>  
<sub>مقال محكّم · المحور 10 · تُحقِّق منه في 2026-09-28</sub>
- **Chernozhukov, V., Chetverikov, D., Demirer, M., Duflo, E., Hansen, C., Newey, W., & Robins, J.** (2018). *Double/debiased machine learning for treatment and structural parameters*. The Econometrics Journal, 21(1), C1–C68. <https://doi.org/10.1111/ectj.12097>  
<sub>مقال محكّم · المحور 10 · تُحقِّق منه في 2026-09-28</sub>
- **Einav, L., & Levin, J.** (2014). *Economics in the age of big data*. Science, 346(6210). <https://doi.org/10.1126/science.1243089>  
<sub>مقال محكّم · المحور 10 · تُحقِّق منه في 2026-09-28</sub>
- **Gentzkow, M., Kelly, B., & Taddy, M.** (2019). *Text as Data*. Journal of Economic Literature, 57(3), 535–574. <https://doi.org/10.1257/jel.20181020>  
<sub>مقال محكّم · المحور 10 · تُحقِّق منه في 2026-09-28</sub>
- **Giannone, D., Reichlin, L., & Small, D.** (2008). *Nowcasting: The real-time informational content of macroeconomic data*. Journal of Monetary Economics, 55(4), 665–676. <https://doi.org/10.1016/j.jmoneco.2008.05.010>  
<sub>مقال محكّم · المحور 10 · تُحقِّق منه في 2026-09-28</sub>
- **Gmyrek, P., Berg, J., & Bescond, D.** (2023). *Generative AI and Jobs: A global analysis of potential effects on job quantity and quality*. ILO Working Paper 96, International Labour Organization. <https://doi.org/10.54394/FHEM8239>  
<sub>تقرير · المحور 10 · تُحقِّق منه في 2026-09-28</sub>
- **Kapoor, S., & Narayanan, A.** (2023). *Leakage and the reproducibility crisis in machine-learning-based science*. Patterns, 4(9), 100804. <https://doi.org/10.1016/j.patter.2023.100804>  
<sub>مقال محكّم · المحور 10 · تُحقِّق منه في 2026-09-28</sub>
- **Kleinberg, J., Ludwig, J., Mullainathan, S., & Obermeyer, Z.** (2015). *Prediction Policy Problems*. American Economic Review, 105(5), 491–495. <https://doi.org/10.1257/aer.p20151023>  
<sub>مقال محكّم · المحور 10 · تُحقِّق منه في 2026-09-28</sub>
- **Korinek, A.** (2023). *Generative AI for Economic Research: Use Cases and Implications for Economists*. Journal of Economic Literature, 61(4), 1281–1317. <https://doi.org/10.1257/jel.20231736>  
<sub>مقال محكّم · المحور 10 · تُحقِّق منه في 2026-09-28</sub>
- **Loughran, T., & McDonald, B.** (2011). *When Is a Liability Not a Liability? Textual Analysis, Dictionaries, and 10-Ks*. The Journal of Finance, 66(1), 35–65. <https://doi.org/10.1111/j.1540-6261.2010.01625.x>  
<sub>مقال محكّم · المحور 10 · تُحقِّق منه في 2026-09-28</sub>
- **Mokyr, J., Vickers, C., & Ziebarth, N. L.** (2015). *The History of Technological Anxiety and the Future of Economic Growth: Is This Time Different?*. Journal of Economic Perspectives, 29(3), 31–50. <https://doi.org/10.1257/jep.29.3.31>  
<sub>مقال محكّم · المحور 10 · تُحقِّق منه في 2026-09-28</sub>
- **Mullainathan, S., & Spiess, J.** (2017). *Machine Learning: An Applied Econometric Approach*. Journal of Economic Perspectives, 31(2), 87–106. <https://doi.org/10.1257/jep.31.2.87>  
<sub>مقال محكّم · المحاور 10، 13 · تُحقِّق منه في 2026-09-28</sub>
- **Noy, S., & Zhang, W.** (2023). *Experimental evidence on the productivity effects of generative artificial intelligence*. Science, 381(6654), 187–192. <https://doi.org/10.1126/science.adh2586>  
<sub>مقال محكّم · المحور 1 · تُحقِّق منه في 2026-09-26</sub>
- **Noy, S., & Zhang, W.** (2023). *Experimental evidence on the productivity effects of generative artificial intelligence*. Science, 381(6654), 187–192. <https://doi.org/10.1126/science.adh2586>  
<sub>مقال محكّم · المحور 8 · تُحقِّق منه في 2026-09-28</sub>
- **Varian, H. R.** (2014). *Big Data: New Tricks for Econometrics*. Journal of Economic Perspectives, 28(2), 3–28. <https://doi.org/10.1257/jep.28.2.3>  
<sub>مقال محكّم · المحور 10 · تُحقِّق منه في 2026-09-28</sub>
- **Wager, S., & Athey, S.** (2018). *Estimation and Inference of Heterogeneous Treatment Effects using Random Forests*. Journal of the American Statistical Association, 113(523), 1228–1242. <https://doi.org/10.1080/01621459.2017.1319839>  
<sub>مقال محكّم · المحور 10 · تُحقِّق منه في 2026-09-28</sub>

## أخلاقيات الذكاء الاصطناعي — AI Ethics (31)

- **Angwin, J., Larson, J., Mattu, S., & Kirchner, L.** (2016). *Machine Bias*. ProPublica. <https://www.propublica.org/article/machine-bias-risk-assessments-in-criminal-sentencing>  
<sub>صفحة ويب · المحور 11 · تُحقِّق منه في 2026-09-28</sub>
- **Barocas, S., Hardt, M., & Narayanan, A.** (2023). *Fairness and Machine Learning: Limitations and Opportunities*. MIT Press. <https://fairmlbook.org/>  
<sub>كتاب · المحاور 11، 13 · تُحقِّق منه في 2026-09-28</sub>
- **Bender, E. M., Gebru, T., McMillan-Major, A., & Shmitchell, S.** (2021). *On the Dangers of Stochastic Parrots: Can Language Models Be Too Big?*. Proceedings of the 2021 ACM Conference on Fairness, Accountability, and Transparency (FAccT). <https://doi.org/10.1145/3442188.3445922>  
<sub>مقال محكّم · المحاور 1، 5، 7، 8، 9 · تُحقِّق منه في 2026-09-26</sub>
- **Bianchi, F., Kalluri, P., Durmus, E., Ladhak, F., Cheng, M., Nozza, D., Hashimoto, T., Jurafsky, D., Zou, J., & Caliskan, A.** (2023). *Easily Accessible Text-to-Image Generation Amplifies Demographic Stereotypes at Large Scale*. arXiv:2211.03759. <https://arxiv.org/abs/2211.03759>  
<sub>مسودة بحثية · المحور 9 · تُحقِّق منه في 2026-09-28</sub>
- **Buolamwini, J., & Gebru, T.** (2018). *Gender Shades: Intersectional Accuracy Disparities in Commercial Gender Classification*. Proceedings of Machine Learning Research, 81, 77–91. <https://proceedings.mlr.press/v81/buolamwini18a.html>  
<sub>مقال محكّم · المحور 11 · تُحقِّق منه في 2026-09-28</sub>
- **Caliskan, A., Bryson, J. J., & Narayanan, A.** (2017). *Semantics derived automatically from language corpora contain human-like biases*. Science, 356(6334), 183–186. <https://doi.org/10.1126/science.aal4230>  
<sub>مقال محكّم · المحور 11 · تُحقِّق منه في 2026-09-28</sub>
- **Chan, M. S., Jones, C. R., Hall Jamieson, K., & Albarracín, D.** (2017). *Debunking: A Meta-Analysis of the Psychological Efficacy of Messages Countering Misinformation*. Psychological Science, 28(11), 1531–1546. <https://doi.org/10.1177/0956797617714579>  
<sub>مقال محكّم · المحور 9 · تُحقِّق منه في 2026-09-28</sub>
- **Chouldechova, A.** (2017). *Fair Prediction with Disparate Impact: A Study of Bias in Recidivism Prediction Instruments*. Big Data, 5(2), 153–163. <https://doi.org/10.1089/big.2016.0047>  
<sub>مقال محكّم · المحور 11 · تُحقِّق منه في 2026-09-28</sub>
- **Coalition for Content Provenance and Authenticity (C2PA)** (2026). *C2PA Technical Specification*. C2PA. <https://c2pa.org/specifications/specifications/2.1/index.html>  
<sub>معيار أو موقف رسمي · المحور 9 · تُحقِّق منه في 2026-09-28</sub>
- **Committee on Publication Ethics (COPE)** (2023). *Authorship and AI tools (COPE position statement)*. COPE Council. <https://doi.org/10.24318/cCVRZBms>  
<sub>معيار أو موقف رسمي · المحاور 8، 9 · تُحقِّق منه في 2026-09-28</sub>  
<sub>⚠︎ الموقع يرفض الطلبات الآلية؛ تُحقِّق منه عبر معرّف DOI.</sub>
- **Content Authenticity Initiative / C2PA** (2026). *Content Credentials*. contentcredentials.org. <https://contentcredentials.org/>  
<sub>توثيق رسمي · المحور 9 · تُحقِّق منه في 2026-09-28</sub>
- **Corbett-Davies, S., & Goel, S.** (2018). *The Measure and Mismeasure of Fairness: A Critical Review of Fair Machine Learning*. arXiv:1808.00023. <https://arxiv.org/abs/1808.00023>  
<sub>مسودة بحثية · المحور 11 · تُحقِّق منه في 2026-09-28</sub>
- **Dwork, C., Hardt, M., Pitassi, T., Reingold, O., & Zemel, R.** (2012). *Fairness through awareness*. Proceedings of the 3rd Innovations in Theoretical Computer Science Conference (ITCS), 214–226. <https://doi.org/10.1145/2090236.2090255>  
<sub>مقال محكّم · المحور 11 · تُحقِّق منه في 2026-09-28</sub>
- **Equal Employment Opportunity Commission et al. (United States)** (1978). *Uniform Guidelines on Employee Selection Procedures, 29 CFR Part 1607 (§ 1607.4(D), the four-fifths rule)*. Code of Federal Regulations, Title 29. <https://www.law.cornell.edu/cfr/text/29/1607.4>  
<sub>نص قانوني · المحور 11 · تُحقِّق منه في 2026-09-29</sub>
- **European Union** (2024). *Regulation (EU) 2024/1689 (Artificial Intelligence Act) — Article 50, transparency obligations*. Official Journal of the European Union. <https://eur-lex.europa.eu/eli/reg/2024/1689/oj>  
<sub>معيار أو موقف رسمي · المحور 9 · تُحقِّق منه في 2026-09-28</sub>
- **Gebru, T., Morgenstern, J., Vecchione, B., Vaughan, J. W., Wallach, H., Daumé III, H., & Crawford, K.** (2021). *Datasheets for datasets*. Communications of the ACM, 64(12), 86–92. <https://doi.org/10.1145/3458723>  
<sub>مقال محكّم · المحاور 11، 12 · تُحقِّق منه في 2026-09-28</sub>
- **Google DeepMind** (2026). *SynthID: watermarking and identifying AI-generated content*. Google DeepMind. <https://deepmind.google/technologies/synthid/>  
<sub>توثيق رسمي · المحور 9 · تُحقِّق منه في 2026-09-28</sub>
- **Hardt, M., Price, E., & Srebro, N.** (2016). *Equality of Opportunity in Supervised Learning*. arXiv:1610.02413. <https://arxiv.org/abs/1610.02413>  
<sub>مسودة بحثية · المحور 11 · تُحقِّق منه في 2026-09-28</sub>
- **International Committee of Medical Journal Editors (ICMJE)** (2026). *Recommendations for the Conduct, Reporting, Editing, and Publication of Scholarly Work in Medical Journals*. ICMJE. <https://www.icmje.org/recommendations/>  
<sub>معيار أو موقف رسمي · المحور 8 · تُحقِّق منه في 2026-09-28</sub>
- **Kleinberg, J., Mullainathan, S., & Raghavan, M.** (2016). *Inherent Trade-Offs in the Fair Determination of Risk Scores*. arXiv:1609.05807. <https://arxiv.org/abs/1609.05807>  
<sub>مسودة بحثية · المحور 11 · تُحقِّق منه في 2026-09-28</sub>
- **Luccioni, A. S., Akiki, C., Mitchell, M., & Jernite, Y.** (2023). *Stable Bias: Analyzing Societal Representations in Diffusion Models*. arXiv:2303.11408. <https://arxiv.org/abs/2303.11408>  
<sub>مسودة بحثية · المحور 9 · تُحقِّق منه في 2026-09-28</sub>
- **Lundberg, S. M., & Lee, S.-I.** (2017). *A Unified Approach to Interpreting Model Predictions*. arXiv:1705.07874. <https://arxiv.org/abs/1705.07874>  
<sub>مسودة بحثية · المحور 11 · تُحقِّق منه في 2026-09-28</sub>
- **Mehrabi, N., Morstatter, F., Saxena, N., Lerman, K., & Galstyan, A.** (2021). *A Survey on Bias and Fairness in Machine Learning*. ACM Computing Surveys, 54(6), 1–35. <https://doi.org/10.1145/3457607>  
<sub>مقال محكّم · المحور 11 · تُحقِّق منه في 2026-09-28</sub>
- **Mitchell, M., Wu, S., Zaldivar, A., Barnes, P., Vasserman, L., Hutchinson, B., Spitzer, E., Raji, I. D., & Gebru, T.** (2019). *Model Cards for Model Reporting*. Proceedings of the Conference on Fairness, Accountability, and Transparency (FAccT), 220–229. <https://doi.org/10.1145/3287560.3287596>  
<sub>مقال محكّم · المحاور 11، 13 · تُحقِّق منه في 2026-09-28</sub>
- **Mitchell, S., Potash, E., Barocas, S., D'Amour, A., & Lum, K.** (2021). *Algorithmic Fairness: Choices, Assumptions, and Definitions*. Annual Review of Statistics and Its Application, 8(1), 141–163. <https://doi.org/10.1146/annurev-statistics-042720-125902>  
<sub>مقال محكّم · المحور 11 · تُحقِّق منه في 2026-09-28</sub>
- **Obermeyer, Z., Powers, B., Vogeli, C., & Mullainathan, S.** (2019). *Dissecting racial bias in an algorithm used to manage the health of populations*. Science, 366(6464), 447–453. <https://doi.org/10.1126/science.aax2342>  
<sub>مقال محكّم · المحاور 1، 4، 11 · تُحقِّق منه في 2026-09-26</sub>
- **Raji, I. D., & Buolamwini, J.** (2019). *Actionable Auditing: Investigating the Impact of Publicly Naming Biased Performance Results of Commercial AI Products*. Proceedings of the 2019 AAAI/ACM Conference on AI, Ethics, and Society, 429–435. <https://doi.org/10.1145/3306618.3314244>  
<sub>مقال محكّم · المحور 11 · تُحقِّق منه في 2026-09-28</sub>
- **Ribeiro, M. T., Singh, S., & Guestrin, C.** (2016). *"Why Should I Trust You?": Explaining the Predictions of Any Classifier*. Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining, 1135–1144. <https://doi.org/10.1145/2939672.2939778>  
<sub>مقال محكّم · المحور 11 · تُحقِّق منه في 2026-09-28</sub>
- **Rudin, C.** (2019). *Stop explaining black box machine learning models for high stakes decisions and use interpretable models instead*. Nature Machine Intelligence, 1(5), 206–215. <https://doi.org/10.1038/s42256-019-0048-x>  
<sub>مقال محكّم · المحور 11 · تُحقِّق منه في 2026-09-28</sub>
- **Selbst, A. D., Boyd, D., Friedler, S. A., Venkatasubramanian, S., & Vertesi, J.** (2019). *Fairness and Abstraction in Sociotechnical Systems*. Proceedings of the Conference on Fairness, Accountability, and Transparency (FAccT), 59–68. <https://doi.org/10.1145/3287560.3287598>  
<sub>مقال محكّم · المحاور 11، 13 · تُحقِّق منه في 2026-09-28</sub>
- **Springer Nature** (2026). *Artificial Intelligence (AI) — editorial policies*. Nature Portfolio. <https://www.nature.com/nature-portfolio/editorial-policies/ai>  
<sub>توثيق رسمي · المحور 8 · تُحقِّق منه في 2026-09-28</sub>

## الخصوصية — Privacy (11)

- **Carlini, N., Ippolito, D., Jagielski, M., Lee, K., Tramèr, F., & Zhang, C.** (2022). *Quantifying Memorization Across Neural Language Models*. arXiv:2202.07646. <https://arxiv.org/abs/2202.07646>  
<sub>مسودة بحثية · المحور 12 · تُحقِّق منه في 2026-09-29</sub>
- **Carlini, N., Tramèr, F., Wallace, E., Jagielski, M., Herbert-Voss, A., Lee, K., Roberts, A., Brown, T., Song, D., Erlingsson, Ú., Oprea, A., & Raffel, C.** (2020). *Extracting Training Data from Large Language Models*. arXiv:2012.07805. <https://arxiv.org/abs/2012.07805>  
<sub>مسودة بحثية · المحور 12 · تُحقِّق منه في 2026-09-29</sub>
- **Dwork, C., & Roth, A.** (2014). *The Algorithmic Foundations of Differential Privacy*. Foundations and Trends in Theoretical Computer Science, 9(3–4), 211–487. <https://doi.org/10.1561/0400000042>  
<sub>مقال محكّم · المحور 12 · تُحقِّق منه في 2026-09-29</sub>
- **Dwork, C., McSherry, F., Nissim, K., & Smith, A.** (2006). *Calibrating Noise to Sensitivity in Private Data Analysis*. Theory of Cryptography (TCC), Lecture Notes in Computer Science, 265–284. <https://doi.org/10.1007/11681878_14>  
<sub>مقال محكّم · المحور 12 · تُحقِّق منه في 2026-09-29</sub>
- **European Parliament & Council of the European Union** (2016). *Regulation (EU) 2016/679 — General Data Protection Regulation (GDPR)*. Official Journal of the European Union. <https://eur-lex.europa.eu/eli/reg/2016/679/oj>  
<sub>نص قانوني · المحور 12 · تُحقِّق منه في 2026-09-29</sub>
- **Narayanan, A., & Shmatikov, V.** (2008). *Robust De-anonymization of Large Sparse Datasets*. 2008 IEEE Symposium on Security and Privacy, 111–125. <https://doi.org/10.1109/SP.2008.33>  
<sub>مقال محكّم · المحور 12 · تُحقِّق منه في 2026-09-29</sub>
- **Nasr, M., Carlini, N., Hayase, J., Jagielski, M., Cooper, A. F., Ippolito, D., Choquette-Choo, C. A., Wallace, E., Tramèr, F., & Lee, K.** (2023). *Scalable Extraction of Training Data from (Production) Language Models*. arXiv:2311.17035. <https://arxiv.org/abs/2311.17035>  
<sub>مسودة بحثية · المحور 12 · تُحقِّق منه في 2026-09-29</sub>
- **Rocher, L., Hendrickx, J. M., & de Montjoye, Y.-A.** (2019). *Estimating the success of re-identifications in incomplete datasets using generative models*. Nature Communications, 10, 3069. <https://doi.org/10.1038/s41467-019-10933-3>  
<sub>مقال محكّم · المحاور 12، 13 · تُحقِّق منه في 2026-09-29</sub>
- **Shokri, R., Stronati, M., Song, C., & Shmatikov, V.** (2017). *Membership Inference Attacks Against Machine Learning Models*. 2017 IEEE Symposium on Security and Privacy, 3–18. <https://doi.org/10.1109/SP.2017.41>  
<sub>مقال محكّم · المحور 12 · تُحقِّق منه في 2026-09-29</sub>
- **Sweeney, L.** (2002). *k-Anonymity: A Model for Protecting Privacy*. International Journal of Uncertainty, Fuzziness and Knowledge-Based Systems, 10(5), 557–570. <https://doi.org/10.1142/S0218488502001648>  
<sub>مقال محكّم · المحور 12 · تُحقِّق منه في 2026-09-29</sub>
- **de Montjoye, Y.-A., Hidalgo, C. A., Verleysen, M., & Blondel, V. D.** (2013). *Unique in the Crowd: The privacy bounds of human mobility*. Scientific Reports, 3, 1376. <https://doi.org/10.1038/srep01376>  
<sub>مقال محكّم · المحور 12 · تُحقِّق منه في 2026-09-29</sub>

## الأمان — Security (3)

- **Greshake, K., Abdelnabi, S., Mishra, S., et al.** (2023). *Not what you've signed up for: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection*. arXiv:2302.12173 (AISec 2023). <https://arxiv.org/abs/2302.12173>  
<sub>مسودة بحثية · المحاور 6، 7، 12 · تُحقِّق منه في 2026-09-28</sub>
- **OWASP Foundation (GenAI Security Project)** (2025). *OWASP Top 10 for LLM Applications 2025*. OWASP. <https://genai.owasp.org/llm-top-10/>  
<sub>معيار أو موقف رسمي · المحاور 6، 7، 12 · تُحقِّق منه في 2026-09-28</sub>
- **Perez, F., & Ribeiro, I.** (2022). *Ignore Previous Prompt: Attack Techniques For Language Models*. arXiv:2211.09527. <https://arxiv.org/abs/2211.09527>  
<sub>مسودة بحثية · المحاور 6، 12 · تُحقِّق منه في 2026-09-28</sub>

## الحوكمة والتنظيم — AI Governance (8)

- **European Parliament & Council of the European Union** (2024). *Regulation (EU) 2024/1689 laying down harmonised rules on artificial intelligence (Artificial Intelligence Act)*. Official Journal of the European Union. <https://eur-lex.europa.eu/eli/reg/2024/1689/oj>  
<sub>نص قانوني · المحاور 1، 3، 5، 6، 11، 13 · تُحقِّق منه في 2026-09-26</sub>
- **National Institute of Standards and Technology (NIST)** (2024). *Artificial Intelligence Risk Management Framework: Generative Artificial Intelligence Profile (NIST AI 600-1)*. NIST. <https://doi.org/10.6028/NIST.AI.600-1>  
<sub>معيار أو موقف رسمي · المحاور 6، 12 · تُحقِّق منه في 2026-09-28</sub>
- **OECD** (2024). *Explanatory memorandum on the updated OECD definition of an AI system*. OECD Artificial Intelligence Papers, No. 8. <https://doi.org/10.1787/623da898-en>  
<sub>تقرير · المحاور 1، 3 · تُحقِّق منه في 2026-09-26</sub>
- **OECD** (2024). *OECD AI Principles (adopted 2019, updated 2024)*. OECD.AI Policy Observatory. <https://oecd.ai/en/ai-principles>  
<sub>معيار أو موقف رسمي · المحور 11 · تُحقِّق منه في 2026-09-26</sub>
- **SAE International** (2021). *J3016: Taxonomy and Definitions for Terms Related to Driving Automation Systems for On-Road Motor Vehicles*. SAE International. <https://www.sae.org/standards/content/j3016_202104/>  
<sub>معيار أو موقف رسمي · المحاور 3، 13 · تُحقِّق منه في 2026-09-26</sub>
- **Tabassi, E. (National Institute of Standards and Technology)** (2023). *Artificial Intelligence Risk Management Framework (AI RMF 1.0)*. NIST AI 100-1, U.S. Department of Commerce. <https://doi.org/10.6028/NIST.AI.100-1>  
<sub>معيار أو موقف رسمي · المحاور 11، 12 · تُحقِّق منه في 2026-09-28</sub>
- **U.S. Food and Drug Administration** (2025). *Artificial Intelligence-Enabled Medical Devices*. FDA. <https://www.fda.gov/medical-devices/software-medical-device-samd/artificial-intelligence-enabled-medical-devices>  
<sub>توثيق رسمي · المحور 1 · تُحقِّق منه في 2026-09-26</sub>
- **UNESCO** (2021). *Recommendation on the Ethics of Artificial Intelligence*. United Nations Educational, Scientific and Cultural Organization. <https://www.unesco.org/en/artificial-intelligence/recommendation-ethics>  
<sub>معيار أو موقف رسمي · المحاور 11، 12 · تُحقِّق منه في 2026-09-28</sub>

## الرقابة البشرية — Human Oversight (7)

- **Bainbridge, L.** (1983). *Ironies of automation*. Automatica, 19(6), 775–779. <https://doi.org/10.1016/0005-1098(83)90046-8>  
<sub>مقال محكّم · المحور 13 · تُحقِّق منه في 2026-09-29</sub>
- **Green, B., & Chen, Y.** (2019). *The Principles and Limits of Algorithm-in-the-Loop Decision Making*. Proceedings of the ACM on Human-Computer Interaction, 3(CSCW), 1–24. <https://doi.org/10.1145/3359152>  
<sub>مقال محكّم · المحور 13 · تُحقِّق منه في 2026-09-29</sub>
- **Lee, J. D., & See, K. A.** (2004). *Trust in Automation: Designing for Appropriate Reliance*. Human Factors, 46(1), 50–80. <https://doi.org/10.1518/hfes.46.1.50_30392>  
<sub>مقال محكّم · المحور 13 · تُحقِّق منه في 2026-09-29</sub>
- **Parasuraman, R., & Manzey, D. H.** (2010). *Complacency and Bias in Human Use of Automation: An Attentional Integration*. Human Factors, 52(3), 381–410. <https://doi.org/10.1177/0018720810376055>  
<sub>مقال محكّم · المحور 13 · تُحقِّق منه في 2026-09-29</sub>
- **Parasuraman, R., & Riley, V.** (1997). *Humans and Automation: Use, Misuse, Disuse, Abuse*. Human Factors, 39(2), 230–253. <https://doi.org/10.1518/001872097778543886>  
<sub>مقال محكّم · المحور 13 · تُحقِّق منه في 2026-09-29</sub>
- **Parasuraman, R., Sheridan, T. B., & Wickens, C. D.** (2000). *A model for types and levels of human interaction with automation*. IEEE Transactions on Systems, Man, and Cybernetics — Part A, 30(3), 286–297. <https://doi.org/10.1109/3468.844354>  
<sub>مقال محكّم · المحور 13 · تُحقِّق منه في 2026-09-29</sub>
- **Skitka, L. J., Mosier, K. L., & Burdick, M.** (1999). *Does automation bias decision-making?*. International Journal of Human-Computer Studies, 51(5), 991–1006. <https://doi.org/10.1006/ijhc.1999.0252>  
<sub>مقال محكّم · المحور 13 · تُحقِّق منه في 2026-09-29</sub>

## الذكاء الاصطناعي والتعليم — AI Education (8)

- **American Psychological Association** (2026). *AI references (APA Style guidelines)*. APA Style. <https://apastyle.apa.org/style-grammar-guidelines/references/examples/ai-references>  
<sub>توثيق رسمي · المحور 8 · تُحقِّق منه في 2026-09-28</sub>
- **American Psychological Association (McAdoo, T.)** (2026). *How to cite ChatGPT (APA Style blog)*. APA Style. <https://apastyle.apa.org/blog/how-to-cite-chatgpt>  
<sub>توثيق رسمي · المحاور 8، 9 · تُحقِّق منه في 2026-09-28</sub>
- **Hayes, A. F., & Krippendorff, K.** (2007). *Answering the Call for a Standard Reliability Measure for Coding Data*. Communication Methods and Measures, 1(1), 77–89. <https://doi.org/10.1080/19312450709336664>  
<sub>مقال محكّم · تُحقِّق منه في 2026-09-28</sub>
- **Sandve, G. K., Nekrutenko, A., Taylor, J., & Hovig, E.** (2013). *Ten Simple Rules for Reproducible Computational Research*. PLoS Computational Biology, 9(10), e1003285. <https://doi.org/10.1371/journal.pcbi.1003285>  
<sub>مقال محكّم · تُحقِّق منه في 2026-09-28</sub>
- **UNESCO (Miao, F., & Cukurova, M.)** (2024). *AI competency framework for teachers*. UNESCO, Paris. <https://unesdoc.unesco.org/ark:/48223/pf0000391104>  
<sub>معيار أو موقف رسمي · المحور 13 · تُحقِّق منه في 2026-09-26</sub>
- **UNESCO (Miao, F., & Holmes, W.)** (2023). *Guidance for generative AI in education and research*. UNESCO, Paris. <https://unesdoc.unesco.org/ark:/48223/pf0000386693>  
<sub>معيار أو موقف رسمي · المحاور 1، 7، 8، 9 · تُحقِّق منه في 2026-09-26</sub>
- **UNESCO (Miao, F., Shiohira, K., & Lao, N.)** (2024). *AI competency framework for students*. UNESCO, Paris. <https://unesdoc.unesco.org/ark:/48223/pf0000391105>  
<sub>معيار أو موقف رسمي · المحاور 1، 5 · تُحقِّق منه في 2026-09-26</sub>
- **Wineburg, S., & McGrew, S.** (2019). *Lateral Reading and the Nature of Expertise: Reading Less and Learning More When Evaluating Digital Information*. Teachers College Record, 121(11), 1–40. <https://doi.org/10.1177/016146811912101102>  
<sub>مقال محكّم · المحور 8 · تُحقِّق منه في 2026-09-28</sub>

## وثائق المنتجات الرسمية — Official Product Documentation (12)

- **Anthropic** (2026). *Prompting best practices (Claude documentation)*. Anthropic / Claude Platform Docs. <https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices>  
<sub>توثيق رسمي · المحاور 5، 6 · تُحقِّق منه في 2026-09-28</sub>
- **Anthropic** (2026). *Prompting best practices — thinking and structured reasoning*. Anthropic / Claude Platform Docs. <https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/chain-of-thought>  
<sub>توثيق رسمي · المحور 6 · تُحقِّق منه في 2026-09-28</sub>
- **Anthropic** (2026). *Models overview (Claude documentation)*. Anthropic / Claude Platform Docs. <https://platform.claude.com/docs/en/docs/about-claude/models/overview>  
<sub>توثيق رسمي · المحور 7 · تُحقِّق منه في 2026-09-28</sub>
- **Anthropic** (2026). *Claude Help Center (features, projects, memory, privacy, usage limits)*. Anthropic. <https://support.claude.com/en/>  
<sub>توثيق رسمي · المحاور 7، 12 · تُحقِّق منه في 2026-09-28</sub>
- **Google** (2026). *Prompt design strategies (Gemini API documentation)*. Google AI for Developers. <https://ai.google.dev/gemini-api/docs/prompting-strategies>  
<sub>توثيق رسمي · المحاور 5، 6 · تُحقِّق منه في 2026-09-28</sub>
- **Google** (2026). *Structured outputs (Gemini API documentation)*. Google AI for Developers. <https://ai.google.dev/gemini-api/docs/structured-output>  
<sub>توثيق رسمي · المحور 6 · تُحقِّق منه في 2026-09-28</sub>
- **Google** (2026). *Models (Gemini API documentation)*. Google AI for Developers. <https://ai.google.dev/gemini-api/docs/models>  
<sub>توثيق رسمي · المحور 7 · تُحقِّق منه في 2026-09-28</sub>
- **Google** (2026). *Gemini Apps Help*. Google Support. <https://support.google.com/gemini>  
<sub>توثيق رسمي · المحاور 7، 12 · تُحقِّق منه في 2026-09-28</sub>
- **OpenAI** (2026). *Prompt engineering (API documentation)*. OpenAI Developers. <https://developers.openai.com/api/docs/guides/prompt-engineering>  
<sub>توثيق رسمي · المحاور 5، 6، 8، 9 · تُحقِّق منه في 2026-09-28</sub>
- **OpenAI** (2026). *Structured model outputs (API documentation)*. OpenAI Developers. <https://developers.openai.com/api/docs/guides/structured-outputs>  
<sub>توثيق رسمي · المحور 6 · تُحقِّق منه في 2026-09-28</sub>
- **OpenAI** (2026). *Models (API documentation)*. OpenAI. <https://platform.openai.com/docs/models>  
<sub>توثيق رسمي · المحور 7 · تُحقِّق منه في 2026-09-28</sub>
- **OpenAI** (2026). *ChatGPT Help Center (capabilities, file uploads, memory, projects, data controls)*. OpenAI Help Center. <https://help.openai.com/en/collections/3742473-chatgpt>  
<sub>توثيق رسمي · المحاور 7، 12 · تُحقِّق منه في 2026-09-28</sub>  
<sub>⚠︎ الموقع يرفض الطلبات الآلية؛ تُحقِّق منه بقراءة الصفحة في متصفح يوم 2026-09-29.</sub>
