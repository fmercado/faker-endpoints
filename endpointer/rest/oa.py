from openai import OpenAI

from django.conf import settings

def get_json(user_input):
    client = OpenAI(api_key=settings.OPENAI_APIKEY)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant and will give sample json file structure for the topic the user will be giving. Output needs to be a extrictly a  JSON file"},
            {"role": "user", "content": user_input}
        ]
    )

    return response.choices[0].message.content

