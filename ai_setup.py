from openai import OpenAI

def ai_question(question):
  client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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",
  )
  # AlgoSensei
  completion = client.chat.completions.create(
    extra_headers={
      "HTTP-Referer": "<YOUR_SITE_URL>",  # Optional. Site URL for rankings on openrouter.ai.
      "X-Title": "<YOUR_SITE_NAME>",  # Optional. Site title for rankings on openrouter.ai.
    },
    model="qwen/qwen-plus",
    messages=[
      {
        "role": "user",
        "content":"представь что ты опытный программист и помоги мне решить эту задачу: " + question
      }
    ]
  )
  return completion.choices[0].message.content