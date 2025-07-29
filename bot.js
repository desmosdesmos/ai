import { Bot } from "grammy";
import { OpenAI } from "openai";

const bot = new Bot("8212092084:AAFArafCif5HOkXjO95ig4O8mLA2BNvEvfA");

const openai = new OpenAI({ 
  apiKey: "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"
});

async function getPostFromTopic(topic) {
  try {
    console.log("Генерирую пост для темы:", topic);
    
    const res = await openai.chat.completions.create({
      model: "gpt-3.5-turbo",
      messages: [{ 
        role: "user", 
        content: `Напиши Telegram-пост по теме: "${topic}". Структура: 1. Заголовок с emoji 2. Затравка в первом абзаце 3. Полезный или провокационный контент 4. Завершение и Call to Action. Оформи для Telegram: отступы, emoji, короткие предложения.`
      }],
      temperature: 0.9,
      max_tokens: 300
    });
    
    const content = res.choices[0]?.message?.content;
    console.log("Получен ответ от OpenAI:", content ? content.substring(0, 100) + "..." : "пустой ответ");
    
    return content || "Ошибка генерации: пустой ответ";
  } catch (error) {
    console.error("Ошибка OpenAI:", error);
    return "Ошибка генерации поста: " + error.message;
  }
}

// Добавляем обработчик ошибок
bot.catch((err) => {
  console.error("Ошибка в боте:", err);
});

bot.command("start", (ctx) => {
  console.log("Получена команда /start");
  return ctx.reply("Привет! Я — AI-контент-бот. Напиши /post и тему, я сгенерирую пост.");
});

bot.command("post", async (ctx) => {
  try {
    console.log("Получена команда /post");
    
    const text = ctx.message?.text?.split(" ").slice(1).join(" ");
    console.log("Тема:", text);

    if (!text) {
      console.log("Тема не указана");
      return ctx.reply("Напиши тему: /post Твоя тема");
    }

    console.log("Отправляю сообщение о генерации...");
    await ctx.reply("Генерирую пост...");

    console.log("Вызываю функцию генерации...");
    const post = await getPostFromTopic(text);
    
    console.log("Отправляю сгенерированный пост...");
    await ctx.reply(post);
    
    console.log("Пост успешно отправлен");
  } catch (error) {
    console.error("Ошибка в команде post:", error);
    await ctx.reply("Произошла ошибка при генерации поста. Попробуй еще раз.");
  }
});

console.log("Запускаю бота...");
bot.start({
  onStart: () => {
    console.log("Бот успешно запущен!");
  },
  onError: (err) => {
    console.error("Ошибка при запуске бота:", err);
  }
});
