# Fatal Force

The Washington Post is [compiling a database of every fatal shooting](https://www.washingtonpost.com/graphics/investigations/police-shootings-database/) in the United States by a police officer in the line of duty since Jan. 1, 2015.

Download the data: https://raw.githubusercontent.com/washingtonpost/data-police-shootings/master/fatal-police-shootings-data.csv

[In 2015](https://www.washingtonpost.com/graphics/national/police-shootings/), The Post began tracking more than a dozen details about each killing — including the race of the deceased, the circumstances of the shooting, whether the person was armed and whether the victim was experiencing a mental-health crisis — by culling local news reports, law enforcement websites and social media and by monitoring independent databases such as Killed by Police and Fatal Encounters. The Post conducted additional reporting in many cases.

In 2016, The Post is gathering additional information about each fatal shooting that occurs this year and is filing open-records requests with departments. More than a dozen additional details are being collected about officers in each shooting.

The Post is documenting only those shootings in which a police officer, in the line of duty, shot and killed a civilian — the circumstances that most closely parallel the 2014 killing of Michael Brown in Ferguson, Mo., which began the protest movement culminating in Black Lives Matter and an increased focus on police accountability nationwide. The Post is not tracking deaths of people in police custody, fatal shootings by off-duty officers or non-shooting deaths.

The FBI and the Centers for Disease Control and Prevention log fatal shootings by police, but officials acknowledge that their data is incomplete. In 2015, The Post documented more than two times more fatal shootings by police than had been recorded by the FBI. Last year, the FBI announced plans to overhaul how it tracks fatal police encounters.

[The Post’s database](https://www.washingtonpost.com/graphics/investigations/police-shootings-database/) is updated regularly as fatal shootings are reported and as facts emerge about individual cases. The Post is seeking assistance in making the database as comprehensive as possible. To provide information about fatal police shootings since Jan. 1, 2015, send us an email at policeshootingsfeedback@washpost.com. The Post is also interested in obtaining photos of the deceased and original videos of fatal encounters with police.

## About the data

The file `fatal-police-shootings-data.csv` contains data about each fatal shooting in CSV format. The file can be [downloaded at this URL](https://raw.githubusercontent.com/washingtonpost/data-police-shootings/master/fatal-police-shootings-data.csv). Each row has the following variables:

`id`: a unique identifier for each victim

`name`: the name of the victim

`date`: the date of the fatal shooting in YYYY-MM-DD format

`manner_of_death`:
- `shot`
- `shot and Tasered`

`armed`: dndicates that the victim was armed with some sort of implement that a police officer believed could inflict harm
- `undetermined`: it is not known whether or not the victim had a weapon
- `unknown`: the victim was armed, but it is not known what the object was
- `unarmed`: the victim was not armed

`age`: the age of the victim

`gender`:
- `M`: Male
- `F`: Female
- `None`: unknown

`race`:
- `W`: White, non-Hispanic
- `B`: Black, non-Hispanic
- `A`: Asian
- `N`: Native American
- `H`: Hispanic
- `O`: Other
- `None`: unknown

`city`: the municipality where the fatal shooting took place. Note that in some cases this field may contain a county name where a more specific municipality is unavailable or unknown.

`state`: two-letter postal code abbreviation

`signs of mental illness`: News reports have indicated the victim had a history of mental health issues, expressed suicidal intentions or was experiencing mental distress at the time of the shooting.

`threat_level`: The threat_level column was used to flag incidents for the story by Amy Brittain in October 2015. http://www.washingtonpost.com/sf/investigative/2015/10/24/on-duty-under-fire/ As described in the story, the general criteria for the attack label was that there was the most direct and immediate threat to life. That would include incidents where officers or others were shot at, threatened with a gun, attacked with other weapons or physical force, etc. The attack category is meant to flag the highest level of threat. The other and undetermined categories represent all remaining cases. Other includes many incidents where officers or others faced significant threats.

`flee`: News reports have indicated the victim was moving away from officers
- `Foot`
- `Car`
- `Not fleeing`

The threat column and the fleeing column are not necessarily related. For example, there is an incident in which the suspect is fleeing and at the same time turns to fire at gun at the officer. Also, attacks represent a status immediately before fatal shots by police while fleeing could begin slightly earlier and involve a chase.

`body_camera`: News reports have indicated an officer was wearing a body camera and it may have recorded some portion of the incident.

## Contributing

We welcome assistance in making the our data as complete and accurate as possible. The best way to contribute is to email policeshootingsfeedback@washpost.com. Please note that we do not accept pull requests as the data file is generated downstream of our internal database.

## Licensing

The data is published under an [Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0) license](https://creativecommons.org/licenses/by-nc-sa/4.0/).

## Contact

Contact policeshootingsfeedback@washpost.com with any questions about the data, feedback, updated information or corrections.

## Credits

Research and reporting: Julie Tate, Jennifer Jenkins and Steven Rich

Database development: John Muyskens
