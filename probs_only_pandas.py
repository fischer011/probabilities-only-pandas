"""vh.probs_only_pandas

Loads dataset into pandas DataFrame.  Computes the probability of each 
car make in the dataset and the conditional probability of each aspiration
type, given each make in the dataset:  P(aspiration = a|make = m). Creates 
a file and saves results to file in same directory as code and datasets.
"""

import sys
import os
import pandas as pd

def main():
    base_dir = os.path.abspath(os.path.dirname(__file__))
    output_dir = base_dir+'\\probs_output.txt'
    

    # Read in csv and create DataFrame.
    # Only need make and aspiration columns.
    cars= pd.read_csv("cars.csv",usecols=['make', 'aspiration'])
    cars_df=pd.DataFrame(cars)

    # Using crosstab to generate frequency distribution
    # of each aspiration type given make.
    frequency_dist = pd.crosstab(cars_df.make, cars_df.aspiration
                                 , normalize=0
                                 )

    # Formatting for percentages. 
    cond_probability = (frequency_dist*100).stack()

    # Storing conditional probability in a DataFrame.
    cond_probability_df = pd.DataFrame({'id': cond_probability
                                        .index.to_list()
                                        , 'probability': cond_probability}
                                       ).round(decimals=2)

    # The lambda function is called to generate the print template.
    print_probability = lambda x: print("Prob(aspiration=" + x.id[1] 
                                        + "|make=" + x.id[0] + ") = "
                                        + str(x.probability) + "%")

    with open(output_dir, 'w') as f:
        original_stdout = sys.stdout
        sys.stdout = f
        cond_probability_df.apply(print_probability, axis=1)
        print('\n')
        
        # Calculate and print probability of each make.
        for make in cars_df['make'].unique():
            make_prob = (cars_df['make'].value_counts().loc[make]
                         / cars_df['make'].value_counts().sum()
                         * (100)).round(decimals=2)
            print(f"Prob(make={make}) = {make_prob}%")
        sys.stdout = original_stdout
            
if __name__ == "__main__":
    main() 

