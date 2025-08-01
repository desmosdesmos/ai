import { Bot } from "grammy";
import { OpenAI } from "openai";

const bot = new Bot(process.env.BOT_TOKEN);

const openai = new OpenAI({ 
  apiKey: process.env.OPENAI_API_KEY,
  organization: process.env.OPENAI_ORG,
  project: process.env.OPENAI_PROJECT,
});


async function getPostFromTopic(topic) {
  try {
    const res = await openai.chat.completions.create({
      model: "gpt-3.5-turbo",
      messages: [{ 
        role: "user", 
        content: `Напиши Telegram-пост по теме: "${topic}". Структура: 1. Заголовок с emoji 2. Затравка в первом абзаце 3. Полезный или провокационный контент 4. Завершение и Call to Action. Оформи для Telegram: отступы, emoji, короткие предложения.`
      }],
      temperature: 0.9,
      max_tokens: 300
    });
    
    return res.choices[0]?.message?.content || "Ошибка генерации";
  } catch (error) {
    console.error("Ошибка OpenAI:", error);
    return "Ошибка генерации поста";
  }
}

bot.command("start", (ctx) =>
  ctx.reply("Привет! Я — AI-контент-бот. Напиши /post и тему, я сгенерирую пост.")
);

bot.command("post", async (ctx) => {
  const text = ctx.message?.text?.split(" ").slice(1).join(" ");

  if (!text) {
    return ctx.reply("Напиши тему: /post Твоя тема");
  }

  ctx.reply("Генерирую пост...");

  try {
    const post = await getPostFromTopic(text);
    await ctx.reply(post);
  } catch (error) {
    console.error("Ошибка:", error);
    await ctx.reply("Ошибка генерации. Попробуй еще раз.");
  }
});

console.log("Запускаю бота...");
bot.start();
console.log("Бот запущен!");
