import json
import uuid

questions = []
options = []
assets = []

subject_id = "asnc-qbank"

topics = []

for file_num in range(1, 5):

    with open(f"{file_num}.json", "r", encoding="utf-8") as f:
        old_data = json.load(f)

    topic_id = str(uuid.uuid4())

    topics.append({
        "id": topic_id,
        "subjectId": subject_id,
        "title": f"Subject-{file_num}",
        "source": {
            "provider": "hippo",
            "id": topic_id
        }
    })

    for item in old_data:
        question_id = f"hippo:question:{uuid.uuid4()}"

        option_ids = []

        for index, option in enumerate(item["options"]):
            option_id = f"{question_id}:option:{index}"
            option_ids.append(option_id)

            options.append({
                "id": option_id,
                "questionId": question_id,
                "body": option,
                "explanation": "",
                "isCorrect": False,
                "explanationAssetIds": [],
                "source": {
                    "provider": "hippo",
                    "questionId": question_id.replace("hippo:question:", ""),
                    "optionIndex": index
                }
            })

        asset_ids = []

        if item.get("asset"):
            asset_id = f"hippo:asset:{uuid.uuid4()}"
            asset_ids.append(asset_id)

            assets.append({
                "id": asset_id,
                "type": "image",
                "role": "question-image",
                "title": None,
                "mimeType": None,
                "source": {
                    "provider": "hippo",
                    "id": asset_id.replace("hippo:asset:", ""),
                    "url": ""
                },
                "localPath": item["asset"]
            })

        questions.append({
            "id": question_id,
            "subjectIds": [subject_id],
            "topicIds": [topic_id],
            "body": item["question"],
            "optionIds": option_ids,
            "assetIds": asset_ids,
            "tags": [
                {
                    "id": topic_id,
                    "title": ""
                }
            ],
            "source": {
                "provider": "hippo",
                "id": question_id.replace("hippo:question:", ""),
                "quizQuestionId": str(uuid.uuid4()),
                "quizId": str(uuid.uuid4())
            }
        })

new_data = {
    "content": {
        "subjects": [
            {
                "id": subject_id,
                "title": "asnc QBank",
                "provider": "hippo"
            }
        ],
        "topics": topics,
        "questions": questions,
        "options": options,
        "assets": assets,
        "boardReview": []
    }
}

with open("new.json", "w", encoding="utf-8") as f:
    json.dump(new_data, f, indent=4, ensure_ascii=False)