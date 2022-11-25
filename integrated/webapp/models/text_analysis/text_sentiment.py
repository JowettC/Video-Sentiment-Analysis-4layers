import pickle
import warnings
import pandas as pd
warnings.filterwarnings('ignore')



def main():
    # importing our best model selected for this project
    best_model = pickle.load(open('./models/text_analysis/best SVC (selected model).pkl', 'rb'))

    # importing our count vectorizer used in training

    cv = pickle.load(open('cv (selected).pickel', 'rb')) 

    # Sample text to illustrate how code runs. Replace content with actual stuff later on
    text = ['happy go lucky']
    new_data=  pd.Series(text, copy=False)

    # Use CV then predict and print result
    X_test_bow = cv.transform(new_data).toarray()
    result = best_model.predict(X_test_bow)
    # calls the function below to return the label (positive/negative).
    # You may add a return function if you want
    print(results(result))

def predict(text):
    best_model = pickle.load(open('./models/text_analysis/best SVC (selected model).pkl', 'rb'))
    cv = pickle.load(open('./models/text_analysis/cv (selected).pickel', 'rb')) 
    text = [text]
    new_data=  pd.Series(text, copy=False)
    X_test_bow = cv.transform(new_data).toarray()
    result = best_model.predict(X_test_bow)
    return(results(result))

# Below method is to convert labels back to positive or negative
def results(result):
    if result[0]==0:
        return 'positive'
    if result[0]==1:
        return 'negative'


print(predict('happy go lucky'))
# if __name__ == "__main__":
#     main()