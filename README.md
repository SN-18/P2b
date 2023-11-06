# P2b: Crowdsourcing and Argumentation

## Introduction
<br>
Crowdsourcing refers to taking a task to be performed and dispersing it among a dispersed group of participants over a network. Crowdsourcing helps in saving time, money and to tap into human resources with different skillsets and/or mindsets.

In this project, we are given 2500 App reviews by people from across the globe regarding applications like Life360 that monitor your location and other metrics to notify it to your family members or guardians. 

Based on the app reviews, we take these 64 sources who have labelled the app as violating any of the 7 consent types, such as “Truth”, “Power”, “Freewill”, “Cognition”, “Attention”,”Statutues” or “Honesty”. These reviewers have taken the app reviews as Truthful, meaning that there is no reason for them to doubt these reviews while labelling the app violation.

For instance, if a review mentions something such as, “The app didn’t portray what it was going to do, it just took more data than it said”, then a typical user might flag the app as having violated “Truth” and “Honesty” consent labels, as it didn’t do what it was supposed to do, and it wasn’t honest in letting it’s users know how it was going to proceed with the data.


## How to run code
<ol>
  <li> Clone the repository using,
    
    ``` git clone https://github.com/SN-18/P2b.git ```
    
  </li>
  <li>
     Open the project using an IDE such as Pycharm or Eclipse.
  </li>
  <li>
    . From a terminal, run python fake_data.py to report top candidates having fake data, if any, is present. The output should look something like:
    
    ![mann_whitney_u_top_10](https://github.com/SN-18/P2b/assets/83748468/bea4b485-c1b4-4453-8693-10706ce7c196)
  </li>
  <li>
    Remove the files manually from P2a_Labels or use the P2a_Real_Labels_Only dataset, that has has segregated the data that has the top candidates for being ‘real’ datapoints. 
  </li>
  <li>
    Run combined_data.py on the above data to get a combined dataset and list of common word embeddings that occur with each of the labels. The output should look something like:

    ![combined_data_after_new](https://github.com/SN-18/P2b/assets/83748468/87392a03-38fd-4acc-9dbe-15ee54b6a477)
  </li>
</ol>
 


## What different files do
1. combined_data.py – It parses over all the review label files available, combines them into one dataset, then filters out the most prominent consent labels from this combined dataset. It then builds and reports a final dataset, with review title, the review and the three most prominent consent violations.
2. fake_data.py – It parses over all the review label files available, and performs the Mann-Whitney U test (read more about that on https://pubmed.ncbi.nlm.nih.gov/14520096/) to test for variability in the given files. Based on its findings, it reports the top candidates for containing fake data.

Here, we used the Mann-Whitney U test as it:
1. Requires no external threshold, like used in standard deviation based tests.
2. Requires no training in the form of ‘original’ data, but is a statistical measure to detect anomalous workflows based on variability.


## How to debug issues
<ul>
  <li>
    Make sure you have python installed. For this, from your IDE, open a terminal and use:

    ```python -- version```

  </li>
  
   
  <li>If the above doesn't print something such as "Python 3.11.X", use [Python's Official Dowload Page](https://www.python.org/downloads/).
  </li>

  <li>Make sure your system has other requirements installed. Use the following command in a terminal, using:
  
  ```pip install -r requirements.txt```
  </li>

<li>
If more problems persist or for further support, 
Contact Author: saurabhnanda.official@gmail.com

</li>
  
</ul>
