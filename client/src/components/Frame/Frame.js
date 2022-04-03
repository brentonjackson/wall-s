import React, { useState, useEffect } from "react";
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
