# Datasets
## haverhill_incident_reports.csv
### Description
A tabular dataset of incident reports coming from Haverhill which was collected from pdf, parsed by a model and stored in csv form. In its current state it is incomplete and requires cleaning and manual verification to be useful. At the moment that data contains police officers name, their rank, date of occurence, location of incident.
### Features
- Filename: name of incident pdf
- Date Ocurred: date of incident
- Incident #: the incident identifier
- Incident Type/Offense: the incident category identifier
- Location: address where incident occured
- Narrative: description of incident
- Offender Age: age of the offender
- Offender Race: race of the offender
- Offender Sex: sex of the offender
- Officer Name: name of the officer handling incident
- Officer Rank: rank of the officer handling incident
- Parent Name: name of parent of victim
- Parent Race: race of parent of victim
- Parent Sex: sex of parent of victim
- Review status: police department report approval status
- Victim Age: age of victim
- Victim Name: name of victim
- Victim Race: race of victim
- Victim sex: sex of the victim

## field_incident_reports.csv
## Description
An Excel file containing data on the names of officers involved in incidents in New Bedford. Other key variables in the dataset include the age, sex, race, and ethnicity of the civilians involved in the incidents.
### Features
- DATE: The date an incident occurred.
- TIME: The time of day an incident occurred.
- NUM: The street number of where an incident occurred.
- ADDRESS: The street address of where an incident occurred.
- LAT: The point of latitude of where an incident occurred.
- LONG: The point of longitude of where an incident occurred.
- SEX: The sex of the individual involved in the incident.
- RACE: The race of the individual involved in the incident.
- AGE: The age of the individual involved in the incident.
- PRECISION: A determination of the accuracy of the location of the incident; equals “Exact” if the location is precise, and equals “Estimate” if the location is only an estimate.
- Ethnicity: The ethnicity of the individual involved in the incident.
- OfficerID: The identification of the police officer involved in the incident.
- OfficerFirstName: The first name of the police officer involved in the incident.
- OfficerLastName: The last name of the police officer involved in the incident.
- OfficerDesignation: The enhanced identification of the police officer involved in the incident.

## haverhill_school_incident_reports.csv
## Description
Information regarding incidents in the city of haverhill schools.
### Features



## springfield_arrest_logs.csv
## Description
Information regarding arrests in the city of Springfield.
### Features
- Arrest: Springfield PD’s unique identifier for the arrest
- Arrest. ID: An identifier (we think it’s the badge number) for the officer who made the arrest
- Reported: The date the arrest was recorded in Springfield’s system
- Status: [not important for our analysis]
- Approved: [not important for our analysis]
- Juvenile: whether the suspect was under 18 years old — this will always be N because the publicly available data does not include juvenile arrests
- Released: Whether the suspect was released after being arrested (with S meaning that they were just given a summons)
- Arrest Date/Time: the exact timestamp for when the arrest was made
- Zone: The sector of the city where the arrest occurred
- Location: The street address where the arrest occurred
- Offenses: A semicolon-delimited list of the general categories of offenses which the suspect is being arrested for
- Offense Codes: A semicolon-delimited list of the numerical codes which describe the suspect’s offenses
- Offense Descriptions: A semicolon-delimited list of slightly longer descriptions of each charge that the suspect was arrested for
- Suspect Name: name of the suspect
- Suspect DOB: suspect’s date of birth
- Suspect Address: suspect’s home address
- Suspect Age on Date of Arrest: suspect’s age on the day they were arrested
