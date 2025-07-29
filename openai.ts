import { OpenAI } from "openai";
import { POST_PROMPT } from "./prompts/postPrompt.js";

const openai = new OpenAI({ 
  apiKey: "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"
});

export async function getPostFromTopic(topic: string): Promise<string> {
  try {
    const prompt = POST_PROMPT.replace("{topic}", topic);
    console.log("Отправляю запрос к OpenAI с темой:", topic);
    
    const res = await openai.chat.completions.create({
      model: "gpt-3.5-turbo",
      messages: [{ role: "user", content: prompt }],
      temperature: 0.9,
      max_tokens: 500
    });
    
    const content = res.choices[0]?.message?.content;
    console.log("Получен ответ от OpenAI:", content);
    
    return content || "Ошибка генерации: пустой ответ от OpenAI";
  } catch (error) {
    console.error("Ошибка при генерации поста:", error);
    return `Ошибка генерации: ${error.message}`;
  }
}
