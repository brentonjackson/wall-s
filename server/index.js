import express from "express";
import bodyParser from "body-parser";
import cors from "cors";
import streamRoutes from "./routes/stream.js";
import detectionRoutes from "./routes/detection.js";

const app = express();

app.use(bodyParser.urlencoded({ extended: false }));
app.use(express.json({ limit: "30mb", extended: true }));
app.use(express.urlencoded({ limit: "30mb", extended: true }));
app.use(cors());

app.use("/stream", streamRoutes);
app.use("/detection", detectionRoutes);
const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
