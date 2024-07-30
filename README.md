# Team Details

- Team name : Fairies
- Team members : Aditya Kadam, Giorgia Sorrentino, Samia Qbaibi

# Task Details

- Task : Part-of-Speech Tagging
- Approaches : Rule-Based, Brill Tagger, HMM, ...
- Evaluation :  Accuracy, Macro & Micro F1-Scores
- Language : Python

# How to run the files

RuleBased.py is the file that performs rule-based tagging for English data.

Brill.py is the file that performs transformation based tagging, using Brill, for English, Italian & French.

hmm_en.py is the file that performs probabilistic tagging, using hidden Markov model and the Viterbi algorithm, for English data.

hmm_it.py is the file that performs probabilistic tagging, using hidden Markov model and the Viterbi algorithm, for Italian data.

hmm_fr.py is the file that performs probabilistic tagging, using hidden Markov model and the Viterbi algorithm, for French data.

evaluation.py is the evaluation file.

train.col, test.col : Data from IMS server

it_train.col, it_test.col, fr_train.col, fr_test.col : Data from universaldependencies.org

- Keep all of these files in the same folder;
  
[Rule Based]
- Run RuleBased.py ; 
- On running RuleBased.py, the Accuracy, Macro & Micro average F1-Score values will be calculated and printed for English data.
  
[Brill Based]
- Run Brill.py ;
- On running Brill.py, the Accuracy, Macro & Micro average F1-Score values will be calculated and printed for English, Italian & French data. Estimated time : 1 Hour

[HMM English]
- Run hmm_en.py ;
- On running hmm_en.py, the Accuracy, Macro & Micro average F1-Score values will be calculated and printed for the English data. 

[HMM Italian]
- Run hmm_it.py ;
- On running hmm_it.py, the Accuracy, Macro & Micro average F1-Score values will be calculated and printed for the Italian data.

[HMM French]
- Run hmm_fr.py ;
- On running hmm_fr.py, the Accuracy, Macro & Micro average F1-Score values will be calculated and printed for the French data. 



