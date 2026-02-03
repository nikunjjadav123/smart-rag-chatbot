const express = require("express");
const router = express.Router();
const multer = require("multer");
const path = require("path");
const fs = require("fs");

const { uploadDocument } = require("../controllers/document.controller");

const UPLOAD_DIR = path.join(__dirname, "../../uploads/documents");

/* 🔹 Ensure upload directory exists */
if (!fs.existsSync(UPLOAD_DIR)) {
    fs.mkdirSync(UPLOAD_DIR, { recursive: true });
}

/* 🔹 Multer storage */
const storage = multer.diskStorage({
    destination: (req, file, cb) => {
        cb(null, UPLOAD_DIR);
    },
    filename: (req, file, cb) => {
        cb(null, Date.now() + "-" + file.originalname);
    },
});

/* 🔹 File filter (PDF only) */
const fileFilter = (req, file, cb) => {
    if (file.mimetype === "application/pdf") {
        cb(null, true);
    } else {
        cb(new Error("Only PDF files are allowed"), false);
    }
};

const upload = multer({
    storage,
    fileFilter,
    limits: { fileSize: 10 * 1024 * 1024 } // 10 MB
});

router.post("/upload", (req, res, next) => {
    console.log("Headers:", req.headers["content-type"]);
    next();
}, upload.single("file"), uploadDocument);

module.exports = router;
