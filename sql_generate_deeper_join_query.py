TABLE_NAME = "SNOWFLAKE_SAMPLE_DATA.TPCH_SF1000.SUPPLIER"
JOIN_COL = "S_SUPPKEY"
REQUIRED_COLUMNS = ["S_SUPPKEY", "S_NAME", "S_ADDRESS", "S_NATIONKEY", "S_PHONE", "S_ACCTBAL", "S_COMMENT"]
number_of_joins = 1


def get_columns_with_prefixes(inp_cols, prefix):
    result = ""
    new_col_names = []
    index = 0

    for col in inp_cols:
        if index == 0:
            sep = ""
        else:
            sep = ","

        index = index + 1

        new_name = f"{prefix}{col}"
        result = result + sep + f"{prefix}.{col} as {new_name}"
        new_col_names.append(new_name)

    return result, new_col_names


res = ""
join_col_1 = JOIN_COL
table_1 = TABLE_NAME
curr_cols_1 = REQUIRED_COLUMNS

for i in range(number_of_joins):
    label_1 = f"t{i}1"
    label_2 = f"t{i}2"
    s1, col_names1 = get_columns_with_prefixes(curr_cols_1, label_1)
    s2, col_names2 = get_columns_with_prefixes(REQUIRED_COLUMNS, label_2)

    res = f"""SELECT {s1},{s2} FROM 
            ({table_1}) {label_1}
            INNER JOIN {TABLE_NAME} {label_2} ON {label_1}.{join_col_1} = {label_2}.{JOIN_COL}
        """

    curr_cols_1 = [*col_names1, *col_names2]
    join_col_1 = f"{label_1}{join_col_1}"
    table_1 = res

print(res)
