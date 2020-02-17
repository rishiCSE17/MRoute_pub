def main(json_list):
    # print(f'received {len(json_list)} entries...')
    with open('./UI/sample.html', 'w') as f:
        f.write('')
    with open('./UI/part1.txt', 'r') as f1:
        for lines in f1:
            with open('./UI/sample.html', 'a') as f2:
                f2.write(lines)

    with open('./UI/sample.html', 'a') as f:
        for item in json_list:
            populate_html(item)

        with open('./UI/part4.txt', 'r') as f1:
            for lines in f1:
                with open('./UI/sample.html', 'a') as f2:
                    f2.write(lines)


def populate_html(item):
    with open('./UI/sample.html', 'a') as f2:
        f2.write(f'<h1> Route : {item["src"]} ---> {item["dst"]} </h1>')
    with open('./UI/part2.txt', 'r') as f1:
        for lines in f1:
            with open('./UI/sample.html', 'a') as f2:
                f2.write(lines)

    with open('./UI/sample.html', 'a') as f2:
        f2.write(item["tree"])
        f2.write('\n')

    with open('./UI/part3.txt', 'r') as f1:
        for lines in f1:
            with open('./UI/sample.html', 'a') as f2:
                f2.write(lines)
