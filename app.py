import elasticsearch
import json
from application import create_app
from flask import request

app = create_app()


@app.route("/search")
def search():
    q = request.args.get("q")
    es = elasticsearch.Elasticsearch()

    numResults = 10

    results = es.search(index="documents",
                        body={
                            "size": numResults,
                            "query": {
                                "match": {
                                    "text": {
                                        "query": q,
                                    }
                                }
                            }
                        })
    final_result = []
    for hit in results['hits']['hits']:
        text = hit["_source"]["text"]
        line_num = hit["_source"]["line_num"]
        score = hit["_score"]
        page_num = hit["_source"]["page_num"]
        file_name = hit["_source"]["file_name"]
        temp = dict()
        temp["text"] = text
        temp["line_num"] = line_num
        temp["page_num"] = page_num
        temp["file_name"] = file_name
        temp["score"] = score
        final_result.append(temp)

    return json.dumps(final_result)


if __name__ == "__main__":
    app.run(debug=True)