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
