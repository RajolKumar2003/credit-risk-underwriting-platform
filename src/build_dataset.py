from src import config
from src.data import (
    assign_split,
    load_applications,
    load_bureau,
    load_installments,
    load_previous_applications,
)
from src.features import add_ratio_features
from src.history import (
    COUNT_COLUMNS,
    bureau_features,
    installment_features,
    previous_application_features,
)
from src.preprocessing import clean_applications


def build_modelling_table():
    applications = add_ratio_features(clean_applications(load_applications()))
    ids = applications[config.ID_COLUMN]

    history = [
        (load_bureau, bureau_features),
        (load_previous_applications, previous_application_features),
        (load_installments, installment_features),
    ]
    table = applications
    for load, build in history:
        records = load()
        records = records[records[config.ID_COLUMN].isin(ids)]
        table = table.merge(build(records), left_on=config.ID_COLUMN, right_index=True, how="left")

    table[COUNT_COLUMNS] = table[COUNT_COLUMNS].fillna(0)
    table["split"] = assign_split(table[config.TARGET])
    return table


if __name__ == "__main__":
    table = build_modelling_table()
    table.to_pickle(config.PROCESSED_DIR / "modelling_table.pkl")
    print(table.shape)
    print(table["split"].value_counts())
