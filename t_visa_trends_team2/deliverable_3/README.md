## Documentation.
The file [t-visas_processing_pdfs.py](https://github.com/hvarelaf/CS506-Fall2020-Projects/blob/deliverable_3/t_visa_trends_team2/deliverable_3/t-visas_processing_pdfs.py) is the script used to process the 'Lexis Dataset -- Non-precedent AAO Decisions'. Necessary imports are included in the script along with the explanation of the functions executed. This script yields the the final preprocessed data for all applications, which  can be found in [processed_data.csv](https://github.com/hvarelaf/CS506-Fall2020-Projects/blob/deliverable_3/t_visa_trends_team2/deliverable_3/processed_data.csv). Our team handled the Motions, which can be found in [motions_data.csv](https://github.com/hvarelaf/CS506-Fall2020-Projects/blob/deliverable_3/t_visa_trends_team2/deliverable_3/motions_data.csv). Below, we explain the features in our data.
\
\
**url** - contains the source of the application's PDF.\
**filename** - contains the filename of the application's PDF.\
**path** - contains the path of the database directory for each application's PDF.\
**ID** - contains the ID listed in the application.\
**date** - contains the date listed in the application.\
**type** - can be 'appeal' or 'motion'.\
**status** - contains the type of Form listed in the application.\
**order** - contains the text under the Order section in the application, i.e. the decision on the application.\
**is_family** - True if it contains “Supplement A, Application for Qualifying Family Member of a T-1 Nonimmigrant” in status.\
**description** - contains the first paragraph of the application under the Opinion or Analysis section.\
**LEXIS Citation** - contains the LEXIS citation listed in the application.\
**counsel** - contains 'no' if the application does not contain a Counsel section, 'yes' otherwise.

The file [t-visas_motions_analysis.ipynb](https://github.com/hvarelaf/CS506-Fall2020-Projects/blob/deliverable_3/t_visa_trends_team2/deliverable_3/t-visas_motions_analysis.ipynb) is the Jupyter Notebook containing the code used for the analysis of the Motions data. Necessary imports are included at the beginning of the Notebook, along with the results of each step of the analysis. This analysis was used for the results presented in [t-visas_motions_report.pdf](https://github.com/hvarelaf/CS506-Fall2020-Projects/blob/deliverable_3/t_visa_trends_team2/deliverable_3/t-visas_motions_report.pdf), which details our findings.



