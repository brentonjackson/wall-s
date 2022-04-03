import React, { useState, useEffect } from "react";
import { fetchTrash } from "../../api/fetchTrash";

const DetectionSignal = () => {
  const [isDisabled, setIsDisabled] = useState(true);
  // const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    const intervalId = setInterval(() => {
      //update frame every 2 seconds
      fetchTrash()
        .then((obj) => {
          let newData = obj.data;
          setIsDisabled((prevState) => newData.data);
          return newData;
        })
        .then((newData) => {
          console.log(newData.data);
          setIsDisabled((prevState) => newData.data);
        })
        .catch((err) => {
          console.log(err);
          setIsDisabled((prevState) => prevState);
        });
    }, 5000);

    return () => {
      clearInterval(intervalId); //This is important
    };
  }, [useState]);

  return isDisabled === "false" ? (
    <button className="trash-detection-button" variant="outlined" disabled>
      NO TRASH DETECTED
    </button>
  ) : (
    <button className="trash-detection-button detected" variant="outlined">
      TRASH DETECTED
    </button>
  );
};

export default DetectionSignal;
