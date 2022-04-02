import React, { useState, useEffect } from "react";
import {
  Card,
  CardContent,
  Typography,
  CircularProgress,
} from "@material-ui/core/";

const OverrideControls = () => {
  const MANUAL_OVERRIDE = process.env.REACT_APP_MANUAL_OVERRIDE;
  const [override, setOverride] = useState(MANUAL_OVERRIDE);

  const overrideHandler = (e) => {
    setOverride((prevState) => {
      !prevState;
    });
  };

  useEffect(() => {
    if (override == true) {
      process.env.REACT_APP_MANUAL_OVERRIDE = true;
    } else {
      process.env.REACT_APP_MANUAL_OVERRIDE = false;
    }
  }, [override]);

  return <Button onclick={overrideHandler}></Button>;
};

export default OverrideControls;
