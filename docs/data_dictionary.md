# Data dictionary

Columns of the final model (142). Source descriptions for application columns come from Home Credit's `HomeCredit_columns_description.csv`; engineered columns are defined in `src/features.py` and `src/history.py`. History features are computed only from records dated before the application (D17).

*Not a lending policy; educational project.*

| Column | Origin | Description |
|---|---|---|
| `NAME_CONTRACT_TYPE` | Application | Identification if loan is cash or revolving |
| `CODE_GENDER` | Application | Gender of the client |
| `FLAG_OWN_CAR` | Application | Flag if the client owns a car |
| `FLAG_OWN_REALTY` | Application | Flag if client owns a house or flat |
| `CNT_CHILDREN` | Application | Number of children the client has |
| `AMT_INCOME_TOTAL` | Application | Income of the client |
| `AMT_CREDIT` | Application | Credit amount of the loan |
| `AMT_ANNUITY` | Application | Loan annuity |
| `AMT_GOODS_PRICE` | Application | For consumer loans it is the price of the goods for which the loan is given |
| `NAME_TYPE_SUITE` | Application | Who was accompanying client when he was applying for the loan |
| `NAME_INCOME_TYPE` | Application | Clients income type (businessman, working, maternity leave,…) |
| `NAME_EDUCATION_TYPE` | Application | Level of highest education the client achieved |
| `NAME_FAMILY_STATUS` | Application | Family status of the client |
| `NAME_HOUSING_TYPE` | Application | What is the housing situation of the client (renting, living with parents, ...) |
| `REGION_POPULATION_RELATIVE` | Application | Normalized population of region where client lives (higher number means the client lives in more populated region) |
| `DAYS_BIRTH` | Application | Client's age in days at the time of application |
| `DAYS_EMPLOYED` | Application | How many days before the application the person started current employment |
| `DAYS_REGISTRATION` | Application | How many days before the application did client change his registration |
| `DAYS_ID_PUBLISH` | Application | How many days before the application did client change the identity document with which he applied for the loan |
| `OWN_CAR_AGE` | Application | Age of client's car |
| `FLAG_MOBIL` | Application | Did client provide mobile phone (1=YES, 0=NO) |
| `FLAG_EMP_PHONE` | Application | Did client provide work phone (1=YES, 0=NO) |
| `FLAG_WORK_PHONE` | Application | Did client provide home phone (1=YES, 0=NO) |
| `FLAG_CONT_MOBILE` | Application | Was mobile phone reachable (1=YES, 0=NO) |
| `FLAG_PHONE` | Application | Did client provide home phone (1=YES, 0=NO) |
| `FLAG_EMAIL` | Application | Did client provide email (1=YES, 0=NO) |
| `OCCUPATION_TYPE` | Application | What kind of occupation does the client have |
| `CNT_FAM_MEMBERS` | Application | How many family members does client have |
| `REGION_RATING_CLIENT` | Application | Our rating of the region where client lives (1,2,3) |
| `REGION_RATING_CLIENT_W_CITY` | Application | Our rating of the region where client lives with taking city into account (1,2,3) |
| `WEEKDAY_APPR_PROCESS_START` | Application | On which day of the week did the client apply for the loan |
| `HOUR_APPR_PROCESS_START` | Application | Approximately at what hour did the client apply for the loan |
| `REG_REGION_NOT_LIVE_REGION` | Application | Flag if client's permanent address does not match contact address (1=different, 0=same, at region level) |
| `REG_REGION_NOT_WORK_REGION` | Application | Flag if client's permanent address does not match work address (1=different, 0=same, at region level) |
| `LIVE_REGION_NOT_WORK_REGION` | Application | Flag if client's contact address does not match work address (1=different, 0=same, at region level) |
| `REG_CITY_NOT_LIVE_CITY` | Application | Flag if client's permanent address does not match contact address (1=different, 0=same, at city level) |
| `REG_CITY_NOT_WORK_CITY` | Application | Flag if client's permanent address does not match work address (1=different, 0=same, at city level) |
| `LIVE_CITY_NOT_WORK_CITY` | Application | Flag if client's contact address does not match work address (1=different, 0=same, at city level) |
| `ORGANIZATION_TYPE` | Application | Type of organization where client works |
| `EXT_SOURCE_1` | Application | Normalized score from external data source |
| `EXT_SOURCE_2` | Application | Normalized score from external data source |
| `EXT_SOURCE_3` | Application | Normalized score from external data source |
| `APARTMENTS_AVG` | Application | Normalized information about building where the client lives, What is average (_AVG suffix), modus (_MODE suffix), median (_MEDI suffix) apartment size, common area, living area, age of building, number of elevators, number of entrances, state of the building, number of floor |
| `BASEMENTAREA_AVG` | Application | Normalized information about building where the client lives, What is average (_AVG suffix), modus (_MODE suffix), median (_MEDI suffix) apartment size, common area, living area, age of building, number of elevators, number of entrances, state of the building, number of floor |
| `YEARS_BEGINEXPLUATATION_AVG` | Application | Normalized information about building where the client lives, What is average (_AVG suffix), modus (_MODE suffix), median (_MEDI suffix) apartment size, common area, living area, age of building, number of elevators, number of entrances, state of the building, number of floor |
| `YEARS_BUILD_AVG` | Application | Normalized information about building where the client lives, What is average (_AVG suffix), modus (_MODE suffix), median (_MEDI suffix) apartment size, common area, living area, age of building, number of elevators, number of entrances, state of the building, number of floor |
| `COMMONAREA_AVG` | Application | Normalized information about building where the client lives, What is average (_AVG suffix), modus (_MODE suffix), median (_MEDI suffix) apartment size, common area, living area, age of building, number of elevators, number of entrances, state of the building, number of floor |
| `ELEVATORS_AVG` | Application | Normalized information about building where the client lives, What is average (_AVG suffix), modus (_MODE suffix), median (_MEDI suffix) apartment size, common area, living area, age of building, number of elevators, number of entrances, state of the building, number of floor |
| `ENTRANCES_AVG` | Application | Normalized information about building where the client lives, What is average (_AVG suffix), modus (_MODE suffix), median (_MEDI suffix) apartment size, common area, living area, age of building, number of elevators, number of entrances, state of the building, number of floor |
| `FLOORSMAX_AVG` | Application | Normalized information about building where the client lives, What is average (_AVG suffix), modus (_MODE suffix), median (_MEDI suffix) apartment size, common area, living area, age of building, number of elevators, number of entrances, state of the building, number of floor |
| `FLOORSMIN_AVG` | Application | Normalized information about building where the client lives, What is average (_AVG suffix), modus (_MODE suffix), median (_MEDI suffix) apartment size, common area, living area, age of building, number of elevators, number of entrances, state of the building, number of floor |
| `LANDAREA_AVG` | Application | Normalized information about building where the client lives, What is average (_AVG suffix), modus (_MODE suffix), median (_MEDI suffix) apartment size, common area, living area, age of building, number of elevators, number of entrances, state of the building, number of floor |
| `LIVINGAPARTMENTS_AVG` | Application | Normalized information about building where the client lives, What is average (_AVG suffix), modus (_MODE suffix), median (_MEDI suffix) apartment size, common area, living area, age of building, number of elevators, number of entrances, state of the building, number of floor |
| `LIVINGAREA_AVG` | Application | Normalized information about building where the client lives, What is average (_AVG suffix), modus (_MODE suffix), median (_MEDI suffix) apartment size, common area, living area, age of building, number of elevators, number of entrances, state of the building, number of floor |
| `NONLIVINGAPARTMENTS_AVG` | Application | Normalized information about building where the client lives, What is average (_AVG suffix), modus (_MODE suffix), median (_MEDI suffix) apartment size, common area, living area, age of building, number of elevators, number of entrances, state of the building, number of floor |
| `NONLIVINGAREA_AVG` | Application | Normalized information about building where the client lives, What is average (_AVG suffix), modus (_MODE suffix), median (_MEDI suffix) apartment size, common area, living area, age of building, number of elevators, number of entrances, state of the building, number of floor |
| `APARTMENTS_MODE` | Application | Normalized information about building where the client lives, What is average (_AVG suffix), modus (_MODE suffix), median (_MEDI suffix) apartment size, common area, living area, age of building, number of elevators, number of entrances, state of the building, number of floor |
| `BASEMENTAREA_MODE` | Application | Normalized information about building where the client lives, What is average (_AVG suffix), modus (_MODE suffix), median (_MEDI suffix) apartment size, common area, living area, age of building, number of elevators, number of entrances, state of the building, number of floor |
| `YEARS_BEGINEXPLUATATION_MODE` | Application | Normalized information about building where the client lives, What is average (_AVG suffix), modus (_MODE suffix), median (_MEDI suffix) apartment size, common area, living area, age of building, number of elevators, number of entrances, state of the building, number of floor |
| `YEARS_BUILD_MODE` | Application | Normalized information about building where the client lives, What is average (_AVG suffix), modus (_MODE suffix), median (_MEDI suffix) apartment size, common area, living area, age of building, number of elevators, number of entrances, state of the building, number of floor |
| `COMMONAREA_MODE` | Application | Normalized information about building where the client lives, What is average (_AVG suffix), modus (_MODE suffix), median (_MEDI suffix) apartment size, common area, living area, age of building, number of elevators, number of entrances, state of the building, number of floor |
| `ELEVATORS_MODE` | Application | Normalized information about building where the client lives, What is average (_AVG suffix), modus (_MODE suffix), median (_MEDI suffix) apartment size, common area, living area, age of building, number of elevators, number of entrances, state of the building, number of floor |
| `ENTRANCES_MODE` | Application | Normalized information about building where the client lives, What is average (_AVG suffix), modus (_MODE suffix), median (_MEDI suffix) apartment size, common area, living area, age of building, number of elevators, number of entrances, state of the building, number of floor |
| `FLOORSMAX_MODE` | Application | Normalized information about building where the client lives, What is average (_AVG suffix), modus (_MODE suffix), median (_MEDI suffix) apartment size, common area, living area, age of building, number of elevators, number of entrances, state of the building, number of floor |
| `FLOORSMIN_MODE` | Application | Normalized information about building where the client lives, What is average (_AVG suffix), modus (_MODE suffix), median (_MEDI suffix) apartment size, common area, living area, age of building, number of elevators, number of entrances, state of the building, number of floor |
| `LANDAREA_MODE` | Application | Normalized information about building where the client lives, What is average (_AVG suffix), modus (_MODE suffix), median (_MEDI suffix) apartment size, common area, living area, age of building, number of elevators, number of entrances, state of the building, number of floor |
| `LIVINGAPARTMENTS_MODE` | Application | Normalized information about building where the client lives, What is average (_AVG suffix), modus (_MODE suffix), median (_MEDI suffix) apartment size, common area, living area, age of building, number of elevators, number of entrances, state of the building, number of floor |
| `LIVINGAREA_MODE` | Application | Normalized information about building where the client lives, What is average (_AVG suffix), modus (_MODE suffix), median (_MEDI suffix) apartment size, common area, living area, age of building, number of elevators, number of entrances, state of the building, number of floor |
| `NONLIVINGAPARTMENTS_MODE` | Application | Normalized information about building where the client lives, What is average (_AVG suffix), modus (_MODE suffix), median (_MEDI suffix) apartment size, common area, living area, age of building, number of elevators, number of entrances, state of the building, number of floor |
| `NONLIVINGAREA_MODE` | Application | Normalized information about building where the client lives, What is average (_AVG suffix), modus (_MODE suffix), median (_MEDI suffix) apartment size, common area, living area, age of building, number of elevators, number of entrances, state of the building, number of floor |
| `APARTMENTS_MEDI` | Application | Normalized information about building where the client lives, What is average (_AVG suffix), modus (_MODE suffix), median (_MEDI suffix) apartment size, common area, living area, age of building, number of elevators, number of entrances, state of the building, number of floor |
| `BASEMENTAREA_MEDI` | Application | Normalized information about building where the client lives, What is average (_AVG suffix), modus (_MODE suffix), median (_MEDI suffix) apartment size, common area, living area, age of building, number of elevators, number of entrances, state of the building, number of floor |
| `YEARS_BEGINEXPLUATATION_MEDI` | Application | Normalized information about building where the client lives, What is average (_AVG suffix), modus (_MODE suffix), median (_MEDI suffix) apartment size, common area, living area, age of building, number of elevators, number of entrances, state of the building, number of floor |
| `YEARS_BUILD_MEDI` | Application | Normalized information about building where the client lives, What is average (_AVG suffix), modus (_MODE suffix), median (_MEDI suffix) apartment size, common area, living area, age of building, number of elevators, number of entrances, state of the building, number of floor |
| `COMMONAREA_MEDI` | Application | Normalized information about building where the client lives, What is average (_AVG suffix), modus (_MODE suffix), median (_MEDI suffix) apartment size, common area, living area, age of building, number of elevators, number of entrances, state of the building, number of floor |
| `ELEVATORS_MEDI` | Application | Normalized information about building where the client lives, What is average (_AVG suffix), modus (_MODE suffix), median (_MEDI suffix) apartment size, common area, living area, age of building, number of elevators, number of entrances, state of the building, number of floor |
| `ENTRANCES_MEDI` | Application | Normalized information about building where the client lives, What is average (_AVG suffix), modus (_MODE suffix), median (_MEDI suffix) apartment size, common area, living area, age of building, number of elevators, number of entrances, state of the building, number of floor |
| `FLOORSMAX_MEDI` | Application | Normalized information about building where the client lives, What is average (_AVG suffix), modus (_MODE suffix), median (_MEDI suffix) apartment size, common area, living area, age of building, number of elevators, number of entrances, state of the building, number of floor |
| `FLOORSMIN_MEDI` | Application | Normalized information about building where the client lives, What is average (_AVG suffix), modus (_MODE suffix), median (_MEDI suffix) apartment size, common area, living area, age of building, number of elevators, number of entrances, state of the building, number of floor |
| `LANDAREA_MEDI` | Application | Normalized information about building where the client lives, What is average (_AVG suffix), modus (_MODE suffix), median (_MEDI suffix) apartment size, common area, living area, age of building, number of elevators, number of entrances, state of the building, number of floor |
| `LIVINGAPARTMENTS_MEDI` | Application | Normalized information about building where the client lives, What is average (_AVG suffix), modus (_MODE suffix), median (_MEDI suffix) apartment size, common area, living area, age of building, number of elevators, number of entrances, state of the building, number of floor |
| `LIVINGAREA_MEDI` | Application | Normalized information about building where the client lives, What is average (_AVG suffix), modus (_MODE suffix), median (_MEDI suffix) apartment size, common area, living area, age of building, number of elevators, number of entrances, state of the building, number of floor |
| `NONLIVINGAPARTMENTS_MEDI` | Application | Normalized information about building where the client lives, What is average (_AVG suffix), modus (_MODE suffix), median (_MEDI suffix) apartment size, common area, living area, age of building, number of elevators, number of entrances, state of the building, number of floor |
| `NONLIVINGAREA_MEDI` | Application | Normalized information about building where the client lives, What is average (_AVG suffix), modus (_MODE suffix), median (_MEDI suffix) apartment size, common area, living area, age of building, number of elevators, number of entrances, state of the building, number of floor |
| `FONDKAPREMONT_MODE` | Application | Normalized information about building where the client lives, What is average (_AVG suffix), modus (_MODE suffix), median (_MEDI suffix) apartment size, common area, living area, age of building, number of elevators, number of entrances, state of the building, number of floor |
| `HOUSETYPE_MODE` | Application | Normalized information about building where the client lives, What is average (_AVG suffix), modus (_MODE suffix), median (_MEDI suffix) apartment size, common area, living area, age of building, number of elevators, number of entrances, state of the building, number of floor |
| `TOTALAREA_MODE` | Application | Normalized information about building where the client lives, What is average (_AVG suffix), modus (_MODE suffix), median (_MEDI suffix) apartment size, common area, living area, age of building, number of elevators, number of entrances, state of the building, number of floor |
| `WALLSMATERIAL_MODE` | Application | Normalized information about building where the client lives, What is average (_AVG suffix), modus (_MODE suffix), median (_MEDI suffix) apartment size, common area, living area, age of building, number of elevators, number of entrances, state of the building, number of floor |
| `EMERGENCYSTATE_MODE` | Application | Normalized information about building where the client lives, What is average (_AVG suffix), modus (_MODE suffix), median (_MEDI suffix) apartment size, common area, living area, age of building, number of elevators, number of entrances, state of the building, number of floor |
| `DAYS_LAST_PHONE_CHANGE` | Application | How many days before application did client change phone |
| `FLAG_DOCUMENT_2` | Application | Did client provide document 2 |
| `FLAG_DOCUMENT_3` | Application | Did client provide document 3 |
| `FLAG_DOCUMENT_4` | Application | Did client provide document 4 |
| `FLAG_DOCUMENT_5` | Application | Did client provide document 5 |
| `FLAG_DOCUMENT_6` | Application | Did client provide document 6 |
| `FLAG_DOCUMENT_7` | Application | Did client provide document 7 |
| `FLAG_DOCUMENT_8` | Application | Did client provide document 8 |
| `FLAG_DOCUMENT_9` | Application | Did client provide document 9 |
| `FLAG_DOCUMENT_10` | Application | Did client provide document 10 |
| `FLAG_DOCUMENT_11` | Application | Did client provide document 11 |
| `FLAG_DOCUMENT_12` | Application | Did client provide document 12 |
| `FLAG_DOCUMENT_13` | Application | Did client provide document 13 |
| `FLAG_DOCUMENT_14` | Application | Did client provide document 14 |
| `FLAG_DOCUMENT_15` | Application | Did client provide document 15 |
| `FLAG_DOCUMENT_16` | Application | Did client provide document 16 |
| `FLAG_DOCUMENT_17` | Application | Did client provide document 17 |
| `FLAG_DOCUMENT_18` | Application | Did client provide document 18 |
| `FLAG_DOCUMENT_19` | Application | Did client provide document 19 |
| `FLAG_DOCUMENT_20` | Application | Did client provide document 20 |
| `FLAG_DOCUMENT_21` | Application | Did client provide document 21 |
| `AMT_REQ_CREDIT_BUREAU_HOUR` | Application | Number of enquiries to Credit Bureau about the client one hour before application |
| `AMT_REQ_CREDIT_BUREAU_DAY` | Application | Number of enquiries to Credit Bureau about the client one day before application (excluding one hour before application) |
| `AMT_REQ_CREDIT_BUREAU_WEEK` | Application | Number of enquiries to Credit Bureau about the client one week before application (excluding one day before application) |
| `AMT_REQ_CREDIT_BUREAU_MON` | Application | Number of enquiries to Credit Bureau about the client one month before application (excluding one week before application) |
| `AMT_REQ_CREDIT_BUREAU_QRT` | Application | Number of enquiries to Credit Bureau about the client 3 month before application (excluding one month before application) |
| `AMT_REQ_CREDIT_BUREAU_YEAR` | Application | Number of enquiries to Credit Bureau about the client one day year (excluding last 3 months before application) |
| `DAYS_EMPLOYED_ANOMALY` | Engineered (application) | 1 if DAYS_EMPLOYED held the 365243 placeholder (set to missing), else 0 |
| `AGE_YEARS` | Engineered (application) | Age in years: -DAYS_BIRTH / 365.25 |
| `CREDIT_INCOME_RATIO` | Engineered (application) | AMT_CREDIT / AMT_INCOME_TOTAL |
| `ANNUITY_INCOME_RATIO` | Engineered (application) | AMT_ANNUITY / AMT_INCOME_TOTAL |
| `CREDIT_ANNUITY_RATIO` | Engineered (application) | AMT_CREDIT / AMT_ANNUITY (implied number of annuity payments) |
| `EMPLOYED_AGE_SHARE` | Engineered (application) | DAYS_EMPLOYED / DAYS_BIRTH (share of life in current job) |
| `INCOME_PER_FAMILY_MEMBER` | Engineered (application) | AMT_INCOME_TOTAL / CNT_FAM_MEMBERS |
| `BUREAU_CREDIT_COUNT` | History table | Number of credits on the bureau record |
| `BUREAU_ACTIVE_COUNT` | History table | Bureau credits currently active |
| `BUREAU_OVERDUE_COUNT` | History table | Bureau credits currently overdue |
| `BUREAU_MAX_DAYS_OVERDUE` | History table | Longest overdue period on the bureau record (days) |
| `BUREAU_DEBT_SUM` | History table | Total current debt across bureau credits |
| `BUREAU_CREDIT_SUM` | History table | Total credit amount across bureau credits |
| `BUREAU_HISTORY_DAYS` | History table | Days since the oldest bureau credit was taken out |
| `BUREAU_DEBT_TO_CREDIT` | History table | Debt / credit amount across bureau credits |
| `PREV_APP_COUNT` | History table | Number of earlier Home Credit applications |
| `PREV_APPROVED_COUNT` | History table | Earlier applications approved |
| `PREV_REFUSED_COUNT` | History table | Earlier applications refused |
| `PREV_DAYS_SINCE_LAST` | History table | Days since the most recent earlier decision |
| `PREV_REFUSED_SHARE` | History table | Refused / all earlier applications (missing if none) |
| `INST_PAID_COUNT` | History table | Number of earlier instalments with a recorded payment |
| `INST_LATE_SHARE` | History table | Share of paid instalments paid after the due date (missing if none) |
| `INST_MAX_DAYS_LATE` | History table | Longest lateness of any earlier paid instalment (days) |
| `INST_UNDERPAID_SHARE` | History table | Share of paid instalments where the payment was below the amount due |
| `INST_PAID_TO_DUE` | History table | Total paid / total due over earlier instalments (missing if nothing was due) |
| `INST_UNPAID_COUNT` | History table | Earlier instalments with no recorded payment |

Excluded on purpose: `SK_ID_CURR` (identifier, D08); `TARGET` (label); the four social-circle columns (D24); `DAYS_FIRST_DRAWING`, `DAYS_LAST_DUE`, `DAYS_TERMINATION` (placeholder values and possible post-decision timing, D17).

Target: `TARGET` = 1 if the client had a late payment of more than X days on at least one of the first Y instalments (X and Y are not disclosed by Home Credit), 0 otherwise. It measures early repayment difficulty, not lifetime default.
