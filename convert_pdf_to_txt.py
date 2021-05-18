import pdfplumber
import elasticsearch

text_pages = []

# it is reading one file which you want to dump
with open("./pdf/c.a._26_2015l.pdf", "rb") as file:
    pdf = pdfplumber.open(file)
    for page in pdf.pages:
        # extracting the text
        text = page.extract_text()
        # storing the one by one page data into text_pages list
        text_pages.append(text)

try:
    # please write the file name which you want to put into elastic search
    filename = "c.a._26_2015l"

    # elastic search object
    es = elasticsearch.Elasticsearch(["localhost:9200"])

    # it is iterating the all the pages
    for page_num in range(0, len(text_pages)):

        # it will fetch the text of page
        page = text_pages[page_num]
        line_num = 0

        # split the text into line
        for line in page.split("\n"):

            # removing the space from front and right
            line = line.strip()

            # checking the file contain the text
            if len(line) > 0:

                # line number increment
                line_num += 1
                actual_page_num = page_num + 1
                id = filename + "_" + str(actual_page_num) + "_" + str(
                    line_num)
                # storing the data into the elastic search
                es.index(index="documents",
                         doc_type="_doc",
                         id=id,
                         body={
                             "page_num": actual_page_num,
                             "line_num": line_num,
                             "text": line,
                             "file_name": filename
                         })
                print("{} with {} {}".format(line, actual_page_num, line_num))

except Exception as e:
    print(e)