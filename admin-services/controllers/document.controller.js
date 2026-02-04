const axios = require("axios");

const documents = [];

exports.uploadDocument = (req, res) => {
    const doc = {
        id: documents.length + 1,
        filename: req.file.filename,
        path: req.file.path,
        status: "pending"
    };

    documents.push(doc);

    res.json({
        message: "Document uploaded successfully",
        document: doc
    });
};

exports.approveDocument = async (req, res) => {
    const docId = parseInt(req.params.id);
    const doc = documents.find(d => d.id === docId);

    if (!doc) {
        return res.status(404).json({ message: "Document not found" });
    }

    doc.status = "approved";

    // 🔥 Trigger rebuild (do NOT await result processing)
    axios.post(`http://localhost:${process.env.PYTHON_PORT}/rebuild-index`)
        .catch(err => {
            console.error("Background rebuild failed:", err.message);
        });

    // ✅ Respond immediately
    res.json({
        message: "Document approved. RAG rebuild started in background.",
        document: doc
    });
};
