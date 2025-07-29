import { Bot, webhookCallback } from "grammy";
import { getPostFromTopic } from "./openai.js";
import { initDB, canGenerate, increaseCount } from "./db.js";
import express from "express";

const bot = new Bot("8212092084:AAFArafCif5HOkXjO95ig4O8mLA2BNvEvfA");
const app = express();

app.use(express.json());

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
    await ctx.reply(post);
  } catch (error) {
    console.error("Ошибка в команде post:", error);
    await ctx.reply("Произошла ошибка при генерации поста. Попробуй еще раз.");
  }
});

// Webhook endpoint
app.post("/", webhookCallback(bot, "express"));

// Health check endpoint
app.get("/", (req, res) => {
  res.send("Bot is running!");
});

// Инициализация
(async () => {
  try {
    await initDB();
    console.log("База данных инициализирована");
    
    const port = process.env.PORT || 3000;
    app.listen(port, () => {
      console.log(`Сервер запущен на порту ${port}`);
    });
  } catch (error) {
    console.error("Ошибка запуска:", error);
  }
})();
