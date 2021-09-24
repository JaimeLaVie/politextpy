# politextpy

## Why is *Politextpy* Developed?

We are overwhelmed by this era of overloading information, emerging misinformation and disinformation yet we are at the same time empowered by it to embark on an unprecedented journey of research for international issues. We are exhilarated by the unexampled possibilities computational methods brought us to delineate the dynamics of domestic and international politics. 

Online public opinion initiates our vision to entrench a novel field of study, *Computational Political Communication*. We hope to build up this vision brick by brick, and *Politextpy* is one of the founding bricks. We believe that it is not only for our own research but for further demand from a broader academia. With this open-source package, we hope to equip *Python* users to process English, Chinese, Japanese and Korean languages text via **1）Reading Files**, **2)Web Content Acquisition**, **3) Mapping Country Names**, **4)Preprocessing**, **5) Topic Models** , **6) Supervised/Unsupervised Sentiment Analysis**, **7)Visualization** and **8)Additional Tools** We are more than ever expecting to add more languages and functions in the very near future.

#### Online Public Opinion as A New Approach

+ Pivot in Objects: Elites and Policy-Making vs. Public and Policy-Perception; 
+ Pivot to New Public Sphere: Crossing border/culture, Inter-formats, Weak-tie based;
+ Pivot to Personalized Expression: Sentiments, “Free Market,” Niche and private clusters.

#### Computational Political Communication as A New Attempt

+ Generating Data and Texts: Sufficient, even surfeit objects for computing;
+ Emerging Methods and Technology: Rapid developing Software & Hardware for research;
+ Arising Global Politics Issues: Interacting Geopolitics Dynamics, Major Powers Play, Aussenpolitik and Innenpolitik.


## How does *Politextpy* function?

*Politextpy* is a Python Package aimed at first to process and analyze political texts, e.g., online posts and news outlets' texts about some certain agenda. With enlarging functions, it can also be applied in the analysis of other text for research projects tackled by academia or industry.

### Reading Files

+ Read from five dif- ferent data formats (*.jsonl, .xlsx, .doc, .pdf, and .jpg*). 
+ The program is **reading.py.**

### Web Content Acquisition

+ Comma, period, space, newline characters and copyright statement would be deleted. 
+ The program is **GetWebpageContext.py**

### Mapping Country Names

+ The official name and multiple aliases, abbreviations, or even nicknames are included.
+ Employs the ISO 3166-1 standard to assign a two- digit code to each country, e.g., Sweden equals ’se’.
+ 64 Countries covering the 5 permanent members of the United Nations Security Council, G7 and G20 countries, member states of Organisation for Economic Co-operation and Development (OECD).
+ The program is **country_code.py**

### Preprocessing

+ The preprocessing includes segmentation, merging negation words (e.g., not, no) with its following word, deleting stop words, removing unnecessary punctuations & phrases.
+ The program is **preprocessing.py**

### Topic Model

+ Politextpy adopts *Latent Dirichlet Allocation (LDA)*
+ The program is **topic_models.py**

### Sentiment Analysis

+ Politextpy offers a fuzzy rule based sentiment analysis tool, an adapted version of Vashishtha and colleague’s work.
+ The program is **sentiment_analysis.py**

### Visualization Tools

+ Politextpy provides basic functions like bar chart and line chart drawing, as well as more complicated word cloud and 3-dimensional figure creating.
+ Politextpy incorporates several map-making functions, especially for world map drawing. It can produce normal jpg or png format maps as well as inter- active maps in html format.

### Additional Tools

+ *Words_frequency* returns the top n frequently used words and their frequencies, where n is specified by the user.
+ *8Detect_lang* detects the language of the text, helping choose the correct preprocessing method.
+ *Key_word_extraction* extracts key words of the given texts, which can complement the results of the topic model.
+ *Tsne_plot* and *tsne_value8*, using t-distributed stochastic neigh- bor embedding (t-SNE) method, conduct dimension reduction to high dimensional vectors, enabling them to be shown in a 2D picture.
+ And MORE...


## Words From Us ##

This project initiated from a Tsinghua University master thesis, two *IEEE* conference submissions, three Starbucks meetings and numerous research questions urging for answers. And it will help more of such assignments and aspiration of more people, in places we may have never been to, in ways we may have never imagined, to solve puzzles we may have never encountered. Afterall that is the very starting point and destination of us as developer, researcher, practitioner and educator.
