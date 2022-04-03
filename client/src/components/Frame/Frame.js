import React, { useState, useEffect } from "react";
<<<<<<< HEAD
import {
  Card,
  CardContent,
  Typography,
  CircularProgress,
} from "@material-ui/core/";
// import stockPhoto from "./stockPhoto.jpg";

=======
>>>>>>> 3bbd040b8954b27dd206f4c4b27efdbb67afb3dd
import { fetchFrame } from "../../api/fetchFrame";

const Frame = () => {
  const [frameSrc, setFrameSrc] = useState("currentFrame.jpg");
  const [imageKey, setImageKey] = useState(Date.now());
  const framePath = "/images/";

  useEffect(() => {
    const intervalId = setInterval(() => {
      // update frame every 2 seconds
      fetchFrame()
        .then((obj) => {
          let newData = obj.data;
          return newData;
        })
        .then((newData) => {
          setFrameSrc((prevState) => newData.data);
          setImageKey((prevState) => newData.key);
          // setIsLoading((prevState) => false);
        })
        .catch((err) => {
          console.log(err);
          setFrameSrc((prevState) => prevState);
        });
    }, 5000);
    return () => {
      clearInterval(intervalId); //This is important
    };
  }, [framePath]);

  return (
    <div className="frame-wrapper">
      <img
        key={imageKey}
        className="frame"
        src={framePath + frameSrc}
        alt="Raspberry Pi Camera Frame"
      />
    </div>
  );
};

export default Frame;
