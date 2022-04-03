import express from "express";

import { postSms } from "../controllers/sms.js";

const router = express.Router();

router.post("/", postSms);

export default router;
