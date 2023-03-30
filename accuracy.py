import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Download required NLTK resources
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')

# Define preprocessing functions
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def preprocess_text(text):
    # Tokenize text into words
    words = word_tokenize(text)
    # Remove stop words, punctuation, and numbers
    words = [word.lower() for word in words if word.isalpha() and word.lower() not in stop_words]
    # Lemmatize words
    words = [lemmatizer.lemmatize(word) for word in words]
    # Join words back into a string
    text = ' '.join(words)
    return text

def compare_paragraphs(paragraph1, paragraph2):
    """
    Compare two paragraphs and save the similarity percentage in a dataframe column.
    """
    # Preprocess paragraphs
    paragraph1 = preprocess_text(paragraph1)
    paragraph2 = preprocess_text(paragraph2)
    
    # Create a CountVectorizer object to convert the paragraphs into a matrix of word counts
    count_vect = CountVectorizer()
    matrix = count_vect.fit_transform([paragraph1, paragraph2])
    
    # Use cosine similarity to compare the paragraphs
    similarity = cosine_similarity(matrix)[0][1]
    
    # Save the similarity percentage in the specified column of the dataframe
    # df[save_column] = similarity * 100
    
    # Return the similarity percentage
    return similarity * 100


