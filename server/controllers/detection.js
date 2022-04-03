import express from "express";
import fs from "fs";

const router = express.Router();

export const getDetection = async (req, res) => {
  try {
    // get frame from file
    let filename = "isThereTrash.txt";
    let trash = fs.readFileSync(process.cwd() + "/" + filename).toString();
    console.log(trash);
    res.json({
      data: trash,
    });
    console.log("got the right file");
  } catch (error) {
    res.status(404).json({ message: error.message });
    console.log("error getting file");
  }
};

export default router;
