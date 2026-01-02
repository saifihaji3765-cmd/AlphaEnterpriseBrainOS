import express from "express";
import cors from "cors";
import jwt from "jsonwebtoken";

const app = express();

app.use(cors());
app.use(express.json());

const USERS = []; // temporary in-memory users

// ✅ HEALTH CHECK
app.get("/api/health", (req, res) => {
  res.json({
    status: "ok",
    message: "Rehman Future Guard Backend LIVE 🚀"
  });
});

// ✅ SIGNUP
app.post("/api/signup", (req, res) => {
  const { email, password } = req.body;

  if (!email || !password) {
    return res.status(400).json({ error: "Email & password required" });
  }

  const exists = USERS.find(u => u.email === email);
  if (exists) {
    return res.status(400).json({ error: "User already exists" });
  }

  USERS.push({ email, password });

  res.json({ message: "Signup successful" });
});

// ✅ LOGIN
app.post("/api/login", (req, res) => {
  const { email, password } = req.body;

  const user = USERS.find(
    u => u.email === email && u.password === password
  );

  if (!user) {
    return res.status(401).json({ error: "Invalid credentials" });
  }

  const token = jwt.sign(
    { email },
    process.env.JWT_SECRET,
    { expiresIn: "7d" }
  );

  res.json({ token });
});

// ✅ PROTECTED TEST API
app.get("/api/secure", (req, res) => {
  const auth = req.headers.authorization;
  if (!auth) {
    return res.status(401).json({ error: "No token" });
  }

  try {
    const decoded = jwt.verify(
      auth.split(" ")[1],
      process.env.JWT_SECRET
    );

    res.json({
      message: "Protected data access granted ✅",
      user: decoded.email
    });
  } catch {
    res.status(401).json({ error: "Invalid token" });
  }
});

export default app;
