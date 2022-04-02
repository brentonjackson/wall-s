import axios from "axios";

const API = axios.create({ baseURL: "http://localhost:5000" });
// local host port

export const fetchFrame = () => {
  return API.get(`/stream`);
};
