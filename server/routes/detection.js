import express from "express";

import { getDetection } from "../controllers/detection.js";

const router = express.Router();

router.get("/", getDetection);

export default router;
