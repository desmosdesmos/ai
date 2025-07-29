import sqlite3 from "sqlite3";
import { open } from "sqlite";

let db: any;

export async function initDB() {
  db = await open({ filename: "./content.db", driver: sqlite3.Database });
  await db.exec(`
    CREATE TABLE IF NOT EXISTS users (
      id INTEGER PRIMARY KEY,
      count INTEGER,
      date TEXT
    );
  `);
}

export async function canGenerate(id: number): Promise<boolean> {
  const today = new Date().toISOString().split("T")[0];
  const row = await db.get("SELECT * FROM users WHERE id = ?", id);

  if (!row) {
    await db.run("INSERT INTO users VALUES (?, ?, ?)", [id, 1, today]);
    return true;
  }

  if (row.date !== today) {
    await db.run("UPDATE users SET count = 1, date = ? WHERE id = ?", [today, id]);
    return true;
  }

  return row.count < 3;
}

export async function increaseCount(id: number) {
  await db.run("UPDATE users SET count = count + 1 WHERE id = ?", [id]);
}
