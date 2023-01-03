# Twitter-Project
Since the process of catching data is time-consuming (in both approaches either by using Tweepy or Snscrape) we should find another way to make the process of analysis much smoother). We can achieve this by creating a Data warehouse in which related subjects are stored and the user request would be query on our databases not Twitter. The speed would be way higher, but the cost would also be higher. 
In order to illustrate this concept, we have stored Twitter data on the Iranian Revolutionary movement in 2022: 
Data was extracted from 6 specific hashtags ["MahsaAmini", "OpIran", "Iranrevolution2022", "MohsenShekari", "HosseinRonaghi", and "WomenLifeFreedom"], and raw data was imported into our database. Additionally, we cleaned the tweets' text to prepare them for NLP analysis.  After that, a simple GUI was created so users could choose what information they wanted to see. While this analysis is fairly simple, it could become more sophisticated in the future. 

