"""
Compares requirement  txt and pip dep tree xml result
to find missing dependencies
"""
import xml.etree.ElementTree as ET

act_req_path = r"D:\Work\Codebase\qualdo\qualdo\core\console\requirement.txt"
tree = ET.parse(r'D:\Work\Codebase\qualdo\miscs\deptree_result.xml')
root = tree.getroot()


def flatten_child_elements(element):
    current_elements = []
    for subelem in element:
        tag_name = subelem.tag
        dep_version = subelem.attrib.get("version")
        fq_data = "{}=={}".format(tag_name, dep_version)
        current_elements.append({"fq_data": fq_data,
                                 "name": tag_name,
                                 "version": dep_version})
        child_list = flatten_child_elements(subelem)
        if len(child_list) > 0:
            current_elements.extend(child_list)

    return current_elements


existing_data = {}
with open(act_req_path) as f:
    for line in f:
        arrs = str(line).split("==")
        name = arrs[0]
        version = "NA"
        if len(arrs) > 1:
            version = arrs[1]

        existing_data[name] = {"fq_data": str(line),
                               "name": name,
                               "version": version}

res = flatten_child_elements(root)
missing_reqs = []
for curr in res:
    lib_name = curr.get("name")
    if existing_data.get(lib_name) is None and lib_name not in missing_reqs:
        missing_reqs.append(lib_name)

print(len(missing_reqs))
print(len(set(missing_reqs)))
print(set(missing_reqs))
