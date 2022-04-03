import React, { useState, useEffect } from "react";
import { fetchTrash } from "../../api/fetchTrash";

const DetectionSignal = () => {
  const [isDisabled, setIsDisabled] = useState(true);

  useEffect(() => {
    const intervalId = setInterval(() => {
      //update frame every 2 seconds
      fetchTrash()
        .then((obj) => {
          let newData = obj.data;
          return newData;
        })
        .then((newData) => {
          setIsDisabled((prevState) => newData.data);
        })
        .catch((err) => {
          console.log(err);
          setIsDisabled((prevState) => prevState);
        });
    }, 4000);

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
