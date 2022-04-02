import React, { useState, useEffect } from "react";
import {
  Card,
  CardContent,
  Typography,
  CircularProgress,
} from "@material-ui/core/";
// import stockPhoto from "./stockPhoto.jpg";

import * as api from "../../api";

import useStyles from "./styles";

const Frame = () => {
  const [frameSrc, setFrameSrc] = useState("stockPhoto.jpg");
  const framePath = "/images/";
  const classes = useStyles();
  useEffect(() => {
    const intervalId = setInterval(() => {
      //update frame every 2 seconds
      api
        .fetchFrame()
        .then((obj) => {
          let newData = obj.data.data;
          console.log(newData);
          return newData;
        })
        .then((newData) => {
          setFrameSrc((prevState) => newData);
          console.log(newData);
        })
        .catch((err) => {
          console.log(err);
          setFrameSrc((prevState) => prevState);
        });
    }, 5000);

    return () => {
      clearInterval(intervalId); //This is important
    };
  }, [useState]);

  return !frameSrc ? (
    <CircularProgress />
  ) : (
    <img
      className="frame"
      src={framePath + frameSrc}
      alt="Raspberry Pi Camera Frame"
    />
  );
};

export default Frame;
