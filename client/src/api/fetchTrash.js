import axios from "axios";

const API = axios.create({ baseURL: "http://localhost:5000" });
// local host port

export const fetchTrash = () => {
<<<<<<< HEAD
  console.log(API.get("/trash"));
=======
>>>>>>> 3bbd040b8954b27dd206f4c4b27efdbb67afb3dd
  return API.get(`/trash`);
};
