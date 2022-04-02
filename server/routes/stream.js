import express from "express";

import { getFrame } from "../controllers/stream.js";

const router = express.Router();

router.get("/", getFrame);

export default router;
