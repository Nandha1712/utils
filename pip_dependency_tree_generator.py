"""
pip install pipdeptree
pipdeptree -fl

Install pipdeptree to get dependency tree of virtual env.
Then use the following script to convert that text into xml format
"""

result_file_name = "az_jul_6_2023_result.xml"
file_path = "dummy.txt"
print("Processing file: {}".format(file_path))

tag_names_list = []
tag_space_lengths = []


def get_empty_spaces(req_count):
    _empty_str = ""
    for _i in range(0, (req_count + 1)):
        _empty_str = " {}".format(_empty_str)
    return _empty_str


with open(result_file_name, "w") as result_file_ctr:
    result_file_ctr.write("<root>\n")
    prev_space = -1

    with open(file_path) as f:
        for line in f:
            if len(tag_space_lengths) > 0:
                prev_space = tag_space_lengths[-1]

            if "-e /qualdo" in line:
                continue

            edt_text = "# Editable install with no version control ("
            if edt_text in line:
                line = line.replace(edt_text, "")
                line = line.replace(")", "")

            split_arr = line.split(" ")

            arr_len = len(split_arr)
            tag_data = split_arr[-1]
            tag_arr = tag_data.split("==")
            tag_name = tag_arr[0].strip()
            tag_ver = ""
            curr_space_count = arr_len - 1
            if curr_space_count <= prev_space and len(tag_space_lengths) > 0:
                # Write pending tags
                i = len(tag_names_list) - 1
                while i >= 0:
                    prev_tag = tag_names_list[i]
                    prev_space = tag_space_lengths[i]

                    if curr_space_count > prev_space:
                        break

                    tag_space_lengths.pop()
                    tag_names_list.pop()

                    empty_str = get_empty_spaces(prev_space)
                    result_file_ctr.write('{}</{}>\n'.format(empty_str, prev_tag))
                    i = i - 1

            tag_space_lengths.append(curr_space_count)
            tag_names_list.append(tag_name)

            if len(tag_arr) > 1:
                tag_ver = tag_arr[1].strip()

            empty_str = get_empty_spaces(curr_space_count)
            result_file_ctr.write('{}<{} version="{}">\n'.format(empty_str, tag_name, tag_ver))

    # Write pending tags
    i = len(tag_names_list) - 1
    while i >= 0:
        prev_tag = tag_names_list[i]
        prev_space = tag_space_lengths[i]
        empty_str = get_empty_spaces(prev_space)
        result_file_ctr.write('{}</{}>\n'.format(empty_str, prev_tag))
        i = i - 1

    result_file_ctr.write("</root>\n")
