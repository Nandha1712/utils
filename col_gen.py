# Contents will be used in file_gen.sh
max_count = 297
start_idx = 197
col_names = ""
col_content = ""
ll = []
for c in range(start_idx, max_count):
    col_names = col_names + f",col_{c}"
    col_content = col_content + f",content_row-$i-col-{c}"
    ll.append(c)

print(len(ll))
print(col_names)
print(col_content)

