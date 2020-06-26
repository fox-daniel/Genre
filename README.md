# Genre and Gender

### Project Team Members: Tom Johnson and Daniel Fox


## Abstract

Digital repositories of knowledge such as Wikipedia continue to use music classification systems derived from prejudiced hierarchical systems. Despite initial claims of neutral algorithmic approaches, broad research has shown how automation perpetuates the existing social inequities. Within music culture it is thus important to ask, Is there gender bias in the genre labels for musicians on Wikipedia? Our project answers this question in the affirmative using a dataset of ~15,000 music artists labeled with their genders and genres. We approach this through three modes of analysis: 1) We have show that female artists are significantly under represented within the set of artists with six or more genre labels. 2) We will use machine learning models to predict gender from genre label combinations. 3) We will analyze gender bias within latent communities of networks of artists and genres. We will present our findings by a) deploying an interactive web app using cloud computing to promote data curiosity and user exploration, b) publishing a peer reviewed article in a music journal, c) publishing popular and technical posts on Medium, c) posting our processed data set on Kaggle.com, and d) posting our code in a public GitHub repository. 
In the context of music studies, our work refines the understanding of how digital databases are reinforcing historical social inequities. We hope that our work can influence the future designs of recommendation systems.



## Project Description

Is there gender bias in the genre labels for musicians on Wikipedia? This project provides an affirmative answer by combining humanistic and data driven approaches. Research has shown that 21st-century repositories of knowledge residing in media(ting) services like Google or Wikipedia re-inscribe systemic asymmetries.  Rather than sidestepping social bias, automation amplifies existing social inequities.  On Wikipedia, only 15% of biographical articles are about women.  More subtle metrics reveal systematic gender bias in more than just article counts. Wagner et al. demonstrate lexical bias (female is the marked gender) and “assortativity” bias (articles about women are more likely to link to men than the other way around).  

As music listening is increasingly influenced by online databases and recommendation systems, the domain-specific cultural practices encoded in music genre labeling is amplified. Classification of musical types has been guided by prejudiced groupings of musicians and audiences.  If Wikipedia’s metadata reflects this hierarchical tradition, then we expect genres to be unevenly associated with male and female artists. Moving beyond the mere preponderance of male artists, our research reveals the modes through which genre labeling amplifies gender bias.  

### The Data

Our cleaned data set of 15,470 music artists includes names, genders, and the music genres from their Wikipedia infoboxes. Starting from a dataset on Kaggle.com containing the name and gender of singers, we scraped genre metadata from Wikipedia.  Removing artists for which the scraper could not retrieve genre labels reduced the dataset from ~22,000 to ~15,000 artists. We verified the gender on a random sample (1% of our corpus) by referencing pronoun usage for each artist on the artist website, social media page, or Wikipedia entry. Of this 1%, we verified the accuracy of 153/154 to be correct, the incorrect item being a band of multiple people. We dropped all bands from the corpus, reducing our dataset by roughly 25 items. Significant cleaning was required to deal with spelling irregularities. Further, because genre labels are not standardized, we used domain specific knowledge about music genres to make decisions about when to equate labels: “rock & roll” was equated with “rock n roll” but their joint category was kept distinct from “rock.” After imposing these equivalences, there were 1,494 distinct genre labels. Many artists have a single genre label, such as “pop,” whereas one artist had 73 genre labels. The gender breakdown is 31% female and 69% male.

### Methods of Analysis

We analyze the correlation between inferred binary gender labels and the genre labels present in Wikipedia infoboxes for musicians through three lines of investigation:

1.	We have measured how the ratio of actual to expected numbers of female and male artists varies with the number of genre labels assigned to the artist. Our analysis shows that female artists are under-represented within the category of artists having at least six genre labels assigned to them, whereas there is no gender bias with regard to the number of genre labels for artists with five or less labels. 
2.	We use machine learning to train models that predict the gender of an artist based only on their genre labels. The predominance of male over female artists creates difficulties for a predictive model. Given any input, a model that always predicts male will be correct 69% of the time. A model using a majority vote for each genre-set that appears has an in-sample accuracy of 73%. This is an upper bound for the full in-sample accuracy of any model. Random forest, GBT, and deep neural net models easily achieve this. Our future work in this direction will be to train and test models on subsamples with balanced numbers of male and female artists. In this way a predictive model may attain higher test-set accuracy and analysis of that model can reveal which features are most predictive of gender.
3.	We will analyze the gender distribution of the latent communities within the network structure of genres and musicians in our dataset. If there is systemic inequality in genre labels, we expect these graph structures to clump into gendered communities. In particular, we form weighted graphs in which the nodes are genre labels and the weight of an edge is the number of artists that have the genre labels of those two nodes. We will then compare the graph-centrality of a genre to its gender bias.

### Presentation

We will present our work in five ways:

1. We will promote data curiosity by deploying an interactive web app allowing users to query the dataset and models. We have a working prototype running on a virtual machine in AWS. 
2. Submission of a peer-reviewed article.
3. A pair of Medium articles. One for a general audience explaining the results and one that focuses on technical aspects (code and statistics) 
4. Posting the code in public GitHub repositories.
5. Posting the processed dataset to Kaggle.com.




## Bios:

Daniel Fox is a doctoral candidate in Music at The Graduate Center, CUNY. His writing on music has appeared in Perspectives of New Music and Hyperallergic. His dissertation examines how technology and performance practices used within American experimental music shape our ideas about what is natural. He holds a PhD in mathematics from Duke University and has published math research in the Transactions of the American Mathematical Society and Communications in Analysis and Geometry. His compositions have been performed by the Jack Quartet and Talea Ensemble.

Tom Johnson is a Visiting Assistant Professor of Music at Skidmore College. His current research focuses on streaming services and musical genre. He is particularly interested in how our musical experiences are mediated by (and in turn mediate) technologies like Spotify or Apple music. Tom has published on race in twenty-first century technologies, the role of tonality in early-20th-century modernist practices and on some recent literature on popular music genres.
