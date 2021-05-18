import elasticsearch
import json

es = elasticsearch.Elasticsearch()

query = "court passed"
numResults = 10

results = es.search(index="documents",
                    body={
                        "size": numResults,
                        "query": {
                            "match": {
                                "text": {
                                    "query": query,
                                }
                            }
                        }
                    })

print(json.dumps(results, sort_keys=False, indent=2, separators=(',', ': ')))
