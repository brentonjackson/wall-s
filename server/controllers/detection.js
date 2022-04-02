import express from "express";
import fs from "fs";
import dotenv from "dotenv";

if (process.env.NODE_ENV !== "production") {
  dotenv.config();
}

const router = express.Router();

export const getDetection = async (req, res) => {
  try {
    // get frame from file
    let filename = "currentFrame.jpg";
    // let price = fs.readFileSync(process.cwd() + "/" + filename).toString();

    res.json({
      data: filename,
    });
  } catch (error) {
    res.status(404).json({ message: error.message });
    console.log("error getting file");
  }
};

export default router;
