# Fatal Force Database (v2)

## About the data

Each day researchers at The Post identify and manually record data for fatal police shootings in the United States. Each record requires at least two sources and must be approved by our editors before being publicly released.

Data about each fatal shooting is provided via two comma-separated value (CSV) files:

**Death Record** data for each victim and incident is included in `/v2/fatal-police-shootings-data.csv`. 

New in v2 is a second **Agencies** csv, `/v2/fatal-police-shootings-agencies.csv`, which contains data for police agencies involved in at least one fatal police shooting since 2015. The agencies csv has a field called `agency_ids`, which can be used to associate each death record with the agencies involved.

To enable joining this dataset with other federal law enforcement datasets, in 2022 The Post undertook an effort to increase the coverage of federal Originating Agency Identifier (ORI) codes recorded for agencies in the database. Using agency data from the FBI and Department of Justice, reporters did a combination of automated and manual name and ORI code matching to fill in missing ORI code data. They also standardized department names. Agency naming, organization, hierarchy and classification varies from state to state. For this reason, sub-agencies and local troops, regions and posts have been aggregated into their parent agencies, meaning that in some cases an individual agency will have multiple associated ORI codes. For instance, a state police department may have the ORI codes of multiple barracks associated with it.

### Major data schema changes between version 1 and version 2

The Post created version 2 of this dataset in 2022 to refine and better define data categories, as well as improve documentation about how the data is obtained and classified. In addition to the altering of fields and formatting, a separate agencies dataset has been added which includes information on the law enforcement agencies which have been involved in at least one fatal shooting since 2015.

**High-level summary of major changes to the data schema introduced in version 2:**

V1 field | V2 Field | Context
---|---|---|
`manner_of_death` | field removed  | This database tracks fatal police shootings. Other weapons (e.g. a Taser) may be involved in the encounter, but the manner of death for victims in these records is always a police shooting. Thus, the field was removed.
`race` (single)| `race` (multiple) | Field converted from a single option to a list of options. Previously multi-racial or multi-ethnic victims were tracked using the `Other` option. This update allows us to more accurately categorize shootings of individuals with multiple ethnic and racial backgrounds.
-- |`race_source` | This field was added to identify the source from which race was determined, which can range from court documents to a researchers' assessment based on a victim's photograph.
`threat_level` | `threat_type`| Renamed field to more accurately portray data we have collected, while removing implication of hierarchy.
`signs_of_mental_illness` |  `was_mental_illness_related` | Renamed field to more accurately portray data we have collected when news accounts or police reports reflect a victim may have had a history of mental health issues or was experiencing mental distress at the time of the shooting.
`flee` | `flee_status`| Renamed field to more accurately portray data we collected
`armed` | `armed_with` | This field originally included the specific weapon if the victim had one and otherwise indicated `unarmed`, `undetermined`, or `unknown`. It has been updated to use federal classifications based on NIBRS, the national incident-level crime reporting system. `toy` category has been renamed to `replica`.
`is_geocoding_exact`|  field removed | Location information for an incident is often only available at the block level (eg. 100 Block of Main St). Precision and accuracy of geocoded location information was not sufficiently represented by this field. 
|-- | `location_precision`| New field to indicate the precision level of the location data which was geocoded to generate the record's coordinate data.
| -- | `agency_ids`| List of agency ids to enable joining with the agencies csv.

### Death Records

**File:** `/v2/fatal-police-shootings-data.csv` 

**Summary:** Death record data about each incident and victim. The file can be downloaded at this URL. Victim information is obtained from any available recordings of the incident, news accounts, court records and/or official statements.

**Fields:**

| | Description| Type| Example value|
| ---| --- | ---- | ---|
| **Incident information** |
| `id`| A unique identifier for each fatal police shooting incident.| number| `2`|
| `date`| The date of the fatal shooting.| string <br> `YYYY-MM-DD`| `2020-06-25`|
| `body_camera`| Whether news reports have indicated an officer was wearing a body camera and it may have recorded some portion of the incident.| boolean `True`/ `False`| `True`
| `city`| The municipality where the fatal shooting took place| string | `New Orleans`|
|`county`| County where the fatal shooting took plce. | string | `Brown`
| `state`| The two-letter postal code abbreviation for the state in which the fatal shooting took place.| string|`LA`|
| `latitude`| The latitude location of the shooting expressed as WGS84 coordinates, geocoded from addresses. Please note that the precision and accuracy of incident coordinates varies depending on the precision of the input address which is often only available at the block level. | decimal number |`47.246826`|
|`longitude`| The longitude location of the shooting expressed as WGS84 coordinates, geocoded from addresses.| decimal number|`-123.121592`|
|`location_precision`| Indicates the precision level of the input which was geocoded to generate the coordinate data. | string <br><br> options:<br>-`address`: Specific address, eg: `1 Main St.`<br>-`poi_small`: A small point of interest, eg: `Jim's Pizza`.<br>-`intersection`: Intersection of two roads, eg: `6th Avenue and Izabel Street` <br>-`poi_large`: A large point of interest, eg: `Central Mall`. <br>-`block`: Block level address, eg: `100 Block of Main St.`<br>-`road`: Road name, eg: `Glenwood Drive` <br>-`highway`: Highway name, eg: `Georgia Highway 11`<br>-`not_available`: Location was entered before current methodology was established. | `block`
| **Victim information**||||
| `name`| The name of the victim.| string| `John Doe`|
| `age`| The age of the victim at the time of the incident.| number| `23`|
| `gender`| The gender of the victim. The Post identifies victims by the gender they identified with if reports indicate that it differs from their biological sex.| string <br><br> options:<br>- `male`<br>- `female`<br>- `non-binary`<br>- `--`: Unknown| `male`|
| `race`| The race and ethnicity (where known) of the victim. May contain multiple values to accommodate for multi-racial or several racial and ethnic identifications. Race has been included where news accounts, police reports or other official documents specifically mention a victim’s race or where researchers were able to make a visual determination on racial identification through photos. With the introduction of v2 of the database, the Post has began tracking multiple race and ethnicity designations; prior to 2021, only one race or ethnicity was assigned to most victims. | string <br><br> options:<br>- `W`: White<br>- `B`: Black<br>- `A`: Asian heritage<br>- `N`: Native American<br>- `H`: Hispanic<br>- `O`: Other<br>- `--`: Unknown| `"B;H"`|
| `race_source`| Sourcing methodology for victim race data. | string <br><br> options: <br>- `public_record`<br>- `clip`<br>- `photo`<br>- `other`<br>- `not_available`: Indicates older records which have `race` populated but The Post does not have details on the methodology because it was collected before the current structure was introduced. <br>- `undetermined`: When The Post's race research avenues have been exhausted and race is still unknown, this indicates that race is still unknown, but research is complete.<br>- `null`| `public_record`|
| `was_mental_illness_related` | Whether news reports have indicated the victim had a history of mental health issues, expressed suicidal intentions or was experiencing mental distress at the time of the shooting.| boolean `True`/`False`| `True`                                                             |
| `threat_type`* | Actions the victim took leading up to the fatal shooting.| string <br><br> options: <br>- `shoot`: The victim fired a weapon.<br>- `point` :The victim pointed a weapon at another individual.<br>- `attack`: The victim attacked with other weapons or physical force.<br>- `threat`: The victim had some kind of weapon visible to the officers on the scene.<br>- `move`: The victim was moving in a threatening way.<br>- `flee`: The victim was fleeing (see `flee_status`)<br>- `accident`:  :question: <br>- `undetermined`: The threat type could not be determined from available evidence| `point`|
| `armed_with`| What, if anything, was the victim armed with per federal classifications based on NIBRS, the national incident-level crime reporting system. These categories are roughly reflected in local police data and forms. A NIBRS manual is can be found here (see values for data element Type Weapon/Force involved, on PDF page 104/report page 94).| string <br><br> options: <br>- `gun`: A firearm, handgun, shotgun, or other firearm<br>- `knife` : A knife or other cutting instrument (razors, hatches, axes, cleavers, scissors, broken bottles, ice picks, etc.)<br>- `blunt_object`: A blunt object (baseball bats, the butt of a handgun, clubs, bricks, tire irons, bottles, etc.)<br>- `other`: Any other weapon (BB guns, pellet guns, Tasers, pepper spray, stun guns, etc.)<br>- `replica`: A toy weapon, replica, or other non-functional firearm.<br>- `undetermined`: Whether the victim had a weapon could not be determined from available evidence.<br>- `unknown`: There was a weapon involved, but we do not know what kind.<br>- `unarmed`: The victim had no weapon according to available evidence.<br>- `vehicle`: A motor vehicle or vessel. | `"gun;knife"`|
| `flee_status`*| How, if at all, was the victim moving relative to officers leading up to the shooting.| string <br><br> options: <br>- `foot` : On foot<br>- `car` : Via car <br>- `other`: Via another vehicle<br>- `not`: Not fleeing                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       | `foot`|
|`agency_ids`| List of agency ids associated with the death record. | string | `"1;2"` 

*Note:* `threat_type` and `flee_status` are not necessarily related. For example, there may be an incident in which the suspect is fleeing and at the same time turns to fire at gun at the officer. 

### Agencies

**File:** `/v2/fatal-police-shootings-agencies.csv`

**Summary:** Data for departments and agencies involved in a fatal police shooting in the database. This separate CSV can be joined with the death record CSV via the `agency_ids` value.

**Fields:**

| | Description| Type| Example value|
| ---| --- | ---- | ---|
| `id`| Department database id | integer | `1`
| `name`| Department name | string | `Davis County Sheriff's Office` 
| `type`| Department type | string <br><br> options: <br>-`local_police`: County or other local police <br>-`local_other`: Other local department<br>-`sheriff`: Sheriff\s office<br>-`other`: Other non-local department<br>-`state_police`: State police<br>-`state_other`: Other statewide law enforcement<br>-`federal`: Federal law enforcement | `state_other`
| `state`| Department state | State in which the agency is located. | `UT`
| `oricodes`| Department ORI codes (federal identifiers). <br><br>Note that there can be multiple ORI codes for a single department due to aggregated sub-departments and/or differing values provided by the FBI vs DOJ. | string | `"ABC123;XYZ987"`
| `total_shootings` | Total death records the agency has been involved with. | integer |`2`
