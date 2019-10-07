Stop words are the exact stopword list of Hazm
Files are tokenized into lists then lists are converted to dictionaries with freq. of each word and then stopwords are deleted from the original dictionaries

All 8 required dictionaries are generated in word_cloud.py and then given as input to the persian_wordcloud to draw word clouds.

It is clear that in the ones with stop words included the stop words have high frequency.
And the ones without stop words are better for making a good judgement about the content. 
The ones that other label does not exist in the main one are very useful for classifying the two labels from each other and can be used as good features
