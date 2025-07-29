import { Bot } from "grammy";
import { getPostFromTopic } from "./openai.js";
import { initDB, canGenerate, increaseCount } from "./db.js";

const bot = new Bot("8212092084:AAFArafCif5HOkXjO95ig4O8mLA2BNvEvfA");

// Добавляем обработчик ошибок
bot.catch((err) => {
  console.error("Ошибка в боте:", err);
  
  // Если это ошибка конфликта, просто логируем её
  if (err.error_code === 409) {
    console.log("Обнаружен конфликт с другим экземпляром бота. Перезапуск...");
    // Можно добавить логику перезапуска
  }
});

bot.command("start", (ctx) =>
  ctx.reply("Привет! Я — AI-контент-бот. Напиши /post и тему, я сгенерирую пост.")
);

bot.command("post", async (ctx) => {
  const userId = ctx.from?.id;
  const text = ctx.message?.text?.split(" ").slice(1).join(" ");

  if (!userId || !text) {
    return ctx.reply("Напиши тему: /post Твоя тема");
  }

  ctx.reply("Генерирую пост...");

  try {
    const post = await getPostFromTopic(text);
    console.log("Отправляю пост пользователю:", post);
    await ctx.reply(post);
  } catch (error) {
    console.error("Ошибка в команде post:", error);
    await ctx.reply("Произошла ошибка при генерации поста. Попробуй еще раз.");
  }
});

// Инициализация и запуск с обработкой ошибок
(async () => {
  try {
    await initDB();
    console.log("База данных инициализирована");
    
    // Добавляем обработку ошибок при запуске
    bot.start({
      onStart: () => {
        console.log("Бот успешно запущен");
      },
      onError: (err) => {
        console.error("Ошибка при запуске бота:", err);
        if (err.error_code === 409) {
          console.log("Попытка перезапуска через 5 секунд...");
          setTimeout(() => {
            bot.start();
          }, 5000);
        }
      }
    });
  } catch (error) {
    console.error("Ошибка запуска:", error);
  }
})();
