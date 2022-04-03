import express from "express";
import fs from "fs";

const router = express.Router();

export const getFrame = async (req, res) => {
  try {
    // get frame from file
    let filePath = "../client/public/images/";
    let filename = "currentFrame.jpg";
    try {
      if (fs.existsSync(filePath + filename)) {
        //file exists
        res.json({
          data: filename,
          key: Date.now(),
        });
      } else {
        res.json({ data: "" });
        console.log("hit no file");
      }
    } catch (err) {
      res.status(404).json({ message: error.message });
    }
  } catch (error) {
    res.status(404).json({ message: error.message });
    console.log("error getting file");
  }
};

export default router;
