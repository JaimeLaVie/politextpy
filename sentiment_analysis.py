# sentiment_analysis.py 情感计算
# import os
import numpy as np
import skfuzzy as fuzz
from nltk.sentiment.vader import SentimentIntensityAnalyzer
sid = SentimentIntensityAnalyzer()
from . import preprocessing
decontracted = preprocessing.preprocessing_en().decontracted

# Generate universe variables
#   * pos and neg on subjective ranges [0, 1]
#   * op has a range of [0, 10] in units of percentage points
x_p = np.arange(0, 1, 0.1)
x_n = np.arange(0, 1, 0.1)
x_op = np.arange(0, 10, 1)

# Generate fuzzy membership functions
p_lo = fuzz.trimf(x_p, [0, 0, 0.5])
p_md = fuzz.trimf(x_p, [0, 0.5, 1])
p_hi = fuzz.trimf(x_p, [0.5, 1, 1])
n_lo = fuzz.trimf(x_n, [0, 0, 0.5])
n_md = fuzz.trimf(x_n, [0, 0.5, 1])
n_hi = fuzz.trimf(x_n, [0.5, 1, 1])
op_Neg = fuzz.trimf(x_op, [0, 0, 5])  # Scale : Neg Neu Pos
op_Neu = fuzz.trimf(x_op, [0, 5, 10])
op_Pos = fuzz.trimf(x_op, [5, 10, 10])

def fuzzyrules(text):
    # 
    text = text.lower()
    tweet = decontracted(text)
    ss = sid.polarity_scores(tweet)
    posscore=ss['pos']
    negscore=ss['neg']
    neuscore=ss['neu']
    compoundscore=ss['compound']
                
    # print("\nPositive Score for each  tweet :")    
    if (posscore==1):
        posscore=0.9 
    else:
        posscore=round(posscore,1)
    # print(posscore)

    # print("\nNegative Score for each  tweet :")
    if (negscore==1):
        negscore=0.9
    else:
        negscore=round(negscore,1)
    # print(negscore)

    # print ('\nHere 1!\n')

# We need the activation of our fuzzy membership functions at these values.
    p_level_lo = fuzz.interp_membership(x_p, p_lo, posscore)
    p_level_md = fuzz.interp_membership(x_p, p_md, posscore)
    p_level_hi = fuzz.interp_membership(x_p, p_hi, posscore)
                
    n_level_lo = fuzz.interp_membership(x_n, n_lo, negscore)
    n_level_md = fuzz.interp_membership(x_n, n_md, negscore)
    n_level_hi = fuzz.interp_membership(x_n, n_hi, negscore)
                
    # Now we take our rules and apply them. Rule 1 concerns bad food OR nice.
    # The OR operator means we take the maximum of these two.
    active_rule1 = np.fmin(p_level_lo, n_level_lo)
    active_rule2 = np.fmin(p_level_md, n_level_lo)
    active_rule3 = np.fmin(p_level_hi, n_level_lo)
    active_rule4 = np.fmin(p_level_lo, n_level_md)
    active_rule5 = np.fmin(p_level_md, n_level_md)
    active_rule6 = np.fmin(p_level_hi, n_level_md)
    active_rule7 = np.fmin(p_level_lo, n_level_hi)
    active_rule8 = np.fmin(p_level_md, n_level_hi)
    active_rule9 = np.fmin(p_level_hi, n_level_hi)
                
    # print ('\nHere 2!\n')

    # Now we apply this by clipping the top off the corresponding output
    # membership function with `np.fmin`
                
    n1=np.fmax(active_rule4,active_rule7)
    n2=np.fmax(n1,active_rule8)     
    op_activation_lo = np.fmin(n2,op_Neg)
                
    neu1=np.fmax(active_rule1,active_rule5)
    neu2=np.fmax(neu1,active_rule9)     
    op_activation_md = np.fmin(neu2,op_Neu)
                
    # print ('\nHere 3!\n')
                
    p1=np.fmax(active_rule2,active_rule3)
    p2=np.fmax(p1,active_rule6)   
    op_activation_hi = np.fmin(p2,op_Pos)
                
    op0 = np.zeros_like(x_op)
                
    # print ('\nHere 4!\n')

    # Aggregate all three output membership functions together
    aggregated = np.fmax(op_activation_lo, np.fmax(op_activation_md, op_activation_hi))
                
    # Calculate defuzzified result
    op = fuzz.defuzz(x_op, aggregated, 'centroid')
    output=round(op,2)

    op_activation = fuzz.interp_membership(x_op, aggregated, op)  # for plot

    # print ('\nHere 5!\n')

    # print("\nFiring Strength of Negative (wneg): "+str(round(n2,4)))
    # print("Firing Strength of Neutral (wneu): "+str(round(neu2,4)))
    # print("Firing Strength of Positive (wpos): "+str(round(p2,4)))
                
    # print("\nResultant consequents MFs:" )
    # print("op_activation_low: "+str(op_activation_lo))
    # print("op_activation_med: "+str(op_activation_md))
    # print("op_activation_high: "+str(op_activation_hi))
                
    # print("\nAggregated Output: "+str(aggregated))

    # print("\nDefuzzified Output: "+str(output))

    # Scale : Neg Neu Pos   
    if 0<(output)<3.33:    # R
        # print("\nOutput after Defuzzification: Negative")
        result = -1
                    
    elif 3.34<(output)<6.66:
        # print("\nOutput after Defuzzification: Neutral")
        result = 0

    elif 6.67<(output)<10:
        # print("\nOutput after Defuzzification: Positive")
        result = 1

    return result

if __name__ == "__main__":
    pass