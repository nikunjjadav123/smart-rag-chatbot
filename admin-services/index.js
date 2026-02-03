const express = require("express");
const cors = require("cors");
const dotenv = require("dotenv");
const path = require("path");
const documentRoutes = require("./routes/document.routes");

dotenv.config({
    path: path.resolve(__dirname, "../.env"),
});

const PORT = process.env.NODE_PORT || 5000;

const app = express();

app.use(cors());
app.use(express.json());

app.use("/api/documents", documentRoutes);

app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
}); 