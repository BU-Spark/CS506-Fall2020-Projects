## Data explanation.
The final preprocessed data for all applications can be found in [processed_data.csv](https://github.com/hvarelaf/CS506-Fall2020-Projects/blob/deliverable_2/t_visa_trends_team2/deliverable_2/processed_data.csv). Our team handled the Motions, which can be found in [motions_data.csv](https://github.com/hvarelaf/CS506-Fall2020-Projects/blob/deliverable_2/t_visa_trends_team2/deliverable_2/motions_data.csv). Below, we explain the features in our data.
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
